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

The sheet went from 20 rows to 18.

## Changes

**Duplicates removed (2)**
- The second "Office chairs" row (2026-03-02, $1,240.00).
- The second "Printer paper" row (03/04/2026, 48.5).
- I kept the "Team lunch" rows on 03-05 and 03-25. They have the same amount but different dates, so they count as separate purchases.

**Dates converted to YYYY-MM-DD (8 rows)**
- `03/04/2026` → 2026-03-04
- `March 5 2026` → 2026-03-05
- `3/9/26` → 2026-03-09
- `10/03/2026` → 2026-03-10
- `Mar 13` → 2026-03-13
- `18/03/2026` → 2026-03-18
- `3/24/2026` → 2026-03-24
- The remaining dates were already in the right format.

**Categories set to Title Case (5 rows)**
- `office supplies` → Office Supplies (the first Printer paper row and Pens; the second Printer paper row was removed as a duplicate)
- `travel` → Travel (Taxi to client)
- `software` → Software (Figma seats)
- `furniture` → Furniture (Desk lamp)

**Amounts normalized**
- I removed `$` and thousands commas, and padded every amount to two decimals. For example, `48.5` → 48.50, `149` → 149.00, `$64` → 64.00 and `"$1,240.00"` → 1240.00.

## Things I wasn't sure about
- **Slash-date order.** The sheet mixes month-first and day-first formats. Since every expense is from March 2026, I picked the reading that lands in March:
  - `03/04/2026` is March 4, not 3 April.
  - `10/03/2026` and `18/03/2026` are 10 and 18 March (day-first).
  - `3/9/26` is March 9, not 3 September.
- **Missing year.** `Mar 13` had no year, so I assumed 2026.
- **Row order.** I kept the original order. It's already chronological, with two entries on 03-10 and two on 03-18.
- **Team lunch.** The two $212.40 lunches are 20 days apart, so they look like separate events. If the second is a double-entry, delete that row.