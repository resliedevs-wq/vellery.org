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

**Dates normalized to YYYY-MM-DD**
- `03/04/2026` → 2026-03-04
- `March 5 2026` → 2026-03-05
- `3/9/26` → 2026-03-09
- `10/03/2026` → 2026-03-10 (day-first)
- `Mar 13` → 2026-03-13
- `18/03/2026` → 2026-03-18 (day-first)
- `3/24/2026` → 2026-03-24

**Duplicates removed (2 rows)**
- "Office chairs" 2026-03-02, $1,240.00 — appeared twice, removed one
- "Printer paper" 2026-03-04, $48.50 — appeared twice, removed one

**Kept as legitimate repeats (different dates)**
- "Team lunch" $212.40 on 2026-03-05 and 2026-03-25 — same amount, different dates

**Categories → Title Case**
- `office supplies` → Office Supplies (3 rows), `travel` → Travel, `software` → Software (2 rows), `furniture` → Furniture, `Office supplies` → Office Supplies (capitalization only)

**Amounts normalized**
- Stripped `$` and thousands commas (e.g., `"$1,240.00"` → 1240.00)
- Added two decimals where missing (48.5 → 48.50, 149 → 149.00, 64 → 64.00)

## Things I wasn't sure about

1. **Ambiguous numeric dates.** The sheet mixes formats, so I inferred each from context: `03/04/2026` (March 4 vs. April 3) and `3/9/26` (March 9 vs. Sept 3) were read as month-first; `10/03/2026` and `18/03/2026` as day-first, since 18 can't be a month and the prompt says everything is March 2026. All four readings are forced by the March-only constraint, but if any source system used a different convention, those dates would shift.
2. **Same-day expense pairs kept.** 2026-03-10 (taxi + train) and 2026-03-18 (Figma + client dinner) each have two rows — not duplicates, so I kept both.
3. **Row order.** I preserved the original ordering, which happens to be chronological. Say the word if you'd like it sorted differently or grouped by category.