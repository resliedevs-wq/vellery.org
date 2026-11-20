Here is the cleaned and standardized CSV:

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

### Summary of Changes
* **Removed exact duplicates (2 rows):**
  * `2026-03-02,Office chairs,Furniture,"$1,240.00"` (appeared twice)
  * `03/04/2026,Printer paper,office supplies,48.5` (appeared twice)
  * *Note:* `Team lunch` (`$212.40`) appears on both `2026-03-05` and `2026-03-25`; both were kept since the dates differ.
* **Standardized dates to `YYYY-MM-DD`:**
  * Resolved mixed US (`MM/DD/YYYY` like `3/24/2026`), international (`DD/MM/YYYY` like `18/03/2026`), and text (`March 5 2026`, `Mar 13`) formats into March 2026 dates based on chronological order (`03/04/2026` $\rightarrow$ `2026-03-04`, `10/03/2026` $\rightarrow$ `2026-03-10`, `Mar 13` $\rightarrow$ `2026-03-13`).
* **Normalized categories to Title Case:** Unified `office supplies` / `Office supplies` $\rightarrow$ `Office Supplies`, `furniture` $\rightarrow$ `Furniture`, `software` $\rightarrow$ `Software`, and `travel` $\rightarrow$ `Travel`.
* **Formatted amounts as plain decimals:** Stripped `$`, commas, and quotes, and padded all values to two decimal places (e.g., `48.5` $\rightarrow$ `48.50`, `$64` $\rightarrow$ `64.00`) so the column works directly for spreadsheet formulas.
