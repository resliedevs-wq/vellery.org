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

* **Duplicates Removed (2 rows):**
  * Row 4 (`2026-03-02,Office chairs,Furniture,"$1,240.00"`) — exact duplicate of Row 1.
  * Row 11 (`03/04/2026,Printer paper,office supplies,48.5`) — exact duplicate of Row 2.
* **Dates Standardized to `YYYY-MM-DD` (7 rows):**
  * Row 2: `03/04/2026` $\rightarrow$ `2026-03-04`
  * Row 3: `March 5 2026` $\rightarrow$ `2026-03-05`
  * Row 5: `3/9/26` $\rightarrow$ `2026-03-09`
  * Row 7: `10/03/2026` $\rightarrow$ `2026-03-10`
  * Row 9: `Mar 13` $\rightarrow$ `2026-03-13` (added year `2026`)
  * Row 13: `18/03/2026` $\rightarrow$ `2026-03-18`
  * Row 16: `3/24/2026` $\rightarrow$ `2026-03-24`
* **Categories Converted to Title Case (5 rows):**
  * Row 2: `office supplies` $\rightarrow$ `Office Supplies`
  * Row 6: `travel` $\rightarrow$ `Travel`
  * Row 12: `software` $\rightarrow$ `Software`
  * Row 14: `furniture` $\rightarrow$ `Furniture`
  * Row 18: `Office supplies` $\rightarrow$ `Office Supplies`
* **Amounts Formatted (17 of 18 kept rows):**
  * Stripped `$`, `,`, and surrounding quotes from rows 1, 3, 6, 7, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, and 20.
  * Added trailing decimal zeroes to rows 2 (`48.5` $\rightarrow$ `48.50`), 5 (`149` $\rightarrow$ `149.00`), and 14 (`$64` $\rightarrow$ `64.00`).
  * *(Row 8 `2026-03-12,Coffee beans,Meals,27.99` required no changes.)*

### Things to Note / Potential Ambiguities

1. **Mixed `MM/DD/YYYY` and `DD/MM/YYYY` Date Formats:** The sheet mixes US (`3/24/2026`) and international (`10/03/2026`, `18/03/2026`) slash formats. Because every expense is from March 2026 (and the sheet is in chronological order), `03/04/2026` (Row 2) and `3/9/26` (Row 5) were treated as `MM/DD` (**March 4** and **March 9**) rather than `DD/MM` (April 3 and September 3).
2. **Repeated `Team lunch` for the Exact Same Amount (`212.40`):** Row 3 (`2026-03-05`) and Row 17 (`2026-03-25`) are both for `Team lunch` under `Meals` for exactly `$212.40`. Per your instructions to keep repeated purchases on different dates, both rows were kept, though identical restaurant totals down to the cent can sometimes indicate an accidental duplicate entry under a different date.
