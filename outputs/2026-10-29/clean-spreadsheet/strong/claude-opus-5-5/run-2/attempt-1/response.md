I deleted 2 exact duplicate rows, which leaves 18. Converting the dates also put the rows in date order, so I didn't need to re-sort them.

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

**Duplicates removed (2)**
- The second copy of `2026-03-02, Office chairs, Furniture, $1,240.00`.
- The second copy of `03/04/2026, Printer paper, office supplies, 48.5`.

**Dates changed to YYYY-MM-DD (8)**
- `03/04/2026` → 2026-03-04
- `March 5 2026` → 2026-03-05
- `3/9/26` → 2026-03-09
- `10/03/2026` → 2026-03-10
- `Mar 13` → 2026-03-13
- `18/03/2026` → 2026-03-18
- `3/24/2026` → 2026-03-24

**Categories changed to Title Case (5)**
- `office supplies` → Office Supplies (Printer paper)
- `travel` → Travel (Taxi to client)
- `software` → Software (Figma seats)
- `furniture` → Furniture (Desk lamp)
- `Office supplies` → Office Supplies (Pens)

**Amounts**
- Removed `$` signs and thousands commas, e.g. `"$1,240.00"` → 1240.00.
- Added two decimals where they were missing: `48.5` → 48.50, `149` → 149.00, `$64` → 64.00.

**Kept on purpose**
- Team lunch, $212.40, appears on 2026-03-05 and again on 2026-03-25. The dates differ, so I kept both.

## Things I wasn't sure about

1. **Mixed date formats.** `03/04/2026` and `3/9/26` are month-first. `10/03/2026` and `18/03/2026` are day-first. I could only read them correctly because every expense is from March. Without that rule, `03/04/2026` could be April 3 and `10/03/2026` could be October 3. If this sheet combines exports from different sources, check the dates there.
2. **`Mar 13` had no year.** I assumed 2026 because of your March 2026 rule.
3. **The two removed duplicates might be real purchases.** Two identical $1,240 chair orders or paper orders on the same day are possible. I treated them as accidental double entries, as you asked. If they were real, the total is $1,288.50 too low.
4. **The two Team lunch entries** have the same amount 20 days apart. That could be a regular lunch or a double entry with a wrong date.
5. **Coffee beans is under Meals.** It might belong under Office Supplies or a pantry category. I left it unchanged.
6. **Currency.** I assumed every amount is in the same currency, since some had `$` and some didn't.