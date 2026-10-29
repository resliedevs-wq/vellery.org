#!/usr/bin/env python3
"""Build the static site into dist/.

Reads tasks/, outputs/ and grading/kitchen/ and writes:
  index.html                 the tasks
  tasks/<slug>/index.html    prompts, model x run grid, each run's output
  rate/<slug>/index.html     blind rating page, one output at a time, ids only
  items.json                 every rateable id (the Worker only accepts these)

Kitchen drawings stay under their blind ids until grading is done, so their
task page is a gallery, not a model grid.

Usage: python3 site/build.py
"""

import csv
import hashlib
import html
import io
import json
import re
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "runner"))
from grade import extract_csv  # noqa: E402

OUTPUTS = ROOT / "outputs"
TASKS = ROOT / "tasks"
KITCHEN = ROOT / "grading" / "kitchen"
DIST = ROOT / "dist"
ORDER = ["shorten-email", "clean-spreadsheet", "kitchen-illustration"]
GRADES = {"good": "Usable as is", "fix": "Needs a fix", "slop": "Slop"}


def esc(s):
    return html.escape(str(s), quote=True)


def blob(data):
    return json.dumps(data).replace("<", "\\u003c")


def page(title, body, scripts=()):
    tags = "".join(f'<script src="/static/{s}" defer></script>' for s in scripts)
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{esc(title)}</title>"
        '<link rel="stylesheet" href="/static/style.css">'
        f'</head><body><header><a href="/">Vellery</a></header><main>{body}</main>{tags}</body></html>'
    )


def write(path, text):
    path = DIST / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def replaced_runs():
    out = set()
    for f in OUTPUTS.glob("*/replaces.json"):
        spec = json.loads(f.read_text())
        out |= {(spec["batch"], r) for r in spec["runs"]}
    return out


def load_runs():
    skip = replaced_runs()
    runs = []
    for meta_path in sorted(OUTPUTS.glob("*/*/*/*/run-*/meta.json")):
        batch = meta_path.relative_to(OUTPUTS).parts[0]
        meta = json.loads(meta_path.read_text())
        if (batch, f"{meta['task']}/{meta['variant']}/{meta['model']}") in skip or not meta.get("ok"):
            continue
        run_dir = meta_path.parent
        attempt = run_dir / f"attempt-{meta['attempts']}"
        grade_file = run_dir / "grade.json"
        digest = hashlib.sha1(f"{batch}/{meta['task']}/{meta['variant']}/{meta['model']}/{meta['run']}".encode())
        runs.append({
            **meta,
            "batch": batch,
            "item": f"{meta['task']}.{digest.hexdigest()[:6]}",
            "response": (attempt / "response.md").read_text(),
            "grade": json.loads(grade_file.read_text()) if grade_file.exists() else None,
            "run_dir": run_dir,
        })
    return runs


def prompt_text(task, variant):
    """The prompt as sent, with line breaks inside a paragraph joined for display."""
    text = re.sub(r"\{\{(.+?)\}\}", r"[\1]", task["prompts"][variant]).strip()
    out = []
    for line in text.splitlines():
        joins = out and out[-1] and not line.startswith(("-", "[")) and not out[-1].startswith("-") and line
        if joins:
            out[-1] += " " + line
        else:
            out.append(line)
    return "\n".join(out)


def sheet_parts(run):
    block = extract_csv(run["response"])
    if block is None:
        for f in sorted(run["run_dir"].glob("attempt-*/files/*.csv")):
            block = f.read_text()
    if block is None:
        return None, run["response"]
    rows = list(csv.reader(io.StringIO(block.strip())))
    prose = run["response"].replace(block, "")
    prose = re.sub(r"```[a-z]*\s*```", "", prose).strip()
    return rows, prose


def item_payload(task, run):
    base = {"id": run["item"], "variant": run["variant"], "kind": task["kind"]}
    if task["slug"] == "clean-spreadsheet":
        rows, prose = sheet_parts(run)
        return {**base, "kind": "sheet", "rows": rows, "text": prose}
    return {**base, "text": run["response"].strip()}


def kitchen_items():
    groups = {}
    for variant in ("strong", "weak"):
        for f in sorted((KITCHEN / variant).glob("K*")):
            m = re.fullmatch(r"(K\d{3})[a-z]?", f.stem)
            if m and f.suffix in (".svg", ".png"):
                groups.setdefault((variant, m.group(1)), []).append(f)
    items = []
    for (variant, kid), files in sorted(groups.items(), key=lambda kv: kv[0][1]):
        srcs = []
        for f in files:
            dest = f"img/kitchen/{f.name}"
            (DIST / dest).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(f, DIST / dest)
            srcs.append("/" + dest)
        items.append({"id": f"kitchen-illustration.{kid}", "variant": variant, "kind": "image", "srcs": srcs})
    return items


def load_tasks():
    tasks = {}
    for f in TASKS.glob("*/task.yaml"):
        t = yaml.safe_load(f.read_text())
        t["dir"] = f.parent
        tasks[t["slug"]] = t
    return [tasks[s] for s in ORDER if s in tasks] + [t for s, t in sorted(tasks.items()) if s not in ORDER]


def prompt_cards(task, selectable):
    out = []
    for variant in ("weak", "strong"):
        tag = "button" if selectable else "div"
        out.append(
            f'<{tag} class="prompt {variant}" data-variant="{variant}">'
            f"<b>{variant.capitalize()} prompt</b><pre>{esc(prompt_text(task, variant))}</pre></{tag}>")
    return f'<div class="prompts">{"".join(out)}</div>'


def build_task_page(task, runs, models, items):
    slug = task["slug"]
    head = (f'<p class="crumb">{esc(task["category"])}</p><h1>{esc(task["title"])}</h1>'
            f'<p><a class="button" href="/rate/{slug}/">Rate outputs</a></p>')
    if task["kind"] == "svg":
        gallery = "".join(
            f'<a href="/rate/{slug}/#{i["id"]}" class="shot" data-id="{i["id"]}" data-variant="{i["variant"]}">'
            f'<img src="{i["srcs"][0]}" alt="" loading="lazy"><span class="tally"></span></a>'
            for i in items)
        body = head + prompt_cards(task, True) + f'<div class="gallery" id="gallery">{gallery}</div>'
        data = {"slug": slug, "mode": "gallery"}
    else:
        by_id, grids = {}, []
        for variant in ("weak", "strong"):
            rows = []
            for m in models:
                mine = sorted((r for r in runs if r["variant"] == variant and r["model"] == m["id"]), key=lambda r: r["run"])
                if not mine:
                    continue
                cells = "".join(
                    f'<button class="cell {r["grade"]["grade"] if r["grade"] else "none"}" data-id="{r["item"]}">{r["run"]}</button>'
                    for r in mine)
                rows.append(f'<div class="model">{esc(m["label"])}</div>{cells}')
                for r in mine:
                    by_id[r["item"]] = {
                        "model": m["label"], "run": r["run"], "variant": variant,
                        "grade": r["grade"]["grade"] if r["grade"] else None,
                        "why": r["grade"]["why"] if r["grade"] else "",
                        "text": r["response"].strip(), "cost": r.get("est_cost_usd"),
                    }
            grids.append(f'<div class="grid" data-variant="{variant}" hidden>{"".join(rows)}</div>')
        legend = "".join(f'<span class="{g}">{label}</span>' for g, label in GRADES.items())
        body = (head + prompt_cards(task, True) + "".join(grids)
                + f'<div class="legend">{legend}</div><section id="detail" hidden></section>')
        data = {"slug": slug, "mode": "grid", "runs": by_id, "grades": GRADES}
    body += f'<script id="data" type="application/json">{blob(data)}</script>'
    write(f"tasks/{slug}/index.html", page(task["title"], body, ["task.js"]))
    for name in task.get("inputs", []):
        shutil.copy(task["dir"] / name, DIST / "tasks" / slug / name)


def build_rate_page(task, items):
    slug = task["slug"]
    data = {"slug": slug, "grades": GRADES, "items": items,
            "prompts": {v: prompt_text(task, v) for v in ("weak", "strong")}}
    body = (f'<p class="crumb"><a href="/tasks/{slug}/">{esc(task["title"])}</a></p>'
            '<div id="rater"><p id="progress"></p><pre id="prompt"></pre><div id="item"></div>'
            '<div id="buttons"></div><div id="result"></div></div>'
            '<p class="note">No sign-in. Anyone can vote, so these ratings are a test and are not part of the grades.</p>'
            f'<script id="data" type="application/json">{blob(data)}</script>')
    write(f"rate/{slug}/index.html", page(f'Rate: {task["title"]}', body, ["rate.js"]))


def main():
    shutil.rmtree(DIST, ignore_errors=True)
    shutil.copytree(Path(__file__).parent / "static", DIST / "static")
    tasks = load_tasks()
    models = yaml.safe_load((ROOT / "models.yaml").read_text())["models"]
    all_runs = load_runs()
    known, cards = [], []
    for task in tasks:
        slug = task["slug"]
        if task["kind"] == "svg":
            items = kitchen_items()
        else:
            runs = [r for r in all_runs if r["task"] == slug]
            items = [item_payload(task, r) for r in runs]
        known += [i["id"] for i in items]
        build_task_page(task, [r for r in all_runs if r["task"] == slug], models, items)
        build_rate_page(task, items)
        cards.append(
            f'<a class="card" href="/tasks/{slug}/"><span class="crumb">{esc(task["category"])}</span>'
            f'<b>{esc(task["title"])}</b><span class="crumb">{len(items)} outputs</span></a>')
    write("items.json", json.dumps(known))
    write("index.html", page("Vellery", f'<h1>Vellery</h1><div class="cards">{"".join(cards)}</div>'))
    print(f"{len(tasks)} tasks, {len(known)} rateable outputs -> {DIST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
