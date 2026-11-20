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
  - Dropped the second `2026-03-02,Office chairs,Furniture,"$1,240.00"` (original row 4).
  - Dropped the second `03/04/2026,Printer paper,office supplies,48.5` (original row 11).
- **Standardized dates to `YYYY-MM-DD`:**
  - `03/04/2026` → `2026-03-04`
  - `March 5 2026` → `2026-03-05`
  - `3/9/26` → `2026-03-09`
  - `10/03/2026` → `2026-03-10`
  - `Mar 13` → `2026-03-13`
  - `18/03/2026` → `2026-03-18`
  - `3/24/2026` → `2026-03-24`
- **Converted categories to Title Case:**
  - `office supplies` / `Office supplies` → `Office Supplies`
  - `travel` → `Travel`
  - `software` → `Software`
  - `furniture` → `Furniture`
- **Standardized amounts (removed `$`, commas, and quotes; formatted to 2 decimal places):**
  - `"$1,240.00"` → `1240.00`
  - `48.5` → `48.50`
  - `$212.40` (×2) → `212.40`
  - `149` → `149.00`
  - `$36.20` → `36.20`
  - `"$184.00"` → `184.00`
  - `$329.00` → `329.00`
  - `$22.75` → `22.75`
  - `$90.00` → `90.00`
  - `"$318.60"` → `318.60`
  - `$64` → `64.00`
  - `"$412.00"` → `412.00`
  - `$31.96` → `31.96`
  - `$9.80` → `9.80`
  - `$58.00` → `58.00`
  - `$96.00` → `96.00`

### Notes / Potential Ambiguities
- **Mixed slash-date conventions (`MM/DD` vs. `DD/MM`):** The sheet mixes US (`03/04/2026`, `3/9/26`, `3/24/2026`) and `DD/MM` (`10/03/2026`, `18/03/2026`) formats. Using your constraint that every expense is from March 2026—and noting the chronological order—`03/04/2026` was parsed as `2026-03-04` and `10/03/2026` as `2026-03-10`. Worth double-checking if either was entered with the day/month swapped by mistake.
- **Identical `Team lunch` amounts on different dates:** Kept both `2026-03-05` and `2026-03-25` (`Team lunch`, `Meals`, `212.40`) per your rule, though having the exact same amount to the cent may be worth verifying in case one was copied erroneously.
- **Category boundaries:** Left existing category assignments as-is (only fixed casing), e.g., `Coffee beans` under `Meals` (rather than `Office Supplies`) and `Monitor` / `USB-C cables` under `Equipment`.
