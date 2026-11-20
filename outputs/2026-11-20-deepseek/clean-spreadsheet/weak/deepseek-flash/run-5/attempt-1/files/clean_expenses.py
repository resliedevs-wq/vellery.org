#!/usr/bin/env python3
"""Clean the pasted expenses export into an analysis-ready CSV."""

import csv
import re
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from itertools import product

SRC = "expenses_raw.csv"
OUT = "expenses_cleaned.csv"

MONTHS = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

CANONICAL_CATEGORIES = {
    "furniture": "Furniture",
    "office supplies": "Office Supplies",
    "meals": "Meals",
    "software": "Software",
    "travel": "Travel",
    "equipment": "Equipment",
}


def parse_date(value):
    """Return (date, ambiguous_candidates). ambiguous is [] or two dates."""
    s = value.strip()

    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        y, mo, d = map(int, m.groups())
        return date(y, mo, d), []

    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{2}|\d{4})", s)
    if m:
        a, b, y = m.groups()
        a, b, y = int(a), int(b), int(y)
        if y < 100:
            y += 2000
        if a > 12:  # definitely day-first
            return date(y, b, a), []
        if b > 12:  # definitely month-first
            return date(y, a, b), []
        # Both components could be a month: collect both readings.
        return None, [date(y, a, b), date(y, b, a)]

    m = re.fullmatch(r"([A-Za-z]+)\.?\s+(\d{1,2})(?:,?\s+(\d{4}))?", s)
    if m:
        mon, d, y = m.groups()
        mo = MONTHS[mon.lower()]
        return date(int(y) if y else 2026, mo, int(d)), []

    raise ValueError(f"Unrecognized date: {value!r}")


def parse_amount(value):
    s = value.strip().replace("$", "").replace(",", "").replace(" ", "")
    negative = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    amt = Decimal(s).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return -amt if negative else amt


def main():
    with open(SRC, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    records = []
    ambiguous = []
    for i, row in enumerate(rows):
        parsed, candidates = parse_date(row["Date"])
        rec = {
            "index": i,
            "raw_date": row["Date"].strip(),
            "date": parsed,
            "candidates": candidates,
            "description": " ".join(row["Description"].split()),
            "raw_category": row["Category"].strip(),
            "category": CANONICAL_CATEGORIES.get(
                " ".join(row["Category"].split()).lower(), row["Category"].strip()
            ),
            "amount": parse_amount(row["Amount"]),
        }
        if candidates:
            ambiguous.append(rec)
        records.append(rec)

    # Resolve ambiguous day/month order by the reading that keeps the ledger in
    # chronological order (fewest inversions against the original row order).
    if ambiguous:
        best = None
        for combo in product(range(2), repeat=len(ambiguous)):
            for rec, pick in zip(ambiguous, combo):
                rec["date"] = rec["candidates"][pick]
            inversions = sum(
                1
                for a, b in zip(records, records[1:])
                if a["date"] and b["date"] and a["date"] > b["date"]
            )
            if best is None or inversions < best[0]:
                best = (inversions, combo)
        for rec, pick in zip(ambiguous, best[1]):
            rec["date"] = rec["candidates"][pick]

    # Remove exact duplicate transactions (same date, description, category, amount).
    seen = set()
    unique = []
    duplicates = []
    for rec in records:
        key = (rec["date"], rec["description"].lower(), rec["category"].lower(), rec["amount"])
        if key in seen:
            duplicates.append(rec)
        else:
            seen.add(key)
            unique.append(rec)

    unique.sort(key=lambda r: (r["date"], r["index"]))

    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["Date", "Description", "Category", "Amount"])
        for rec in unique:
            writer.writerow(
                [rec["date"].isoformat(), rec["description"], rec["category"], f"{rec['amount']:.2f}"]
            )

    total = sum((r["amount"] for r in unique), Decimal("0"))
    print(f"Input rows:  {len(rows)}")
    print(f"Duplicates:  {len(duplicates)} removed")
    for rec in duplicates:
        print(f"  - row {rec['index'] + 1}: {rec['raw_date']} / {rec['description']} / {rec['amount']}")
    print(f"Clean rows:  {len(unique)}")
    print(f"Total spend: ${total:,.2f}")
    print("\nDate interpretations for ambiguous values:")
    for rec in ambiguous:
        print(f"  {rec['raw_date']!r} -> {rec['date'].isoformat()}")
    print("\nCategories:")
    for raw, canon in sorted({(r["raw_category"], r["category"]) for r in records}):
        if raw != canon:
            print(f"  {raw!r} -> {canon!r}")


if __name__ == "__main__":
    main()
