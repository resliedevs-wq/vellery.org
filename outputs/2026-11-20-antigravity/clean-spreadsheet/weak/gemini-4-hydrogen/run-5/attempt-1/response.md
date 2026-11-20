Here is the cleaned CSV, standardized to `YYYY-MM-DD` dates, Title Case categories, plain two-decimal numeric amounts, and deduplicated/sorted chronologically:

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

### Changes & Assumptions
- **Removed 2 exact duplicate rows** (20 → 18 rows):
  - `2026-03-02, Office chairs, Furniture, $1,240.00`
  - `03/04/2026, Printer paper, office supplies, 48.5`
  - *(Kept both `Team lunch` entries for `$212.40` since they have different dates: `2026-03-05` and `2026-03-25`.)*
- **Standardized dates to `YYYY-MM-DD`**:
  - The raw data mixes `MM/DD/YYYY` (e.g., `3/24/2026`) and `DD/MM/YYYY` (e.g., `18/03/2026`), and `Mar 13` omits the year.
  - Because the sheet is ordered chronologically within March 2026, `03/04/2026` (`2026-03-04`), `3/9/26` (`2026-03-09`), `10/03/2026` (`2026-03-10`), and `Mar 13` (`2026-03-13`) were resolved as March 2026 dates—please double-check `10/03/2026` (`Train tickets`) and `03/04/2026` (`Printer paper`) if any entries were actually from April or October.
- **Standardized `Category` casing** to Title Case (`Office Supplies`, `Travel`, `Software`, `Furniture`, `Meals`, `Equipment`).
- **Standardized `Amount` values** by removing `$`, thousands separators, and extra quotes, and formatting all values to 2 decimal places for spreadsheet/formula compatibility (assuming all amounts are in the same currency, e.g. USD).
