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

**Changes made**
- Converted non-ISO dates:
  - `03/04/2026` → `2026-03-04`
  - `March 5 2026` → `2026-03-05`
  - `3/9/26` → `2026-03-09`
  - `10/03/2026` → `2026-03-10`
  - `Mar 13` → `2026-03-13`
  - `18/03/2026` → `2026-03-18`
  - `3/24/2026` → `2026-03-24`
- Removed 2 duplicate rows:
  - One exact duplicate of the March 2 Office chairs row.
  - One Printer paper row for March 4; the two raw rows differed in category capitalization and amount formatting, but matched after normalization.
- Standardized categories to Title Case:
  - `office supplies` → `Office Supplies`
  - `travel` → `Travel`
  - `software` → `Software`
  - `furniture` → `Furniture`
- Converted all amounts to plain two-decimal numbers, removing `$` and commas and padding values such as `48.5` → `48.50`, `149` → `149.00`, and `$64` → `64.00`.
- Kept both Team lunch rows because they are on different dates: March 5 and March 25.
- Preserved the original row order after removing duplicates.

**Unsure about**
- The sheet mixes date formats. I interpreted every ambiguous date as March because you said every expense is from March 2026. In particular, `03/04/2026` was treated as March 4, not April 3, and `10/03/2026` as March 10, not October 3.
- The Printer paper rows were not byte-for-byte identical before cleanup. I treated them as duplicates because they describe the same date, vendor item, category, and amount. If “exact duplicate” means only identical raw text, that row would need to be restored.
- Currency was not specified beyond the dollar signs, so I treated all amounts as the same currency.