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
1. **Removed exact duplicate rows (2 rows removed, 18 data rows remaining):**
   - Row 4 (`2026-03-02,Office chairs,Furniture,"$1,240.00"`), exact duplicate of row 1.
   - Row 11 (`03/04/2026,Printer paper,office supplies,48.5`), exact duplicate of row 2.
2. **Standardized dates to `YYYY-MM-DD`:**
   - `03/04/2026` → `2026-03-04`
   - `March 5 2026` → `2026-03-05`
   - `3/9/26` → `2026-03-09`
   - `10/03/2026` → `2026-03-10`
   - `Mar 13` → `2026-03-13`
   - `18/03/2026` → `2026-03-18`
   - `3/24/2026` → `2026-03-24`
3. **Standardized categories to Title Case:**
   - `office supplies` (row 2) and `Office supplies` (row 18) → `Office Supplies`
   - `travel` (row 6) → `Travel`
   - `software` (row 12) → `Software`
   - `furniture` (row 14) → `Furniture`
4. **Standardized amounts to plain numbers with two decimal places (no `$`, commas, or CSV quotes):**
   - `"$1,240.00"` → `1240.00`
   - `48.5` → `48.50`
   - `149` → `149.00`
   - `$64` → `64.00`
   - Quoted dollar strings (`"$184.00"`, `"$318.60"`, `"$412.00"`) → `184.00`, `318.60`, `412.00`
   - Unquoted dollar strings (`$212.40`, `$36.20`, `$329.00`, `$22.75`, `$90.00`, `$31.96`, `$9.80`, `$58.00`, `$96.00`) → stripped `$` (`27.99` on `2026-03-12` required no changes).

### Things Worth Double-Checking / Uncertainties
- **Mixed `MM/DD/YYYY` and `DD/MM/YYYY` date formats in source:** The original sheet mixes US month-first dates (`03/04/2026`, `3/9/26`, `3/24/2026`) and day-first dates (`10/03/2026`, `18/03/2026`), plus `Mar 13` without a year. The rule that every expense is from March 2026 resolves `03/04/2026` (`2026-03-04`), `10/03/2026` (`2026-03-10`), and `Mar 13` (`2026-03-13`), so there is no ambiguity here, though you may want to enforce one input format upstream.
- **Identical `Team lunch` amount on two different dates:** `2026-03-05` and `2026-03-25` are both `Team lunch,Meals,212.40`. I kept both per your rule to retain repeated purchases on different dates, but the identical `$212.40` total down to the cent may be worth verifying in case one was entered with the wrong date rather than being a separate order of the exact same amount.
- **Category boundaries:** I preserved all existing category names as written (only normalizing casing), though items like `Coffee beans` (`Meals`), `Desk lamp` (`Furniture`), or `USB-C cables` (`Equipment`) might belong under `Office Supplies` depending on your accounting rules.
