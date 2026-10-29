```csv
Date,Description,Category,Amount (USD)
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

Changes made:
- **Removed 2 exact duplicates:** the Office chairs row and the Printer paper row each appeared twice. If you actually bought two of each, add those rows back.
- **Dates:** converted everything to ISO `YYYY-MM-DD` and sorted chronologically.
- **Ambiguous dates:** `03/04/2026` is read as March 4 and `10/03/2026` as March 10, since the rest of the sheet is March. `Mar 13` and `3/9/26` are assumed to be 2026.
- **Categories:** standardized capitalization (`office supplies` → `Office Supplies`, `travel` → `Travel`, `software` → `Software`, `furniture` → `Furniture`).
- **Amounts:** stripped `$` and commas and used two decimals. I assumed all amounts are USD.
- **Team lunch:** it appears on Mar 5 and Mar 25 at the same amount. I kept both since the dates differ, but it's worth a check.

The cleaned total is $3,542.60 across 18 rows.