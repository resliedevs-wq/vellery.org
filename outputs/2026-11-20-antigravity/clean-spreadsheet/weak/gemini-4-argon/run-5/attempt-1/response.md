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

### Summary of Changes
1. **Standardized Dates (`YYYY-MM-DD`)**:
   - Converted mixed formats (`MM/DD/YYYY`, `DD/MM/YYYY` on `10/03/2026` and `18/03/2026`, `M/D/YY`, and written month names) to ISO `YYYY-MM-DD`.
   - Inferred year `2026` for `Mar 13` (`2026-03-13`).
2. **Removed Exact Duplicates (2 rows)**:
   - `2026-03-02,Office chairs,Furniture,"$1,240.00"`
   - `03/04/2026,Printer paper,office supplies,48.5`
   - *Note:* `Team lunch` ($212.40) appears on both `2026-03-05` and `2026-03-25`; both were kept since the dates differ.
3. **Normalized Categories**: Standardized capitalization to Title Case (`Office Supplies`, `Furniture`, `Software`, `Travel`, `Meals`, `Equipment`).
4. **Cleaned Amounts**: Stripped `$`, quotes, and thousands separators, and formatted all values to two decimal places (`0.00`) so the column can be summed directly as numbers.
