Done — cleaned file saved to `expenses_2026-03_clean.csv` (Bash isn't available in this session, so the total below is hand-verified arithmetic rather than script-checked).

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

**What I fixed**

1. **Dates → ISO `YYYY-MM-DD`**, sorted chronologically.
2. **Duplicates removed (2):** "Office chairs" 2026-03-02 $1,240.00 and "Printer paper" 03/04 $48.50 each appeared twice with identical date/description/amount — treated as accidental double-entries. (The two $212.40 "Team lunch" rows are on different dates, so I kept both.)
3. **Categories normalized** to Title Case: `office supplies`/`Office Supplies`/`Office supplies` → `Office Supplies`, same for `travel`, `software`, `furniture`. Six clean categories remain.
4. **Amounts → plain numbers** with 2 decimals, no `$` or commas, so they sum correctly in a spreadsheet. New total: **$3,542.60** (18 rows).

**Assumptions to double-check**

- **Ambiguous slash dates:** your data mixes `M/D/YYYY` and `D/M/YYYY`. I placed every row in March based on its position in the sequence:
  - `03/04/2026` → **2026-03-04** (read as M/D; D/M would mean April 3, breaking the order)
  - `10/03/2026` → **2026-03-10** (read as D/M; M/D would mean October 3, out of place)
  - `18/03/2026` → **2026-03-18** (only D/M is possible)
  - If the sheet isn't strictly chronological, `10/03/2026` is the one to verify.
- `Mar 13` had no year — assumed 2026 like the rest.
- If any "duplicate" was actually a legitimate repeat purchase (e.g., two chair orders same day), let me know and I'll restore it.