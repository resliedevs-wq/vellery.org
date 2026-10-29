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

- **Removed 2 exact duplicates:** the second "2026-03-02, Office chairs" row and the second "03/04/2026, Printer paper" row. The input had 20 rows; the output has 18.
- **Kept both "Team lunch" rows** (2026-03-05 and 2026-03-25) because they fall on different dates.
- **Converted dates to YYYY-MM-DD:** `03/04/2026` → 2026-03-04, `March 5 2026` → 2026-03-05, `3/9/26` → 2026-03-09, `10/03/2026` → 2026-03-10, `18/03/2026` → 2026-03-18, `Mar 13` → 2026-03-13, `3/24/2026` → 2026-03-24.
- **Fixed category case:** `office supplies` → Office Supplies, `furniture` → Furniture, `software` → Software, `travel` → Travel. Meals and Equipment were already correct.
- **Normalized amounts:** removed `$` and commas, and added two decimals (`48.5` → 48.50, `149` → 149.00, `$64` → 64.00, `$1,240.00` → 1240.00).

**Things I wasn't sure about**

- **Ambiguous dates:** `03/04/2026` could be March 4 or April 3, and `10/03/2026` could be March 10 or October 3. I read both as March because you said every expense is from March 2026. That makes them DD/MM and MM/DD respectively. The `18/03/2026` row shows the sheet uses DD/MM in places, which supports this reading. If any of these are wrong, the dates need correcting.
- **Possible duplicate purchases:** the two Team lunch entries have the same amount ($212.40) on different dates. I kept both, but they may be the same charge logged twice. Check them against receipts.
- **Printer paper:** I removed the second copy as an exact duplicate. If you actually bought paper twice on March 4 at the same price, that second purchase was dropped in error.