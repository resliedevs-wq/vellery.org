from __future__ import annotations

import csv
import re
from collections import Counter
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile

RAW = """Date,Description,Category,Amount
2026-03-02,Office chairs,Furniture,"$1,240.00"
03/04/2026,Printer paper,office supplies,48.5
March 5 2026,Team lunch,Meals,$212.40
2026-03-02,Office chairs,Furniture,"$1,240.00"
3/9/26,Zoom subscription,Software,149
2026-03-10,Taxi to client,travel,$36.20
10/03/2026,Train tickets,Travel,"$184.00"
2026-03-12,Coffee beans,Meals,27.99
Mar 13,Monitor,Equipment,$329.00
2026-03-15,Notebooks,Office Supplies,$22.75
03/04/2026,Printer paper,office supplies,48.5
2026-03-18,Figma seats,software,$90.00
18/03/2026,Client dinner,Meals,"$318.60"
2026-03-20,Desk lamp,furniture,$64
2026-03-22,Hotel (2 nights),Travel,"$412.00"
3/24/2026,USB-C cables,Equipment,$31.96
2026-03-25,Team lunch,Meals,$212.40
2026-03-27,Pens,Office supplies,$9.80
2026-03-30,Taxi to airport,Travel,$58.00
2026-03-31,Notion subscription,Software,$96.00"""

MONTHS = {
    "jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3,
    "apr": 4, "april": 4, "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7,
    "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9, "oct": 10,
    "october": 10, "nov": 11, "november": 11, "dec": 12, "december": 12,
}


def parse_date(value: str) -> date:
    value = value.strip()

    # ISO date (the unambiguous format).
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", value)
    if m:
        return date(*map(int, m.groups()))

    # Month-name dates, with an optional year. The data is a March 2026
    # ledger, so a missing year is completed from the surrounding entries.
    m = re.fullmatch(r"([A-Za-z]+)\s+(\d{1,2})(?:,?\s+(\d{2,4}))?", value)
    if m:
        month_name, day, year = m.groups()
        month = MONTHS[month_name.lower()]
        y = 2026 if year is None else int(year)
        if y < 100:
            y += 2000
        return date(y, month, int(day))

    # Slash dates. The source mixes US and day-first conventions, so use
    # unambiguous values and the surrounding date sequence to disambiguate.
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{2,4})", value)
    if m:
        first, second, year = map(int, m.groups())
        if year < 100:
            year += 2000
        if first > 12:
            # Clearly day-first (e.g. 18/03/2026).
            day, month = first, second
        elif second > 12:
            # Clearly month-first (e.g. 3/24/2026).
            month, day = first, second
        else:
            # Both readings are possible. Resolve these two by the ledger's
            # chronological sequence: 03/04 falls between Mar 2 and Mar 5,
            # and 10/03 falls between Mar 10 and Mar 12.
            contextual = {
                (3, 4): (3, 4),    # 03/04/2026 -> 2026-03-04
                (10, 3): (3, 10),  # 10/03/2026 -> 2026-03-10
                (3, 9): (3, 9),    # 3/9/2026   -> 2026-03-09
            }
            month, day = contextual.get((first, second), (first, second))
        return date(year, month, day)

    raise ValueError(f"Unrecognized date: {value!r}")


def parse_amount(value: str) -> Decimal:
    cleaned = re.sub(r"[^0-9.\-]", "", value)
    return Decimal(cleaned).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def clean_rows() -> list[dict]:
    rows = list(csv.DictReader(RAW.splitlines()))
    cleaned = []
    seen = set()

    for row in rows:
        record = {
            "Date": parse_date(row["Date"]),
            "Description": " ".join(row["Description"].split()),
            "Category": " ".join(row["Category"].split()).title(),
            "Amount": parse_amount(row["Amount"]),
        }
        # Exact duplicate check on the normalized values. Same-description
        # purchases on different dates are intentionally retained.
        key = (record["Date"], record["Description"].casefold(),
               record["Category"].casefold(), record["Amount"])
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(record)

    cleaned.sort(key=lambda r: r["Date"])
    return cleaned


def write_csv(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\r\n")
        writer.writerow(["Date", "Description", "Category", "Amount"])
        for row in rows:
            writer.writerow([
                row["Date"].isoformat(),
                row["Description"],
                row["Category"],
                f'{row["Amount"]:.2f}',
            ])


def excel_serial(d: date) -> int:
    return (d - date(1899, 12, 30)).days


def write_xlsx(rows: list[dict], path: Path) -> None:
    total_rows = len(rows) + 1
    cell_ref = f"A1:D{total_rows}"

    def inline_cell(ref: str, value: str, style: int | None = None) -> str:
        s = f' s="{style}"' if style is not None else ""
        return f'<c r="{ref}" t="inlineStr"{s}><is><t>{escape(value)}</t></is></c>'

    def number_cell(ref: str, value: str, style: int) -> str:
        return f'<c r="{ref}" s="{style}"><v>{value}</v></c>'

    sheet_rows = []
    headers = ["Date", "Description", "Category", "Amount"]
    header_cells = "".join(
        inline_cell(f"{col}1", value, 1)
        for col, value in zip("ABCD", headers)
    )
    sheet_rows.append(f'<row r="1" ht="22" customHeight="1">{header_cells}</row>')

    for idx, record in enumerate(rows, start=2):
        cells = [
            number_cell(f"A{idx}", str(excel_serial(record["Date"])), 2),
            inline_cell(f"B{idx}", record["Description"]),
            inline_cell(f"C{idx}", record["Category"]),
            number_cell(f"D{idx}", f'{record["Amount"]:.2f}', 3),
        ]
        sheet_rows.append(f'<row r="{idx}">{"".join(cells)}</row>')

    sheet_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <dimension ref="{cell_ref}"/>
  <sheetViews>
    <sheetView tabSelected="1" workbookViewId="0">
      <pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>
      <selection pane="bottomLeft" activeCell="A2" sqref="A2"/>
    </sheetView>
  </sheetViews>
  <sheetFormatPr defaultRowHeight="15"/>
  <cols>
    <col min="1" max="1" width="12.5" customWidth="1"/>
    <col min="2" max="2" width="25" customWidth="1"/>
    <col min="3" max="3" width="18" customWidth="1"/>
    <col min="4" max="4" width="14" customWidth="1"/>
  </cols>
  <sheetData>
    {''.join(sheet_rows)}
  </sheetData>
  <autoFilter ref="{cell_ref}"/>
  <pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>
</worksheet>
'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <numFmts count="2">
    <numFmt numFmtId="164" formatCode="yyyy-mm-dd"/>
    <numFmt numFmtId="165" formatCode="&quot;$&quot;#,##0.00"/>
  </numFmts>
  <fonts count="2">
    <font><sz val="11"/><name val="Calibri"/><family val="2"/></font>
    <font><b/><color rgb="FFFFFFFF"/><sz val="11"/><name val="Calibri"/><family val="2"/></font>
  </fonts>
  <fills count="3">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1F4E5A"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border>
      <left/><right/><top/>
      <bottom style="thin"><color rgb="FFB7C9CE"/></bottom>
      <diagonal/>
    </border>
  </borders>
  <cellStyleXfs count="1">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
  </cellStyleXfs>
  <cellXfs count="4">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">
      <alignment horizontal="left" vertical="center"/>
    </xf>
    <xf numFmtId="164" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1" applyAlignment="1">
      <alignment horizontal="left" vertical="center"/>
    </xf>
    <xf numFmtId="165" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1" applyAlignment="1">
      <alignment horizontal="right" vertical="center"/>
    </xf>
  </cellXfs>
  <cellStyles count="1">
    <cellStyle name="Normal" xfId="0" builtinId="0"/>
  </cellStyles>
</styleSheet>
'''

    workbook_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <bookViews><workbookView xWindow="0" yWindow="0" windowWidth="16000" windowHeight="9000"/></bookViews>
  <sheets><sheet name="Transactions" sheetId="1" r:id="rId1"/></sheets>
  <calcPr calcId="191029"/>
</workbook>
'''

    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
'''

    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
'''

    workbook_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
'''

    now = datetime.now().astimezone().replace(microsecond=0).isoformat()
    core_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:dcterms="http://purl.org/dc/terms/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Cleaned Expense Transactions</dc:title>
  <dc:creator>DeepSeek Harness</dc:creator>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
'''

    app_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
            xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft Excel</Application>
  <DocSecurity>0</DocSecurity>
  <ScaleCrop>false</ScaleCrop>
  <HeadingPairs>
    <vt:vector size="2" baseType="variant">
      <vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant>
      <vt:variant><vt:i4>1</vt:i4></vt:variant>
    </vt:vector>
  </HeadingPairs>
  <TitlesOfParts>
    <vt:vector size="1" baseType="lpstr"><vt:lpstr>Transactions</vt:lpstr></vt:vector>
  </TitlesOfParts>
  <Company></Company>
  <LinksUpToDate>false</LinksUpToDate>
  <SharedDoc>false</SharedDoc>
  <HyperlinksChanged>false</HyperlinksChanged>
  <AppVersion>16.0300</AppVersion>
</Properties>
'''

    with ZipFile(path, "w", compression=ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("docProps/core.xml", core_xml)
        zf.writestr("docProps/app.xml", app_xml)
        zf.writestr("xl/workbook.xml", workbook_xml)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        zf.writestr("xl/styles.xml", styles_xml)
        zf.writestr("xl/worksheets/sheet1.xml", sheet_xml)


def main() -> None:
    rows = clean_rows()
    base = Path("cleaned_expenses")
    write_csv(rows, base.with_suffix(".csv"))
    write_xlsx(rows, base.with_suffix(".xlsx"))

    total = sum((r["Amount"] for r in rows), Decimal("0.00"))
    categories = Counter(r["Category"] for r in rows)
    print(f"Unique transactions: {len(rows)}")
    print(f"Removed duplicate rows: {20 - len(rows)}")
    print(f"Total: ${total:,.2f}")
    print("Categories:", dict(sorted(categories.items())))
    print(f"Date range: {rows[0]['Date']} to {rows[-1]['Date']}")


if __name__ == "__main__":
    main()
