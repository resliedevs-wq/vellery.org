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

- **Removed 2 exact duplicates:**
  - The second "Office chairs" row (2026-03-02, $1,240.00).
  - The second "Printer paper" row (03/04/2026, 48.5).
- **Converted dates to YYYY-MM-DD:**
  - `03/04/2026` → 2026-03-04
  - `March 5 2026` → 2026-03-05
  - `3/9/26` → 2026-03-09
  - `10/03/2026` → 2026-03-10
  - `Mar 13` → 2026-03-13
  - `18/03/2026` → 2026-03-18
  - `3/24/2026` → 2026-03-24
- **Title-cased categories:** `office supplies` and `Office supplies` → Office Supplies; `furniture` → Furniture; `software` → Software; `travel` → Travel.
- **Normalized amounts:** removed `$` and thousands commas, and added two decimals (`$1,240.00` → 1240.00, `$64` → 64.00, `149` → 149.00, etc.).
- **Kept both "Team lunch" rows** because they fall on different dates (03-05 and 03-25).
- **Result:** 20 rows in, 18 rows out.

**Things I wasn't sure about**

- **Ambiguous slash dates:** I read them as month-first where that gives a March date, and day-first otherwise. `03/04/2026` could be April 3, but that's outside March, so I used March 4. `10/03/2026` could be October 3, so I used March 10. If your source is day-first throughout, `03/04/2026` would be wrong. Please check this one.
- **Missing year:** "Mar 13" had no year. I assumed 2026, since you said every expense is from March 2026.
- **Possible double entry:** Both "Team lunch" rows are $212.40. I kept them because the dates differ, but one could be a mis-dated copy. Worth a quick check against receipts.
- **Same-day duplicate:** The two "Printer paper" rows were identical, including the date. I removed one as you asked, but if you bought paper twice that day, the second purchase was lost.