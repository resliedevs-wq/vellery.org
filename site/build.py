#!/usr/bin/env python3
"""Build the static site into dist/.

Reads tasks/, outputs/ and grading/kitchen/ and writes:
  index.html                 the finding, every task, and how each model did
  tasks/<slug>/index.html    both prompts with their results, the input, every run
  items.json                 the drawings visitors can rate (the Worker only accepts these)

Scripted tasks (email, spreadsheet) show one row per model with the vague and
specific prompt side by side. Puzzles show each model's chances and whether
it found the answer. Drawings stay under blind ids until a visitor
asks to reveal them; the Worker holds the model mapping.

Usage: python3 site/build.py
"""

import csv
import hashlib
import html
import json
import re
import shutil
import sys
from pathlib import Path
from xml.etree import ElementTree

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "runner"))
from grade import EMAIL_FACTS, extract_csv, grade_answer, pair_rows, parse_amount, parse_date, sheet_rows  # noqa: E402

OUTPUTS = ROOT / "outputs"
TASKS = ROOT / "tasks"
KITCHEN = ROOT / "grading" / "kitchen"
DIST = ROOT / "dist"
REPO = "https://github.com/resliedevs-wq/vellery.org"
ORDER = ["shorten-email", "clean-spreadsheet", "kitchen-illustration", "pelican-bicycle", "night-sky-message"]
VARIANTS = ("weak", "strong")
VARIANT_LABEL = {"weak": "Vague prompt", "strong": "Specific prompt"}
VARIANT_SHORT = {"weak": "Vague", "strong": "Specific"}
GRADES = {"good": "Usable", "fix": "Needs fixing", "slop": "Unusable"}
GLYPH = {"good": "✓", "fix": "!", "slop": "✕"}
COLUMNS = ["Date", "Description", "Category", "Amount"]
# Where each fact shows up in a text, for highlighting. Presence itself comes
# from the grader, so the page and the grade can't disagree.
FACT_SPANS = {**EMAIL_FACTS, "AV fee waived": r"\bAV\b|\bwaiv\w*"}
PROBLEMS = {
    "wrong_date": "date wrong", "wrong_amount": "amount changed", "wrong_category": "category wrong",
    "unconverted_date": "date not converted", "format": "formatting", "extra_or_renamed": "extra or renamed row",
}
# Drawings take their verdict from visitor ratings once enough have come in.
RULES = {"min": 3, "green": 0.8, "red": 0.3}
REVEAL_MODULE = ROOT / "site" / "reveal.generated.js"
HOW = {
    "text": "Checked by script",
    "sheet": "Checked by script",
    "svg": "Rated blind by visitors",
    "puzzle": "Checked by script",
}
SCRIPTED = ("text", "sheet")
CHANCE = {1: "first", 2: "second"}


def esc(s):
    return html.escape(str(s), quote=True)


def blob(data):
    return json.dumps(data).replace("<", "\\u003c")


def pct(n, d):
    return round(100 * n / d) if d else 0


def page(title, body, scripts=(), description=""):
    tags = "".join(f'<script src="/static/{s}" defer></script>' for s in scripts)
    full = "Vellery" if title == "Vellery" else f"{title} · Vellery"
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{esc(full)}</title>"
        + (f'<meta name="description" content="{esc(description)}">' if description else "")
        + '<link rel="icon" href="/static/favicon.svg" type="image/svg+xml">'
        '<link rel="preload" href="/static/fonts/fraunces.woff2" as="font" type="font/woff2" crossorigin>'
        '<link rel="preload" href="/static/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>'
        '<link rel="stylesheet" href="/static/style.css">'
        '</head><body>'
        '<header class="site"><div class="wrap bar">'
        '<a class="brand" href="/"><span class="mark" aria-hidden="true"><i></i><i></i><i></i></span>Vellery</a>'
        '<nav><a href="/#tasks">Tasks</a><a href="/#models">Models</a><a href="/#method">Method</a>'
        f'<a href="{REPO}">GitHub</a></nav></div></header>'
        f"<main>{body}</main>"
        '<footer class="site"><div class="wrap foot">'
        '<p><b>Vellery</b> is an independent record of how AI models handle real tasks. '
        'It is not affiliated with any model maker.</p>'
        f'<p>Every prompt, raw output and grading script is public on <a href="{REPO}">GitHub</a>.</p>'
        f"</div></footer>{tags}</body></html>"
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
            "tested": json.loads((attempt / "attempt.json").read_text())["started"][:10],
            "item": f"{meta['task']}.{digest.hexdigest()[:6]}",
            "response": (attempt / "response.md").read_text(),
            "grade": json.loads(grade_file.read_text()) if grade_file.exists() else None,
            "run_dir": run_dir,
            "source": f"{REPO}/tree/main/{run_dir.relative_to(ROOT)}",
        })
    return runs


def prompt_text(task, variant):
    """The prompt as sent, with line breaks inside a paragraph joined for display."""
    text = re.sub(r"\{\{(.+?)\}\}", r"[\1 attached]", task["prompts"][variant]).strip()
    out = []
    for line in text.splitlines():
        joins = out and out[-1] and not line.startswith(("-", "[")) and not out[-1].startswith("-") and line
        if joins:
            out[-1] += " " + line
        else:
            out.append(line)
    return "\n".join(out)


def money(value):
    if value is None:
        return "–"
    if value == 0:
        return "$0"
    return f"${value:.2f}" if value >= 0.01 else "<$0.01"


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
    checks = run["grade"]["checks"]
    strong = run["variant"] == "strong"
    limit = task["checks"]["max_words"] if strong else checks["original_words"]
    over = checks["words"] > limit if strong else checks["words"] >= limit
    meter = (f'<div class="meter{" over" if over else ""}"><span style="width:{min(100, 100 * checks["words"] / limit):.0f}%"></span></div>'
             f'<span><b>{checks["words"]}</b> words · {"limit" if strong else "original had"} {limit}</span>')
    chips = "".join(f'<li class="{"miss" if name in checks["missing"] else "hit"}">{esc(name)}</li>' for name in FACT_SPANS)
    chips += "".join(f'<li class="miss">added: {esc(i)}</li>' for i in checks["invented"])
    return (
        f'<div class="checks"><div class="words">{meter}</div>'
        f'<div><p class="label">Facts that must survive</p><ul class="chips">{chips}</ul></div></div>'
        '<div class="pair">'
        f'<div><p class="label">This run</p><pre class="doc">{mark_facts(run["response"].strip(), checks["invented"])}</pre></div>'
        f'<div><p class="label">A reference answer</p><pre class="doc muted">{mark_facts(reference)}</pre></div>'
        "</div>"
    )


def email_metric(run):
    return f'{run["grade"]["checks"]["words"]}'


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
    checks = run["grade"]["checks"]
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
                f'<td class="{cell_class(c, out.get(c), ref[c])}" title="Expected: {esc(ref[c])}">{esc(out.get(c) or "")}</td>'
                for c in COLUMNS)
        body.append(f'<tr>{right}<td class="gap"></td>{left}</tr>')
    for best, out, _ in pairs:
        if best is None:
            right = "".join(f'<td class="bad">{esc(out.get(c) or "")}</td>' for c in COLUMNS)
            body.append(f'<tr class="extra">{right}<td class="gap"></td><td colspan="4" class="gone">not in the correct sheet</td></tr>')
    head = "".join(f"<th>{c}</th>" for c in COLUMNS)
    table = (
        '<div class="scroll"><table class="diff"><thead>'
        '<tr class="over"><th colspan="4">This run</th><th class="gap"></th><th colspan="4">Correct answer</th></tr>'
        f'<tr>{head}<th class="gap"></th>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'
    )
    chips = [f'<li class="{"hit" if checks.get("rows") == checks.get("expected_rows") else "miss"}">'
             f'{checks.get("rows", 0)} of {checks.get("expected_rows", len(expected))} rows</li>']
    for key, label in PROBLEMS.items():
        n = len(checks.get("problems", {}).get(key, []))
        if n:
            chips.append(f'<li class="{"warn" if key in ("format", "unconverted_date") else "miss"}">{n} × {label}</li>')
    if run["variant"] == "strong":
        chips.append(f'<li class="{"hit" if checks.get("change_list") else "miss"}">list of changes</li>')
    notes = sheet_notes(run, block)
    notes_html = (f'<details class="notes"><summary>The rest of the reply</summary><pre>{esc(notes)}</pre></details>'
                  if notes else "")
    key = ('<p class="hint"><span class="sw bad"></span>wrong value <span class="sw fmt"></span>right value, '
           'wrong format · hover a cell to see what was expected</p>')
    return f'<div class="checks"><ul class="chips">{"".join(chips)}</ul></div>{key}{table}{notes_html}'


# ---------- loading ----------

def load_tasks():
    tasks = {}
    for f in TASKS.glob("*/task.yaml"):
        t = yaml.safe_load(f.read_text())
        if not t.get("published", True):
            continue
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
        items.append({"id": f"kitchen-illustration.{kid}", "variant": variant, "srcs": srcs, "text": ""})
    return items


def drawing_items(runs):
    """Keep every response, including inline SVG and text-only drawings."""
    items = []
    for r in runs:
        attempt = r["run_dir"] / f"attempt-{r['attempts']}"
        files = sorted(p for p in (attempt / "files").rglob("*") if p.suffix.lower() in (".svg", ".png"))
        srcs = []
        invalid_svg = False
        repaired = False
        for n, source in enumerate(files):
            dest = f"img/{r['task']}/{r['item'].split('.')[1]}-{n}{source.suffix.lower()}"
            if source.suffix.lower() == ".svg":
                try:
                    ElementTree.parse(source)
                except ElementTree.ParseError:
                    # XML forbids "--" inside comments. Remove decorative comments
                    # from the preview only, and require the result to parse.
                    raw = source.read_text()
                    preview = re.sub(r"<!--(.*?)-->", lambda m: "" if "--" in m[1] else m[0], raw, flags=re.S)
                    try:
                        ElementTree.fromstring(preview)
                    except ElementTree.ParseError:
                        invalid_svg = True
                        continue
                    repaired = True
                    write(dest, preview)
                    srcs.append("/" + dest)
                    continue
            (DIST / dest).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(source, DIST / dest)
            srcs.append("/" + dest)
        if not srcs and not files:
            svg = re.search(r"<svg\b[\s\S]*?</svg>", r["response"])
            if svg:
                dest = f"img/{r['task']}/{r['item'].split('.')[1]}.svg"
                write(dest, svg.group())
                srcs.append("/" + dest)
        text = r["response"] if not srcs else ""
        if invalid_svg and not srcs:
            text = "The returned SVG contains invalid XML and cannot be displayed.\n\n" + text
        # Strip only the presentation fence, leaving the model's drawing intact.
        if text.strip().startswith("```"):
            text = re.sub(r"^```[^\n]*\n|\n```\s*$", "", text.strip())
        items.append({"id": r["item"], "variant": r["variant"], "srcs": srcs, "text": text, "repaired": repaired})
    return items


def counts(runs, variant):
    c = {g: 0 for g in GRADES}
    for r in runs:
        if r["variant"] == variant and r["grade"]:
            c[r["grade"]["grade"]] += 1
    return c


def stack(c):
    total = sum(c.values())
    if not total:
        return '<div class="stack"></div>'
    return '<div class="stack">' + "".join(
        f'<span class="{g}" style="width:{100 * n / total:.2f}%" title="{n} {GRADES[g].lower()}"></span>'
        for g, n in c.items() if n) + "</div>"


def breakdown(c):
    return '<ul class="breakdown">' + "".join(
        f'<li class="{g}"><b>{n}</b> {GRADES[g].lower()}</li>' for g, n in c.items()) + "</ul>"


def reveal_key(models, drawings=()):
    """id -> model and run for the blind drawings. Never written into the pages: only
    the Worker holds it, and hands it out when a visitor asks to see the models."""
    key_file = KITCHEN / "key.json"
    labels = {m["id"]: m["label"] for m in models}
    out = {}
    if not key_file.exists():
        raise ValueError("Missing grading/kitchen/key.json: cannot build model reveal")
    key = json.loads(key_file.read_text())
    drawing_ids = {p.stem[:4] for variant in VARIANTS
                   for p in (KITCHEN / variant).iterdir() if p.suffix in (".svg", ".png")}
    if not drawing_ids or drawing_ids != set(key):
        raise ValueError("Kitchen model key must cover exactly all blind drawings")
    for kid, k in key.items():
        out[f"kitchen-illustration.{kid}"] = {"id": k["model"], "label": labels[k["model"]], "run": k["run"]}
    for r in drawings:
        out[r["item"]] = {"id": r["model"], "label": labels[r["model"]], "run": r["run"]}
    REVEAL_MODULE.write_text(f"export default {json.dumps(out)};\n")
    return bool(out)


def avg_cost(selected):
    costs = [r.get("est_cost_usd_all_attempts", r.get("est_cost_usd")) for r in selected]
    if not costs or any(c is None for c in costs):
        return None
    return sum(costs) / len(costs)


def tested(selected):
    dates = sorted({r["tested"] for r in selected})
    return " – ".join(dict.fromkeys([dates[0], dates[-1]])) if dates else ""


# ---------- task pages ----------

def task_head(task, extra=""):
    return (
        '<section class="wrap taskhead">'
        f'<p class="crumb"><a href="/#tasks">Tasks</a><span>/</span>{esc(task["category"])}</p>'
        f'<h1>{esc(task["title"])}</h1>'
        f'<p class="lede">{esc(task.get("summary", ""))}</p>'
        f'<p class="how"><span class="pill">{HOW[task["kind"]]}</span>{extra}</p>'
        "</section>"
    )


def prompt_card(task, variant, result):
    rubric = task.get("rubric", {}).get(variant, {}).get("good", "")
    rubric = esc(" ".join(str(rubric).split()))
    checks = task.get("checks", {})
    if task["kind"] == "svg" and variant == "strong" and isinstance(checks, dict) and checks.get("major"):
        items = [*checks.get("major", []), *checks.get("minor", [])]
        rubric = (f"<details><summary>all {len(items)} checks pass</summary>"
                  f"<ul>{''.join(f'<li>{esc(i)}</li>' for i in items)}</ul></details>")
    return (
        f'<article class="pcard {variant}" data-variant="{variant}">'
        f'<header><span class="ptag">{VARIANT_LABEL[variant]}</span></header>'
        f'<pre class="ptext">{esc(prompt_text(task, variant))}</pre>'
        f'<div class="presult">{result}</div>'
        + (f'<div class="rubric"><b>Counts as usable:</b> {rubric}</div>' if rubric else "")
        + "</article>"
    )


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
            content = f'<div class="scroll"><table class="raw">{table}</table></div>'
            what = f"{len(rows) - 1} rows"
        else:
            text = src.read_text()
            content = f'<pre class="doc">{esc(text)}</pre>'
            what = f"{len(text.split())} words"
        parts.append(
            f'<details class="input"><summary><span class="fname">{esc(name)}</span>'
            f'<span class="muted">{what} · attached to both prompts</span><span class="open">Show</span></summary>'
            f'<div class="inputbody">{content}<a class="dl" href="{esc(name)}" download>Download {esc(name)}</a></div></details>')
    return "".join(parts)


def build_scripted(task, runs, models):
    slug = task["slug"]
    reference = (task["dir"] / task["reference"]).read_text() if task["kind"] == "text" else None
    expected = list(csv.DictReader((task["dir"] / "expected.csv").open())) if task["kind"] == "sheet" else None
    cards = []
    for v in VARIANTS:
        c = counts(runs, v)
        total = sum(c.values())
        result = (f'<div class="big"><b>{pct(c["good"], total)}%</b><span>usable as is</span></div>'
                  f'{stack(c)}{breakdown(c)}')
        cards.append(prompt_card(task, v, result))
    detail = {}
    rows = []
    for order, m in enumerate(models):
        mine = [r for r in runs if r["model"] == m["id"]]
        if not mine:
            continue
        groups = []
        score = 0
        for v in VARIANTS:
            cells = []
            for r in sorted((r for r in mine if r["variant"] == v), key=lambda r: r["run"]):
                g = r["grade"]
                grade = g["grade"]
                score += grade == "good"
                why = g["why"] or GRADES[grade]
                metric = email_metric(r) if task["kind"] == "text" else ""
                compare = email_compare(task, r, reference) if reference is not None else sheet_compare(task, r, expected)
                cost = r.get("est_cost_usd_all_attempts", r.get("est_cost_usd"))
                detail[r["item"]] = (
                    f'<div class="dhead"><div><p class="crumb">{VARIANT_LABEL[v]} · run {r["run"]} of 5</p>'
                    f'<h2>{esc(m["label"])}</h2>'
                    f'<p class="meta">Tested {r["tested"]}'
                    + (f" · {money(cost)} at API prices" if cost is not None else "")
                    + f' · <a href="{r["source"]}">Raw output</a></p></div>'
                    f'<div class="verdict {grade}"><b>{GLYPH[grade]} {GRADES[grade]}</b>'
                    + (f'<span>{esc(g["why"])}</span>' if g["why"] else "") + "</div></div>"
                    + compare)
                cells.append(
                    f'<button class="cell {grade}" data-id="{r["item"]}" '
                    f'title="Run {r["run"]}: {esc(why)}" aria-label="{esc(m["label"])}, {VARIANT_SHORT[v].lower()} prompt, run {r["run"]}: {esc(why)}">'
                    f'<span class="g">{GLYPH[grade]}</span>'
                    + (f'<span class="n">{metric}</span>' if metric else "") + "</button>")
            groups.append(f'<div class="cells" data-variant="{v}"><span class="vlab">{VARIANT_SHORT[v]}</span>{"".join(cells)}</div>')
        cost = avg_cost(mine)
        rows.append((-score, order,
            f'<div class="rrow"><div class="rmodel"><b>{esc(m["label"])}</b><span>{tested(mine)}</span></div>'
            f'{"".join(groups)}<div class="rnum"><b>{score}</b>/10</div><div class="rcost">{money(cost)}</div></div>'))
    rows.sort(key=lambda r: r[:2])
    metric_note = (" Numbers in the cells are word counts; the original email has "
                   f'{runs[0]["grade"]["checks"]["original_words"]} words.' if task["kind"] == "text" and runs else "")
    table = (
        '<div class="results" id="results">'
        '<div class="rrow rhead"><div>Model</div>'
        f'<div class="ch">{VARIANT_LABEL["weak"]} <small>runs 1–5</small></div>'
        f'<div class="ch">{VARIANT_LABEL["strong"]} <small>runs 1–5</small></div>'
        '<div class="rnum">Usable</div><div class="rcost" title="Average estimated API cost per run">Cost/run</div></div>'
        + "".join(r[2] for r in rows) + "</div>")
    legend = '<div class="legend">' + "".join(
        f'<span class="{g}"><i>{GLYPH[g]}</i>{label}</span>' for g, label in GRADES.items()) + "</div>"
    body = (
        task_head(task)
        + f'<section class="wrap block"><h2 class="sec">The two prompts</h2><div class="pcards">{"".join(cards)}</div>'
        + input_section(task) + "</section>"
        + '<section class="wrap block"><div class="sechead"><h2 class="sec">Every run</h2>' + legend + "</div>"
        + f'<p class="hint">Each model ran each prompt five times. Select a cell to see the output and what the check found.{metric_note}</p>'
        + table + "</section>"
    )
    data = {"slug": slug, "mode": "scripted", "detail": detail}
    body += f'<script id="data" type="application/json">{blob(data)}</script>'
    write(f"tasks/{slug}/index.html", page(task["title"], body, ["task.js"], task.get("summary", "")))
    return {}


def puzzle_results(task, runs, models):
    """Per model, in models.yaml order: its runs and the chance that solved it (None if none did)."""
    out = []
    for m in models:
        mine = sorted((r for r in runs if r["model"] == m["id"]), key=lambda r: r["run"])
        if mine:
            won = next((r["run"] for r in mine if r["grade"] and r["grade"]["grade"] == "good"), None)
            out.append((m, mine, won))
    return out


def mark_answer(text, answer):
    words = [re.escape(w) for w in answer.split()]
    pattern = re.compile(r"[\W_]*".join(words), re.I)
    out, last = [], 0
    for m in pattern.finditer(text):
        out += [esc(text[last:m.start()]), f"<mark>{esc(m.group(0))}</mark>"]
        last = m.end()
    return "".join(out) + esc(text[last:])


def solution_figure(task, image):
    stars = json.loads((task["dir"] / "stars.json").read_text())
    marks = "".join(
        f'<circle class="space" cx="{x}" cy="{y}" r="6"/>' if c == " " else
        f'<g><circle cx="{x}" cy="{y}" r="7"/><text x="{x}" y="{y - 12}">{esc(c)}</text></g>'
        for x, y, c in stars)
    return (f'<figure class="solved"><img src="{image}" alt="">'
            f'<svg viewBox="0 0 800 500" aria-hidden="true">{marks}</svg></figure>')


def build_puzzle(task, runs, models):
    slug = task["slug"]
    variant = next(iter(task["prompts"]))
    image = task["files"][0]
    shutil.copy(task["dir"] / image, DIST / "tasks" / slug / image)
    results = puzzle_results(task, runs, models)
    chances = task["runs"]
    by = {n: sum(1 for *_, won in results if won == n) for n in range(1, chances + 1)}
    solved = sum(by.values())
    missed = sum(1 for _, mine, won in results if not won and len(mine) == chances)
    finished = solved + missed
    detail, rows = {}, []
    for order, (m, mine, won) in enumerate(results):
        cells = []
        for n in range(1, chances + 1):
            r = next((r for r in mine if r["run"] == n), None)
            if r is None:
                why = "Not needed: solved on the first chance" if won and won < n else "Not run"
                cells.append(f'<span class="cell skip" title="{why}">–</span>')
                continue
            grade = r["grade"]["grade"]
            cost = r.get("est_cost_usd_all_attempts", r.get("est_cost_usd"))
            verdict = "Found the message" if grade == "good" else "Missed it"
            detail[r["item"]] = (
                f'<div class="dhead"><div><p class="crumb">Chance {n} of {chances}</p>'
                f'<h2>{esc(m["label"])}</h2>'
                f'<p class="meta">Tested {r["tested"]}'
                + (f" · {money(cost)} at API prices" if cost is not None else "")
                + f' · <a href="{r["source"]}">Raw output</a></p></div>'
                f'<div class="verdict {grade}"><b>{GLYPH[grade]} {verdict}</b></div></div>'
                f'<div class="answerwrap"><p class="label">The model’s answer</p>'
                f'<pre class="doc answer">{mark_answer(re.sub(r"\*\*|__|`", "", r["response"]).strip(), task["answer"])}</pre></div>')
            cells.append(
                f'<button class="cell {grade}" data-id="{r["item"]}" title="Chance {n}: {verdict.lower()}" '
                f'aria-label="{esc(m["label"])}, chance {n}: {verdict.lower()}"><span class="g">{GLYPH[grade]}</span></button>')
        outcome = (f'<b class="good">Solved on the {CHANCE.get(won, f"#{won}")} chance</b>' if won
                   else f'<b class="slop">Not solved</b>' if len(mine) == chances
                   else '<b class="muted">Still running</b>')
        costs = [r.get("est_cost_usd_all_attempts", r.get("est_cost_usd")) for r in mine]
        cost = None if None in costs else sum(costs)
        rows.append((won or 99, order,
            f'<div class="prow"><div class="rmodel"><b>{esc(m["label"])}</b><span>{tested(mine)}</span></div>'
            f'<div class="cells two">{"".join(cells)}</div><div class="pout">{outcome}</div>'
            f'<div class="rcost">{money(cost)}</div></div>'))
    rows.sort(key=lambda r: r[:2])
    table = ('<div class="results" id="results"><div class="prow rhead"><div>Model</div>'
             + "".join(f'<div class="ch">Chance {n}</div>' for n in range(1, chances + 1)).join(['<div class="cells two">', "</div>"])
             + '<div>Outcome</div><div class="rcost" title="Estimated API cost of all chances">Cost</div></div>'
             + "".join(r[2] for r in rows) + "</div>")
    breakdown_ = "".join(
        f'<li class="{g}"><b>{n}</b> {label}</li>' for g, label, n in (
            ("good", "on the first chance", by.get(1, 0)), ("fix", "on the second", sum(v for k, v in by.items() if k > 1)),
            ("slop", "not solved", missed)))
    card = (
        '<article class="pcard strong puzzle">'
        '<header><span class="ptag">The prompt</span></header>'
        f'<pre class="ptext">{esc(prompt_text(task, variant))}</pre>'
        f'<div class="presult"><div class="big"><b>{solved}<small>/{finished}</small></b><span>models found the message</span></div>'
        f'<ul class="breakdown">{breakdown_}</ul></div>'
        f'<div class="rubric"><b>Counts as solved:</b> the answer contains the hidden sentence. '
        f'Each model gets {chances} chances in fresh sessions; the second only if the first misses.</div>'
        "</article>")
    spoiler = (
        '<details class="spoiler"><summary><span>Show the answer</span><span class="muted">Try it yourself first</span></summary>'
        f'<div class="spoilbody"><p class="sentence">“{esc(task["answer"].capitalize())}.”</p>'
        f'<p>{esc(" ".join(task["solution"].split()))}</p>{solution_figure(task, image)}</div></details>')
    body = (
        task_head(task)
        + '<section class="wrap block"><h2 class="sec">The puzzle</h2><div class="puzzle-top">'
        f'<figure class="pimage"><img src="{image}" alt="A moonlit lake under a starry sky with an aurora">'
        f'<figcaption><span class="fname">{esc(image)}</span> · given to the model as a file · '
        f'<a href="{esc(image)}" download>Download</a></figcaption></figure>{card}</div>{spoiler}</section>'
        + '<section class="wrap block"><h2 class="sec">Every model</h2>'
        + '<p class="hint">Select a chance to read the model’s full answer.</p>' + table + "</section>")
    data = {"slug": slug, "mode": "scripted", "detail": detail}
    body += f'<script id="data" type="application/json">{blob(data)}</script>'
    write(f"tasks/{slug}/index.html", page(task["title"], body, ["task.js"], task.get("summary", "")))
    return {}


def build_gallery(task, items, models, can_reveal):
    slug = task["slug"]
    detail, votable = {}, {}
    cards = []
    for v in VARIANTS:
        n = sum(1 for i in items if i["variant"] == v)
        result = (f'<div class="big" data-crowd="{v}"><b>–</b><span>usable, by visitor ratings</span></div>'
                  f'<div class="stack" data-crowd-stack="{v}"></div>'
                  f'<p class="crowdnote" data-crowd-note="{v}">{n} drawings</p>')
        cards.append(prompt_card(task, v, result))
    tiles = []
    for i in items:
        kid = i["id"].split(".")[1]
        preview = (f'<img src="{i["srcs"][0]}" alt="" loading="lazy" decoding="async">' if i["srcs"]
                   else f'<pre class="drawing-text">{esc(i.get("text") or "No drawing returned.")}</pre>')
        artwork = ("".join(f'<img src="{src}" alt="Drawing {kid}">' for src in i["srcs"])
                   if i["srcs"] else f'<pre class="drawing-response">{esc(i.get("text") or "No drawing returned.")}</pre>')
        note = '<p class="hint">Invalid XML comments were removed so this preview can render.</p>' if i.get("repaired") else ""
        tiles.append(
            f'<button class="shot" data-id="{i["id"]}" data-variant="{i["variant"]}" aria-label="Drawing {kid}">'
            f'<span class="frame">{preview}</span><span class="cap"></span></button>')
        detail[i["id"]] = {"kid": kid, "html": f'<div class="art">{artwork}</div>{note}', "variant": i["variant"]}
        votable[i["id"]] = {"basic": True}
    tabs = '<div class="seg" role="tablist" aria-label="Which prompt">' + "".join(
        f'<button role="tab" data-variant="{v}" aria-selected="{str(v == "strong").lower()}">{VARIANT_LABEL[v]}'
        f' <small>{sum(1 for i in items if i["variant"] == v)}</small></button>' for v in VARIANTS) + "</div>"
    toolbar = (
        '<div class="toolbar">' + tabs +
        '<div class="progress"><span id="progress"></span>'
        '<div class="pbar"><span id="pbar"></span></div></div>'
        '<div class="actions"><button class="btn primary" id="rate">Start rating</button>'
        + ('<button class="btn" id="reveal">Reveal models</button>' if can_reveal else "") + "</div></div>")
    gallery = (
        '<div id="blind"><h3 class="sub">Unrevealed <span class="count"></span></h3>'
        f'<div class="grid" id="grid">{"".join(tiles)}</div></div>'
        '<div id="revealed" hidden><h3 class="sub">Revealed, by model <span class="count"></span></h3>'
        '<p class="hint">Borders show the visitor verdict once a drawing has at least three ratings.</p>'
        '<div id="byModel"></div></div>')
    body = (
        task_head(task, '<span class="muted">Model names stay hidden until you reveal them.</span>')
        + f'<section class="wrap block"><h2 class="sec">The two prompts</h2><div class="pcards">{"".join(cards)}</div></section>'
        + '<section class="wrap block"><div class="sechead"><h2 class="sec">The drawings</h2></div>'
        + '<p class="hint">Rate each drawing the way you would if you had asked for it: could you use it as is? '
          'Your ratings are anonymous and tied to this browser. Revealing a drawing’s model ends rating for it.</p>'
        + toolbar + gallery + "</section>"
    )
    data = {"slug": slug, "mode": "gallery", "detail": detail, "rules": RULES, "grades": GRADES,
            "reveal": can_reveal, "models": [{"id": m["id"], "label": m["label"]} for m in models]}
    body += f'<script id="data" type="application/json">{blob(data)}</script>'
    write(f"tasks/{slug}/index.html", page(task["title"], body, ["task.js"], task.get("summary", "")))
    return votable


# ---------- home ----------

def home(tasks, models, all_runs, galleries):
    scripted = [t for t in tasks if t["kind"] in SCRIPTED]
    puzzles = [t for t in tasks if t["kind"] == "puzzle"]
    by_variant = {v: counts([r for r in all_runs if r["task"] in {t["slug"] for t in scripted}], v) for v in VARIANTS}
    share = {v: pct(by_variant[v]["good"], sum(by_variant[v].values())) for v in VARIANTS}
    total_runs = len(all_runs)
    rows = []
    for t in tasks:
        runs = [r for r in all_runs if r["task"] == t["slug"]]
        if t["kind"] == "svg":
            thumbs = [i for i in galleries.get(t["slug"], []) if i["srcs"] and i["variant"] == "strong"][:4]
            right = ('<div class="tside"><div class="thumbs">' + "".join(f'<img src="{i["srcs"][0]}" alt="" loading="lazy">' for i in thumbs)
                     + '</div><span class="cta">Rate the drawings →</span></div>')
            stat = f'{len(galleries.get(t["slug"], []))} drawings'
        elif t["kind"] == "puzzle":
            results = puzzle_results(t, runs, models)
            results = [x for x in results if x[2] or len(x[1]) == t["runs"]]
            won = sum(1 for *_, w in results if w)
            dots = "".join(f'<i class="{"good" if w == 1 else "fix" if w else "slop"}" title="{esc(m["label"])}"></i>'
                           for m, _, w in results)
            right = (f'<div class="tside puz"><img src="/tasks/{t["slug"]}/{t["files"][0]}" alt="" loading="lazy">'
                     f'<p class="pstat"><b>{won} of {len(results)}</b> models found it<span class="dots">{dots}</span></p></div>')
            stat = f"{len(runs)} runs"
        else:
            bars = []
            for v in VARIANTS:
                c = counts(runs, v)
                bars.append(f'<div class="vbar"><span class="vl">{VARIANT_SHORT[v]}</span>{stack(c)}'
                            f'<b>{pct(c["good"], sum(c.values()))}%</b></div>')
            right = '<div class="vbars">' + "".join(bars) + '<p class="vcap">share of runs usable as is</p></div>'
            stat = f"{len(runs)} runs"
        rows.append(
            f'<a class="trow" href="/tasks/{t["slug"]}/"><div class="tinfo"><p class="crumb">{esc(t["category"])}'
            f'<span>·</span>{HOW[t["kind"]]}<span>·</span>{stat}</p>'
            f'<h3>{esc(t["title"])}</h3><p>{esc(t.get("summary", ""))}</p></div>{right}</a>')

    # How each model did on the checked tasks. Drawings stay out: their models are blind.
    head = "".join(f'<th colspan="2" class="tcol">{esc(t["title"])}</th>' for t in scripted)
    sub = "".join(f'<th>{VARIANT_SHORT[v]}</th>' for _ in scripted for v in VARIANTS)
    body = []
    for order, m in enumerate(models):
        mine = [r for r in all_runs if r["model"] == m["id"] and r["task"] in {t["slug"] for t in scripted}]
        if not mine:
            continue
        pz = []
        for t in puzzles:
            res = puzzle_results(t, [r for r in all_runs if r["task"] == t["slug"]], [m])
            if not res:
                pz.append('<td class="pz" title="Not run yet">–</td>')
                continue
            won = res[0][2]
            if not won and len(res[0][1]) < t["runs"]:
                pz.append('<td class="pz" title="Still running">…</td>')
            elif not won:
                pz.append(f'<td class="pz"><span class="slop" title="Not solved in {t["runs"]} chances">{GLYPH["slop"]}</span></td>')
            else:
                pz.append(f'<td class="pz"><span class="{"good" if won == 1 else "fix"}" title="Solved on chance {won}">'
                          f'{GLYPH["good"]}{"" if won == 1 else f"<small>{won}</small>"}</span></td>')
        cells, total = [], 0
        for t in scripted:
            for v in VARIANTS:
                sel = [r for r in mine if r["task"] == t["slug"] and r["variant"] == v]
                good = sum(r["grade"]["grade"] == "good" for r in sel if r["grade"])
                total += good
                dots = "".join(f'<i class="{r["grade"]["grade"] if r["grade"] else ""}"></i>'
                               for r in sorted(sel, key=lambda r: r["run"]))
                first = " first" if v == VARIANTS[0] and t is not scripted[0] else ""
                cells.append(f'<td class="run{first}"><span class="dots" title="{good} of {len(sel)} usable">{dots}</span></td>')
        body.append((-total, order, f'<tr><th scope="row">{esc(m["label"])}</th>{"".join(cells)}'
                                    f'<td class="num"><b>{total}</b>/{len(mine)}</td><td class="num">{money(avg_cost(mine))}</td>{"".join(pz)}</tr>'))
    body.sort(key=lambda r: r[:2])
    table = (f'<div class="scroll"><table class="models"><thead><tr><th rowspan="2">Model</th>{head}'
             '<th rowspan="2" class="num">Usable</th><th rowspan="2" class="num" title="Average estimated API cost per run">Cost/run</th>'
             + "".join(f'<th rowspan="2" class="pzh" title="{esc(t["title"])}: ✓ first chance, ✓2 second chance">{esc(t["category"])}</th>' for t in puzzles)
             + '</tr>'
             f'<tr class="subh">{sub}</tr></thead><tbody>{"".join(r[2] for r in body)}</tbody></table></div>')
    legend = '<div class="legend">' + "".join(
        f'<span class="{g}"><i>{GLYPH[g]}</i>{label}</span>' for g, label in GRADES.items()) + "</div>"

    finding = (
        '<div class="finding">'
        f'<div class="fig weak"><b>{share["weak"]}%</b><span>usable with a <em>vague</em> prompt</span></div>'
        f'<div class="fig strong"><b>{share["strong"]}%</b><span>usable with a <em>specific</em> prompt</span></div>'
        f'<p class="fnote">Across the {sum(sum(by_variant[v].values()) for v in VARIANTS)} runs of the script-checked tasks.</p>'
        "</div>")
    method = [
        ("Same request, many times", "Each model gets each everyday prompt five separate times, in a fresh session. "
         "A model that gets it right once can still get it wrong the next time, so we show every try. "
         "Puzzles get two chances; the second only if the first misses."),
        ("Vague versus specific", "Every task has a vague prompt, the way people often type, and a specific one "
         "that says what a good result needs. Both get the same input."),
        ("Graded in the open", "Text, spreadsheets and puzzle answers are checked by a script anyone can rerun. "
         "Drawings are rated by visitors, blind, before the model is revealed."),
        ("Run like a real user would", "Each model runs through its maker’s own app or command-line tool with its default "
         "settings. Costs are estimated at each maker’s published API prices."),
    ]
    html_ = (
        '<section class="wrap hero">'
        '<p class="kicker">An open record of what AI models actually do</p>'
        '<h1>Ask the same thing twice. <em>Get a different answer.</em></h1>'
        f'<p class="lede">We give {len(models)} AI models the same tasks again and again, each time in a fresh session: '
        f'everyday work with a vague and a specific prompt, drawings rated blind, and puzzles with one right answer. '
        f'Here are all {total_runs} results.</p>'
        + finding + "</section>"
        + f'<section class="wrap block" id="tasks"><h2 class="sec">Tasks</h2><div class="tasks">{"".join(rows)}</div></section>'
        + '<section class="wrap block" id="models"><div class="sechead"><h2 class="sec">How each model did</h2>' + legend + "</div>"
        + '<p class="hint">Script-checked tasks only, one dot per run. In the puzzle column, ✓ means solved on the first chance, '
        '✓2 on the second, ✕ missed both. Drawing results stay off this table so ratings stay blind.</p>'
        + table + "</section>"
        + '<section class="wrap block" id="method"><h2 class="sec">Method</h2><div class="method">'
        + "".join(f"<div><h3>{esc(h)}</h3><p>{esc(p)}</p></div>" for h, p in method)
        + "</div></section>"
    )
    write("index.html", page("Vellery", html_, (), "How AI models handle the same tasks again and again: everyday work, blind-rated drawings and puzzles."))


def main():
    shutil.rmtree(DIST, ignore_errors=True)
    shutil.copytree(Path(__file__).parent / "static", DIST / "static")
    tasks = load_tasks()
    models = yaml.safe_load((ROOT / "models.yaml").read_text())["models"]
    all_runs = load_runs()
    published = {t["slug"] for t in tasks}
    all_runs = [r for r in all_runs if r["task"] in published]
    # A puzzle's grade is one rule; apply it to runs grade.py hasn't reached yet.
    by_slug = {t["slug"]: t for t in tasks}
    for r in all_runs:
        if r["grade"] is None and by_slug[r["task"]]["kind"] == "puzzle":
            r["grade"] = grade_answer(by_slug[r["task"]], r["response"])
    gallery_slugs = {t["slug"] for t in tasks if t["kind"] == "svg" and t["slug"] != "kitchen-illustration"}
    # Preserve the original blind IDs, including their existing votes.
    original = {(k["batch"], k["variant"], k["model"], k["run"])
                for k in json.loads((KITCHEN / "key.json").read_text()).values()}
    new_kitchen = [r for r in all_runs if r["task"] == "kitchen-illustration"
                   and (r["batch"], r["variant"], r["model"], r["run"]) not in original]
    can_reveal = reveal_key(models, new_kitchen + [r for r in all_runs if r["task"] in gallery_slugs])
    known, galleries = {}, {}
    for task in tasks:
        slug = task["slug"]
        runs = [r for r in all_runs if r["task"] == slug]
        (DIST / "tasks" / slug).mkdir(parents=True, exist_ok=True)
        if task["kind"] == "svg":
            items = kitchen_items() + drawing_items(new_kitchen) if slug == "kitchen-illustration" else drawing_items(runs)
            galleries[slug] = items
            known.update(build_gallery(task, items, models, can_reveal))
        elif task["kind"] == "puzzle":
            build_puzzle(task, runs, models)
        else:
            known.update(build_scripted(task, runs, models))
    write("items.json", json.dumps(known))
    home(tasks, models, all_runs, galleries)
    print(f"{len(tasks)} tasks, {len(known)} votable outputs -> {DIST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
