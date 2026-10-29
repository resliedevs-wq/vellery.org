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

**Dates changed to YYYY-MM-DD**
- `03/04/2026` → `2026-03-04` (read as month/day)
- `March 5 2026` → `2026-03-05`
- `3/9/26` → `2026-03-09`
- `10/03/2026` → `2026-03-10` (read as day/month)
- `Mar 13` → `2026-03-13` (added the year)
- `18/03/2026` → `2026-03-18` (read as day/month)
- `3/24/2026` → `2026-03-24`

**Exact duplicates removed (2 rows)**
- The second `2026-03-02, Office chairs, Furniture, $1,240.00`
- The second `03/04/2026, Printer paper, office supplies, 48.5`

**Categories changed to Title Case**
- `office supplies` → `Office Supplies` (Printer paper)
- `Office supplies` → `Office Supplies` (Pens)
- `travel` → `Travel` (Taxi to client)
- `software` → `Software` (Figma seats)
- `furniture` → `Furniture` (Desk lamp)

**Amounts changed to plain numbers**
- Removed `$` and the thousands comma, and the quotes that came with them (e.g. `"$1,240.00"` → `1240.00`)
- Added two decimals where they were missing: `48.5` → `48.50`, `149` → `149.00`, `$64` → `64.00`

The sheet went from 20 rows to 18. Once the dates were fixed, the rows were already in date order, so I didn't reorder anything.

## Things I wasn't sure about

1. **Day/month order isn't consistent.** `03/04/2026` is month-first, but `10/03/2026` and `18/03/2026` are day-first. Since every expense is from March, only one reading of each works, so I'm confident in these dates. But it suggests the data came from more than one source or person.
2. **`Mar 13` had no year.** I used 2026 because you said all expenses are from March 2026.
3. **`3/9/26` has a two-digit year.** I read it as 2026.
4. **The removed duplicates might be real purchases.** Two identical $1,240 chair orders, or two identical paper orders, on the same day could be separate buys. I removed them because they match exactly, which is what you asked. Check the receipts if you can. Together they're worth $1,288.50.
5. **Team lunch shows up twice for $212.40** (Mar 5 and Mar 25). The dates differ, so I kept both. An identical amount three weeks apart could be a recurring lunch, or the same receipt entered twice with the wrong date.
6. **I only fixed category capitalization.** I didn't change what category anything is in. For example, Coffee beans is under Meals and Desk lamp is under Furniture. Those may be fine, but your categories might be set up differently.