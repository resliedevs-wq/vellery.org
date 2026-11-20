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

### Changes Made (by original data row)

- **Row 1 (`2026-03-02, Office chairs`)**: Reformatted amount from `"$1,240.00"` to `1240.00` (removed quotes, `$`, and comma).
- **Row 2 (`03/04/2026, Printer paper`)**: Converted date to `2026-03-04`; changed category `office supplies` to `Office Supplies`; formatted amount `48.5` as `48.50`.
- **Row 3 (`March 5 2026, Team lunch`)**: Converted date to `2026-03-05`; removed `$` from `$212.40`.
- **Row 4 (`2026-03-02, Office chairs`)**: **Removed** as an exact duplicate of Row 1.
- **Row 5 (`3/9/26, Zoom subscription`)**: Converted date to `2026-03-09`; formatted amount `149` as `149.00`.
- **Row 6 (`2026-03-10, Taxi to client`)**: Changed category `travel` to `Travel`; removed `$` from `$36.20`.
- **Row 7 (`10/03/2026, Train tickets`)**: Converted date to `2026-03-10`; removed quotes and `$` from `"$184.00"`.
- **Row 8 (`2026-03-12, Coffee beans`)**: No changes needed.
- **Row 9 (`Mar 13, Monitor`)**: Converted date to `2026-03-13`; removed `$` from `$329.00`.
- **Row 10 (`2026-03-15, Notebooks`)**: Removed `$` from `$22.75`.
- **Row 11 (`03/04/2026, Printer paper`)**: **Removed** as an exact duplicate of Row 2.
- **Row 12 (`2026-03-18, Figma seats`)**: Changed category `software` to `Software`; removed `$` from `$90.00`.
- **Row 13 (`18/03/2026, Client dinner`)**: Converted date to `2026-03-18`; removed quotes and `$` from `"$318.60"`.
- **Row 14 (`2026-03-20, Desk lamp`)**: Changed category `furniture` to `Furniture`; formatted amount `$64` as `64.00`.
- **Row 15 (`2026-03-22, Hotel (2 nights)`)**: Removed quotes and `$` from `"$412.00"`.
- **Row 16 (`3/24/2026, USB-C cables`)**: Converted date to `2026-03-24`; removed `$` from `$31.96`.
- **Row 17 (`2026-03-25, Team lunch`)**: Removed `$` from `$212.40` (kept row since it is on a different date than Row 3).
- **Row 18 (`2026-03-27, Pens`)**: Changed category `Office supplies` to `Office Supplies`; removed `$` from `$9.80`.
- **Row 19 (`2026-03-30, Taxi to airport`)**: Removed `$` from `$58.00`.
- **Row 20 (`2026-03-31, Notion subscription`)**: Removed `$` from `$96.00`.

### Anything Unclear / Worth Double-Checking

1. **Mixed `MM/DD` and `DD/MM` date formats**: The original sheet mixes US (`03/04/2026`, `3/9/26`, `3/24/2026`) and non-US (`10/03/2026`, `18/03/2026`) numeric date formats, plus a yearless `Mar 13`. Using your constraint that every expense is from March 2026 resolves `03/04/2026` as March 4, `3/9/26` as March 9, `10/03/2026` as March 10, `Mar 13` as `2026-03-13`, and `18/03/2026` as March 18—though it's worth verifying those source receipts weren't accidentally entered with the wrong month/day order (e.g., April 3 or October 3).
2. **Identical amount on repeated `Team lunch` (`212.40`)**: Kept both `2026-03-05` and `2026-03-25` per the instruction to keep repeated purchases on different dates, though having the exact same amount to the cent (`212.40`) may be worth confirming as two separate lunches rather than a duplicated entry with a different date.
3. **Existing category groupings**: Preserved all original category names (only changing casing to Title Case)—for example, `Coffee beans` remains under `Meals` rather than `Office Supplies`, and `USB-C cables` remains under `Equipment` rather than `Office Supplies`.
