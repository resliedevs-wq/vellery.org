Here is the cleaned CSV:

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
- **Removed 2 exact duplicate rows** (20 → 18 rows):
  - `2026-03-02, Office chairs, Furniture, $1,240.00`
  - `03/04/2026, Printer paper, office supplies, 48.5`
- **Standardized dates to `YYYY-MM-DD`** (ISO 8601), resolving mixed formats (`MM/DD/YYYY`, `DD/MM/YYYY`, `M/D/YY`, text dates, and a missing year).
- **Standardized categories to Title Case**: `Equipment`, `Furniture`, `Meals`, `Office Supplies`, `Software`, `Travel`.
- **Standardized amounts to plain numbers with 2 decimal places**: stripped `$`, thousands commas, and quotes so spreadsheet tools parse them as numeric values.

### Notes & Items to Verify
- **Ambiguous dates inferred as March 2026** based on surrounding chronological entries (and explicit `DD/MM/YYYY` in `18/03/2026` alongside `MM/DD/YYYY` in `3/24/2026`):
  - `03/04/2026` → `2026-03-04` (rather than April 3)
  - `3/9/26` → `2026-03-09` (rather than September 3)
  - `10/03/2026` → `2026-03-10` (rather than October 3)
  - `Mar 13` → `2026-03-13` (missing year assumed `2026`)
- **Kept `2026-03-25, Team lunch, Meals, 212.40`**: it matches the March 5 entry in description and exact amount, but has a different date—worth double-checking if it was an accidental duplicate or a second lunch with the same total.
