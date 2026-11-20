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

**Removed exact duplicates (2 rows):**
- Removed duplicate `2026-03-02,Office chairs,Furniture,"$1,240.00"` (original row 4).
- Removed duplicate `03/04/2026,Printer paper,office supplies,48.5` (original row 11).

**Standardized dates to `YYYY-MM-DD` (7 rows):**
- `Printer paper`: `03/04/2026` → `2026-03-04`
- `Team lunch` (first): `March 5 2026` → `2026-03-05`
- `Zoom subscription`: `3/9/26` → `2026-03-09`
- `Train tickets`: `10/03/2026` → `2026-03-10`
- `Monitor`: `Mar 13` → `2026-03-13`
- `Client dinner`: `18/03/2026` → `2026-03-18`
- `USB-C cables`: `3/24/2026` → `2026-03-24`

**Converted categories to Title Case (5 rows):**
- `Printer paper`: `office supplies` → `Office Supplies`
- `Taxi to client`: `travel` → `Travel`
- `Figma seats`: `software` → `Software`
- `Desk lamp`: `furniture` → `Furniture`
- `Pens`: `Office supplies` → `Office Supplies`

**Formatted amounts as plain two-decimal numbers (17 rows; `Coffee beans` at `27.99` was unchanged):**
- `Office chairs`: `"$1,240.00"` → `1240.00` (removed quotes, `$`, and comma)
- `Printer paper`: `48.5` → `48.50` (added trailing zero)
- `Team lunch` (Mar 5): `$212.40` → `212.40`
- `Zoom subscription`: `149` → `149.00` (added `.00`)
- `Taxi to client`: `$36.20` → `36.20`
- `Train tickets`: `"$184.00"` → `184.00` (removed quotes and `$`)
- `Monitor`: `$329.00` → `329.00`
- `Notebooks`: `$22.75` → `22.75`
- `Figma seats`: `$90.00` → `90.00`
- `Client dinner`: `"$318.60"` → `318.60` (removed quotes and `$`)
- `Desk lamp`: `$64` → `64.00` (removed `$` and added `.00`)
- `Hotel (2 nights)`: `"$412.00"` → `412.00` (removed quotes and `$`)
- `USB-C cables`: `$31.96` → `31.96`
- `Team lunch` (Mar 25): `$212.40` → `212.40`
- `Pens`: `$9.80` → `9.80`
- `Taxi to airport`: `$58.00` → `58.00`
- `Notion subscription`: `$96.00` → `96.00`

### Uncertainties / Notes to Double-Check
- **Mixed slash date formats (`MM/DD/YYYY` vs. `DD/MM/YYYY`):** The sheet mixes US-style dates (`03/04/2026`, `3/9/26`, `3/24/2026`) and day-first dates (`10/03/2026`, `18/03/2026`). Using the rule that all expenses are from March 2026 (which also matches the sheet's chronological ordering), `03/04/2026`, `3/9/26`, and `10/03/2026` were resolved to `2026-03-04`, `2026-03-09`, and `2026-03-10`. Worth confirming none were typos for other months.
- **Missing year on `Mar 13` (`Monitor`):** Assumed `2026` (`2026-03-13`) based on the March 2026 constraint.
- **Identical amount on repeated `Team lunch` (`212.40`):** Kept both `2026-03-05` and `2026-03-25` per your rule to retain repeated purchases on different dates, but having the exact same amount down to the cent (`212.40`) is worth verifying in case it was copied from the earlier entry rather than a recurring fixed-price order.
