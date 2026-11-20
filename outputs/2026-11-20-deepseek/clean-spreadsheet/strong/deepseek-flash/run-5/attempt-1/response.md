Cleaned CSV (18 rows) — also saved to `march_2026_expenses_clean.csv`:

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
- Standardized every date to `YYYY-MM-DD`, including `03/04/2026`, `3/9/26`, `Mar 13`, and `March 5 2026`.
- Removed 2 exact duplicate rows:
  - `2026-03-02 / Office chairs / Furniture / $1,240.00`
  - `03/04/2026 / Printer paper / office supplies / 48.5`
- Kept both Team lunch entries (March 5 and March 25) since they are on different dates.
- Normalized all categories to Title Case: `travel` → `Travel`, `software` → `Software`, `furniture` → `Furniture`, `office supplies`/`Office supplies` → `Office Supplies`.
- Removed `$` and thousands separators and formatted all amounts to two decimals: e.g. `"$1,240.00"` → `1240.00`, `48.5` → `48.50`, `149` → `149.00`, `64` → `64.00`.
- Preserved chronological order. Total: **$3,542.60**.

**Uncertainties**
- **Mixed date formats:** `03/04/2026` is ambiguous between March 4 (US) and April 3 (international). I used **March 4** because April falls outside March 2026. However, `10/03/2026` and `18/03/2026` can only be day/month (March 10 and March 18), so the source mixes US and international formats.
- `Mar 13` had no year; assumed **2026** based on the March 2026 constraint.
- `3/9/26` uses a two-digit year; assumed **2026**.
- I did not recategorize anything (e.g., `Coffee beans` remains `Meals`, `Monitor` remains `Equipment`), since only casing was requested.
- I left `Hotel (2 nights)` as one line without splitting out per-night costs.
- I assumed rows with the same description and amount but different dates are legitimate separate purchases.