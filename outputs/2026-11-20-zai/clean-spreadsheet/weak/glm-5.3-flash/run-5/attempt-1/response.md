Bash isn't available in this session, but the file is written and I verified the math manually. Cleaned spreadsheet saved to `expenses_clean.csv`:

| Date | Description | Category | Amount |
|------|-------------|----------|-------:|
| 2026-03-02 | Office chairs | Furniture | 1240.00 |
| 2026-03-04 | Printer paper | Office Supplies | 48.50 |
| 2026-03-05 | Team lunch | Meals | 212.40 |
| 2026-03-09 | Zoom subscription | Software | 149.00 |
| 2026-03-10 | Taxi to client | Travel | 36.20 |
| 2026-03-10 | Train tickets | Travel | 184.00 |
| 2026-03-12 | Coffee beans | Meals | 27.99 |
| 2026-03-13 | Monitor | Equipment | 329.00 |
| 2026-03-15 | Notebooks | Office Supplies | 22.75 |
| 2026-03-18 | Figma seats | Software | 90.00 |
| 2026-03-18 | Client dinner | Meals | 318.60 |
| 2026-03-20 | Desk lamp | Furniture | 64.00 |
| 2026-03-22 | Hotel (2 nights) | Travel | 412.00 |
| 2026-03-24 | USB-C cables | Equipment | 31.96 |
| 2026-03-25 | Team lunch | Meals | 212.40 |
| 2026-03-27 | Pens | Office Supplies | 9.80 |
| 2026-03-30 | Taxi to airport | Travel | 58.00 |
| 2026-03-31 | Notion subscription | Software | 96.00 |

**Total: $3,542.60** · 18 rows (was 20)

What I fixed:

- **Removed 2 exact duplicates** — Office chairs ($1,240.00) and Printer paper ($48.50) each appeared twice. The two "Team lunch" entries were kept since they're on different dates (Mar 5 vs Mar 25).
- **Normalized dates to ISO `YYYY-MM-DD`.** Ambiguous ones were resolved using the fact that the sheet runs in chronological order through March 2026:
  - `03/04/2026` → 2026-03-04 (M/D; it falls between Mar 2 and Mar 5)
  - `10/03/2026` → 2026-03-10 (D/M; between Mar 9 and Mar 12)
  - `18/03/2026` → 2026-03-18 (D/M; matches the Figma seats row the same day)
  - `3/9/26` → 2026-03-09, `Mar 13` → 2026-03-13 (year inferred from context)
- **Standardized category casing** (e.g. `office supplies`/`Office supplies` → Office Supplies, `travel` → Travel, `software` → Software, `furniture` → Furniture).
- **Normalized amounts to plain numbers** — stripped `$` and thousands commas, padded to 2 decimals so they parse as numeric in any spreadsheet tool.

One thing to double-check: the `10/03/2026` and `18/03/2026` rows were read as day-first. If your source system was actually inconsistent in the other direction, those two dates (and `03/04`) would shift.