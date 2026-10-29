Here's the cleaned CSV. It has 18 rows, down from 20.

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
- **Dates:** All are now `YYYY-MM-DD`, and the rows are sorted by date.
- **Amounts:** I removed the `$` signs and thousands separators and set every amount to two decimals.
- **Categories:** I standardized the capitalization, so `office supplies`, `Office Supplies`, `travel` and `software` each now have a single form.
- **Duplicates:** I removed 2 exact repeats, Office chairs (03-02) and Printer paper (03-04).

**Assumptions to check**
- **Ambiguous dates:** I used neighboring rows to decide the order of day and month.
  - `03/04/2026` became Mar 4 (month first).
  - `10/03/2026` became Mar 10 (day first).
  - `18/03/2026` can only be Mar 18.
  - `Mar 13` had no year, so I assumed 2026.
- **Team lunch:** It appears on 03-05 and 03-25 at the same $212.40. I kept both because the dates differ, but check it isn't a double entry.

The total is $3,542.60.

I haven't saved this to a file. I can write it to `cleaned.csv` if you want.