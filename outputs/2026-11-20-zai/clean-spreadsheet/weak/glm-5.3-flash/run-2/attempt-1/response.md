Done — the cleaned file is at `expenses_march_2026_clean.csv`. (I couldn't run a script to verify since shell access was denied, so I checked the math by hand.)

```
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

**What I fixed**
- **Removed 2 duplicate rows** — Office chairs (2026-03-02) and Printer paper (2026-03-04) each appeared twice
- **Normalized dates to ISO format** (YYYY-MM-DD) and sorted chronologically
- **Standardized category casing** — `office supplies`/`Office supplies` → `Office Supplies`, same for `Software`, `Travel`, `Furniture`. Now 6 clean categories
- **Standardized amounts** — stripped `$` and quotes, padded to 2 decimals (`48.5` → `48.50`, `149` → `149.00`)

**18 rows, total $3,542.60**

Two judgment calls to flag:
- `03/04/2026` → I read it as **March 4**, not April 3 — every other entry is March, and it sits between the Mar 2 and Mar 5 rows. Similarly `10/03/2026` → **March 10** (not October 3). The source data mixes both conventions, so worth a spot-check if these came from different people.
- `Mar 13` had no year; I assumed 2026. I also dropped the `$` from amounts so the column works as numbers — say the word if you'd rather keep a currency format.