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

**Changes made**

- **Dates:** All converted to ISO `YYYY-MM-DD` and sorted chronologically. The sheet is all March 2026, so I read the ambiguous ones that way: `03/04/2026` is March 4 (not April 3), `3/9/26` is March 9, `3/24/2026` is March 24, `18/03/2026` is March 18, and `10/03/2026` is March 10 (not October 3).
- **Duplicates removed:** "Office chairs" (2026-03-02) and "Printer paper" (2026-03-04) each appeared twice with identical values, so I kept one of each. If you actually bought two chairs or two packs of paper, add those rows back. Both "Team lunch" rows are kept because they're on different dates (03-05 and 03-25).
- **Amounts:** Stripped `$` and thousands separators and standardized to two decimals (`1,240.00` → `1240.00`, `48.5` → `48.50`).
- **Categories:** Fixed inconsistent capitalization: `furniture`, `software`, `travel` → title case, and `office supplies`/`Office supplies` → `Office Supplies`.

The sheet now has 18 rows totaling **3,542.60**. The original 20 rows had a total of 3,542.60 + 240.00 (the two duplicates: 1,240.00 + 48.50 = 1,288.50), so the figure that matters is that the duplicate removal dropped 1,288.50 in total.