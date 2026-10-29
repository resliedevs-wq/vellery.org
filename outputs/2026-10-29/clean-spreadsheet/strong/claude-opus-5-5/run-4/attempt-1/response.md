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

**Changes**

*Dates changed to YYYY-MM-DD (7 rows):*
- `03/04/2026` → 2026-03-04 (Printer paper)
- `March 5 2026` → 2026-03-05
- `3/9/26` → 2026-03-09
- `10/03/2026` → 2026-03-10 (Train tickets; read as day/month)
- `Mar 13` → 2026-03-13 (added the year)
- `18/03/2026` → 2026-03-18 (Client dinner; read as day/month)
- `3/24/2026` → 2026-03-24

*Exact duplicates removed (2 rows):*
- The second `2026-03-02, Office chairs, Furniture, $1,240.00`
- The second `03/04/2026, Printer paper, office supplies, 48.5`

*Categories changed to Title Case (5 rows):*
- `office supplies` → Office Supplies (Printer paper)
- `Office supplies` → Office Supplies (Pens)
- `travel` → Travel (Taxi to client)
- `software` → Software (Figma seats)
- `furniture` → Furniture (Desk lamp)

*Amounts:* I removed `$` and commas and set two decimals everywhere. For example, `"$1,240.00"` → 1240.00, `48.5` → 48.50, `149` → 149.00 and `$64` → 64.00.

*Order:* I kept the original row order. After fixing the dates, the rows are already in date order.

**Things I wasn't sure about**

1. **The sheet uses both date styles.** `10/03/2026` and `18/03/2026` only make sense as day/month, but `3/24/2026` only makes sense as month/day. Only March 2026 dates were allowed, so each date had one possible reading. `03/04/2026` could have been April 3, and `3/9/26` could have been September 3. Both became March dates for that reason. Check those two if the March-only rule might not be strict.
2. **`Mar 13` had no year.** I assumed 2026.
3. **The two duplicates may have been real purchases.** They matched in every field, so I removed them as you asked. If two lots of office chairs or printer paper really were bought on the same day, add those rows back. That's $1,240.00 and $48.50.
4. **Team lunch shows up twice at the same price.** The dates are March 5 and March 25, so I kept both. Because the amount is identical ($212.40), it could still be a double entry.
5. **I didn't change any category choices.** For example, Coffee beans are under Meals. I only fixed the capitalization.