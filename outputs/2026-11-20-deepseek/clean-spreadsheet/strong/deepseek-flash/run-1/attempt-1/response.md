Cleaned CSV:

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

Changes made:

1. **Normalized dates to YYYY-MM-DD**, including:
   - `03/04/2026` → `2026-03-04`
   - `March 5 2026` → `2026-03-05`
   - `3/9/26` → `2026-03-09`
   - `10/03/2026` → `2026-03-10`
   - `Mar 13` → `2026-03-13`
   - `18/03/2026` → `2026-03-18`
   - `3/24/2026` → `2026-03-24`

2. **Removed two exact duplicate rows**:
   - Duplicate `Office chairs` row dated 2026-03-02.
   - Duplicate `Printer paper` row dated 2026-03-04.

3. **Kept both `Team lunch` rows** because they are on different dates: 2026-03-05 and 2026-03-25.

4. **Standardized categories to Title Case**, e.g. `office supplies` → `Office Supplies`, `travel` → `Travel`, `software` → `Software`, `furniture` → `Furniture`.

5. **Reformatted amounts** as plain numbers with two decimals: removed `$` and thousands separators, and padded values such as `48.5` → `48.50`, `149` → `149.00`, and `$64` → `64.00`.

Uncertainties:

- The sheet mixes date conventions. I interpreted `03/04/2026` as **2026-03-04** because all expenses are stated to be in March 2026. If it meant 3 April 2026, it would fall outside the requested scope.
- `Mar 13` had no year, so I assumed 2026.
- `Hotel (2 nights)` was kept as a single expense row rather than split into two nights.
- I treated “exact duplicate” as all four fields matching exactly; the repeated Team lunch was not removed because its date differs.