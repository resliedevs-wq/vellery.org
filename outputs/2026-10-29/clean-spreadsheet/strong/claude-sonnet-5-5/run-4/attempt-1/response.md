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

## Changes made

**Dates (all converted to YYYY-MM-DD)**
- `03/04/2026` → `2026-03-04`
- `March 5 2026` → `2026-03-05`
- `3/9/26` → `2026-03-09`
- `10/03/2026` → `2026-03-10` (read as day/month)
- `Mar 13` → `2026-03-13` (year added)
- `18/03/2026` → `2026-03-18` (read as day/month)
- `3/24/2026` → `2026-03-24`

**Duplicates removed (2 rows)**
- The second "Office chairs" row on 2026-03-02 was identical to the first.
- The second "Printer paper" row on 03/04/2026 was identical to the first.
- I kept both "Team lunch" rows (03-05 and 03-25) because the dates differ.

**Categories (Title Case)**
- `office supplies` → `Office Supplies` (3 rows)
- `travel` → `Travel`
- `software` → `Software`
- `furniture` → `Furniture`

**Amounts**
- Removed `$` and thousands separators, and padded to two decimals. For example, `"$1,240.00"` became `1240.00`, `48.5` became `48.50`, `149` became `149.00`, and `$64` became `64.00`.

The 20 input rows became 18. I left the rows in their original order, which was already chronological.

## Things I wasn't sure about

- **Ambiguous dates:** `03/04/2026` could be 3 April or 4 March, and `3/9/26` could be 3 September or 9 March. Because every expense is from March 2026, I read both as month/day, which gives March 4 and March 9. I made the same assumption for `10/03/2026` and `18/03/2026`, where only day/month gives a March date. The sheet mixes US and non-US formats, so check these against your receipts.
- **Duplicate detection:** I compared rows after cleaning, so the duplicate rows were identical in every field. The chairs pair differed only in formatting, but it was the same in value, so I treated it as a duplicate.
- **Possible real repeats:** If you actually bought two sets of chairs or two reams of paper on the same day, those removals would be wrong. Nothing in the sheet suggests that.
- **Mar 13:** The year was missing. I assumed 2026, as you said.