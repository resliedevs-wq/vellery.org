Here is the cleaned CSV:

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
- Normalized dates to `YYYY-MM-DD`:
  - `03/04/2026` → `2026-03-04`
  - `March 5 2026` → `2026-03-05`
  - `3/9/26` → `2026-03-09`
  - `10/03/2026` → `2026-03-10`
  - `Mar 13` → `2026-03-13`
  - `18/03/2026` → `2026-03-18`
  - `3/24/2026` → `2026-03-24`
- Removed 2 exact duplicate rows:
  - The second “Office chairs” row dated `2026-03-02`.
  - The second “Printer paper” row dated `2026-03-04`.
- Converted categories to Title Case: `office supplies` / `Office supplies` → `Office Supplies`; `travel` → `Travel`; `software` → `Software`; `furniture` → `Furniture`.
- Reformatted all amounts as plain two-decimal numbers, removing `$` and thousands separators—for example, `"$1,240.00"` → `1240.00`, `48.5` → `48.50`, and `149` → `149.00`.
- Retained both “Team lunch” entries because they are on different dates.
- Final row count: **18** (down from 20).

**Uncertainties / assumptions**
- The mixed date formats are ambiguous. I interpreted `03/04/2026` as **March 4** and `10/03/2026` as **March 10** because every expense is stated to be from March 2026. Under a different date convention, these could mean April 3 and October 3.
- `Mar 13` had no year; I assumed **2026**.
- I did not reclassify any descriptions. For example, `Coffee beans` remains categorized as `Meals`.