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

- **Duplicates.** Removed one exact duplicate each of Office chairs and Printer paper, leaving 18 rows. Kept both Team lunch purchases because they occurred on March 5 and March 25.
- **Dates.** Changed Printer paper (`03/04/2026` → `2026-03-04`), March 5 Team lunch (`March 5 2026` → `2026-03-05`), Zoom subscription (`3/9/26` → `2026-03-09`), Train tickets (`10/03/2026` → `2026-03-10`), Monitor (`Mar 13` → `2026-03-13`), Client dinner (`18/03/2026` → `2026-03-18`), and USB-C cables (`3/24/2026` → `2026-03-24`).
- **Categories.** Changed Printer paper and Pens to `Office Supplies`, Taxi to client to `Travel`, Figma seats to `Software`, and Desk lamp to `Furniture`.
- **Amounts.** Changed Office chairs from `$1,240.00` to `1240.00`, Printer paper from `48.5` to `48.50`, Zoom subscription from `149` to `149.00`, and Desk lamp from `$64` to `64.00`. Removed `$` from both Team lunch entries, Taxi to client, Train tickets, Monitor, Notebooks, Figma seats, Client dinner, Hotel (2 nights), USB-C cables, Pens, Taxi to airport, and Notion subscription.

### Date interpretations

The slash-formatted dates use mixed conventions. The March 2026 constraint resolves `03/04/2026` as March 4 and `10/03/2026` as March 10. It also supplies the year for `Mar 13`. No uncertainties remained after applying that constraint.