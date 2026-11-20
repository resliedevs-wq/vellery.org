Here is the cleaned CSV (18 unique rows, down from 20):

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

### What was cleaned
- **Removed 2 exact duplicates:**
  - `2026-03-02,Office chairs,Furniture,"$1,240.00"` (appeared twice)
  - `03/04/2026,Printer paper,office supplies,48.5` (appeared twice)
- **Standardized dates to `YYYY-MM-DD`:** Normalized mixed US/EU/text formats (`03/04/2026`, `March 5 2026`, `3/9/26`, `10/03/2026`, `Mar 13`, `18/03/2026`, `3/24/2026`).
- **Standardized categories to Title Case:** `office supplies` / `Office supplies` → `Office Supplies`, `travel` → `Travel`, `software` → `Software`, `furniture` → `Furniture`.
- **Normalized `Amount` to plain 2-decimal numbers:** Stripped `$`, thousands commas, and unnecessary quotes, and padded decimals (`48.5` → `48.50`, `149` → `149.00`, `$64` → `64.00`) so the column imports cleanly as numeric values.

### Items to verify
- **Ambiguous dates inferred from row order (March 2026):**
  - `03/04/2026` → assumed `2026-03-04` (US `MM/DD/YYYY`, rather than April 3).
  - `10/03/2026` → assumed `2026-03-10` (EU `DD/MM/YYYY`, rather than October 3).
  - `Mar 13` → assumed year `2026`.
- **Possible near-duplicate:** `Team lunch` (`Meals`, `212.40`) appears on both `2026-03-05` and `2026-03-25`. Kept both since the dates differ, though the identical dollar amount is worth checking.
