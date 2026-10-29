Here's the cleaned spreadsheet, sorted by date:

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
- **Dates:** All dates now use the same format (YYYY-MM-DD). "Mar 13" had no year, so I set it to 2026.
- **Categories:** Capitalization is now consistent, giving six categories: Furniture, Office Supplies, Meals, Software, Travel and Equipment.
- **Amounts:** I removed `$`, commas and quotes, and gave every amount two decimal places. They're now plain numbers, so they'll sum and sort correctly.
- **Duplicates:** I removed two rows that were exact copies: the Office chairs on 03-02 and the Printer paper on 03-04. That takes it from 20 rows to 18.

**Please check these**
- **`10/03/2026` and `18/03/2026`:** I read these as day/month (March 10 and March 18). 18 can't be a month, and March fits the rest of the file.
- **`03/04/2026` (Printer paper):** I read this as month/day (March 4) because it falls between the March 2 and March 5 rows. If it actually means April 3, it belongs to a different month.
- **Team lunch, $212.40:** This appears on both 03-05 and 03-25. The dates are different, so I kept both. If it's the same receipt entered twice, delete one.

**Totals: $3,542.60**
| Category | Total |
|---|---|
| Furniture | 1,304.00 |
| Meals | 771.39 |
| Travel | 690.20 |
| Equipment | 360.96 |
| Software | 335.00 |
| Office Supplies | 81.05 |