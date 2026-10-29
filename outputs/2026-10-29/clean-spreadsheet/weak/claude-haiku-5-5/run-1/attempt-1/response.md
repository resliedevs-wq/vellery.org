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

Changes made:
- **Removed 2 exact duplicates:** the second "Office chairs" (2026-03-02) and the second "Printer paper" (03/04/2026). The table now has 18 rows, down from 20.
- **Dates:** All converted to ISO format (YYYY-MM-DD). Three entries were ambiguous, so I read them as March 2026 to match the rest of the sheet: `03/04/2026` as March 4, `10/03/2026` as March 10 (day-first, like `18/03/2026` elsewhere), and `3/9/26` as March 9. If any of these were meant as day-first or April dates, tell me and I'll fix them.
- **Amounts:** Removed `$` and thousands separators and standardized to two decimals (e.g. `$1,240.00` → `1240.00`, `48.5` → `48.50`).
- **Categories:** Standardized capitalization (`office supplies`, `Office Supplies`, and `Office supplies` → `Office Supplies`; `travel` → `Travel`; `software` → `Software`; `furniture` → `Furniture`).

Two "Team lunch" entries (March 5 and March 25) and two "Taxi" entries were kept because they're on different dates and are separate expenses.