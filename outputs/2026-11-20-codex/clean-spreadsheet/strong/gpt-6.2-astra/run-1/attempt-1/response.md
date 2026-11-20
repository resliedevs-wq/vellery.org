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

- **Duplicates.** Removed the second Office chairs row and the second Printer paper row, leaving 18 expenses. Kept both Team lunch purchases because they occurred on March 5 and March 25.
- **Dates.** Converted `03/04/2026` to `2026-03-04`, `March 5 2026` to `2026-03-05`, `3/9/26` to `2026-03-09`, `10/03/2026` to `2026-03-10`, `Mar 13` to `2026-03-13`, `18/03/2026` to `2026-03-18`, and `3/24/2026` to `2026-03-24`.
- **Categories.** Changed `office supplies` (Printer paper) and `Office supplies` (Pens) to `Office Supplies`, `travel` (Taxi to client) to `Travel`, `software` (Figma seats) to `Software`, and `furniture` (Desk lamp) to `Furniture`.
- **Amounts.** Removed dollar signs wherever present and the thousands separator from Office chairs. Added decimal places for Printer paper (`48.5` → `48.50`), Zoom subscription (`149` → `149.00`), and Desk lamp (`$64` → `64.00`).

**Uncertainty.** The sheet mixes month-first and day-first dates. Your March 2026 instruction resolved the ambiguous dates and supplied the missing year for `Mar 13`. No entries remain unresolved.