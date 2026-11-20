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

**Exact duplicates removed (2 rows):**
- Removed duplicate row 4: `2026-03-02,Office chairs,Furniture,"$1,240.00"` (exact match to row 1).
- Removed duplicate row 11: `03/04/2026,Printer paper,office supplies,48.5` (exact match to row 2).

**Dates standardized to `YYYY-MM-DD` (7 rows):**
- `03/04/2026` → `2026-03-04` (Printer paper)
- `March 5 2026` → `2026-03-05` (Team lunch)
- `3/9/26` → `2026-03-09` (Zoom subscription)
- `10/03/2026` → `2026-03-10` (Train tickets)
- `Mar 13` → `2026-03-13` (Monitor)
- `18/03/2026` → `2026-03-18` (Client dinner)
- `3/24/2026` → `2026-03-24` (USB-C cables)

**Categories converted to Title Case (5 rows):**
- `office supplies` → `Office Supplies` (Printer paper)
- `travel` → `Travel` (Taxi to client)
- `software` → `Software` (Figma seats)
- `furniture` → `Furniture` (Desk lamp)
- `Office supplies` → `Office Supplies` (Pens)

**Amounts formatted as plain numbers with 2 decimals (17 of 18 remaining rows; only `27.99` for Coffee beans needed no change):**
- Removed `$`, commas, and surrounding quotes: `"$1,240.00"` → `1240.00`, `"$184.00"` → `184.00`, `"$318.60"` → `318.60`, `"$412.00"` → `412.00`.
- Removed `$` from: `$212.40` (×2), `$36.20`, `$329.00`, `$22.75`, `$90.00`, `$31.96`, `$9.80`, `$58.00`, `$96.00`.
- Removed `$` and added decimals: `$64` → `64.00`.
- Added trailing decimal places: `48.5` → `48.50`, `149` → `149.00`.

### Notes & Items to Double-Check
- **Mixed date formats (`MM/DD/YYYY` vs `DD/MM/YYYY`):** `03/04/2026`, `3/9/26`, and `3/24/2026` are month-first, while `10/03/2026` and `18/03/2026` are day-first. Because every expense is from March 2026, each resolves uniquely (and fits the sheet's chronological order), so `03/04/2026` → March 4, `3/9/26` → March 9, and `10/03/2026` → March 10.
- **Missing year on `Mar 13` (Monitor):** Assumed `2026` per the March 2026 rule.
- **Repeated `Team lunch` for the exact same amount (`212.40`):** Kept both `2026-03-05` and `2026-03-25` since they are on different dates, though the identical cent-level total is worth verifying in case it was a copy-paste error rather than a fixed-price/recurring order.
