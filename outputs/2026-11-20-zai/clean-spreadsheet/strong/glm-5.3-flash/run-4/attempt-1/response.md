Here's the cleaned sheet:

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

**Dates normalized to YYYY-MM-DD:**
- `03/04/2026` (×2) → `2026-03-04`
- `March 5 2026` → `2026-03-05`
- `3/9/26` → `2026-03-09`
- `10/03/2026` → `2026-03-10`
- `Mar 13` → `2026-03-13` (year inferred)
- `18/03/2026` → `2026-03-18`
- `3/24/2026` → `2026-03-24`

**Duplicates removed (2 rows):**
- Office chairs, 2026-03-02, $1,240.00 (appeared twice)
- Printer paper, 03/04/2026, 48.5 (appeared twice)

**Kept despite looking similar:**
- Team lunch $212.40 appears twice (2026-03-05 and 2026-03-25) — different dates, so both kept per your rule.

**Categories to Title Case:**
- `office supplies` / `Office supplies` → `Office Supplies`
- `travel` → `Travel`
- `software` → `Software` (Figma seats row)
- `furniture` → `Furniture`

**Amounts reformatted:** stripped `$` and thousands commas, forced two decimals (`48.5` → `48.50`, `149` → `149.00`, `64` → `64.00`, `$1,240.00` → `1240.00`).

## Things I wasn't sure about

1. **The sheet mixes US (M/D) and European (D/M) date formats.** Each ambiguous date resolves uniquely because you said everything is from March 2026, but the conventions conflict:
   - `03/04/2026` must be M/D (March 4) — as D/M it'd be April 3.
   - `10/03/2026` must be D/M (March 10) — as M/D it'd be October 3.
   - No single locale explains the whole sheet, so I resolved row-by-row using the March-2026 constraint. **Printer paper (2026-03-04) is the one to double-check**, since it's the only row where the alternative reading is a valid date in a different month.
2. **`Mar 13` had no year** — assumed 2026 from context.
3. **`3/9/26` two-digit year** — assumed 2026. (As D/M it would be September 3, so M/D is the only reading that fits March.)
4. **"Coffee beans" is categorized as Meals** — left as given, though some sheets would class it as Office Supplies or a separate category. Similarly "Hotel (2 nights)" kept the parenthetical verbatim rather than splitting the description.