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

- **Removed 2 exact duplicates:** the second "Office chairs" row (2026-03-02, $1,240.00) and the second "Printer paper" row (03/04/2026, 48.5). The sheet had 20 rows and now has 18.
- **Dates converted to YYYY-MM-DD:**
  - `03/04/2026` → `2026-03-04`
  - `March 5 2026` → `2026-03-05`
  - `3/9/26` → `2026-03-09`
  - `10/03/2026` → `2026-03-10`
  - `Mar 13` → `2026-03-13` (year added)
  - `18/03/2026` → `2026-03-18`
  - `3/24/2026` → `2026-03-24`
- **Categories in Title Case:** `travel` → `Travel`, `office supplies` → `Office Supplies` (2 rows), `furniture` → `Furniture`, `software` → `Software`.
- **Amounts as plain two-decimal numbers:** removed `$` and thousands commas, and padded to two decimals. `$1,240.00` → `1240.00`, `48.5` → `48.50`, `149` → `149.00`, `$64` → `64.00`, and so on.

**Things I'm not sure about**

- **Train tickets, `10/03/2026`:** I read this as 10 March (day first). Read as month first, it would be 3 October, which is outside March 2026, so I went with 10 March. Please confirm.
- **Printer paper, `03/04/2026`:** I read this as 4 March (month first). The alternative, 3 April, is excluded by the March-only rule.
- **Two "Team lunch" rows at $212.40** (2026-03-05 and 2026-03-25): they have different dates, so I kept both as you specified. They could still be a double entry, so you may want to check them against receipts.
- **Monitor, "Mar 13":** the year was missing, so I assumed 2026.
- **Currency:** I assumed all amounts are in the same currency, since none were marked except by `$`.