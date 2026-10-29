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

**Changes made**

1. **Removed 2 exact duplicates:** the second "2026-03-02 Office chairs $1,240.00" row and the second "03/04/2026 Printer paper 48.5" row. The other repeats (Team lunch on 03-05 and 03-25, both $212.40) have different dates, so I kept them.
2. **Normalized dates to YYYY-MM-DD:**
   - `03/04/2026` → 2026-03-04 and `10/03/2026` → 2026-03-10. Both could be read as day/month or month/day, so I used the rule that every expense is from March 2026.
   - `3/9/26` → 2026-03-09, `Mar 13` → 2026-03-13, `3/24/2026` → 2026-03-24, `March 5 2026` → 2026-03-05, `18/03/2026` → 2026-03-18.
3. **Category names in Title Case:** "office supplies" and "Office supplies" → Office Supplies; "furniture" → Furniture; "software" → Software; "travel" → Travel.
4. **Amounts as plain two-decimal numbers:** removed `$` and commas (`"$1,240.00"` → 1240.00), and added decimals to whole numbers (`149` → 149.00, `$64` → 64.00, `48.5` → 48.50).

18 rows remain, down from 20.

**Things I'm not sure about**

- **Ambiguous dates:** I read `03/04/2026` as March 4 and `10/03/2026` as March 10. If the sheet actually uses day/month for these, the dates would be 2026-04-03 and 2026-10-03, but the March-only rule makes that unlikely.
- **Missing or short year:** "Mar 13" had no year and "3/9/26" had a two-digit year. I assumed 2026 for both.
- **Possible real duplicates:** the removed chair and printer paper rows might be genuine second purchases (two chairs, or two paper orders) that were entered twice. Check the receipts before relying on the removal.
- **Possible double-claimed lunch:** Team lunch appears on 03-05 and 03-25 with the same amount. I kept both, but if only one lunch happened, one row should go.