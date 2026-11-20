#!/usr/bin/env python3
"""Clean the pasted March 2026 expense export.

Input is embedded verbatim from the user's message so the transformation is
reproducible and auditable.
"""

import csv
import re
from collections import OrderedDict
from datetime import date, datetime

RAW = '''Date,Description,Category,Amount
2026-03-02,Office chairs,Furniture,"$1,240.00"
03/04/2026,Printer paper,office supplies,48.5
March 5 2026,Team lunch,Meals,$212.40
2026-03-02,Office chairs,Furniture,"$1,240.00"
3/9/26,Zoom subscription,Software,149
2026-03-10,Taxi to client,travel,$36.20
10/03/2026,Train tickets,Travel,"$184.00"
2026-03-12,Coffee beans,Meals,27.99
Mar 13,Monitor,Equipment,$329.00
2026-03-15,Notebooks,Office Supplies,$22.75
03/04/2026,Printer paper,office supplies,48.5
2026-03-18,Figma seats,software,$90.00
18/03/2026,Client dinner,Meals,"$318.60"
2026-03-20,Desk lamp,furniture,$64
2026-03-22,Hotel (2 nights),Travel,"$412.00"
3/24/2026,USB-C cables,Equipment,$31.96
2026-03-25,Team lunch,Meals,$212.40
2026-03-27,Pens,Office supplies,$9.80
2026-03-30,Taxi to airport,Travel,$58.00
2026-03-31,Notion subscription,Software,$96.00
'''

CATEGORY_MAP = {
    "furniture": "Furniture",
    "office supplies": "Office Supplies",
    "meals": "Meals",
    "software": "Software",
    "travel": "Travel",
    "equipment": "Equipment",
}

# Slash dates are a mix of m/d/y and d/m/y. These are the only ambiguous or
# non-month-first values; each is resolved against the March 2026 sequence.
SLASH_OVERRIDES = {
    "03/04/2026": date(2026, 3, 4),   # sits between Mar 2 and Mar 5
    "10/03/2026": date(2026, 3, 10),  # day-first; 10 cannot be a month
    "18/03/2026": date(2026, 3, 18),  # day-first; 18 cannot be a month
}

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def parse_date(value):
    value = value.strip()
    if value in SLASH_OVERRIDES:
        return SLASH_OVERRIDES[value]

    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass

    # "March 5 2026" / "Mar 13" (year inferred as 2026)
    m = re.fullmatch(r"([A-Za-z]+)\s+(\d{1,2})(?:,?\s+(\d{4}))?", value)
    if m:
        month = MONTHS[m.group(1)[:3].lower()]
        year = int(m.group(3)) if m.group(3) else 2026
        return date(year, month, int(m.group(2)))

    raise ValueError(f"Unrecognized date: {value!r}")


def parse_amount(value):
    cleaned = re.sub(r"[^0-9.\-]", "", value.strip())
    return round(float(cleaned), 2)


def main():
    rows = list(csv.DictReader(RAW.splitlines()))

    cleaned = []
    for row in rows:
        cleaned.append({
            "Date": parse_date(row["Date"]).isoformat(),
            "Description": " ".join(row["Description"].split()),
            "Category": CATEGORY_MAP[row["Category"].strip().lower()],
            "Amount": f"{parse_amount(row['Amount']):.2f}",
        })

    # Exact duplicates: same date + description + category + amount.
    unique = list(OrderedDict(
        ((r["Date"], r["Description"], r["Category"], r["Amount"]), r)
        for r in cleaned
    ).values())

    unique.sort(key=lambda r: (r["Date"], r["Description"]))

    fieldnames = ["Date", "Description", "Category", "Amount"]
    with open("expenses_cleaned.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique)

    duplicates = [r for r in cleaned if cleaned.count(r) > 1]
    removed = len(cleaned) - len(unique)
    total = round(sum(float(r["Amount"]) for r in unique), 2)

    by_category = OrderedDict()
    for row in sorted(unique, key=lambda r: r["Category"]):
        by_category.setdefault(row["Category"], []).append(float(row["Amount"]))

    print(f"Input rows: {len(cleaned)}")
    print(f"Duplicates removed: {removed}")
    print(f"Clean rows: {len(unique)}")
    print(f"Total: ${total:,.2f}")
    print("\nBy category:")
    for category, amounts in sorted(by_category.items()):
        print(f"  {category:<16} {len(amounts):>2} rows  ${sum(amounts):>9,.2f}")

    print("\nRemoved duplicate values:")
    for key in sorted({(r["Date"], r["Description"], r["Category"], r["Amount"])
                       for r in duplicates}):
        print("  " + " | ".join(key))


if __name__ == "__main__":
    main()
