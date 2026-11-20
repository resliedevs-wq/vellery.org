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

1. **Removed Exact Duplicates (2 rows removed):**
   - Removed the duplicate `2026-03-02,Office chairs,Furniture,"$1,240.00"` (originally row 4).
   - Removed the duplicate `03/04/2026,Printer paper,office supplies,48.5` (originally row 11).

2. **Standardized Dates to `YYYY-MM-DD` (7 rows updated):**
   - `03/04/2026` $\rightarrow$ `2026-03-04` (Printer paper)
   - `March 5 2026` $\rightarrow$ `2026-03-05` (Team lunch)
   - `3/9/26` $\rightarrow$ `2026-03-09` (Zoom subscription)
   - `10/03/2026` $\rightarrow$ `2026-03-10` (Train tickets)
   - `Mar 13` $\rightarrow$ `2026-03-13` (Monitor — added year `2026`)
   - `18/03/2026` $\rightarrow$ `2026-03-18` (Client dinner)
   - `3/24/2026` $\rightarrow$ `2026-03-24` (USB-C cables)

3. **Converted Categories to Title Case (5 rows updated):**
   - `office supplies` $\rightarrow$ `Office Supplies` (2026-03-04, Printer paper)
   - `travel` $\rightarrow$ `Travel` (2026-03-10, Taxi to client)
   - `software` $\rightarrow$ `Software` (2026-03-18, Figma seats)
   - `furniture` $\rightarrow$ `Furniture` (2026-03-20, Desk lamp)
   - `Office supplies` $\rightarrow$ `Office Supplies` (2026-03-27, Pens)

4. **Formatted Amounts to Plain Numbers with Two Decimals (17 rows updated):**
   - Stripped `$`, commas, and surrounding quotes (`"$1,240.00"` $\rightarrow$ `1240.00`, `"$184.00"` $\rightarrow$ `184.00`, `"$318.60"` $\rightarrow$ `318.60`, `"$412.00"` $\rightarrow$ `412.00`, plus all `$`-prefixed values).
   - Added trailing decimal zeroes where missing: `48.5` $\rightarrow$ `48.50`, `149` $\rightarrow$ `149.00`, `$64` $\rightarrow$ `64.00`.
   - (`27.99` on 2026-03-12 was already formatted properly.)

---

### Notes & Potential Ambiguities

- **Mixed `MM/DD/YYYY` and `DD/MM/YYYY` Date Formats:** The sheet mixes US (`3/24/2026`) and day-first (`10/03/2026`, `18/03/2026`) formats. For `03/04/2026` and `3/9/26`, the day and month could be ambiguous in isolation, but your rule that every expense is from March 2026 (along with chronological ordering in the sheet) confirms they are **March 4 (`2026-03-04`)** and **March 9 (`2026-03-09`)**.
- **Repeated `Team lunch` for the Exact Same Amount (`212.40`):** `Team lunch` appears on both `2026-03-05` and `2026-03-25` for the exact same down-to-the-cent amount (`$212.40`). Both rows were kept per your instruction to keep repeated purchases on different dates, though in practice an identical restaurant bill down to the cent might warrant verifying whether it was a fixed catering order or a duplicate receipt logged under the wrong date.
