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

**Dates converted to YYYY-MM-DD**
- `03/04/2026` → 2026-03-04
- `March 5 2026` → 2026-03-05
- `3/9/26` → 2026-03-09
- `10/03/2026` → 2026-03-10
- `Mar 13` → 2026-03-13 (year added)
- `18/03/2026` → 2026-03-18
- `3/24/2026` → 2026-03-24

**Duplicates removed (2 rows)**
- Office chairs, 2026-03-02, 1240.00 appeared twice, so I kept one.
- Printer paper, 2026-03-04, 48.50 appeared twice, so I kept one.

**Categories in Title Case**
- `office supplies` → Office Supplies (this also covers Printer paper and Pens).
- `travel` → Travel.
- `software` → Software.
- `furniture` → Furniture.

**Amounts**
- I removed `$` and thousands commas, and padded every amount to two decimals. Examples: `48.5` → 48.50, `149` → 149.00, `$64` → 64.00 and `"$1,240.00"` → 1240.00.

The 18 rows are still in their original order, which was already chronological.

## Things I wasn't sure about

- **Ambiguous dates:** I used your "every expense is from March 2026" rule to resolve them. `03/04/2026` could be 4 March or 3 April. I read it as 4 March, since April isn't allowed. `10/03/2026` and `18/03/2026` can only be day/month, so I read them as 10 and 18 March. `3/9/26` and `3/24/2026` are month/day. `3/9/26` could technically be 3 September, but March is the only valid reading.
- **`Mar 13`:** It has no year. I assumed 2026.
- **Team lunch:** It appears on 2026-03-05 and 2026-03-25 at exactly 212.40. I kept both because the dates differ, as you asked. The identical amount 20 days apart could be a copy-paste error, so check it.
- **Printer paper:** I treated the two rows as true duplicates because every field matched. If you actually bought paper twice on 4 March, add one back.