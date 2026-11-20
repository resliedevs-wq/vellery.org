Here's the cleaned CSV (18 rows — down from 20):

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

**Dates normalized to YYYY-MM-DD:**
- `03/04/2026` → 2026-03-04 (month-first)
- `March 5 2026` → 2026-03-05
- `3/9/26` → 2026-03-09
- `10/03/2026` → 2026-03-10 (day-first — see notes)
- `Mar 13` → 2026-03-13
- `18/03/2026` → 2026-03-18 (day-first)
- `3/24/2026` → 2026-03-24

**Duplicates removed (2 rows):**
- Second `Office chairs` row (identical to the 2026-03-02 row)
- Second `Printer paper` row (identical to the 03/04/2026 row)

**Kept on purpose:**
- Both `Team lunch` rows (2026-03-05 and 2026-03-25) — same description and amount, but different dates, so they count as repeated purchases per your rule.

**Categories title-cased:**
- `office supplies` → Office Supplies (2 rows), `travel` → Travel, `software` → Software (1 row), `furniture` → Furniture (1 row); `Office supplies`/`Office Supplies` casing unified.

**Amounts cleaned:**
- Stripped `$` and thousands commas, removed quote wrapping, padded to two decimals (`48.5` → 48.50, `149` → 149.00, `64` → 64.00).

**Left alone:** descriptions (as-is, including `Hotel (2 nights)`) and original row order.

## Things I wasn't sure about

- **`10/03/2026`** is ambiguous: day-first reads March 10; month-first would be October 3, which falls outside March. I used March 10 — conveniently, even if the clerk *meant* to type `03/10/2026`, it lands on the same date. The source mixes month-first and day-first styles, so it's worth confirming the convention if more of this person's data comes through.
- **The two Team lunch entries** are identical in description and amount ($212.40). I kept both since the dates differ, but if one was entered with a wrong date, it would be a duplicate — you may want to verify against receipts.
- **`18/03/2026`** had to be day-first (there's no month 18), so that one's unambiguous.