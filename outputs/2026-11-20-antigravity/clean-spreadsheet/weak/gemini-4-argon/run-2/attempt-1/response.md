Here is the cleaned CSV data, followed by a summary of the fixes applied:

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
1. **Standardized Dates (`YYYY-MM-DD`)**:
   - Converted mixed formats (`03/04/2026`, `March 5 2026`, `3/9/26`, `10/03/2026`, `18/03/2026`, `3/24/2026`) to ISO 8601 format.
   - Added the year `2026` to `Mar 13` (`2026-03-13`) based on surrounding entries.
2. **Normalized Categories (Title Case)**:
   - Standardized casing across `Furniture`, `Office Supplies`, `Software`, and `Travel`.
3. **Cleaned Numeric Amounts**:
   - Stripped `$` symbols, commas, and quotes, and normalized all values to two decimal places (e.g., `"$1,240.00"` $\rightarrow$ `1240.00`, `48.5` $\rightarrow$ `48.50`, `149` $\rightarrow$ `149.00`).
4. **Removed Exact Duplicates**:
   - Removed duplicate `2026-03-02,Office chairs,Furniture,"$1,240.00"`.
   - Removed duplicate `03/04/2026,Printer paper,office supplies,48.5`.

### Items to Verify
- **Ambiguous Slash Dates**: `03/04/2026` was treated as `MM/DD/YYYY` (`2026-03-04`) and `10/03/2026` as `DD/MM/YYYY` (`2026-03-10`) to match the chronological March 2026 ordering.
- **Repeated Amount on Different Date**: `Team lunch` (`212.40`) appears on both `2026-03-05` and `2026-03-25`. Both were kept since the dates differ.
