Here is the cleaned CSV:

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

### Changes made
- **Removed 2 exact duplicates:** `2026-03-02` Office chairs (`$1,240.00`) and `03/04/2026` Printer paper (`48.5`) (20 rows → 18 rows).
- **Standardized dates** to ISO `YYYY-MM-DD` and kept chronological order.
- **Standardized categories** to Title Case (`Office Supplies`, `Travel`, `Software`, `Furniture`, `Meals`, `Equipment`).
- **Standardized amounts** to plain 2-decimal numbers (removed `$`, commas, and quotes) so spreadsheet tools parse them directly as numbers.

### Assumptions to double-check
- **Mixed/ambiguous dates:** Resolved `03/04/2026` as `2026-03-04` (`MM/DD/YYYY`), `10/03/2026` as `2026-03-10` (`DD/MM/YYYY`, matching `18/03/2026`), and `Mar 13` as `2026-03-13` based on the chronological March 2026 sequence.
- **Same description & amount on different dates:** Kept both `Team lunch` (`212.40`) rows (`2026-03-05` and `2026-03-25`), but worth verifying the second entry isn't a copy-paste error.
