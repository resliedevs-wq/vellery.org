I cleaned the spreadsheet and saved it as `/tmp/vellery-c2px26an/work/cleaned.csv`. It now has 18 rows, down from 20.

**Changes**
- **Dates:** every date is now `YYYY-MM-DD`. The original mixed ISO, US, day-first and text formats.
- **Duplicates:** I removed 2 exact duplicate rows, the second "Office chairs" and the second "Printer paper".
- **Categories:** I standardized the capitalization, for example `office supplies`, `Office Supplies` and `Office supplies` all became `Office Supplies`. The same applies to `travel`, `software` and `furniture`.
- **Amounts:** I removed the `$` signs and thousands separators, and every amount now has two decimals.
- **Order:** rows are sorted by date.

**Assumptions to check**
- **Ambiguous dates:** every entry falls in March 2026, so I read the ambiguous ones that way.
  - `03/04/2026` became March 4.
  - `10/03/2026` and `18/03/2026` were day-first, so March 10 and March 18.
  - `3/9/26` became March 9.
  - `3/24/2026` became March 24.
- **Missing year:** "Mar 13" had no year, so I assumed 2026.
- **Team lunch:** it appears on 03-05 and 03-25 at the same $212.40. The dates differ, so I kept both. If the second one is a double entry, delete it.