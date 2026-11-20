Here is the cleaned spreadsheet:

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

### Changes Made
- **Dates:** Standardized all dates to `YYYY-MM-DD` (sorted chronologically).
- **Categories:** Normalized casing to Title Case (`Equipment`, `Furniture`, `Meals`, `Office Supplies`, `Software`, `Travel`).
- **Amounts:** Removed `$`, commas, and quotes, and standardized to 2 decimal places so values import cleanly as numbers (18 rows totaling **$3,542.60**).
- **Duplicates removed (2 exact matches):**
  - `2026-03-02` — Office chairs (`$1,240.00`)
  - `03/04/2026` — Printer paper (`48.5`)

### Items to Double-Check
- **Mixed/ambiguous date formats:** The input mixed `MM/DD/YYYY` (e.g., `3/24/2026`) and `DD/MM/YYYY` (e.g., `18/03/2026`). Based on chronological order within March 2026, `03/04/2026`, `3/9/26`, and `10/03/2026` were resolved as `2026-03-04`, `2026-03-09`, and `2026-03-10`.
- **Missing year:** `Mar 13` (Monitor) was assumed to be `2026-03-13`.
- **Same-amount entry kept:** `Team lunch` (`212.40`) appears on both `2026-03-05` and `2026-03-25`; both were kept since the dates differ, but worth verifying if it's a copy-paste error.
