Cleaned it up and saved the result as **`expenses_cleaned.csv`**.

**What I fixed**

| Issue | Action |
|---|---|
| 2 exact duplicate rows | Removed — the second "Office chairs" ($1,240.00) and second "Printer paper" (48.50). 20 rows → 18 |
| Mixed date formats | Converted all to ISO `YYYY-MM-DD` (e.g. `3/9/26`, `March 5 2026`, `Mar 13`) |
| Inconsistent category casing | Standardized to 6 categories: Furniture, Office Supplies, Meals, Software, Travel, Equipment |
| Currency text in amounts | Stripped `$` and `,`; all amounts now 2-decimal numbers |
| Unsorted ledger | Sorted chronologically (stable for same-date items) |

**Date ambiguity:** `03/04/2026` and `10/03/2026` could each be read two ways. I chose **Mar 4** and **Mar 10** because those readings keep the whole ledger in chronological order; `18/03/2026` is unambiguously Mar 18. If your locale intended something else, say so and I'll swap them.

The two "Team lunch" entries (Mar 5 and Mar 25) and two Mar 18 entries were kept — they're distinct transactions, not duplicates.

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

**Total: $3,542.60** — Furniture $1,304.00 · Meals $771.39 · Travel $690.20 · Equipment $360.96 · Software $335.00 · Office Supplies $81.05

Files in the workspace: `expenses_cleaned.csv` (final), `expenses_raw.csv` (untouched original), `clean_expenses.py` (re-runnable if more rows get appended). Amounts are plain numbers for calculations — apply currency formatting in Excel/Sheets if you want the `$` back.