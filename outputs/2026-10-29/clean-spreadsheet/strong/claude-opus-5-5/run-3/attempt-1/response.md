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

**Removed exact duplicates (2 rows, so 20 rows became 18)**
- The second `2026-03-02, Office chairs, Furniture, $1,240.00`
- The second `03/04/2026, Printer paper, office supplies, 48.5`

**Dates changed to YYYY-MM-DD**
- `03/04/2026` → 2026-03-04
- `March 5 2026` → 2026-03-05
- `3/9/26` → 2026-03-09
- `10/03/2026` → 2026-03-10 (written day first)
- `Mar 13` → 2026-03-13 (year added)
- `18/03/2026` → 2026-03-18 (written day first)
- `3/24/2026` → 2026-03-24

**Categories changed to Title Case**
- `office supplies` / `Office supplies` → Office Supplies
- `travel` → Travel
- `software` → Software
- `furniture` → Furniture

**Amounts changed to plain numbers with two decimals**
- Removed `$` signs and the comma in `1,240.00`
- `48.5` → 48.50, `149` → 149.00, `$64` → 64.00

The rows stay in their original order, which is already in date order after cleanup.

## Things I wasn't sure about

1. **Dates written different ways.** The sheet mixes month-first (`3/24/2026`) and day-first (`18/03/2026`) dates. Because every expense is from March, I read each one so it lands in March. For `03/04/2026` and `3/9/26`, reading them day-first would give April 3 and September 3, so I used March 4 and March 9. If your source really means another month, those two rows need checking.
2. **"Mar 13" had no year.** I assumed 2026.
3. **"Team lunch" at $212.40 appears twice,** on March 5 and March 25. I kept both because the dates are different, as you asked. But the same description and exact amount could mean it was entered twice by mistake, so check it against the receipts.
4. **Possible duplicate printer paper.** If someone really bought printer paper twice on March 4 for the same amount, removing the second row would undercount. I treated it as a duplicate because the row was identical.
5. **Categories I left alone.** "Coffee beans" is under Meals, which may belong under something like Office Supplies, depending on your policy. I didn't change any category assignments, only their capitalization.