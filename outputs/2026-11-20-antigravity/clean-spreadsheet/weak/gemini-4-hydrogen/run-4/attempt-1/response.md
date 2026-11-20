Here is the cleaned CSV (18 rows, down from 20):

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

### Changes & Notes
- **Removed 2 exact duplicates:** `2026-03-02, Office chairs` and `03/04/2026, Printer paper`.
- **Standardized dates to `YYYY-MM-DD`** (sorted chronologically):
  - `03/04/2026` was interpreted as `2026-03-04` (`MM/DD/YYYY`) based on surrounding March entries (vs. April 3).
  - `10/03/2026` was interpreted as `2026-03-10` (`DD/MM/YYYY`) based on surrounding March 10–12 entries and `18/03/2026` (vs. October 3).
  - `Mar 13` had no year; inferred `2026`.
- **Standardized categories** to Title Case (`Office Supplies`, `Travel`, `Software`, `Furniture`, `Meals`, `Equipment`).
- **Standardized amounts** by stripping `$`, quotes, and commas, and formatting to two decimal places (total: **$3,542.60**).
- **Flagged for review:** `Team lunch` (`Meals`, `212.40`) appears on both `2026-03-05` and `2026-03-25`—both were kept since the dates differ.
