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

- **Exact duplicates removed (2 rows):**
  - Removed duplicate row 4: `2026-03-02,Office chairs,Furniture,"$1,240.00"` (exact match of row 1).
  - Removed duplicate row 11: `03/04/2026,Printer paper,office supplies,48.5` (exact match of row 2).
- **Dates standardized to `YYYY-MM-DD` (7 rows):**
  - `03/04/2026` → `2026-03-04` (Printer paper)
  - `March 5 2026` → `2026-03-05` (Team lunch)
  - `3/9/26` → `2026-03-09` (Zoom subscription)
  - `10/03/2026` → `2026-03-10` (Train tickets)
  - `Mar 13` → `2026-03-13` (Monitor)
  - `18/03/2026` → `2026-03-18` (Client dinner)
  - `3/24/2026` → `2026-03-24` (USB-C cables)
- **Categories converted to Title Case (5 rows):**
  - `office supplies` → `Office Supplies` (Printer paper)
  - `travel` → `Travel` (Taxi to client)
  - `software` → `Software` (Figma seats)
  - `furniture` → `Furniture` (Desk lamp)
  - `Office supplies` → `Office Supplies` (Pens)
- **Amounts formatted as plain numbers with 2 decimals (17 rows):**
  - Removed `$`, commas, and surrounding quotes on: `Office chairs` (`"$1,240.00"` → `1240.00`), `Train tickets` (`"$184.00"` → `184.00`), `Client dinner` (`"$318.60"` → `318.60`), `Hotel (2 nights)` (`"$412.00"` → `412.00`).
  - Removed `$` on: `Team lunch` (Mar 5, `$212.40` → `212.40`), `Taxi to client` (`$36.20` → `36.20`), `Monitor` (`$329.00` → `329.00`), `Notebooks` (`$22.75` → `22.75`), `Figma seats` (`$90.00` → `90.00`), `USB-C cables` (`$31.96` → `31.96`), `Team lunch` (Mar 25, `$212.40` → `212.40`), `Pens` (`$9.80` → `9.80`), `Taxi to airport` (`$58.00` → `58.00`), `Notion subscription` (`$96.00` → `96.00`).
  - Added trailing decimal places (and removed `$` where present) on: `Printer paper` (`48.5` → `48.50`), `Zoom subscription` (`149` → `149.00`), `Desk lamp` (`$64` → `64.00`).
- **Unchanged (1 row):**
  - `2026-03-12,Coffee beans,Meals,27.99` required no edits.

### Things Worth Double-Checking

- **Mixed `MM/DD/YYYY` and `DD/MM/YYYY` date formats:** `03/04/2026`, `3/9/26`, and `3/24/2026` use month-first ordering, while `10/03/2026` and `18/03/2026` use day-first ordering. Using your rule that all expenses are from March 2026 (which also aligns with the sheet's chronological order), `03/04/2026` was interpreted as March 4, `3/9/26` as March 9, `10/03/2026` as March 10, and `18/03/2026` as March 18.
- **Missing year on `Mar 13` (Monitor):** Assumed `2026` per the March 2026 rule.
- **Identical `Team lunch` amounts on two dates:** Both `2026-03-05` and `2026-03-25` have `Team lunch` for the exact same amount (`212.40`). Both were kept per your rule to keep repeated purchases on different dates, though you may want to verify the March 25 amount wasn't accidentally copied from March 5.
- **Category assignments left as-is:** Only casing was changed (e.g., `Coffee beans` remained under `Meals` rather than `Office Supplies`).
