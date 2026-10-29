I cleaned the spreadsheet and saved it as `/tmp/vellery-l0hrfl9o/work/cleaned.csv`. It now has 18 rows, down from 20, and the total is $3,542.60.

**What I changed**
- **Duplicates:** I removed 2 exact repeats, Office chairs (03-02) and Printer paper (03-04).
- **Dates:** All dates are now `YYYY-MM-DD`. "March 5 2026" became 2026-03-05, "Mar 13" became 2026-03-13 (I assumed 2026), and "3/9/26" became 2026-03-09.
- **Categories:** Capitalization is consistent, so `office supplies` and `Office Supplies` are one category. The categories are Furniture, Office Supplies, Meals, Software, Travel and Equipment.
- **Amounts:** I removed the `$` and thousands separators and put every amount at two decimals, for example `1240.00`, `48.50` and `64.00`.
- **Order:** Rows are sorted by date.

**Please check these**
- **Mixed date formats:** Two rows were day/month, `10/03/2026` and `18/03/2026`, which I read as March 10 and March 18. The other slash dates (`03/04/2026`, `3/9/26`, `3/24/2026`) I read as month/day. Every row is in March, and these readings fit the dates around them.
- **Team lunch twice:** It appears on 03-05 and 03-25, both at $212.40. The dates differ, so I kept both. If the second is a repeat entry, delete it and the total drops by $212.40.