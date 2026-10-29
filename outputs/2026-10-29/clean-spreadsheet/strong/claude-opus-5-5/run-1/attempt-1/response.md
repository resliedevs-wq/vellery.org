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

**Dates**
- `03/04/2026` → `2026-03-04`
- `March 5 2026` → `2026-03-05`
- `3/9/26` → `2026-03-09`
- `10/03/2026` → `2026-03-10` (read as day/month)
- `Mar 13` → `2026-03-13` (I added the year)
- `18/03/2026` → `2026-03-18` (read as day/month)
- `3/24/2026` → `2026-03-24`

**Duplicates removed (2 rows, 20 → 18)**
- The second `2026-03-02, Office chairs, Furniture, $1,240.00`
- The second `03/04/2026, Printer paper, office supplies, 48.5`

**Categories changed to Title Case**
- `office supplies` / `Office supplies` → `Office Supplies` (Printer paper, Pens)
- `travel` → `Travel` (Taxi to client)
- `software` → `Software` (Figma seats)
- `furniture` → `Furniture` (Desk lamp)

**Amounts**
- Removed `$` and the thousands comma, so `"$1,240.00"` became `1240.00`. The quotes are gone because no field contains a comma anymore.
- Added two decimals where missing: `48.5` → `48.50`, `149` → `149.00`, `$64` → `64.00`

I kept the original row order.

## What I wasn't sure about

1. **The sheet mixes day/month orders.** `10/03/2026` and `18/03/2026` only work as day/month for a March date. `03/04/2026` only works as month/day: read as day/month it would be April 3. I relied on your "everything is March" rule to settle each one. If that rule has exceptions, the Printer paper date could be wrong.
2. **Missing or short years.** `Mar 13` had no year and `3/9/26` had a two-digit year. I assumed 2026 for both.
3. **Team lunch appears twice, on 03-05 and 03-25, for the same $212.40.** I kept both because the dates differ, as you asked. But a matching amount could also mean one entry was logged twice with the wrong date. It's worth checking against the receipt.
4. **The removed duplicates matched exactly in every field.** I treated them as data-entry errors. If two identical purchases really happened on the same day (two chair orders, for example), add them back.
5. **Descriptions weren't changed.** I left their capitalization alone, including "Hotel (2 nights)", since you only asked for Title Case on categories.