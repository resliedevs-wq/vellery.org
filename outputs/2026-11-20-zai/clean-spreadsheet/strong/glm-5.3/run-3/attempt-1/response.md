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

**Dates** — normalized five non-standard formats to YYYY-MM-DD:
- `03/04/2026` → 2026-03-04, `3/9/26` → 2026-03-09, `10/03/2026` → 2026-03-10, `Mar 13` → 2026-03-13, `18/03/2026` → 2026-03-18, `3/24/2026` → 2026-03-24

**Duplicates removed** (2 rows):
- Office chairs, 2026-03-02, $1,240.00 (appeared twice)
- Printer paper, 2026-03-04, $48.50 (appeared twice)

**Categories** — Title Cased: `office supplies`/`Office supplies` → Office Supplies, `travel` → Travel, `software` → Software, `furniture` → Furniture

**Amounts** — stripped `$` and thousands commas; padded to two decimals (`48.5` → 48.50, `149` → 149.00, `$64` → 64.00, `$1,240.00` → 1240.00, etc.)

**Kept as-is:** Team lunch $212.40 appears on 03-05 and 03-25 — same amount, different dates, so both kept per your rule.

## Things I wasn't sure about

1. **Mixed date conventions.** The sheet uses both month-first (`3/24/2026`, where 24 can't be a month) and day-first (`18/03/2026`, where 18 can't be a month). For the ambiguous ones I relied on your "everything is March 2026" rule: `03/04/2026` → March 4 (day-first would make it April 3) and `3/9/26` → March 9 (day-first would make it September). Worth a sanity check against receipts if you have them.
2. **Team lunch duplicate?** Identical description *and* identical amount ($212.40) on two dates is a little suspicious — it could be one real expense with a date typo rather than two lunches. I kept both as instructed, but flagging it.
3. **Two March 10 travel rows** (Taxi to client + Train tickets). These are clearly different expenses, so both kept — just noting they're not duplicates despite sharing a date.
4. **Row order.** I preserved the original order (already chronological after deduping); I didn't re-sort, in case order matters to you.