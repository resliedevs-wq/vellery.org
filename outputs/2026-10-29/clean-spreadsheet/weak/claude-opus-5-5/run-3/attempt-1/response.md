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

That's 18 rows, totalling **$3,542.60**.

**What I changed**
- **Dates:** Every date now uses the YYYY-MM-DD format, and the rows are sorted by date.
- **Categories:** Fixed inconsistent capitalization, so there are now six categories: Furniture, Office Supplies, Meals, Software, Travel and Equipment.
- **Amounts:** Removed `$` signs, commas and quotes, and gave every amount two decimal places. They'll now sort and add up as numbers.
- **Duplicates:** Removed 2 exact duplicate rows: the second "Office chairs" ($1,240.00) and the second "Printer paper" ($48.50). With them included, the total would be $4,831.10.

**Please check these**
- **`10/03/2026` and `18/03/2026`:** I read these as day/month, so March 10 and March 18. That matches where they sat in the list, and 18 can't be a month.
- **`03/04/2026`:** I read this as March 4 because of where it sat in the list. If it was meant as day/month, it's April 3.
- **`Mar 13`:** This had no year, so I assumed 2026.
- **"Team lunch":** It appears twice for the same amount ($212.40), on March 5 and March 25. I kept both because the dates differ, but it could be a double entry.
- **Duplicate rows:** If you really did buy two sets of chairs or two orders of paper on the same day, add those rows back.