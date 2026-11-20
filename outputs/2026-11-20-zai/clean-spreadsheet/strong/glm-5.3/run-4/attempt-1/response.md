The sandbox blocked the scripted check, so I verified the output by hand instead: 18 data rows (20 minus 2 duplicates), every date in `2026-03` and in non-decreasing order, all amounts two decimals with no `$`/commas, and the column sums to 3542.60.

Cleaned CSV (also saved to `expenses_cleaned.csv`):

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

## Changes made

**Dates normalized to YYYY-MM-DD** (7 rows):
| Original | Cleaned |
|---|---|
| `03/04/2026` (×2) | `2026-03-04` |
| `March 5 2026` | `2026-03-05` |
| `3/9/26` | `2026-03-09` |
| `10/03/2026` | `2026-03-10` |
| `Mar 13` | `2026-03-13` |
| `18/03/2026` | `2026-03-18` |
| `3/24/2026` | `2026-03-24` |

**Exact duplicates removed** (2 rows):
- Second `Office chairs` row (2026-03-02, $1,240.00)
- Second `Printer paper` row (2026-03-04, $48.50)

**Categories title-cased:** `office supplies`/`Office supplies` → `Office Supplies` (3 rows), `travel` → `Travel`, `software` → `Software`, `furniture` → `Furniture`. (Meals, Equipment were already correct.)

**Amounts normalized:** stripped `$` and thousands comma (`"$1,240.00"` → `1240.00`); padded to two decimals (`48.5` → `48.50`, `149` → `149.00`, `64` → `64.00`).

## Things I wasn't sure about

1. **`10/03/2026` (Train tickets)** — genuinely ambiguous. The sheet mixes conventions: `03/04/2026` and `3/24/2026` are month-first, while `18/03/2026` must be day-first (18 can't be a month). I read `10/03/2026` as **March 10** because month-first would give October 3, outside March. That also lands it on the same day as the Taxi to client.
2. **`Mar 13`** had no year — assumed 2026 per your note.
3. **Team lunch, $212.40, on both 03-05 and 03-25** — kept both per your "different dates" rule, but the identical amount is suspicious if you only had one such lunch; it could be a date typo in the source.
4. **Row order** — kept the original order (already chronological after date normalization) rather than re-sorting; the two March 10 and two March 18 rows stay in source order.