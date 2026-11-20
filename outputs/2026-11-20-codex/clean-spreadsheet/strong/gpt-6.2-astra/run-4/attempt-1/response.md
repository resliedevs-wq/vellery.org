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

**Change log**

- Removed the second copies of the Office chairs and Printer paper rows, leaving 18 expenses. Kept both Team lunch purchases because they occurred on March 5 and March 25.
- Standardized seven dates. `03/04/2026` became `2026-03-04`, `March 5 2026` became `2026-03-05`, `3/9/26` became `2026-03-09`, `10/03/2026` became `2026-03-10`, `Mar 13` became `2026-03-13`, `18/03/2026` became `2026-03-18`, and `3/24/2026` became `2026-03-24`.
- Capitalized categories for Printer paper and Pens (`Office Supplies`), Taxi to client (`Travel`), Figma seats (`Software`), and Desk lamp (`Furniture`).
- Removed `$` from all 15 retained amounts that had it and the thousands separator from Office chairs. Added trailing zeros for Printer paper (`48.50`), Zoom subscription (`149.00`), and Desk lamp (`64.00`).

**Uncertainty:** The sheet mixed month-first and day-first dates, and `Mar 13` omitted the year. Your March 2026 constraint resolved each case.