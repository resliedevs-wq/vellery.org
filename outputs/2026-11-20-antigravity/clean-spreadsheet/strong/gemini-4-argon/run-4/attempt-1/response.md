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

1. **Dates Standardized to `YYYY-MM-DD`**:
   - `03/04/2026` (Printer paper) $\rightarrow$ `2026-03-04`
   - `March 5 2026` (Team lunch) $\rightarrow$ `2026-03-05`
   - `3/9/26` (Zoom subscription) $\rightarrow$ `2026-03-09`
   - `10/03/2026` (Train tickets) $\rightarrow$ `2026-03-10`
   - `Mar 13` (Monitor) $\rightarrow$ `2026-03-13`
   - `18/03/2026` (Client dinner) $\rightarrow$ `2026-03-18`
   - `3/24/2026` (USB-C cables) $\rightarrow$ `2026-03-24`

2. **Exact Duplicates Removed**:
   - Removed the second occurrence of `2026-03-02,Office chairs,Furniture,"$1,240.00"` (row 4).
   - Removed the second occurrence of `03/04/2026,Printer paper,office supplies,48.5` (row 11).
   - Kept both `Team lunch` entries (`2026-03-05` and `2026-03-25`) as they occurred on different dates.

3. **Categories Converted to Title Case**:
   - `office supplies` (Printer paper) $\rightarrow$ `Office Supplies`
   - `travel` (Taxi to client) $\rightarrow$ `Travel`
   - `software` (Figma seats) $\rightarrow$ `Software`
   - `furniture` (Desk lamp) $\rightarrow$ `Furniture`
   - `Office supplies` (Pens) $\rightarrow$ `Office Supplies`

4. **Amounts Formatted as Plain Numbers with Two Decimals**:
   - Stripped `$`, commas, and surrounding quotes from `"$1,240.00"` $\rightarrow$ `1240.00`, `"$184.00"` $\rightarrow$ `184.00`, `"$318.60"` $\rightarrow$ `318.60`, and `"$412.00"` $\rightarrow$ `412.00`.
   - Stripped `$` from `$212.40` (x2), `$36.20`, `$329.00`, `$22.75`, `$90.00`, `$31.96`, `$9.80`, `$58.00`, and `$96.00`.
   - Added trailing decimal zeroes to `48.5` $\rightarrow$ `48.50`, `149` $\rightarrow$ `149.00`, and `$64` $\rightarrow$ `64.00` (also removed `$`).

### Things to Note / Potential Ambiguities

- **Mixed `MM/DD/YYYY` and `DD/MM/YYYY` formats**: The sheet mixes US (`03/04/2026`, `3/9/26`, `3/24/2026`) and day-first (`10/03/2026`, `18/03/2026`) slash-separated dates. Normally `03/04/2026`, `3/9/26`, and `10/03/2026` could be ambiguous, but your rule that every expense is from March 2026 makes the intended day and month unambiguous (`2026-03-04`, `2026-03-09`, and `2026-03-10`).
- **Missing year on `Mar 13`**: Inferred as `2026-03-13` based on the March 2026 constraint.
- **Identical `Team lunch` amount (`$212.40`) on `2026-03-05` and `2026-03-25`**: Kept per your instruction to keep repeated purchases on different dates, though in practice an identical Down-to-the-cent restaurant bill on two different dates might warrant a receipt check to ensure it wasn't a copy-paste error.
