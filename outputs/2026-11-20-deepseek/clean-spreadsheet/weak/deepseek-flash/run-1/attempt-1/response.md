Cleaned and verified.

**Files**
- [cleaned_expenses.csv](cleaned_expenses.csv) — 18 cleaned transactions
- [expense_summary.csv](expense_summary.csv) — category totals

**Changes made**
- Removed 2 exact duplicate rows: Office chairs and Printer paper.
- Standardized dates to `YYYY-MM-DD`.
- Normalized categories to consistent title case.
- Converted amounts to numeric values with 2 decimals.
- Kept both Team lunch entries (Mar 5 and Mar 25) since they’re separate transactions.

**Date assumptions:** mixed slash formats were resolved using row chronology: `03/04/2026` → Mar 4, `3/9/26` → Mar 9, `10/03/2026` → Mar 10, `18/03/2026` → Mar 18.

| Category | Total |
|---|---:|
| Furniture | $1,304.00 |
| Meals | $771.39 |
| Travel | $690.20 |
| Equipment | $360.96 |
| Software | $335.00 |
| Office Supplies | $81.05 |
| **Total** | **$3,542.60** |