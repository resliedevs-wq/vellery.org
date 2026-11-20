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
- **Removed exact duplicates (2 rows):**
  - `2026-03-02,Office chairs,Furniture,"$1,240.00"` (duplicate of row 1)
  - `03/04/2026,Printer paper,office supplies,48.5` (duplicate of row 2)
- **Standardized dates to `YYYY-MM-DD`:**
  - `03/04/2026` → `2026-03-04`
  - `March 5 2026` → `2026-03-05`
  - `3/9/26` → `2026-03-09`
  - `10/03/2026` → `2026-03-10`
  - `Mar 13` → `2026-03-13`
  - `18/03/2026` → `2026-03-18`
  - `3/24/2026` → `2026-03-24`
- **Normalized categories to Title Case:**
  - `office supplies` / `Office supplies` → `Office Supplies` (`2026-03-04`, `2026-03-27`)
  - `travel` → `Travel` (`2026-03-10`)
  - `software` → `Software` (`2026-03-18`)
  - `furniture` → `Furniture` (`2026-03-20`)
- **Formatted amounts as plain two-decimal numbers (stripped `$`, commas, and surrounding quotes; padded missing decimals):**
  - `"$1,240.00"` → `1240.00`
  - `48.5` → `48.50`
  - `149` → `149.00`
  - `$64` → `64.00`
  - Removed `$` (and quotes where present) from `$212.40`, `$36.20`, `"$184.00"`, `$329.00`, `$22.75`, `$90.00`, `"$318.60"`, `"$412.00"`, `$31.96`, `$9.80`, `$58.00`, `$96.00`.

### Anything Unclear / Worth Double-Checking
- **Mixed US (`MM/DD`) and non-US (`DD/MM`) date formats:** The input mixes `MM/DD/YYYY` (`03/04/2026`, `3/9/26`, `3/24/2026`), `DD/MM/YYYY` (`10/03/2026`, `18/03/2026`), and yearless (`Mar 13`). Using your constraint that every expense is from March 2026, each date maps to a single valid March 2026 date, though if `03/04/2026` or `3/9/26` were entered by someone strictly using `DD/MM`, they would originally have meant April 3 or September 3.
- **Identical `Team lunch` amounts on different dates:** Both `2026-03-05` and `2026-03-25` have `Team lunch,Meals,212.40`. I kept both per your rule to keep repeated purchases on different dates, though the identical dollar-and-cent total (`212.40`) could be worth confirming if one was entered with a mistyped date or copied from the earlier entry.
