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

1. **Duplicate Rows Removed (2 rows):**
   - Removed duplicate `2026-03-02,Office chairs,Furniture,"$1,240.00"` (originally row 4).
   - Removed duplicate `03/04/2026,Printer paper,office supplies,48.5` (originally row 11).

2. **Dates Standardized to `YYYY-MM-DD` (7 rows):**
   - `03/04/2026` (Printer paper) $\rightarrow$ `2026-03-04`
   - `March 5 2026` (Team lunch) $\rightarrow$ `2026-03-05`
   - `3/9/26` (Zoom subscription) $\rightarrow$ `2026-03-09`
   - `10/03/2026` (Train tickets) $\rightarrow$ `2026-03-10`
   - `Mar 13` (Monitor) $\rightarrow$ `2026-03-13`
   - `18/03/2026` (Client dinner) $\rightarrow$ `2026-03-18`
   - `3/24/2026` (USB-C cables) $\rightarrow$ `2026-03-24`

3. **Categories Converted to Title Case (5 rows):**
   - `office supplies` (Printer paper, `2026-03-04`) $\rightarrow$ `Office Supplies`
   - `travel` (Taxi to client, `2026-03-10`) $\rightarrow$ `Travel`
   - `software` (Figma seats, `2026-03-18`) $\rightarrow$ `Software`
   - `furniture` (Desk lamp, `2026-03-20`) $\rightarrow$ `Furniture`
   - `Office supplies` (Pens, `2026-03-27`) $\rightarrow$ `Office Supplies`

4. **Amounts Formatted as Plain Numbers with Two Decimals (17 rows):**
   - Stripped `$`, commas, and surrounding quotes from `"$1,240.00"` $\rightarrow$ `1240.00`, `"$184.00"` $\rightarrow$ `184.00`, `"$318.60"` $\rightarrow$ `318.60`, and `"$412.00"` $\rightarrow$ `412.00`.
   - Added trailing decimal zeroes to `48.5` $\rightarrow$ `48.50`, `149` $\rightarrow$ `149.00`, and `$64` $\rightarrow$ `64.00`.
   - Stripped `$` from `$212.40` (both `2026-03-05` and `2026-03-25`), `$36.20`, `$329.00`, `$22.75`, `$90.00`, `$31.96`, `$9.80`, `$58.00`, and `$96.00`.
   - (`2026-03-12,Coffee beans,Meals,27.99` required no changes.)

---

### Notes & Potential Ambiguities

- **Mixed `MM/DD/YYYY` and `DD/MM/YYYY` slash formats:** The input mixes US (`03/04/2026`, `3/9/26`, `3/24/2026`) and day-first (`10/03/2026`, `18/03/2026`) date formats. Because you specified that every expense is from March 2026 (and the rows are in chronological order), `03/04/2026` was parsed as March 4 (`2026-03-04`) and `10/03/2026` as March 10 (`2026-03-10`), rather than April 3 or October 3.
- **Missing year on `Mar 13`:** Inferred as `2026-03-13` based on the rule that all expenses are from March 2026.
- **Identical `Team lunch` amounts on two dates (`2026-03-05` and `2026-03-25`):** Both rows are for `Team lunch,Meals` with the exact same amount (`212.40`). Both were kept per your rule to keep repeated purchases on different dates, though in practice an identical restaurant total to the cent could also be a copy-paste error worth double-checking against receipts.
