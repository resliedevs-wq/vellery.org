Here's the cleaned CSV:

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
- `03/04/2026` → `2026-03-04` (interpreted as month/day/year, matching the `3/24/2026` row's format)
- `March 5 2026` → `2026-03-05`
- `3/9/26` → `2026-03-09`
- `10/03/2026` → `2026-03-10` (day-first; see notes)
- `Mar 13` → `2026-03-13`
- `18/03/2026` → `2026-03-18` (day-first; see notes)
- `3/24/2026` → `2026-03-24`

**Exact duplicates removed** (2 rows):
- Line 5: `2026-03-02, Office chairs, Furniture, $1,240.00` — identical to line 2
- Line 12: `2026-03-04, Printer paper, office supplies, 48.5` — identical to line 3 after normalization

**Categories converted to Title Case** (8 cells): `office supplies` → `Office Supplies` (×3), `travel` → `Travel` (×1), `software` → `Software` (×2), `furniture` → `Furniture` (×1).

**Amounts normalized** — removed `$` and thousands commas, forced two decimals: e.g. `"$1,240.00"` → `1240.00`, `48.5` → `48.50`, `149` → `149.00`, `$64` → `64.00`.

Result: 20 rows in, 18 out. Total: 3542.60.

## Judgment calls / things I wasn't sure about

1. **`10/03/2026` and `18/03/2026` were almost certainly day-first European format.** The month-first reading gives October 3 (not March) and "month 18" (invalid), and both contradict your note that everything is March 2026 — so day-first was the only consistent interpretation. Flagging it since the sheet mixes US-style dates elsewhere.
2. **Team lunch appears twice with the identical amount ($212.40)** — on 2026-03-05 and 2026-03-25. I kept both per your rule that repeated purchases on different dates stay, but if one was a mis-entered date, the amounts are suspiciously identical.
3. **The two duplicate rows were only exact after normalization** — e.g. the second Printer paper row had the lowercase category and unformatted amount, so I treated "exact duplicate" as matching on the normalized values. If you wanted duplicates removed only when the raw text matched byte-for-byte, no rows would have qualified.
4. **Ambiguous date formats in one column mean errors are possible in principle** — `03/04/2026` could be April 3 in a day-first scheme. I read it as month-first since `3/9/26` and `3/24/2026` are unambiguously month-first and appear to come from the same entry habit.