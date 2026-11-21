"""Monthly project data, including the two-header workbooks produced by SRCLET 1."""
import calendar
import csv
import json
import math
import os
import re
import shutil
import tempfile
from pathlib import Path

from openpyxl import Workbook, load_workbook

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"


def catalog():
    """Stable column identifiers and their legacy display names."""
    fields = {}
    for path in sorted((ROOT / "parameters/basic").glob("*.json")):
        item = json.loads(path.read_text(encoding="utf-8"))
        name = item["name"].strip()
        key = {"M": "Month", "Y": "Year"}.get(item["symbol"], item["symbol"])
        fields[key] = (name, item["unit"].strip())
    return fields


def column_id(header, fields):
    value = str(header or "").strip().casefold()
    aliases = {"pet":"ET0", "eto":"ET0", "mjesec": "Month", "godina": "Year", "y": "Year", "d": "Deficit",
               "manjak": "Deficit", "manjak vode": "Deficit", "δm": "Deficit",
               "wind": "uz", "wind speed at 2m":"u2", "u(x)": "uz", "p": "PRCP", "average reletive air humidity": "RHmean"}
    if value in aliases:
        return aliases[value]
    for key, (name, _) in fields.items():
        if value in (key.casefold(), name.casefold()):
            return key
    return None


def read_table(path, delimiter="auto"):
    path = Path(path)
    if path.suffix.lower() == ".xlsx":
        book = load_workbook(path, read_only=True, data_only=True)
        try:
            sheet = book["data_input"] if "data_input" in book.sheetnames else book.active
            table = list(sheet.values)
            if table and sheet.title == "data_input" and list(table[0]) == list(range(len(table[0]))):
                table.pop(0)
        finally:
            book.close()
    else:
        try:
            source = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            source = path.read_text(encoding="cp1250")
        lines = [line for line in source.splitlines() if line.strip()]
        if delimiter == "auto" and lines:
            delimiter = next((sep for sep in ("\t", ";", ",") if sep in lines[0]), "space")
        if delimiter in ("auto", "space"):
            table = [line.split() for line in lines]
        else:
            table = list(csv.reader(lines, delimiter=delimiter, strict=True))
    table = [list(row) for row in table if any(x is not None and str(x).strip() for x in row)]
    if len(table) < 2:
        raise ValueError("A header and at least one data row are required.")
    headers = [str(x or "").strip() for x in table[0]]
    for line, row in enumerate(table[1:], 2):
        if len(row) != len(headers):
            raise ValueError(f"Row {line}: {len(row)} / {len(headers)} columns.")
    return headers, table[1:]


def number(value, decimal="."):
    if value is None or not str(value).strip():
        return None
    if isinstance(value, str):
        value = value.strip()
        if decimal == ",":
            value = value.replace(",", ".")
    n = float(value)
    if not math.isfinite(n):
        raise ValueError(str(value))
    return None if n == -999 else n


def mapped_rows(mapping, rows, decimal="."):
    keys = [key for key in mapping if key]
    if not {"Year", "Month"}.issubset(keys) or len(keys) != len(set(keys)) or len(keys) < 3:
        raise ValueError("Select year, month and a measurement. Each column ID must be unique.")
    result = []
    periods = set()
    for i, source in enumerate(rows, 2):
        row = {}
        for key, raw in zip(mapping, source):
            if key:
                try:
                    row[key] = number(raw, decimal)
                except (ValueError, TypeError) as exc:
                    raise ValueError(f"{i} · {key}: {raw}") from exc
        y, m = row["Year"], row["Month"]
        if y is None or m is None or not y.is_integer() or not m.is_integer() or not 1 <= y <= 9999 or not 1 <= m <= 12:
            raise ValueError(f"{i} · Year / Month: {y} / {m}")
        row["Year"], row["Month"] = int(y), int(m)
        if (y, m) in periods:
            raise ValueError(f"{i} · Duplicate month: {int(y)}-{int(m):02}")
        periods.add((y, m))
        result.append(row)
    return result


def save_json(path, data):
    path = Path(path)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as out:
        tmp = Path(out.name)
    try:
        with tmp.open("w", encoding="utf-8") as out:
            json.dump(data, out, ensure_ascii=False, indent=2, allow_nan=False)
            out.flush()
            os.fsync(out.fileno())
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def create_project(parent, name, metadata, rows):
    parent = Path(parent)
    if not name.strip() or name in (".", "..") or re.search(r'[\\/\x00]', name):
        raise ValueError("Invalid project name.")
    target = parent / name
    if target.exists():
        raise FileExistsError(str(target))
    staging = Path(tempfile.mkdtemp(dir=parent, prefix=".srclet-"))
    try:
        headers = list(rows[0])
        book = Workbook()
        sheet = book.active
        sheet.title = "data_input"
        sheet.append(list(range(len(headers))))
        sheet.append(headers)
        for row in rows:
            sheet.append([row[key] for key in headers])
        book.save(staging / "data.xlsx")
        save_json(staging / "data.json", {**metadata, "format_version": 2, "columns": headers})
        if target.exists():
            raise FileExistsError(str(target))
        staging.rename(target)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return target


def load_project(path):
    path = Path(path)
    meta = json.loads((path / "data.json").read_text(encoding="utf-8-sig"))
    edited = path / "inputs.json"
    if edited.exists():
        data = json.loads(edited.read_text(encoding="utf-8"))
        return {**meta, **data.get("metadata", {})}, data["columns"], data["rows"]
    headers, data = read_table(path / "data.xlsx")
    fields = catalog()
    ids = [column_id(h, fields) or h for h in headers]
    return meta, ids, [dict(zip(ids, row)) for row in data]


def period_values(row):
    y, m = number(row.get("Year")), number(row.get("Month"))
    if y is None or m is None or not y.is_integer() or not m.is_integer() or not 1 <= y <= 9999 or not 1 <= m <= 12:
        raise ValueError("Invalid year or month.")
    return int(y), int(m), calendar.monthrange(int(y), int(m))[1]

