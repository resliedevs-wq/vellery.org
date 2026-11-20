Cleaned both formats:

- [Download the Excel workbook](cleaned_expenses.xlsx) — formatted table with frozen header, filters, real dates, and currency values
- [Download the CSV](cleaned_expenses.csv)

**Changes made**
- 18 unique transactions; 2 exact duplicates removed
- Dates normalized to `YYYY-MM-DD` and sorted chronologically
- Categories standardized to title case
- Amounts converted to numeric values with 2 decimals
- Total: **$3,542.60**

**Date assumptions**
- `03/04/2026` → `2026-03-04`
- `10/03/2026` → `2026-03-10`
- `18/03/2026` → `2026-03-18`
- `Mar 13` → `2026-03-13`

The two team-lunch entries were retained because they occur on different dates. If `03/04/2026` was intended as April 3, I can switch it.