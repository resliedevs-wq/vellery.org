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

**Changes**

- **Removed 2 exact duplicates:** the second "Office chairs" row (2026-03-02, $1,240.00) and the second "Printer paper" row (03/04/2026, 48.5). The sheet had 20 rows and now has 18.
- **Dates converted to YYYY-MM-DD:**
  - `03/04/2026` → 2026-03-04
  - `March 5 2026` → 2026-03-05
  - `3/9/26` → 2026-03-09
  - `10/03/2026` → 2026-03-10
  - `Mar 13` → 2026-03-13
  - `18/03/2026` → 2026-03-18
  - `3/24/2026` → 2026-03-24
- **Amounts:** removed `$` and commas and added two decimals (e.g., `$1,240.00` → `1240.00`, `48.5` → `48.50`, `149` → `149.00`).
- **Categories in Title Case:** `office supplies` and `Office supplies` → `Office Supplies`; `furniture` → `Furniture`; `software` → `Software`; `travel` → `Travel`.
- **Kept as separate rows:** the two "Team lunch" entries at $212.40 (2026-03-05 and 2026-03-25) and the two "Travel" taxi rows, since they fall on different dates.

**Uncertain**

- **Ambiguous dates:** I read `03/04/2026` as March 4 and `10/03/2026` as March 10. The sheet also contains `18/03/2026` (day-first) and `3/24/2026` (month-first), so the format isn't consistent. Since every expense is from March, I took the March reading in both cases.
- **Missing or short years:** `Mar 13` had no year and `3/9/26` had a two-digit year. I assumed 2026 for both.
- **Duplicates that may be real:** the removed chairs and paper could have been multiple units bought at once (for example, two chairs or two packs of paper). If so, the removal is wrong and those rows should go back in.
- **Team lunch:** the two $212.40 entries may be a double entry rather than two lunches. I kept both because you asked to keep repeated purchases on different dates.