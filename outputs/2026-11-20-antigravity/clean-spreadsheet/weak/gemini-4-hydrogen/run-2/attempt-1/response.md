Here is the cleaned spreadsheet in CSV format:

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
- **Standardized dates (`YYYY-MM-DD`)**: Converted mixed formats (`03/04/2026`, `March 5 2026`, `3/9/26`, `10/03/2026`, `Mar 13`, `18/03/2026`, `3/24/2026`) to ISO format.
- **Removed 2 exact duplicate rows**:
  - `2026-03-02,Office chairs,Furniture,$1,240.00`
  - `03/04/2026,Printer paper,office supplies,48.5` (appeared out of order after `2026-03-15`)
- **Normalized `Category` casing**: Standardized to Title Case (`Furniture`, `Office Supplies`, `Meals`, `Software`, `Travel`, `Equipment`).
- **Standardized `Amount` values**: Removed `$` signs, thousands commas, and unnecessary quotes, and formatted all values to two decimal places so the column is cleanly numeric.

### Items to Double-Check
- **Ambiguous/inferred dates**: Based on the surrounding March 2026 chronological sequence, `03/04/2026` was interpreted as `2026-03-04` (MM/DD/YYYY), `10/03/2026` as `2026-03-10` (DD/MM/YYYY), and `Mar 13` was assigned the year `2026`.
- **Possible recurring/duplicate expense**: `Team lunch` (`Meals`, `212.40`) appears on both `2026-03-05` and `2026-03-25`—both were kept since the dates differ.
