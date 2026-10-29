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

## Changes

**Duplicates removed (2 rows)**
- The second "Office chairs" on 2026-03-02 ($1,240.00).
- The second "Printer paper" on 03/04/2026 (48.5).

**Dates converted to YYYY-MM-DD**
- `03/04/2026` → 2026-03-04
- `March 5 2026` → 2026-03-05
- `3/9/26` → 2026-03-09
- `10/03/2026` → 2026-03-10
- `Mar 13` → 2026-03-13
- `18/03/2026` → 2026-03-18
- `3/24/2026` → 2026-03-24

**Categories put in Title Case**
- `office supplies` → Office Supplies (the Printer paper and Pens rows)
- `travel` → Travel (Taxi to client)
- `software` → Software (Figma seats)
- `furniture` → Furniture (Desk lamp)

**Amounts**
- I removed `$` and thousands separators, and the CSV quoting those needed.
- I padded every amount to two decimals: `48.5` → 48.50, `149` → 149.00, `$64` → 64.00.

## Things I wasn't sure about

- **Mixed date formats:** The sheet mixes month-first (`3/24/2026`) and day-first (`18/03/2026`, `10/03/2026`) dates. For the ambiguous ones, I picked the reading that falls in March, since you said every expense is from March 2026. `03/04/2026` and `3/9/26` became March 4 and March 9. If the source was day-first, those would be April, so they would be wrong. `10/03/2026` became March 10 because the October reading isn't in March.
- **`Mar 13`:** It has no year. I assumed 2026.
- **Team lunch:** It appears on 03-05 and 03-25, both at $212.40. I kept both because the dates differ. The identical amount could mean a mistaken re-entry, so check it.
- **Coffee beans:** I left it under Meals. It might belong under Office Supplies, but I didn't change categories beyond casing.
- **Row order:** I kept the original order. It stays chronological after cleanup.