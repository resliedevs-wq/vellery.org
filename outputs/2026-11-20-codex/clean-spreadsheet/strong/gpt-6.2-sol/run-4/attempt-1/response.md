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

### Changes made

Removed the second copy of each exact duplicate: Office chairs on March 2 and Printer paper on March 4. Kept both Team lunch purchases, dated March 5 and March 25. The CSV contains 18 expenses.

| Expense | Date change | Category change | Amount change |
|---|---|---|---|
| Office chairs | | | `$1,240.00` → `1240.00` |
| Printer paper | `03/04/2026` → `2026-03-04` | `office supplies` → `Office Supplies` | `48.5` → `48.50` |
| Team lunch, March 5 | `March 5 2026` → `2026-03-05` | | `$212.40` → `212.40` |
| Zoom subscription | `3/9/26` → `2026-03-09` | | `149` → `149.00` |
| Taxi to client | | `travel` → `Travel` | `$36.20` → `36.20` |
| Train tickets | `10/03/2026` → `2026-03-10` | | `$184.00` → `184.00` |
| Monitor | `Mar 13` → `2026-03-13` | | `$329.00` → `329.00` |
| Notebooks | | | `$22.75` → `22.75` |
| Figma seats | | `software` → `Software` | `$90.00` → `90.00` |
| Client dinner | `18/03/2026` → `2026-03-18` | | `$318.60` → `318.60` |
| Desk lamp | | `furniture` → `Furniture` | `$64` → `64.00` |
| Hotel (2 nights) | | | `$412.00` → `412.00` |
| USB-C cables | `3/24/2026` → `2026-03-24` | | `$31.96` → `31.96` |
| Team lunch, March 25 | | | `$212.40` → `212.40` |
| Pens | | `Office supplies` → `Office Supplies` | `$9.80` → `9.80` |
| Taxi to airport | | | `$58.00` → `58.00` |
| Notion subscription | | | `$96.00` → `96.00` |

### Date assumptions

The slash dates used mixed conventions. Your March 2026 constraint resolved the ambiguous entries: `03/04/2026` is March 4, `3/9/26` is March 9, and `10/03/2026` is March 10. I also used 2026 for `Mar 13`, which omitted the year. No uncertainties remained.