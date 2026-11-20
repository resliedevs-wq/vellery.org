# Expense cleanup summary

**Output:** `expenses_cleaned.csv` (18 rows, $3,542.60 total)

## What changed

| Issue | Before | After |
|---|---|---|
| Duplicate rows | 20 rows | 2 exact duplicates removed → 18 rows |
| Date formats | ISO, `MM/DD/YYYY`, `DD/MM/YYYY`, `Mon DD`, 2-digit years | All ISO `YYYY-MM-DD` |
| Category casing | `office supplies`, `travel`, `software`, `furniture` | Canonical title case |
| Amount formats | `$1,240.00`, `48.5`, `149`, `$64` | Plain numeric, 2 decimals |
| Row order | Unsorted | Chronological, then description |

## Removed duplicates

- `2026-03-02 | Office chairs | Furniture | 1240.00`
- `2026-03-04 | Printer paper | Office Supplies | 48.50`

## Date assumptions

- `03/04/2026` → **2026-03-04** (sits between Mar 2 and Mar 5; sheet is a March ledger)
- `10/03/2026` → **2026-03-10** and `18/03/2026` → **2026-03-18** (day-first; 18 cannot be a month)
- `3/9/26` → **2026-03-09**; `Mar 13` → **2026-03-13** (year inferred as 2026)

## Totals by category

| Category | Rows | Total |
|---|---:|---:|
| Equipment | 2 | $360.96 |
| Furniture | 2 | $1,304.00 |
| Meals | 4 | $771.39 |
| Office Supplies | 3 | $81.05 |
| Software | 3 | $335.00 |
| Travel | 4 | $690.20 |
| **Total** | **18** | **$3,542.60** |

## Worth a quick look

- **Team lunch** appears on both Mar 5 and Mar 25 for the same $212.40. The dates differ, so both were kept; remove the Mar 25 entry if it was a duplicate keyed with the wrong date.
- `03/04/2026` is the only genuinely ambiguous date. If your source is day-first, it would be **2026-04-03** and the row would move to the end.
