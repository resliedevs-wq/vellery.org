[Download the cleaned March 2026 expense CSV](/tmp/vellery-tq3bf21t/work/march-2026-expenses.csv)

The CSV contains 18 expenses in their original order. I removed the second occurrence of two exact duplicates: Office chairs on March 2 (source row 4) and Printer paper on March 4 (source row 11), counting rows below the header. I kept both $212.40 team lunches because they occurred on March 5 and March 25.

| Expense | Changes |
|---|---|
| Office chairs | `$1,240.00` → `1240.00` |
| Printer paper | `03/04/2026` → `2026-03-04`, `office supplies` → `Office Supplies`, `48.5` → `48.50` |
| Team lunch, March 5 | `March 5 2026` → `2026-03-05`, `$212.40` → `212.40` |
| Zoom subscription | `3/9/26` → `2026-03-09`, `149` → `149.00` |
| Taxi to client | `travel` → `Travel`, `$36.20` → `36.20` |
| Train tickets | `10/03/2026` → `2026-03-10`, `$184.00` → `184.00` |
| Monitor | `Mar 13` → `2026-03-13`, `$329.00` → `329.00` |
| Notebooks | `$22.75` → `22.75` |
| Figma seats | `software` → `Software`, `$90.00` → `90.00` |
| Client dinner | `18/03/2026` → `2026-03-18`, `$318.60` → `318.60` |
| Desk lamp | `furniture` → `Furniture`, `$64` → `64.00` |
| Hotel (2 nights) | `$412.00` → `412.00` |
| USB-C cables | `3/24/2026` → `2026-03-24`, `$31.96` → `31.96` |
| Team lunch, March 25 | `$212.40` → `212.40` |
| Pens | `Office supplies` → `Office Supplies`, `$9.80` → `9.80` |
| Taxi to airport | `$58.00` → `58.00` |
| Notion subscription | `$96.00` → `96.00` |

**Date interpretation.** Your instruction that every expense occurred in March 2026 resolved the mixed month/day order and supplied the missing year for `Mar 13`. No uncertainties remain.