from __future__ import annotations

import argparse
import csv
import html
import re
import zipfile
from pathlib import Path


NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"


SOURCES = [
    ("README", "README.md"),
    ("Brief", "00-brief.md"),
    ("Site Inventory", "01-site-inventory.md"),
    ("Seed Map", "02-seed-map.md"),
    ("Wordstat Raw", "03-wordstat-raw.csv"),
    ("Keywords Clean", "04-keywords-clean.csv"),
    ("Clusters", "05-clusters.csv"),
    ("URL Map", "06-url-map.csv"),
    ("Content Briefs", "07-content-briefs.md"),
    ("SERP GEO Notes", "08-serp-geo-notes.md"),
    ("Quality Report", "09-quality-report.md"),
    ("Roadmap", "12-implementation-roadmap.md"),
]


def safe_sheet_name(name: str, used: set[str]) -> str:
    clean = re.sub(r"[\[\]:*?/\\]", " ", name).strip()[:31] or "Sheet"
    base = clean
    suffix = 1
    while clean in used:
        marker = f" {suffix}"
        clean = (base[: 31 - len(marker)] + marker).strip()
        suffix += 1
    used.add(clean)
    return clean


def column_name(index: int) -> str:
    result = ""
    while index:
        index, rem = divmod(index - 1, 26)
        result = chr(65 + rem) + result
    return result


def read_csv(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [row for row in csv.reader(f)]


def read_markdown(path: Path) -> list[list[str]]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return [["line", "text"], *[[str(i), line] for i, line in enumerate(lines, start=1)]]


def sheet_xml(rows: list[list[str]]) -> str:
    xml_rows: list[str] = []
    for r_idx, row in enumerate(rows, start=1):
        cells: list[str] = []
        for c_idx, value in enumerate(row, start=1):
            ref = f"{column_name(c_idx)}{r_idx}"
            text = html.escape("" if value is None else str(value))
            cells.append(f'<c r="{ref}" t="inlineStr"><is><t>{text}</t></is></c>')
        xml_rows.append(f'<row r="{r_idx}">{"".join(cells)}</row>')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<worksheet xmlns="{NS_MAIN}" xmlns:r="{NS_REL}">'
        f"<sheetData>{''.join(xml_rows)}</sheetData>"
        "</worksheet>"
    )


def workbook_xml(sheet_names: list[str]) -> str:
    sheets = []
    for idx, name in enumerate(sheet_names, start=1):
        sheets.append(f'<sheet name="{html.escape(name)}" sheetId="{idx}" r:id="rId{idx}"/>')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<workbook xmlns="{NS_MAIN}" xmlns:r="{NS_REL}">'
        f"<sheets>{''.join(sheets)}</sheets>"
        "</workbook>"
    )


def workbook_rels_xml(count: int) -> str:
    rels = []
    for idx in range(1, count + 1):
        rels.append(
            f'<Relationship Id="rId{idx}" '
            f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            f'Target="worksheets/sheet{idx}.xml"/>'
        )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<Relationships xmlns="{NS_PKG_REL}">{"".join(rels)}</Relationships>'
    )


def root_rels_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<Relationships xmlns="{NS_PKG_REL}">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/>'
        "</Relationships>"
    )


def content_types_xml(count: int) -> str:
    overrides = [
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
    ]
    for idx in range(1, count + 1):
        overrides.append(
            f'<Override PartName="/xl/worksheets/sheet{idx}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        f'{"".join(overrides)}'
        "</Types>"
    )


def build_workbook(run_dir: Path, output: Path) -> None:
    used_names: set[str] = set()
    sheets: list[tuple[str, list[list[str]]]] = []

    for title, filename in SOURCES:
        path = run_dir / filename
        if not path.exists():
            continue
        rows = read_csv(path) if path.suffix.lower() == ".csv" else read_markdown(path)
        sheets.append((safe_sheet_name(title, used_names), rows))

    if not sheets:
        raise SystemExit(f"No source files found in {run_dir}")

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types_xml(len(sheets)))
        z.writestr("_rels/.rels", root_rels_xml())
        z.writestr("xl/workbook.xml", workbook_xml([name for name, _ in sheets]))
        z.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml(len(sheets)))
        for idx, (_, rows) in enumerate(sheets, start=1):
            z.writestr(f"xl/worksheets/sheet{idx}.xml", sheet_xml(rows))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    output = args.output or args.run_dir / "semantic-core.xlsx"
    build_workbook(args.run_dir, output)
    print(output)


if __name__ == "__main__":
    main()
