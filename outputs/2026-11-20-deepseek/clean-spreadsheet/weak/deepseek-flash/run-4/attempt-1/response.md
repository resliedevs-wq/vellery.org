Cleaned **20 rows → 18**, removing 2 exact duplicates, normalizing dates/categories/amounts, and sorting chronologically.

**Files:** `expenses_cleaned.csv` · `cleaning_summary.md`

| Date | Description | Category | Amount |
|---|---|---|---:|
| 2026-03-02 | Office chairs | Furniture | $1,240.00 |
| 2026-03-04 | Printer paper | Office Supplies | $48.50 |
| 2026-03-05 | Team lunch | Meals | $212.40 |
| 2026-03-09 | Zoom subscription | Software | $149.00 |
| 2026-03-10 | Taxi to client | Travel | $36.20 |
| 2026-03-10 | Train tickets | Travel | $184.00 |
| 2026-03-12 | Coffee beans | Meals | $27.99 |
| 2026-03-13 | Monitor | Equipment | $329.00 |
| 2026-03-15 | Notebooks | Office Supplies | $22.75 |
| 2026-03-18 | Client dinner | Meals | $318.60 |
| 2026-03-18 | Figma seats | Software | $90.00 |
| 2026-03-20 | Desk lamp | Furniture | $64.00 |
| 2026-03-22 | Hotel (2 nights) | Travel | $412.00 |
| 2026-03-24 | USB-C cables | Equipment | $31.96 |
| 2026-03-25 | Team lunch | Meals | $212.40 |
| 2026-03-27 | Pens | Office Supplies | $9.80 |
| 2026-03-30 | Taxi to airport | Travel | $58.00 |
| 2026-03-31 | Notion subscription | Software | $96.00 |

**Total: $3,542.60**

- **Removed:** duplicate Office chairs ($1,240.00, Mar 2) and Printer paper ($48.50, Mar 4).
- **Categories normalized:** `office supplies` → Office Supplies, plus Travel, Software, Furniture.
- **Amounts:** plain numbers with 2 decimals, no `$` or thousands separators.
- **Dates:** all ISO. `03/04/2026` read as **Mar 4** (it sits between Mar 2 and Mar 5); `10/03` and `18/03` are day-first; `Mar 13` and `3/9/26` use 2026.
- **Flag:** Team lunch appears Mar 5 and Mar 25 at the same $212.40. Both were kept since the dates differ — delete the Mar 25 one if it's a mis-dated duplicate.