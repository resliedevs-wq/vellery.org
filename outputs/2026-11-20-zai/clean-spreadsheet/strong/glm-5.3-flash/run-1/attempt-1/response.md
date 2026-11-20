Here's the cleaned CSV — 18 rows (started with 20, removed 2 exact duplicates):

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
- `Office chairs, 2026-03-02, $1,240.00` — appeared twice identically; kept one
- `Printer paper, 03/04/2026, 48.5` — appeared twice identically; kept one

**Dates normalized**
- `03/04/2026` → `2026-03-04` (read as month/day; day-first would be April, contradicting the all-March rule)
- `March 5 2026` → `2026-03-05`
- `3/9/26` → `2026-03-09`
- `10/03/2026` → `2026-03-10` (read day-first; month-first would be October)
- `Mar 13` → `2026-03-13` (year was missing; assumed 2026)
- `18/03/2026` → `2026-03-18` (18 can't be a month, so day-first)
- `3/24/2026` → `2026-03-24` (24 can't be a month, so month-first)

**Categories Title Cased**
- `office supplies` / `Office supplies` → `Office Supplies` (3 rows)
- `travel` → `Travel`
- `software` → `Software`
- `furniture` → `Furniture`

**Amounts reformatted**
- Stripped `$` and thousands commas; padded to two decimals (`$1,240.00` → `1240.00`, `48.5` → `48.50`, `149` → `149.00`, `$64` → `64.00`, etc.)

## Things I wasn't sure about

1. **The sheet mixes US and European date formats.** `03/04/2026` only makes sense as month/day, while `10/03/2026` only makes sense as day/month. The "everything is March 2026" constraint forces a unique answer in each case, so the dates above are unambiguous — but the original sheet's format inconsistency is worth knowing about if you parse it programmatically later.
2. **`Team lunch` appears twice with the identical $212.40 amount** (Mar 5 and Mar 25). Different dates, so per your rules I kept both — but since the amount matches exactly, you may want to confirm the second one is a genuine repeat and not a re-keyed entry.
3. **Two expenses share 2026-03-10** (taxi and train tickets). They're clearly different purchases, so both were kept.
4. **`Mar 13` had no year** — I assumed 2026 based on your instruction; if the sheet predates that assumption, double-check it.