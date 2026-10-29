I cleaned the spreadsheet and saved it as `/tmp/vellery-_v9nrciu/work/expenses_clean.csv`. It has 18 rows, down from 20.

**What I changed**
- **Duplicates:** I removed 2 exact repeats, the Office chairs on 03-02 and the Printer paper on 03-04.
- **Dates:** Everything is now `YYYY-MM-DD`. That covers `March 5 2026`, `3/9/26`, `Mar 13` and the slash formats.
- **Categories:** I standardized the capitalization, so `office supplies`, `Office Supplies`, `travel` and `software` each became one consistent label. There are now 5 categories: Furniture, Office Supplies, Meals, Software, Equipment, plus Travel.
- **Amounts:** I removed the `$` signs and thousands commas and gave every amount two decimals, for example `$1,240.00` became `1240.00` and `149` became `149.00`.
- **Order:** Rows are sorted by date.

**Assumptions to check**
- `10/03/2026` (Train tickets) is day/month, so 2026-03-10. It sits between 03-10 and 03-12 in the original, and the neighboring `18/03/2026` is clearly day/month.
- `03/04/2026` (Printer paper) is month/day, so 2026-03-04. It sits between 03-02 and 03-05.
- `Mar 13` has no year, so I assumed 2026 like the rest of the data.
- I kept both Team lunch rows (03-05 and 03-25, each 212.40). The dates differ, so they may be separate lunches, but the identical amount could also be a data-entry repeat.