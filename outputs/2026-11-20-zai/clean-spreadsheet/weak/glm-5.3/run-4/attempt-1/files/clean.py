import csv
from datetime import date
from decimal import Decimal

RAW = "messy.csv"
OUT = "expenses_clean.csv"

CATEGORY_FIXES = {
    "furniture": "Furniture",
    "office supplies": "Office Supplies",
    "meals": "Meals",
    "software": "Software",
    "travel": "Travel",
    "equipment": "Equipment",
}

MONTHS = {m.lower()[:3]: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], start=1)}


def parse_date(raw):
    """Normalize any date style in the sheet to ISO (YYYY-MM-DD)."""
    raw = raw.strip()

    # ISO: 2026-03-02
    if len(raw.split("-")) == 3 and len(raw.split("-")[0]) == 4:
        y, m, d = (int(x) for x in raw.split("-"))
        return date(y, m, d)

    # Written month: "March 5 2026" or "Mar 13" (year omitted -> dataset year 2026)
    parts = raw.replace(",", " ").split()
    if parts[0][:3].lower() in MONTHS:
        m = MONTHS[parts[0].lower()[:3]]
        d = int(parts[1])
        y = int(parts[2]) if len(parts) > 2 else 2026
        return date(y, m, d)

    # Slash formats. The sheet mixes US (3/24/2026) and EU (18/03/2026) styles,
    # so where both readings are valid (03/04, 3/9, 10/03) prefer the one that
    # lands in the dataset's dominant month (March 2026).
    a, b, y = (int(x) for x in raw.split("/"))
    if y < 100:
        y += 2000
    us = date(y, a, b) if a <= 12 else None          # M/D
    eu = date(y, b, a) if b <= 12 else None          # D/M
    candidates = [c for c in (us, eu) if c and c.month == 3] or [c for c in (us, eu) if c]
    return candidates[0]


def parse_amount(raw):
    return Decimal(raw.strip().strip('"').replace("$", "").replace(",", ""))


rows = []
with open(RAW, newline="") as f:
    for r in csv.DictReader(f):
        rows.append((
            parse_date(r["Date"]),
            r["Description"].strip(),
            CATEGORY_FIXES[r["Category"].strip().lower()],
            parse_amount(r["Amount"]),
        ))

seen, clean, dupes = set(), [], 0
for row in rows:
    if row in seen:
        dupes += 1
        continue
    seen.add(row)
    clean.append(row)

clean.sort(key=lambda r: r[0])  # stable: preserves original order within a day

with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Date", "Description", "Category", "Amount"])
    for d, desc, cat, amt in clean:
        w.writerow([d.isoformat(), desc, cat, f"{amt:.2f}"])

print(f"rows in: {len(rows)}  |  duplicates removed: {dupes}  |  rows out: {len(clean)}")
print(f"total: ${sum(a for *_, a in clean):,.2f}")
