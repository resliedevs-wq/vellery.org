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

Total: 3,542.60 across 18 rows.

**What I changed**
- **Removed 2 exact duplicates:** the second "Office chairs" row and the second "Printer paper" row.
- **Standardized dates** to ISO `YYYY-MM-DD`.
- **Standardized amounts** to plain numbers with two decimals, without `$`, commas, or quotes.
- **Standardized categories:** "office supplies" and "Office supplies" became "Office Supplies", "furniture" became "Furniture", "software" became "Software", and "travel" became "Travel".

**Please check these**
- **Ambiguous slash dates:** I read `03/04/2026` as March 4 (US order), which fits the rest of the March data. I read `10/03/2026` and `18/03/2026` as day/month because the 18 can only be a day. If `03/04/2026` was meant to be April 3, change that row.
- **"Mar 13" had no year.** I assumed 2026.
- **Two "Team lunch" rows for $212.40** on March 5 and March 25 have different dates, so I kept both. Confirm they aren't a double entry.

I can save this as a file in the working directory if you want it.