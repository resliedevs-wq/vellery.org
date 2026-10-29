#!/usr/bin/env python3
"""Build the static site into dist/.

Reads tasks/, outputs/ and grading/kitchen/ and writes:
  index.html                 the tasks, every run as a dot
  tasks/<slug>/index.html    input, prompts, runs ordered green/yellow/red, each beside the reference
  items.json                 the outputs visitors can vote on (the Worker only accepts these)

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
from grade import EMAIL_FACTS, extract_csv, pair_rows, parse_amount, parse_date, sheet_rows  # noqa: E402

OUTPUTS = ROOT / "outputs"
TASKS = ROOT / "tasks"
KITCHEN = ROOT / "grading" / "kitchen"
DIST = ROOT / "dist"
REPO = "https://github.com/resliedevs-wq/vellery.org"
ORDER = ["shorten-email", "clean-spreadsheet", "kitchen-illustration"]
VARIANTS = ("weak", "strong")
GRADES = {"good": "Usable as is", "fix": "Needs a fix", "slop": "Slop"}
COLUMNS = ["Date", "Description", "Category", "Amount"]
# Where each fact shows up in a text, for highlighting. Presence itself comes
# from the grader, so the page and the grade can't disagree.
FACT_SPANS = {**EMAIL_FACTS, "AV fee waived": r"\bAV\b|\bwaiv\w*"}
PROBLEMS = {
    "wrong_date": "date wrong", "wrong_amount": "amount changed", "wrong_category": "category wrong",
    "unconverted_date": "date not converted", "format": "formatting", "extra_or_renamed": "extra or renamed row",
}


def esc(s):
    return html.escape(str(s), quote=True)


def blob(data):
    return json.dumps(data).replace("<", "\\u003c")


def page(title, body, scripts=()):
    tags = "".join(f'<script src="/static/{s}" defer></script>' for s in ("auth.js", *scripts))
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{esc(title)}</title>"
        '<link rel="preload" href="/static/fonts/fraunces.woff2" as="font" type="font/woff2" crossorigin>'
        '<link rel="stylesheet" href="/static/style.css">'
        '</head><body><header class="top"><a class="brand" href="/">Vellery</a>'
        '<nav><a href="/#tasks">Tasks</a><span id="auth"></span></nav></header>'
        f'<main>{body}</main>'
        f'<footer>Every prompt, raw output and grading script is on <a href="{REPO}">GitHub</a>.</footer>'
        f"{tags}</body></html>"
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
            "source": f"{REPO}/tree/main/{run_dir.relative_to(ROOT)}",
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


# ---------- emails ----------

def mark_facts(text, invented=()):
    spans = []
    for pattern in FACT_SPANS.values():
        spans += [(m.start(), m.end(), "") for m in re.finditer(pattern, text, re.I)]
    for item in invented:
        spans += [(m.start(), m.end(), "bad") for m in re.finditer(re.escape(item), text)]
    out, at = [], 0
    for start, end, cls in sorted(spans):
        if start < at:
            continue
        out.append(esc(text[at:start]))
        out.append(f'<mark class="{cls}">{esc(text[start:end])}</mark>')
        at = end
    out.append(esc(text[at:]))
    return "".join(out)


def email_compare(task, run, reference):
    g = run["grade"]
    checks = g["checks"]
    limit = task["checks"]["max_words"] if run["variant"] == "strong" else checks["original_words"]
    over = checks["words"] > limit if run["variant"] == "strong" else checks["words"] >= limit
    meter = (f'<div class="meter{" over" if over else ""}"><span style="width:{min(100, 100 * checks["words"] / limit):.0f}%"></span></div>'
             f'<b>{checks["words"]}</b> words · '
             + (f"limit {limit}" if run["variant"] == "strong" else f"original {limit}"))
    chips = "".join(f'<li class="{"miss" if name in checks["missing"] else "hit"}">{esc(name)}</li>' for name in FACT_SPANS)
    chips += "".join(f'<li class="miss">added: {esc(i)}</li>' for i in checks["invented"])
    return (
        f'<div class="checks"><div class="words">{meter}</div><ul class="facts">{chips}</ul></div>'
        '<div class="pair">'
        f'<div><h3>Reference</h3><pre class="doc">{mark_facts(reference)}</pre></div>'
        f'<div><h3>This run</h3><pre class="doc">{mark_facts(run["response"].strip(), checks["invented"])}</pre></div>'
        "</div>"
    )


# ---------- spreadsheets ----------

def sheet_block(run):
    block = extract_csv(run["response"])
    if block is None:
        for f in sorted(run["run_dir"].glob("attempt-*/files/*.csv")):
            block = f.read_text()
    return block


def sheet_notes(run, block):
    prose = run["response"].replace(block or "", "")
    return re.sub(r"```[a-z]*\s*```", "", prose).strip()


def cell_class(col, value, want):
    value = (value or "").strip()
    if value == want:
        return ""
    if col == "Date":
        iso, kind = parse_date(value, want)
        return "fmt" if kind == "unconverted" else "bad"
    if col == "Amount":
        amount = parse_amount(value)
        return "fmt" if amount is not None and abs(amount - float(want)) < 0.005 else "bad"
    return "fmt" if value.lower() == want.lower() else "bad"


def sheet_compare(task, run, expected):
    g = run["grade"]
    block = sheet_block(run)
    rows = sheet_rows(block) if block else []
    copies = [dict(r) for r in expected]
    pairs, unmatched = pair_rows(rows, copies)
    matched = {id(best): r for best, r, _ in pairs if best is not None}
    body = []
    for ref in copies:
        out = matched.get(id(ref))
        left = "".join(f"<td>{esc(ref[c])}</td>" for c in COLUMNS)
        if out is None:
            right = '<td class="gone" colspan="4">missing</td>'
        else:
            right = "".join(
                f'<td class="{cell_class(c, out.get(c), ref[c])}" title="{esc(ref[c])}">{esc(out.get(c) or "")}</td>'
                for c in COLUMNS)
        body.append(f'<tr>{left}<td class="gap"></td>{right}</tr>')
    for best, out, _ in pairs:
        if best is None:
            right = "".join(f'<td class="bad">{esc(out.get(c) or "")}</td>' for c in COLUMNS)
            body.append(f'<tr class="extra"><td colspan="4" class="gone">not in reference</td><td class="gap"></td>{right}</tr>')
    head = "".join(f"<th>{c}</th>" for c in COLUMNS)
    table = (
        '<div class="sheetwrap"><table class="diff"><thead>'
        '<tr><th colspan="4"><h3>Reference</h3></th><th class="gap"></th><th colspan="4"><h3>This run</h3></th></tr>'
        f'<tr>{head}<th class="gap"></th>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'
    )
    checks = g["checks"]
    chips = [f'<li class="{"hit" if checks.get("rows") == checks.get("expected_rows") else "miss"}">'
             f'{checks.get("rows", 0)} of {checks.get("expected_rows", len(expected))} rows</li>']
    for key, label in PROBLEMS.items():
        n = len(checks.get("problems", {}).get(key, []))
        if n:
            chips.append(f'<li class="{"warn" if key in ("format", "unconverted_date") else "miss"}">{n} × {label}</li>')
    if run["variant"] == "strong":
        chips.append(f'<li class="{"hit" if checks.get("change_list") else "miss"}">list of changes</li>')
    notes = sheet_notes(run, block)
    notes_html = f'<details class="notes"><summary>Rest of the reply</summary><pre>{esc(notes)}</pre></details>' if notes else ""
    return f'<div class="checks"><ul class="facts">{"".join(chips)}</ul></div>{table}{notes_html}'


# ---------- pages ----------

def load_tasks():
    tasks = {}
    for f in TASKS.glob("*/task.yaml"):
        t = yaml.safe_load(f.read_text())
        t["dir"] = f.parent
        tasks[t["slug"]] = t
    return [tasks[s] for s in ORDER if s in tasks] + [t for s, t in sorted(tasks.items()) if s not in ORDER]


def kitchen_items():
    groups = {}
    for variant in VARIANTS:
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


def counts(runs, variant):
    c = {g: 0 for g in GRADES}
    for r in runs:
        if r["variant"] == variant and r["grade"]:
            c[r["grade"]["grade"]] += 1
    return c


def stack(c, total):
    if not total:
        return '<div class="stack pending"><span style="width:100%"></span></div>'
    return '<div class="stack">' + "".join(
        f'<span class="{g}" style="width:{100 * n / total:.2f}%" title="{n} {GRADES[g].lower()}"></span>'
        for g, n in c.items() if n) + "</div>"


def dots(runs, variant):
    mine = sorted((r for r in runs if r["variant"] == variant), key=lambda r: (r["model"], r["run"]))
    return "".join(f'<i class="{r["grade"]["grade"] if r["grade"] else ""}"></i>' for r in mine)


def summary(runs, total_per_variant):
    rows = []
    for variant in VARIANTS:
        c = counts(runs, variant)
        graded = sum(c.values())
        label = f'{c["good"]} of {graded} usable' if graded else "voting open"
        rows.append(f'<div class="sumrow"><span>{variant.capitalize()} prompt</span>'
                    f'{stack(c, graded)}<span class="num">{label}</span></div>')
    return f'<div class="summary">{"".join(rows)}</div>'


def input_section(task):
    parts = []
    for name in task.get("inputs", []):
        src = task["dir"] / name
        shutil.copy(src, DIST / "tasks" / task["slug"] / name)
        if name.endswith(".csv"):
            rows = list(csv.reader(src.open()))
            table = "".join(
                "<tr>" + "".join(f"<{'th' if i == 0 else 'td'}>{esc(c)}</{'th' if i == 0 else 'td'}>" for c in row) + "</tr>"
                for i, row in enumerate(rows))
            content = f'<div class="sheetwrap"><table class="raw">{table}</table></div>'
        else:
            content = f'<pre class="doc">{esc(src.read_text())}</pre>'
        parts.append(f'<div class="file"><div class="filehead"><span>{esc(name)}</span>'
                     f'<a href="{esc(name)}" download>Download</a></div>{content}</div>')
    return f'<section class="block"><h2>Input</h2>{"".join(parts)}</section>' if parts else ""


def prompt_cards(task):
    return '<div class="prompts">' + "".join(
        f'<button class="prompt {v}" data-variant="{v}"><b>{v.capitalize()} prompt</b>'
        f"<pre>{esc(prompt_text(task, v))}</pre></button>" for v in VARIANTS) + "</div>"


BUCKETS = {"good": "Usable as is", "fix": "Needs a fix", "slop": "Slop", "none": "Waiting for votes"}
# Personal-call tasks (no scripted check) take their color from votes.
RULES = {"min": 3, "green": 0.8, "red": 0.3}


def board(tiles):
    """tiles: list of (bucket, html). Groups are filled here and moved by task.js."""
    groups = []
    for bucket, label in BUCKETS.items():
        mine = "".join(h for b, h in tiles if b == bucket)
        groups.append(f'<div class="group {bucket}" data-g="{bucket}"><h3>{label} <span class="count"></span></h3>'
                      f'<div class="tiles">{mine}</div></div>')
    return f'<div class="board" id="board">{"".join(groups)}</div>'


def build_task_page(task, runs, models, items):
    slug = task["slug"]
    head = (f'<section class="hero task"><div><p class="eyebrow">{esc(task["category"])}</p>'
            f'<h1>{esc(task["title"])}</h1></div>{summary(runs, len(items) // 2)}</section>')
    body = head
    (DIST / "tasks" / slug).mkdir(parents=True, exist_ok=True)
    body += input_section(task)
    body += f'<section class="block"><h2>Prompt</h2>{prompt_cards(task)}</section>'
    votable, detail, tiles = {}, {}, []
    if task["kind"] == "svg":
        for i in items:
            tiles.append(("none",
                f'<button class="tile shot" data-id="{i["id"]}" data-variant="{i["variant"]}" '
                f'aria-label="Drawing {i["id"].split(".")[1]}"><img src="{i["srcs"][0]}" alt="" loading="lazy">'
                f'<span class="sid">{i["id"].split(".")[1]}</span><span class="score"></span></button>'))
            detail[i["id"]] = (
                f'<div class="dhead"><div><h2>{i["id"].split(".")[1]}</h2>'
                '<p class="note">Model hidden until the drawings are graded.</p></div></div>'
                f'<div class="art">{"".join(f"<img src={chr(34)}{src}{chr(34)} alt={chr(34)}{chr(34)}>" for src in i["srcs"])}</div>')
            votable[i["id"]] = {"basic": True}
        note = ('<p class="note">Only logged-in visitors can vote. A drawing needs '
                f'{RULES["min"]} votes to be placed. Green: {RULES["green"]:.0%} or more upvotes. Red: under '
                f'{RULES["red"]:.0%} upvotes and more "not meeting basic standard" than plain downvotes. Otherwise yellow.</p>')
    else:
        reference = (task["dir"] / task["reference"]).read_text() if task["kind"] == "text" else None
        expected = list(csv.DictReader((task["dir"] / "expected.csv").open())) if task["slug"] == "clean-spreadsheet" else None
        for m in models:
            for variant in VARIANTS:
                for r in sorted((r for r in runs if r["variant"] == variant and r["model"] == m["id"]), key=lambda r: r["run"]):
                    g = r["grade"]
                    why = f"<small>{esc(g['why'])}</small>" if g["why"] else ""
                    compare = (email_compare(task, r, reference) if reference is not None
                               else sheet_compare(task, r, expected))
                    cost = f' · ${r["est_cost_usd"]:.4f} at API prices' if r.get("est_cost_usd") is not None else ""
                    detail[r["item"]] = (
                        f'<div class="dhead"><div><h2>{esc(m["label"])} <span>run {r["run"]}</span></h2>'
                        f'<p class="note"><a href="{r["source"]}">Raw output</a>{cost}</p></div>'
                        f'<span class="verdict {g["grade"]}">{GRADES[g["grade"]]}{why}</span></div>' + compare)
                    tiles.append((g["grade"],
                        f'<button class="tile" data-id="{r["item"]}" data-variant="{variant}" '
                        f'aria-label="{esc(m["label"])}, run {r["run"]}: {GRADES[g["grade"]]}">'
                        f'<b>{esc(m["label"])}</b><span>run {r["run"]}</span><span class="score"></span></button>'))
                    if g["grade"] == "good":
                        votable[r["item"]] = {}
        note = ('<p class="note">Usable runs can be upvoted or downvoted by logged-in visitors. '
                'Their order is shuffled on every visit.</p>')
    body += f'<section class="block"><h2>Outputs</h2>{note}{board(tiles)}</section><section id="detail" class="block" hidden></section>'
    data = {"slug": slug, "mode": "gallery" if task["kind"] == "svg" else "grid", "detail": detail,
            "votable": votable, "rules": RULES, "buckets": BUCKETS}
    body += f'<script id="data" type="application/json">{blob(data)}</script>'
    write(f"tasks/{slug}/index.html", page(task["title"], body, ["task.js"]))
    return votable


def main():
    shutil.rmtree(DIST, ignore_errors=True)
    shutil.copytree(Path(__file__).parent / "static", DIST / "static")
    tasks = load_tasks()
    models = yaml.safe_load((ROOT / "models.yaml").read_text())["models"]
    all_runs = load_runs()
    known, cards = {}, []
    for task in tasks:
        slug = task["slug"]
        runs = [r for r in all_runs if r["task"] == slug]
        items = kitchen_items() if task["kind"] == "svg" else [{"id": r["item"], "variant": r["variant"]} for r in runs]
        known.update(build_task_page(task, runs, models, items))
        field = "".join(f'<div class="field"><span>{v.capitalize()}</span><div class="dots">{dots(runs, v)}</div></div>'
                        for v in VARIANTS)
        cards.append(
            f'<a class="card" href="/tasks/{slug}/"><p class="eyebrow">{esc(task["category"])}</p>'
            f'<h2>{esc(task["title"])}</h2>{field}</a>')
    write("items.json", json.dumps(known))
    legend = "".join(f'<span class="{g}">{label}</span>' for g, label in GRADES.items())
    write("index.html", page("Vellery", (
        '<section class="hero home"><h1>Same prompt.<br>Different results.</h1>'
        f'<p class="lede">{len(models)} AI models did the same everyday tasks five times each, once with a vague prompt and once '
        'with a precise one. Every output is here, graded, with the reason it passed or failed.</p></section>'
        f'<section id="tasks" class="block"><div class="legend">{legend}<span>not graded yet</span></div>'
        f'<div class="cards">{"".join(cards)}</div></section>')))
    print(f"{len(tasks)} tasks, {len(known)} votable outputs -> {DIST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
