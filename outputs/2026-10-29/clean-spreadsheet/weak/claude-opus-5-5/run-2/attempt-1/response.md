Here's the cleaned version. It has 18 rows, sorted by date:

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
- **Dates:** All dates now use one format (YYYY-MM-DD).
- **Categories:** Fixed inconsistent capitalization, so "office supplies", "travel" and "software" now match the rest.
- **Amounts:** Removed `$`, commas and quotes, and gave every amount two decimals. They'll now add up as numbers in Excel or Sheets instead of being treated as text.
- **Duplicates:** Removed two rows that were exact repeats: Office chairs on 03-02 and Printer paper on 03-04.

**Please check these guesses**
- **`10/03/2026` (Train tickets) and `18/03/2026` (Client dinner):** I read these day-first, as March 10 and March 18. Read month-first, the first would be October 3, and "18" can't be a month.
- **`03/04/2026` (Printer paper):** I read this month-first, as March 4, because it fits the order of the list.
- **`Mar 13` (Monitor):** It had no year, so I assumed 2026.
- **Team lunch:** It appears on 03-05 and again on 03-25 for the same $212.40. I kept both because the dates are different, but it could be a double entry.

**Totals:** $3,542.60
| Category | Total |
|---|---|
| Furniture | 1,304.00 |
| Meals | 771.39 |
| Travel | 690.20 |
| Equipment | 360.96 |
| Software | 335.00 |
| Office Supplies | 81.05 |

If the second Team lunch is a duplicate, the total drops to $3,130.20.