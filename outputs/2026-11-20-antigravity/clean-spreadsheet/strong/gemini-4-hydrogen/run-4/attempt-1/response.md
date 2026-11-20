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
- **Removed exact duplicate rows (2):**
  - Row 4 (`2026-03-02,Office chairs,Furniture,"$1,240.00"`) — exact duplicate of row 1.
  - Row 11 (`03/04/2026,Printer paper,office supplies,48.5`) — exact duplicate of row 2.
- **Standardized dates to `YYYY-MM-DD`:**
  - `03/04/2026` → `2026-03-04` (Printer paper)
  - `March 5 2026` → `2026-03-05` (Team lunch)
  - `3/9/26` → `2026-03-09` (Zoom subscription)
  - `10/03/2026` → `2026-03-10` (Train tickets)
  - `Mar 13` → `2026-03-13` (Monitor)
  - `18/03/2026` → `2026-03-18` (Client dinner)
  - `3/24/2026` → `2026-03-24` (USB-C cables)
- **Standardized categories to Title Case:**
  - `office supplies` → `Office Supplies` (Printer paper)
  - `travel` → `Travel` (Taxi to client)
  - `software` → `Software` (Figma seats)
  - `furniture` → `Furniture` (Desk lamp)
  - `Office supplies` → `Office Supplies` (Pens)
- **Standardized amounts (removed `$`, commas, and surrounding quotes; padded to 2 decimals):**
  - `"$1,240.00"` → `1240.00` (Office chairs)
  - `48.5` → `48.50` (Printer paper)
  - `$212.40` → `212.40` (Team lunch on 2026-03-05 and 2026-03-25)
  - `149` → `149.00` (Zoom subscription)
  - `$36.20` → `36.20` (Taxi to client)
  - `"$184.00"` → `184.00` (Train tickets)
  - `$329.00` → `329.00` (Monitor)
  - `$22.75` → `22.75` (Notebooks)
  - `$90.00` → `90.00` (Figma seats)
  - `"$318.60"` → `318.60` (Client dinner)
  - `$64` → `64.00` (Desk lamp)
  - `"$412.00"` → `412.00` (Hotel (2 nights))
  - `$31.96` → `31.96` (USB-C cables)
  - `$9.80` → `9.80` (Pens)
  - `$58.00` → `58.00` (Taxi to airport)
  - `$96.00` → `96.00` (Notion subscription)
  - (`Coffee beans` at `27.99` required no changes.)

### Uncertainties / Items to Verify
- **Mixed slash date conventions:** The input mixes `MM/DD/YYYY` / `M/D/YY` (`03/04/2026`, `3/9/26`, `3/24/2026`) and `DD/MM/YYYY` (`10/03/2026`, `18/03/2026`), plus a yearless `Mar 13`. All resolved cleanly under the "every expense is from March 2026" rule (and match the sheet's chronological order), assuming none of the source entries were actually from April 3 or September 3 misdated into the wrong month.
- **Identical `Team lunch` amount on two dates:** Kept both `2026-03-05` and `2026-03-25` (`Team lunch,Meals,212.40`) per your instruction to keep repeated purchases on different dates, though the exact-to-the-cent match (`212.40`) is worth double-checking in case one date was entered in error.
