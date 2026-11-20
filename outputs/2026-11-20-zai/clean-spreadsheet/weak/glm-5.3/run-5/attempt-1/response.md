Cleaned up and saved to `expenses_cleaned.csv`. Here's the result:

| Date | Description | Category | Amount |
|---|---|---|---|
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

**What I fixed**

- **Dates** → normalized to ISO `YYYY-MM-DD`. The sheet mixes US (`3/9/26`), day-first (`18/03/2026`), and written-out (`March 5 2026`, `Mar 13`) formats. Ambiguous ones like `10/03/2026` were resolved by where they fall in the sheet's chronological order (March 10, not October 3). `Mar 13` was assumed to be 2026.
- **Categories** → consistent Title Case (`office supplies`/`Office supplies` → `Office Supplies`, etc.).
- **Amounts** → plain two-decimal numbers, stripping `$`, thousands commas, and quote-wrapping so `SUM()` and friends actually work in a spreadsheet. (Apply currency formatting in the app rather than in the data.)
- **Duplicates** → removed 2 exact duplicate rows: *Office chairs* (3/2) and *Printer paper* (3/4).
- **Sorting** → ordered by date ascending.

**One thing to check**: *Team lunch* for $212.40 appears on both **Mar 5** and **Mar 25** — same description and amount, different dates. That's plausibly two real lunches, so I kept both, but it's worth verifying it's not a mis-entered duplicate.

Final tally: 18 rows (down from 20), totaling **$3,542.60**.