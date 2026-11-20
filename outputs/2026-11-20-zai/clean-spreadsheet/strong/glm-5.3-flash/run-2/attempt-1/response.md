Here's the cleaned sheet — 18 rows (started with 20, removed 2 exact duplicates):

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

**Duplicates removed (2)**
- `2026-03-02 Office chairs` — exact duplicate of row 1
- `03/04/2026 Printer paper` — exact duplicate of row 2

**Dates normalized (7)**
- `March 5 2026` → `2026-03-05`
- `3/9/26` → `2026-03-09`
- `10/03/2026` → `2026-03-10`
- `Mar 13` → `2026-03-13` (year was missing; assumed 2026)
- `18/03/2026` → `2026-03-18`
- `03/04/2026` → `2026-03-04`
- `3/24/2026` → `2026-03-24`

**Categories recased (5 rows)**
- `office supplies` → `Office Supplies` (Printer paper ×2)
- `travel` → `Travel` (Taxi to client)
- `software` → `Software` (Figma seats)
- `furniture` → `Furniture` (Desk lamp)
- `Office supplies` → `Office Supplies` (Pens — only "supplies" was lowercase)

**Amounts reformatted**
- Stripped `$` and thousands comma (`"$1,240.00"` → `1240.00`); padded to two decimals (`48.5` → `48.50`, `149` → `149.00`, `$64` → `64.00`). No other values changed.

## Things I wasn't sure about

1. **Mixed date conventions.** The slash dates mix formats: `03/04/2026` and `3/9/26` only make sense as month-first (March 4, March 9), while `10/03/2026` and `18/03/2026` only make sense as day-first (March 10, March 18) — the other reading would put them in April/October/September, violating "all March 2026." I resolved each using that constraint, but it's worth checking the receipts, since the sheet isn't internally consistent.
2. **The two `Team lunch` / `$212.40` rows** (March 5 and March 25) are identical except for date, so per your rule I kept both. If one is actually a duplicate with a typo'd date, remove one.
3. **`Mar 13` Monitor** — assumed 2026 since everything else is; no way to verify from the sheet itself.
4. **Two entries on 2026-03-10** (taxi + train) and on 2026-03-18 (Figma + client dinner) — different descriptions, so kept both.

I left category assignments and descriptions untouched apart from casing — e.g., "Coffee beans" under Meals stays as-is.