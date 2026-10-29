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
- **Dates:** All dates now use the same format (YYYY-MM-DD), and the rows are sorted by date.
- **Categories:** Fixed the inconsistent capitalization ("office supplies", "travel", "software", "furniture"), so there are now 6 categories.
- **Amounts:** Removed the `$` signs, commas and quotes, and gave every amount two decimal places. Spreadsheets will now read them as numbers you can add up.
- **Duplicates:** Removed 2 exact repeats: the Office chairs row on 03-02 and the Printer paper row on 03/04.

That leaves 18 rows totaling **$3,542.60**.

**Please check these guesses**
- **`10/03/2026` and `18/03/2026`:** I read these as day/month (March 10 and March 18) because `18` can't be a month and everything else is in March.
- **`03/04/2026`:** This could be March 4 or April 3. I went with March 4 so it matches the rest of the sheet.
- **`Mar 13`:** It had no year, so I assumed 2026.
- **Team lunch:** $212.40 appears on both March 5 and March 25. I kept both because the dates are different, but it could be a duplicate entry worth checking.