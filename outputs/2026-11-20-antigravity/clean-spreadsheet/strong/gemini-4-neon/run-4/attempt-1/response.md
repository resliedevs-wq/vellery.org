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

### Changes Made

**Removed exact duplicate rows (2):**
- Original row 4: `2026-03-02,Office chairs,Furniture,"$1,240.00"` (exact duplicate of row 1)
- Original row 11: `03/04/2026,Printer paper,office supplies,48.5` (exact duplicate of row 2)

**Standardized dates to `YYYY-MM-DD` (7 rows):**
- `03/04/2026` → `2026-03-04` (Printer paper)
- `March 5 2026` → `2026-03-05` (Team lunch)
- `3/9/26` → `2026-03-09` (Zoom subscription)
- `10/03/2026` → `2026-03-10` (Train tickets)
- `Mar 13` → `2026-03-13` (Monitor)
- `18/03/2026` → `2026-03-18` (Client dinner)
- `3/24/2026` → `2026-03-24` (USB-C cables)

**Converted categories to Title Case (5 rows):**
- `office supplies` → `Office Supplies` (Printer paper)
- `travel` → `Travel` (Taxi to client)
- `software` → `Software` (Figma seats)
- `furniture` → `Furniture` (Desk lamp)
- `Office supplies` → `Office Supplies` (Pens)

**Formatted amounts to plain two-decimal numbers (17 rows; only `Coffee beans` at `27.99` was unchanged):**
- Stripped quotes, `$`, and commas: `"$1,240.00"` → `1240.00`, `"$184.00"` → `184.00`, `"$318.60"` → `318.60`, `"$412.00"` → `412.00`
- Stripped `$`: `$212.40` → `212.40` (both Team lunch rows), `$36.20` → `36.20`, `$329.00` → `329.00`, `$22.75` → `22.75`, `$90.00` → `90.00`, `$31.96` → `31.96`, `$9.80` → `9.80`, `$58.00` → `58.00`, `$96.00` → `96.00`
- Added missing decimals (and stripped `$` where present): `48.5` → `48.50`, `149` → `149.00`, `$64` → `64.00`

### Uncertainties / Notes to Double-Check
- **Mixed date formats (`MM/DD/YYYY` vs. `DD/MM/YYYY`):** The sheet mixes US-style dates (`3/24/2026`, `3/9/26`, `03/04/2026`) and day-first dates (`10/03/2026`, `18/03/2026`), plus `Mar 13` with no year. All ambiguous dates (`03/04/2026`, `3/9/26`, `10/03/2026`) were resolved as March 2026 per your rule—which also keeps the entire sheet in chronological order.
- **Identical `Team lunch` totals on different dates:** Both `2026-03-05` and `2026-03-25` are `Team lunch, Meals, 212.40`. Kept both per your instruction to keep repeated purchases on different dates, though the exact same amount down to the cent may be worth verifying in case it was a copy/paste error.
- **Category assignments kept as-is:** Only casing was changed—e.g., `Coffee beans` remains `Meals` and `Desk lamp` remains `Furniture`—in case your accounting rules expect different categories.
