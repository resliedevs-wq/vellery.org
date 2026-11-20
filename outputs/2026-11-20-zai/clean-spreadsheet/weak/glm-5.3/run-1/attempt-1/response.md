Cleaned and saved to `expenses_clean.csv`. Here's the result:

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

**What I fixed:**
- **Dates** — normalized six different formats (`03/04/2026`, `March 5 2026`, `3/9/26`, `Mar 13`, etc.) to ISO `YYYY-MM-DD` and sorted chronologically.
- **Duplicates** — removed the repeated *Office chairs* (Mar 2) and *Printer paper* (Mar 4) rows. *Team lunch* appears twice with the same amount but on different dates (Mar 5 and Mar 25), so I kept both — flag me if one is wrong.
- **Categories** — standardized capitalization (`office supplies`/`Office supplies` → `Office Supplies`, `software` → `Software`, etc.).
- **Amounts** — stripped `$`, commas, and quotes; stored as plain two-decimal numbers so they parse as numeric in Excel/Sheets.

**One assumption to verify:** `10/03/2026` and `18/03/2026` fit the surrounding dates as **day/month** (March 10 and March 18), so I read them that way rather than US month/day (which would put Oct 3 out of order). Say the word if they were actually meant differently.

**Total: $3,542.60** across 18 transactions.