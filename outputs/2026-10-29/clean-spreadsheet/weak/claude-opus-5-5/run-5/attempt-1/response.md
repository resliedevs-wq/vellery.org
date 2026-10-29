Here's the cleaned version:

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
- **Dates:** Changed every date to `YYYY-MM-DD` and sorted the rows by date.
- **Amounts:** Removed `$` signs, commas and quotes, and gave every amount two decimal places so they work as numbers.
- **Categories:** Made the capitalization consistent (`office supplies` and `Office supplies` both became `Office Supplies`, `travel` became `Travel`, and so on).
- **Duplicates:** Removed 2 rows that were exact copies: the second "Office chairs" on 2026-03-02 and the second "Printer paper" on 03/04. That leaves 18 rows totaling **$3,542.60**.

**Please check these**
- **`03/04/2026` (Printer paper):** This could be March 4 or April 3. I read it as March 4 because it sits between the March 2 and March 5 rows.
- **`10/03/2026` (Train tickets):** I read this as day/month, so March 10. The `18/03/2026` row has to be day/month, and every other date is in March.
- **`Mar 13`:** It had no year, so I assumed 2026.
- **Team lunch at $212.40:** This shows up on both Mar 5 and Mar 25. The dates differ, so I kept both, but check that it isn't a double entry.