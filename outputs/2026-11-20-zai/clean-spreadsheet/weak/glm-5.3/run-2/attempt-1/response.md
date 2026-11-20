Cleaned up and saved to `expenses_clean.csv` (19 rows → 18):

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

What was fixed:

- **Dates** — normalized everything to ISO `YYYY-MM-DD`, including `03/04/2026`, `March 5 2026`, `3/9/26`, `Mar 13`, and the two day-first entries (`10/03/2026`, `18/03/2026` — day-first is the only valid reading since 18 can't be a month). Sorted by date.
- **Duplicates removed** — the second *Office chairs* (2026-03-02) and second *Printer paper* (2026-03-04) rows. Kept both *Team lunch* entries since they're on different dates.
- **Categories** — standardized to Title Case (*office supplies* → *Office Supplies*, etc.).
- **Amounts** — stripped `$` and thousands commas, padded to two decimals (`48.5` → `48.50`, `149` → `149.00`) so they import as numbers rather than text.

One judgment call to flag: `03/04/2026` is ambiguous — I read it as March 4 (US style), consistent with `3/24/2026`. If it was actually April 3, let me know and I'll flip it.