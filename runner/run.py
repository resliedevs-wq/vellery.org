#!/usr/bin/env python3
"""Run every task prompt through each model's own agent CLI and save the results.

Results go to outputs/<batch>/<task>/<variant>/<model>/run-<n>/. A batch
records the commit its tasks and model list came from, and refuses to start
while those files have uncommitted changes. Finished runs are never
overwritten; to redo anything, start a new batch.

Each run starts in an empty temporary directory with the user's personal
config, memory, MCP servers, apps, and plugins excluded, and web tools off
for both CLIs. Both can run shell commands inside a sandbox that limits
writes to the working directory and blocks the network. Codex's image
generator is off. If the CLI itself fails (crash,
timeout, unreadable output), the run is retried up to MAX_ATTEMPTS times.
Every attempt is kept under run-<n>/attempt-<k>/. A run whose attempts all
fail is recorded as failed, not dropped.

A task can list `files` to copy into the working directory before each run.
A task with `stop_on_success` runs its runs one after another and stops at
the first one the grader marks solved: its runs are chances, not repeats.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import yaml

from functools import partial

from zcode import run_zcode
from cost import estimate_claude, estimate_codex, estimate_usage, total
from grade import grade_answer

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "tasks"
MODELS = ROOT / "models.yaml"
OUTPUTS = ROOT / "outputs"
TIMEOUT_S = 900
MAX_ATTEMPTS = 3


def load_tasks():
    tasks = {}
    for path in sorted(TASKS.glob("*/task.yaml")):
        task = yaml.safe_load(path.read_text())
        task["dir"] = path.parent
        tasks[task["slug"]] = task
    return tasks


def load_models():
    config = yaml.safe_load(MODELS.read_text())
    return [{**config.get("defaults", {}), **m} for m in config["models"]]


def render_prompt(task, variant):
    def inline(match):
        return (task["dir"] / match.group(1)).read_text().rstrip("\n")

    return re.sub(r"\{\{(.+?)\}\}", inline, task["prompts"][variant]).rstrip("\n")


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def cli_version(cmd):
    return subprocess.run([cmd, "--version"], capture_output=True, text=True).stdout.strip()


def execute(cmd, **kwargs):
    """Run a CLI, keeping whatever it printed even if it times out."""
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_S, **kwargs)
        return proc.returncode, proc.stdout, proc.stderr, None
    except subprocess.TimeoutExpired as e:
        decode = lambda b: b.decode(errors="replace") if isinstance(b, bytes) else (b or "")
        return None, decode(e.stdout), decode(e.stderr), f"timed out after {TIMEOUT_S}s"


def run_claude(model, prompt, workdir):
    cmd = [
        "claude", "-p", prompt,
        "--model", model["id"],
        "--effort", model["effort"],
        "--setting-sources", "project",
        "--strict-mcp-config",
        "--no-session-persistence",
        "--permission-mode", "acceptEdits",
        "--disallowedTools", "WebSearch", "WebFetch",
        # Shell commands run sandboxed: writes limited to the working
        # directory, no network. Matches codex's workspace-write sandbox.
        "--settings", json.dumps({"sandbox": {
            "enabled": True, "autoAllowBashIfSandboxed": True, "allowUnsandboxedCommands": False}}),
        "--output-format", "json",
    ]
    env = {**os.environ, "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"}
    code, out, err, error = execute(cmd, cwd=workdir, env=env)
    result = {"command": cmd[:2] + ["<prompt>"] + cmd[3:], "raw": out, "stderr": err, "error": error}
    if error:
        return result
    try:
        data = json.loads(out)
    except json.JSONDecodeError as e:
        return {**result, "error": f"unreadable cli output: {e}"}
    model_usage = data.get("modelUsage") or {}
    return {
        **result,
        "error": None if code == 0 and not data.get("is_error") else "cli reported an error",
        "response": data.get("result", ""),
        "served_models": sorted(u.get("canonicalModel", m) for m, u in model_usage.items()),
        "usage": {"usage": data.get("usage"), "modelUsage": model_usage},
        "est_cost": estimate_claude(data, model["id"]),
        "cli_reported_cost_usd": data.get("total_cost_usd"),
    }


def run_codex(model, prompt, workdir):
    last = Path(workdir).parent / "last-message.txt"
    cmd = [
        "codex", "exec",
        "--ignore-user-config",
        "--ephemeral",
        "--skip-git-repo-check",
        "--sandbox", "workspace-write",
        "--disable", "apps",
        "--disable", "plugins",
        # The built-in image generator calls a separate image model; runs
        # should show what the tested model makes itself.
        "--disable", "image_generation",
        # Its skill would otherwise tell the model the tool is missing and
        # to ask the user before using a fallback.
        "-c", f'skills.config=[{{path="{Path.home()}/.codex/skills/.system/imagegen/SKILL.md",enabled=false}}]',
        "-c", 'web_search="disabled"',
        "--cd", str(workdir),
        "--model", model["id"],
        "-c", f'model_reasoning_effort="{model["effort"]}"',
        "--json",
        "--output-last-message", str(last),
        prompt,
    ]
    code, out, err, error = execute(cmd, stdin=subprocess.DEVNULL)
    usage = None
    for line in out.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "turn.completed":
            usage = event.get("usage")
    if not error and (code != 0 or not last.exists()):
        error = "cli reported an error"
    return {
        "command": cmd[:-1] + ["<prompt>"],
        "raw": out,
        "stderr": err,
        "error": error,
        "response": last.read_text() if last.exists() else "",
        # codex does not report which model served the run.
        "served_models": None,
        "usage": usage,
        "est_cost": estimate_codex(usage, model["id"]),
        "cli_reported_cost_usd": None,
    }


def run_deepseek(model, prompt, workdir):
    patch = ROOT / "runner" / "deepseek-flash.yaml"
    cmd = ["dsh", "--profile", "headless", "--patch", str(patch),
           "--permission-mode", "workspace-write", "--approval-policy", "never", "--json", "-"]
    code, out, err, error = execute(cmd, input=prompt, cwd=workdir,
                                    env={**os.environ, "DSH_HOME": str(workdir.parent / "dsh-home")})
    final = {}
    usage = []
    for line in out.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") == "final":
            final = event
        if event.get("phase") == "step_end" and event.get("usage"):
            usage.append(event["usage"])
    if code != 0 or final.get("reason", {}).get("kind") != "completed":
        error = error or "DeepSeek Harness did not complete the turn"
    return {"command": cmd, "raw": out, "stderr": err, "error": error,
            "usage": usage, "response": final.get("text", "")}


def collect_agy_drawing(response, workdir):
    """Collect a linked SVG only from the bridge session bound to this attempt."""
    links = re.findall(r"/tmp/(magpie-agy-bridge-[a-zA-Z0-9]{6})/([\w.-]+\.svg)\b", response)
    missing = []
    for folder, name in links:
        destination = workdir / name
        if destination.is_symlink():
            return "Antigravity drawing destination is a symlink"
        if not destination.is_file():
            missing.append((folder, name))
    if not missing:
        return None
    state_root = Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local/state")
    ledger = Path(os.environ.get("AGY_BRIDGE_STATE_FILE") or state_root / "magpie-agy-bridge/sessions.json")
    owned = {entry.get("workspace") for entry in json.loads(ledger.read_text())["entries"]
             if entry.get("workDir") == str(workdir)}
    for folder, name in missing:
        scratch = Path("/tmp") / folder
        source = scratch / name
        if (str(scratch) not in owned or scratch.is_symlink() or source.is_symlink()
                or not source.is_file()):
            return "Antigravity linked an SVG that could not be verified in this attempt's bridge session"
        shutil.copyfile(source, workdir / name)
    return None


def run_agy(model, prompt, workdir):
    route = "agy-cli/" + model["id"]
    alias = "magpie/" + route
    settings = {
        "modelProvider": "gemini",
        "customModelsConfig": {"customModels": {alias: {
            "apiProvider": "API_PROVIDER_GOOGLE_GEMINI", "modelName": route}}},
        "permissions": {"deny": ["read_url(*)", "execute_url(*)", "download_url(*)"]},
    }
    cmd = ["agy", "--model", alias, "--settings", json.dumps(settings), "--sandbox",
           "--mode", "accept-edits", "--effort", model["effort"], "--output-format", "json",
           "-p", prompt]
    home = workdir.parent / "home"
    home.mkdir()
    if model.get("workspace_files_only"):
        agents = home / ".gemini" / "config" / "agents"
        agents.mkdir(parents=True)
        profile = (ROOT / "runner" / "agy-workspace-files.md").read_text()
        (agents / "workspace-files.md").write_text(profile.replace("WORKSPACE_PATH", str(workdir)))
        cmd[1:1] = ["--agent", "workspace-files"]
    env = {"HOME": str(home), "PATH": os.environ["PATH"],
           "GOOGLE_GEMINI_BASE_URL": os.environ["MAGPIE_BASE_URL"],
           "GEMINI_API_KEY": os.environ["MAGPIE_API_KEY"]}
    code, out, err, error = execute(cmd, cwd=workdir, env=env)
    try:
        data = json.loads(out)
    except ValueError:
        data = {}
    if code != 0 or data.get("status") != "SUCCESS":
        error = error or data.get("error") or "Antigravity reported an error"
    elif data.get("denied_actions"):
        denied = [action.get("display_name") or action.get("action", "unknown")
                  for action in data["denied_actions"]]
        error = "Antigravity denied: " + ", ".join(denied)
    response = data.get("response", "")
    if not error and model.get("workspace_files_only"):
        try:
            error = collect_agy_drawing(response, workdir)
        except (OSError, ValueError) as exc:
            error = f"could not collect Antigravity drawing: {exc}"
    return {"command": cmd[:-1] + ["<prompt>"], "raw": out, "stderr": err,
            "error": error, "response": response, "usage": data.get("usage")}


HARNESSES = {"claude": run_claude, "codex": run_codex, "dsh": run_deepseek,
             "zcode": partial(run_zcode, execute=execute), "agy": run_agy}


def attempt(model, prompt, dest, inputs=()):
    """Run the CLI once in a fresh directory and save everything to dest."""
    with tempfile.TemporaryDirectory(prefix="vellery-") as tmp:
        workdir = Path(tmp) / "work"
        workdir.mkdir()
        for src in inputs:
            shutil.copyfile(src, workdir / src.name)
        started = datetime.now(timezone.utc)
        t0 = time.monotonic()
        result = HARNESSES[model["harness"]](model, prompt, workdir)

        if result.get("est_cost") is None:
            result["est_cost"] = estimate_usage(model["harness"], model["id"], result.get("usage"))

        dest.mkdir(parents=True)
        (dest / "response.md").write_text(result.get("response", ""))
        log = result.get("raw", "")
        if result.get("stderr"):
            log += "\n--- stderr ---\n" + result["stderr"]
        (dest / "transcript.log").write_text(log)
        files = sorted(p.relative_to(workdir).as_posix() for p in workdir.rglob("*") if p.is_file())
        # Inputs the model left unchanged are already in tasks/.
        unchanged = {src.name for src in inputs
                     if (workdir / src.name).is_file() and (workdir / src.name).read_bytes() == src.read_bytes()}
        if set(files) - unchanged:
            shutil.copytree(workdir, dest / "files", ignore=lambda d, names: [
                n for n in names if Path(d) == workdir and n in unchanged])
        info = {
            "ok": result["error"] is None,
            "error": result["error"],
            "started": started.isoformat(timespec="seconds"),
            "duration_s": round(time.monotonic() - t0, 1),
            "command": result["command"],
            "served_models": result.get("served_models"),
            "usage": result.get("usage"),
            # None means the cost could not be estimated, not that it was free.
            "est_cost_usd": total(result.get("est_cost")),
            "est_cost": result.get("est_cost"),
            "cli_reported_cost_usd": result.get("cli_reported_cost_usd"),
            "files": files,
        }
        (dest / "attempt.json").write_text(json.dumps(info, indent=2) + "\n")
        return info


def run_one(task, variant, model, n, out):
    """Attempt a run until the CLI succeeds or attempts run out, then write meta.json."""
    if model["harness"] == "agy" and task["slug"] == "kitchen-illustration":
        model = {**model, "workspace_files_only": True}
    prompt = render_prompt(task, variant)
    inputs = [task["dir"] / name for name in task.get("files", [])]
    out.mkdir(parents=True, exist_ok=True)
    # Attempts saved by an interrupted batch count: a finished success is
    # kept, and earlier failures count toward the limit.
    saved = sorted(out.glob("attempt-*/attempt.json"), key=lambda p: int(p.parent.name.split("-")[1]))
    infos = [json.loads(p.read_text()) for p in saved]
    while not (infos and infos[-1]["ok"]) and len(infos) < MAX_ATTEMPTS:
        infos.append(attempt(model, prompt, out / f"attempt-{len(infos) + 1}", inputs))
    info = infos[-1]
    costs = [i["est_cost_usd"] for i in infos]
    meta = {
        "task": task["slug"],
        "variant": variant,
        "model": model["id"],
        "label": model["label"],
        "harness": model["harness"],
        "effort": model["effort"],
        "run": n,
        "ok": info["ok"],
        "attempts": len(infos),
        "est_cost_usd": info["est_cost_usd"],
        "est_cost_usd_all_attempts": None if None in costs else round(sum(costs), 6),
    }
    # meta.json is written last: its presence marks the run as finished.
    (out / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    return info["ok"], len(infos), info["duration_s"]


def solved(task, out):
    meta = json.loads((out / "meta.json").read_text())
    if not meta["ok"]:
        return False
    response = (out / f"attempt-{meta['attempts']}" / "response.md").read_text()
    return grade_answer(task, response)["grade"] == "good"


def run_chances(task, variant, model, outs):
    """Give a model its chances in order, stopping at the first solved run."""
    for n, out in enumerate(outs, 1):
        if not (out / "meta.json").exists():
            run_one(task, variant, model, n, out)
        if solved(task, out):
            return f"solved on chance {n}"
    return f"not solved in {len(outs)} chances"


def start_batch(batch_dir, harnesses):
    """Record what this batch runs against. Reuse the record when resuming."""
    record = batch_dir / "batch.json"
    commit = git("rev-parse", "HEAD")
    versions = {h: cli_version(h) for h in sorted(harnesses)}
    if record.exists():
        existing = json.loads(record.read_text())
        if existing["commit"] != commit or existing["cli_versions"] != versions:
            sys.exit(
                f"batch {batch_dir.name} was started at {existing['commit'][:7]} with "
                f"{existing['cli_versions']}; now at {commit[:7]} with {versions}. "
                "Start a new batch instead."
            )
        return
    batch_dir.mkdir(parents=True)
    record.write_text(json.dumps({
        "batch": batch_dir.name,
        "commit": commit,
        "started": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "cli_versions": versions,
    }, indent=2) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("batch", help="batch name, e.g. 2026-10-29")
    ap.add_argument("--task", action="append", help="task slug (repeatable; default all)")
    ap.add_argument("--model", action="append", help="model id (repeatable; default all)")
    ap.add_argument("--variant", action="append", help="prompt variant (repeatable; default all of a task's)")
    ap.add_argument("--runs", type=int, help="override runs per task")
    ap.add_argument("--jobs", type=int, default=4, help="parallel runs")
    ap.add_argument("--dry-run", action="store_true", help="list runs without executing")
    args = ap.parse_args()

    tasks = load_tasks()
    models = load_models()
    for name, known in (("task", tasks), ("model", {m["id"] for m in models})):
        for value in getattr(args, name) or []:
            if value not in known:
                sys.exit(f"unknown {name}: {value}")

    batch_dir = OUTPUTS / args.batch
    jobs = []
    for task in tasks.values():
        if args.task and task["slug"] not in args.task:
            continue
        for variant in task["prompts"]:
            if args.variant and variant not in args.variant:
                continue
            for model in models:
                if args.model and model["id"] not in args.model:
                    continue
                outs = [batch_dir / task["slug"] / variant / model["id"] / f"run-{n}"
                        for n in range(1, (args.runs or task["runs"]) + 1)]
                if task.get("stop_on_success"):
                    # One job per model: later chances depend on earlier results.
                    if not any(solved(task, o) for o in outs if (o / "meta.json").exists()) \
                            and not all((o / "meta.json").exists() for o in outs):
                        jobs.append((task, variant, model, outs))
                    continue
                for n, out in enumerate(outs, 1):
                    if not (out / "meta.json").exists():
                        jobs.append((task, variant, model, n, out))

    print(f"{len(jobs)} jobs to do in batch {args.batch}")
    if args.dry_run:
        for *_, out in jobs:
            if isinstance(out, list):
                print(f"  {out[0].parent.relative_to(batch_dir)} (up to {len(out)} chances, stops when solved)")
            else:
                print(f"  {out.relative_to(batch_dir)}")
        return

    if "claude" in {job[2]["harness"] for job in jobs}:
        # Test the sandbox itself: the sysctl can be restrictive while this
        # process is still permitted to create the required namespaces.
        if not shutil.which("bwrap"):
            sys.exit("Claude's shell sandbox requires bubblewrap (bwrap).")
        probe = subprocess.run(
            ["bwrap", "--ro-bind", "/", "/", "--unshare-user", "--unshare-pid", "--unshare-net", "--", "/bin/true"],
            capture_output=True, text=True,
        )
        if probe.returncode:
            sys.exit(f"Claude's shell sandbox cannot start: {probe.stderr.strip()}")
    if git("status", "--porcelain", "--", "tasks", "models.yaml", "prices.yaml", "runner"):
        sys.exit("tasks/, models.yaml, prices.yaml, or runner/ has uncommitted changes. Commit them before running a batch.")
    start_batch(batch_dir, {job[2]["harness"] for job in jobs})

    failed = 0
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(run_chances if len(job) == 4 else run_one, *job): job[-1] for job in jobs}
        for i, future in enumerate(as_completed(futures), 1):
            out = futures[future]
            if isinstance(out, list):
                print(f"[{i}/{len(jobs)}] {out[0].parent.relative_to(batch_dir)}: {future.result()}", flush=True)
                continue
            ok, attempts, duration = future.result()
            failed += not ok
            note = f", {attempts} attempts" if attempts > 1 else ""
            print(f"[{i}/{len(jobs)}] {'ok  ' if ok else 'FAIL'} "
                  f"{out.relative_to(batch_dir)} ({duration}s{note})", flush=True)
    if failed:
        print(f"{failed} runs failed after {MAX_ATTEMPTS} attempts; they are recorded as failed.")


if __name__ == "__main__":
    main()
