Cleaned and saved to `expenses_clean.csv`:

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

**What I fixed:**
- **Dates** — normalized 6 different formats (`03/04/2026`, `March 5 2026`, `3/9/26`, `Mar 13`, `10/03/2026`, `18/03/2026`) to ISO `YYYY-MM-DD`, sorted oldest→newest
- **Duplicates** — removed 2 exact duplicate rows (Office chairs $1,240.00 and Printer paper $48.50), saving $1,288.50
- **Categories** — title-cased the inconsistent ones (`office supplies`, `software`, `furniture`, `travel`)
- **Amounts** — plain numbers with 2 decimals, no `$`/commas (spreadsheet apps handle these cleanly; format the column as currency for display)

**Assumptions worth confirming:**
- `10/03/2026` and `18/03/2026` read as day-first (DD/MM → March 10 and March 18), since 18 can't be a month. The other slashed dates read as month-first since `3/24/2026` can't be day-first. The file mixes US and European conventions, so double-check `03/04/2026` — I took it as **March 4**, but it could be April 3.
- **Team lunch $212.40** appears on both Mar 5 and Mar 25 — kept both since the dates differ, but one might be a mistyped duplicate.

Total after cleanup: **$3,542.60** across 18 transactions.