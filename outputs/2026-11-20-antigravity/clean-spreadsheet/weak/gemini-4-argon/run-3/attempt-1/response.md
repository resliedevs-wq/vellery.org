Here is the cleaned spreadsheet data as both a copy-ready CSV and a formatted table.

### Cleaned CSV

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

### Formatted Table

| Date | Description | Category | Amount |
| :--- | :--- | :--- | ---: |
| 2026-03-02 | Office chairs | Furniture | $1,240.00 |
| 2026-03-04 | Printer paper | Office Supplies | $48.50 |
| 2026-03-05 | Team lunch | Meals | $212.40 |
| 2026-03-09 | Zoom subscription | Software | $149.00 |
| 2026-03-10 | Taxi to client | Travel | $36.20 |
| 2026-03-10 | Train tickets | Travel | $184.00 |
| 2026-03-12 | Coffee beans | Meals | $27.99 |
| 2026-03-13 | Monitor | Equipment | $329.00 |
| 2026-03-15 | Notebooks | Office Supplies | $22.75 |
| 2026-03-18 | Figma seats | Software | $90.00 |
| 2026-03-18 | Client dinner | Meals | $318.60 |
| 2026-03-20 | Desk lamp | Furniture | $64.00 |
| 2026-03-22 | Hotel (2 nights) | Travel | $412.00 |
| 2026-03-24 | USB-C cables | Equipment | $31.96 |
| 2026-03-25 | Team lunch | Meals | $212.40 |
| 2026-03-27 | Pens | Office Supplies | $9.80 |
| 2026-03-30 | Taxi to airport | Travel | $58.00 |
| 2026-03-31 | Notion subscription | Software | $96.00 |
| **Total** | | | **$3,542.60** |

### Changes Made
1. **Removed Exact Duplicates (2 rows):**
   - `2026-03-02,Office chairs,Furniture,"$1,240.00"` (appeared twice)
   - `03/04/2026,Printer paper,office supplies,48.5` (appeared twice)
   - *(Note: The two `Team lunch` entries for `$212.40` on `2026-03-05` and `2026-03-25` have different dates and were both kept.)*
2. **Standardized Dates to ISO 8601 (`YYYY-MM-DD`):** Converted mixed US (`MM/DD/YYYY`, `M/D/YY`), UK/EU (`10/03/2026`, `18/03/2026`), and text formats (`March 5 2026`, `Mar 13`) to `2026-03-XX` and sorted chronologically.
3. **Normalized Categories:** Unified inconsistent casing (`office supplies` / `Office supplies` $\rightarrow$ `Office Supplies`, `travel` $\rightarrow$ `Travel`, `software` $\rightarrow$ `Software`, `furniture` $\rightarrow$ `Furniture`).
4. **Standardized Amounts:** Stripped `$`, commas, and quotes in the CSV and formatted all values to two decimal places so spreadsheet software parses them cleanly as numbers.
