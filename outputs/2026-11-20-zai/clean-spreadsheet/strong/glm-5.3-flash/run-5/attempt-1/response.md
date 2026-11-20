Here's the cleaned CSV (18 rows, original order preserved):

```csv
Date,Description,Category,Amount
2026-03-02,Office chairs,Furniture,1240.00
2026-03-04,Printer paper,Office Supplies,48.50
2026-03-05,Team lunch,Meals,212.40
2026-03-09,Zoom subscription,Software,149.00
2026-03-10,Taxi to client,Travel,36.20
2026-03-10,Train tickets,Travel,184.00
2026-03-12,Coffee beans,Meals,27.99
2026-03-13,Monitor,Equipment,329.00
2026-03-15,Notebooks,Office Supplies,22.75
2026-03-18,Figma seats,Software,90.00
2026-03-18,Client dinner,Meals,318.60
2026-03-20,Desk lamp,Furniture,64.00
2026-03-22,Hotel (2 nights),Travel,412.00
2026-03-24,USB-C cables,Equipment,31.96
2026-03-25,Team lunch,Meals,212.40
2026-03-27,Pens,Office Supplies,9.80
2026-03-30,Taxi to airport,Travel,58.00
2026-03-31,Notion subscription,Software,96.00
```

## Changes made

**Duplicates removed (2 rows):**
- "Office chairs", 2026-03-02 — appeared twice identically; kept one.
- "Printer paper", 03/04/2026 — appeared twice identically; kept one.

**Dates normalized:**
- `03/04/2026` (Printer paper) → 2026-03-04
- `March 5 2026` → 2026-03-05
- `3/9/26` → 2026-03-09 (Zoom)
- `10/03/2026` → 2026-03-10 (Train tickets)
- `Mar 13` → 2026-03-13 (Monitor)
- `18/03/2026` → 2026-03-18 (Client dinner)
- `3/24/2026` → 2026-03-24 (USB-C cables)

**Categories to Title Case:** `office supplies` → Office Supplies (Printer paper, Pens), `travel` → Travel (Taxi to client), `software` → Software (Figma seats), `furniture` → Furniture (Desk lamp).

**Amounts reformatted:** stripped `$` and thousands separators, padded to two decimals (e.g. `$1,240.00` → `1240.00`, `48.5` → `48.50`, `149` → `149.00`, `$64` → `64.00`).

**Kept deliberately:** the two Team lunch rows (2026-03-05 and 2026-03-25, both $212.40) — same description and amount but different dates, so treated as repeated purchases, not duplicates. Figma seats and Client dinner also share 2026-03-18 but are different purchases.

## Things I wasn't sure about

1. **Slash-format dates** (`03/04/2026`, `10/03/2026`, `3/9/26`, `18/03/2026`) don't declare day-first vs. month-first. I resolved each using your "everything is March 2026" rule, and in every case exactly one interpretation lands in March (e.g., `10/03/2026` as month-first would be October 3; `03/04/2026` as day-first would be April 3), so the readings above are the only March-consistent ones — but they rely on that constraint being true.
2. **"Mar 13" (Monitor)** has no year; I assumed 2026 per your instructions.
3. **Printer paper duplicate** — two identical rows on the same date could be either a double entry or a genuine second purchase that happened to be identical. Your rule says remove exact duplicates, so I removed one, but worth a quick check against receipts since a same-day duplicate is indistinguishable from a double-entry.