Here's the cleaned version, sorted by date:

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

**What I changed**
- **Dates:** All are now `YYYY-MM-DD`. They were in at least five formats.
- **Amounts:** I removed `$` and thousands separators, and every amount now has two decimals.
- **Categories:** Casing is consistent (`office supplies` and `Office Supplies` are now one category, and `travel`, `software` and `furniture` are capitalized).
- **Duplicates removed (2):** The second "Office chairs" ($1,240.00, 03-02) and the second "Printer paper" ($48.50, 03-04) were exact repeats.

The cleaned file has 18 rows and totals $3,542.60.

**Assumptions to check**
- **Ambiguous dates:** I used the neighboring rows to decide the order of day and month.
  - `03/04/2026` is March 4 (month first).
  - `10/03/2026` is March 10 (day first).
  - `18/03/2026` is March 18 (day first).
  - The sorted order only makes sense with those readings, but please check them against your receipts.
- **Missing year:** `Mar 13` had no year, so I assumed 2026.
- **Team lunch:** I kept both entries, on 03-05 and 03-25. They have the same $212.40 amount but different dates, so they could be a repeat or a mistake. Remove one if it's wrong.

I can save this as a file if you want. Tell me where.