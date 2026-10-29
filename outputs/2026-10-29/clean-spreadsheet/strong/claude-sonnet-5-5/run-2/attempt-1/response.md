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

**Duplicates removed (2 rows, 20 → 18):**
- The second `2026-03-02 Office chairs $1,240.00`.
- The second `03/04/2026 Printer paper 48.5`.

**Dates converted to YYYY-MM-DD:**
- `03/04/2026` → 2026-03-04
- `March 5 2026` → 2026-03-05
- `3/9/26` → 2026-03-09
- `10/03/2026` → 2026-03-10
- `Mar 13` → 2026-03-13 (year added)
- `18/03/2026` → 2026-03-18
- `3/24/2026` → 2026-03-24

**Categories changed to Title Case:**
- `office supplies` → Office Supplies (3 rows, including the one with the removed duplicate)
- `travel` → Travel
- `software` → Software
- `furniture` → Furniture

**Amounts:**
- I removed `$` and thousands separators, and padded every amount to two decimals (for example `48.5` → 48.50, `149` → 149.00, `$64` → 64.00).
- With the commas gone, no field needs quoting.

## Things I wasn't sure about
- **Mixed date formats.** The sheet mixes month-first (`3/24/2026`) and day-first (`18/03/2026`, `10/03/2026`). I used your rule that every expense is from March 2026 to resolve them. So `03/04/2026` is March 4, not 3 April, and `10/03/2026` is 10 March. If those rows came from a system that isn't consistent, check them against the receipts.
- **`Mar 13` has no year.** I assumed 2026, since you said everything is from March 2026.
- **Team lunch appears twice**, on 03-05 and 03-25, both at $212.40. I kept both because the dates differ, as you asked. The identical amount could mean a double entry, so it's worth a quick check.
- **Row order.** I kept the original order instead of sorting by date. It's almost chronological already, but I can sort it if you want.