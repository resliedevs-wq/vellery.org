#!/usr/bin/env python3
"""Scripted grading for the email and spreadsheet tasks.

Writes grade.json next to each run's meta.json. A grade comes from rules
that anyone can rerun; whatever needs a person's judgment is listed under
`review` instead of guessed. The kitchen drawings are graded by eye,
blind, and are not handled here.

Where a replacement batch has a replaces.json, runs it replaces are
skipped (their originals are kept on disk but not graded).

Usage: python3 runner/grade.py <batch> [<batch> ...]
"""

import csv
import io
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = ROOT / "outputs"
TASKS = ROOT / "tasks"

EMAIL_FACTS = {
    "Dana": r"\bDana\b",
    "Sam": r"\bSam\b",
    "Harbor Hall": r"Harbor Hall",
    "Priya": r"\bPriya\b",
    "March 12": r"March 12\b|Mar\.? 12\b",
    "March 3": r"March 3\b|Mar\.? 3\b",
    "$4,200": r"\$4,200|\$4\.2k|4,200",
    "AV fee waived": r"\bAV\b.*\bwaiv|waiv.*\bAV\b",
    "85 guests": r"\b85\b",
    "Friday": r"\bFriday\b",
}
# Qualifiers a keyword match can't confirm; a miss goes to a person.
CAPACITY = r"up to 85|85 (?:guests|people|attendees|max)|capacity|cover[s]? 85|maximum"
CONDITION = r"\b(?:if|unless|until|otherwise|hear|reply|respond|object|flag)\b"
SIGNED = r"\bsign"
ALLOWED_MONTH_DAYS = {"12", "3"}
ALLOWED_AMOUNTS = {"4,200"}


def strip_markup(text):
    return re.sub(r"[*_`]", "", text)


def grade_email(task_dir, variant, response):
    text = strip_markup(response).strip()
    lines = text.splitlines()
    body = "\n".join(l for l in lines if not re.match(r"\s*subject\s*:", l, re.I))
    words = len(body.split())
    original = len((task_dir / "email.txt").read_text().split())
    missing = [name for name, pat in EMAIL_FACTS.items() if not re.search(pat, text, re.I | re.S)]
    invented = sorted(
        {f"March {d}" for d in re.findall(r"\bMarch (\d+)", text) if d not in ALLOWED_MONTH_DAYS}
        | {f"${a}" for a in re.findall(r"\$(\d[\d,\.]*\d|\d)", text) if a.rstrip(".") not in ALLOWED_AMOUNTS})
    first = next((l for l in lines if l.strip()), "")
    extra_text = not re.match(r"(subject|hi|hello|dear)\b", first, re.I)
    review = []
    if not re.search(CAPACITY, text, re.I):
        review.append("does the email keep 85 as a capacity ('up to 85'), not a headcount?")
    if not (re.search(SIGNED, text, re.I) and re.search(CONDITION, text, re.I)):
        review.append("is the signed-contract-on-Friday-if-no-reply condition kept?")
    if invented:
        review.append(f"possible invented facts: {', '.join(invented)}")
    review.append("any other fact changed or added (e.g. who spoke to whom, the RSVP count)?")

    checks = {"words": words, "original_words": original, "missing": missing, "invented": invented,
              "text_outside_email": extra_text}
    if missing or invented:
        grade, why = "slop", "fact missing or invented" if missing else "possible invented fact"
    elif variant == "strong":
        grade, why = ("fix", f"{words} words, limit 120") if words > 120 else ("good", "")
        if extra_text:
            grade, why = "fix", "text besides the email"
    else:
        grade, why = ("good", "") if words < original else ("fix", "not shorter than the original")
    return {"grade": grade, "why": why, "checks": checks, "review": review}


def title_case(s):
    return " ".join(w.capitalize() for w in s.split())


def parse_date(cell, expected):
    """Return (iso date or None, kind) for a date cell, given the expected iso date."""
    cell = cell.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", cell):
        return cell, "iso"
    # Not ISO: see whether this reads as the expected date under some convention.
    y, m, d = (int(x) for x in expected.split("-"))
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    low = cell.lower()
    nums = [int(n) for n in re.findall(r"\d+", cell)]
    names = [i + 1 for i, mn in enumerate(months) if mn in low]
    candidates = set()
    if names and nums:
        candidates.add((names[0], nums[0] if nums[0] <= 31 else nums[1] if len(nums) > 1 else 0))
    elif len(nums) >= 2:
        candidates.add((nums[0], nums[1]))
        candidates.add((nums[1], nums[0]))
    if (m, d) in candidates:
        return expected, "unconverted"
    return None, "unparsed"


def extract_csv(response):
    blocks = re.findall(r"```(?:csv|text)?\s*\n(.*?)```", response, re.S)
    for block in blocks:
        if block.lower().lstrip().startswith("date"):
            return block
    for i, line in enumerate(response.splitlines()):
        if line.lower().startswith("date,"):
            return "\n".join(response.splitlines()[i:])
    return None


def grade_sheet(task_dir, variant, response, run_dir):
    expected = list(csv.DictReader((task_dir / "expected.csv").open()))
    block = extract_csv(response)
    if block is None:
        for f in sorted(run_dir.glob("attempt-*/files/*.csv")):
            block = f.read_text()
    if block is None:
        return {"grade": "slop", "why": "no table returned", "checks": {}, "review": []}
    def canonical(row):
        # A header like "Amount (USD)" is the same column, not a change.
        out = {}
        for key, value in row.items():
            name = next((n for n in ("Date", "Description", "Category", "Amount")
                         if (key or "").strip().lower().startswith(n.lower())), key)
            out[name] = value
        return out

    rows = [canonical(r) for r in csv.DictReader(io.StringIO(block.strip()))
            if any((v or "").strip() for v in r.values())]
    checks = {"rows": len(rows), "expected_rows": len(expected)}
    problems = {"wrong_date": [], "wrong_amount": [], "wrong_category": [], "format": [], "unconverted_date": []}
    keyed = {}
    for r in expected:
        keyed.setdefault(r["Description"].strip().lower(), []).append(r)
    matched = []
    for r in rows:
        desc = (r.get("Description") or "").strip().lower()
        pool = keyed.get(desc, [])
        if not pool:
            problems.setdefault("extra_or_renamed", []).append(r.get("Description"))
            continue
        # Pair with the closest expected row of that description (by amount, then position).
        try:
            amount = float(re.sub(r"[$,\s]", "", r.get("Amount") or ""))
        except ValueError:
            amount = None
        best = min(pool, key=lambda e: abs(float(e["Amount"]) - amount) if amount is not None else 0)
        pool.remove(best)
        matched.append(best["Description"])
        if amount is None or abs(amount - float(best["Amount"])) > 0.005:
            problems["wrong_amount"].append(f"{best['Description']}: {r.get('Amount')} (expected {best['Amount']})")
        elif not re.fullmatch(r"\d+\.\d{2}", (r.get("Amount") or "").strip()):
            problems["format"].append(f"amount '{r.get('Amount')}'")
        iso, kind = parse_date(r.get("Date") or "", best["Date"])
        if kind == "iso" and iso != best["Date"] or kind == "unparsed":
            problems["wrong_date"].append(f"{best['Description']}: {r.get('Date')} (expected {best['Date']})")
        elif kind == "unconverted":
            problems["unconverted_date"].append(f"{best['Description']}: {r.get('Date')}")
        cat = (r.get("Category") or "").strip()
        if cat.lower() != best["Category"].lower():
            problems["wrong_category"].append(f"{best['Description']}: {cat}")
        elif cat != best["Category"]:
            problems["format"].append(f"category '{cat}'")
    missing = [r["Description"] + " " + r["Date"] for pool in keyed.values() for r in pool]
    checks["missing_rows"] = missing
    checks["problems"] = {k: v for k, v in problems.items() if v}

    prose = re.sub(r"```.*?```", "", response, flags=re.S)
    has_changes = len(prose.split()) >= 25
    checks["change_list"] = has_changes
    review = ["are the ambiguous dates (03/04/2026, 10/03/2026, Mar 13) disclosed as guesses?"]

    lunches = [r for r in rows if (r.get("Description") or "").strip().lower() == "team lunch"]
    slop = []
    if len(rows) != len(expected) or missing or problems.get("extra_or_renamed"):
        slop.append(f"{len(rows)} rows, {len(missing)} expected rows missing")
    if len(lunches) < 2:
        slop.append("team lunches merged")
    if problems["wrong_amount"]:
        slop.append("an amount changed")
    if problems["wrong_date"]:
        slop.append("a date in the wrong place")
    if variant == "strong":
        fix = [k for k in ("format", "wrong_category", "unconverted_date") if problems[k]]
        if not has_changes:
            fix.append("no list of changes")
    else:
        fix = [k for k in ("format", "wrong_category", "unconverted_date") if problems[k]]
        if len(rows) == len(expected) + 2:
            fix.append("duplicates kept")
    if slop:
        grade, why = "slop", "; ".join(slop)
    elif fix:
        grade, why = "fix", "; ".join(fix)
    else:
        grade, why = "good", ""
    return {"grade": grade, "why": why, "checks": checks, "review": review}


def replaced_runs(batches):
    replaced = set()
    for batch in batches:
        f = OUTPUTS / batch / "replaces.json"
        if f.exists():
            spec = json.loads(f.read_text())
            replaced |= {(spec["batch"], r) for r in spec["runs"]}
    return replaced


def main(batches):
    replaced = replaced_runs(batches)
    for batch in batches:
        for meta_path in sorted((OUTPUTS / batch).glob("*/*/*/run-*/meta.json")):
            meta = json.loads(meta_path.read_text())
            if meta["task"] not in ("shorten-email", "clean-spreadsheet"):
                continue
            run_dir = meta_path.parent
            if (batch, f"{meta['task']}/{meta['variant']}/{meta['model']}") in replaced:
                continue
            response = (run_dir / f"attempt-{meta['attempts']}" / "response.md").read_text()
            task_dir = TASKS / meta["task"]
            if meta["task"] == "shorten-email":
                result = grade_email(task_dir, meta["variant"], response)
            else:
                result = grade_sheet(task_dir, meta["variant"], response, run_dir)
            (run_dir / "grade.json").write_text(json.dumps(
                {"graded_by": "runner/grade.py", **result}, indent=2) + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
