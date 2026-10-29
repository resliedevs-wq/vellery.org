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

Changes made:

- Removed two exact duplicate rows: the second Office chairs entry and the second Printer paper entry. Kept both Team lunch purchases because their dates differ.
- Standardized dates:
  - `03/04/2026` → `2026-03-04`
  - `March 5 2026` → `2026-03-05`
  - `3/9/26` → `2026-03-09`
  - `10/03/2026` → `2026-03-10`
  - `Mar 13` → `2026-03-13`
  - `18/03/2026` → `2026-03-18`
  - `3/24/2026` → `2026-03-24`
- Changed categories to Title Case for Printer paper, Taxi to client, Figma seats, Desk lamp, and Pens.
- Removed `$` from all 15 retained amounts containing it, and removed the comma from `1,240.00`.
- Added decimal places: `48.5` → `48.50`, `149` → `149.00`, and `64` → `64.00`.

Date interpretation: Some numeric dates could otherwise be ambiguous. Your instruction that every expense is from March 2026 resolves them; nothing remains uncertain.