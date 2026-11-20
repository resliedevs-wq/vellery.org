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

1. **Standardized Dates to `YYYY-MM-DD`:**
   - `03/04/2026` → `2026-03-04` (Printer paper)
   - `March 5 2026` → `2026-03-05` (Team lunch)
   - `3/9/26` → `2026-03-09` (Zoom subscription)
   - `10/03/2026` → `2026-03-10` (Train tickets)
   - `Mar 13` → `2026-03-13` (Monitor — added year `2026`)
   - `18/03/2026` → `2026-03-18` (Client dinner)
   - `3/24/2026` → `2026-03-24` (USB-C cables)

2. **Removed Exact Duplicate Rows (2 rows):**
   - Removed duplicate `2026-03-02,Office chairs,Furniture,"$1,240.00"` (originally row 4).
   - Removed duplicate `03/04/2026,Printer paper,office supplies,48.5` (originally row 11).
   - *Kept* the second `Team lunch` (`2026-03-25`) because it occurred on a different date than the `2026-03-05` entry.

3. **Converted Categories to Title Case:**
   - `office supplies` → `Office Supplies` (2026-03-04, Printer paper)
   - `travel` → `Travel` (2026-03-10, Taxi to client)
   - `software` → `Software` (2026-03-18, Figma seats)
   - `furniture` → `Furniture` (2026-03-20, Desk lamp)
   - `Office supplies` → `Office Supplies` (2026-03-27, Pens)

4. **Formatted Amounts (removed `$`, commas, and quotes; padded to 2 decimal places):**
   - `"$1,240.00"` → `1240.00` (2026-03-02, Office chairs)
   - `48.5` → `48.50` (2026-03-04, Printer paper)
   - `$212.40` → `212.40` (2026-03-05 & 2026-03-25, Team lunch)
   - `149` → `149.00` (2026-03-09, Zoom subscription)
   - `$36.20` → `36.20` (2026-03-10, Taxi to client)
   - `"$184.00"` → `184.00` (2026-03-10, Train tickets)
   - `$329.00` → `329.00` (2026-03-13, Monitor)
   - `$22.75` → `22.75` (2026-03-15, Notebooks)
   - `$90.00` → `90.00` (2026-03-18, Figma seats)
   - `"$318.60"` → `318.60` (2026-03-18, Client dinner)
   - `$64` → `64.00` (2026-03-20, Desk lamp)
   - `"$412.00"` → `412.00` (2026-03-22, Hotel (2 nights))
   - `$31.96` → `31.96` (2026-03-24, USB-C cables)
   - `$9.80` → `9.80` (2026-03-27, Pens)
   - `$58.00` → `58.00` (2026-03-30, Taxi to airport)
   - `$96.00` → `96.00` (2026-03-31, Notion subscription)

---

### Notes & Potential Ambiguities

- **Mixed `MM/DD/YYYY` and `DD/MM/YYYY` Date Formats:** The source data mixes US (`03/04/2026`, `3/9/26`, `3/24/2026`) and European (`10/03/2026`, `18/03/2026`) slash-date formats. On their own, `03/04/2026`, `3/9/26`, and `10/03/2026` could be read two ways, but the rule that **all expenses are from March 2026** (confirmed by the chronological ordering of the rows) resolves them unambiguously to `2026-03-04`, `2026-03-09`, and `2026-03-10`.
- **Missing Year on `Mar 13`:** Inferred `2026-03-13` based on the instruction that every expense is from March 2026.
- **Identical `Team lunch` Amounts (`212.40` on `2026-03-05` and `2026-03-25`):** Both rows were kept per the rule to keep repeated purchases on different dates, though in practice an identical meal total down to the cent on two different dates may be worth verifying against receipts in case one was an accidental duplicate with a mistyped date.
