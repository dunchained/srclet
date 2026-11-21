import csv
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from openpyxl import Workbook

from plambas.hydrology import (
    BALANCE,
    FAO,
    FREQUENCY,
    balance_rows,
    fao_inputs,
    frequency_rows,
)
from plambas.formulas import symbols_used, walk
from plambas.method_series import formula_rows, comparison_rows
from plambas.frequency import frequency_result
from plambas.monthly_data import ROOT, number, period_values, save_json


def project_methods():
    methods = []
    coefficients = {}
    for path in (ROOT / "parameters/changable").glob("*.json"):
        item = json.loads(path.read_text(encoding="utf-8"))
        try:
            coefficients[item["symbol"]] = number(item.get("value"), ",")
        except (TypeError, ValueError):
            continue
    for path in sorted((ROOT / "methods").glob("*/*.json")):
        item = json.loads(path.read_text(encoding="utf-8"))
        if "group" in item and "expression" in item:
            methods.append(item)
            continue
        if (
            item.get("formula_math") is not None
            and not item.get("method_conditions", "").strip()
        ):
            required = symbols_used(item["formula_math"])
            params = {
                key: val
                for key, val in coefficients.items()
                if key in required and val is not None
            }
            methods.append(
                {
                    "id": path.stem,
                    "group": path.parent.name,
                    "parameters": params,
                    "symbol": item["symbol"],
                    "output": item["symbol"],
                    "name": item["name"],
                    "unit": item["unit"],
                    "source": item.get("description", ""),
                    "version": 1,
                    "expression": item["formula_math"],
                    "latex": item["method_formula"],
                }
            )
    return sorted(methods, key=lambda m: (m.get("order", 10), m["name"]))


def symbol_values(row, wanted, parameters=None):
    year, month, days = period_values(row)
    values = {}
    for name in wanted:
        if name == "d":
            value = days
        elif parameters and name in parameters:
            value = parameters[name]
        else:
            key = {"D": "Deficit", "Y": "Year", "M": "Month"}.get(name, name)
            value = number(row.get(key), ",")
        values[name] = value
    return year, month, values


def scalar_results(method, rows):
    required = symbols_used(method["expression"])
    walk(method["expression"], required, check=True)
    output = []
    for i, row in enumerate(rows, 1):
        try:
            params = method.get("parameters", {}) if method["id"] != FAO["id"] else {}
            year, month, values = symbol_values(row, required, params)
            if (
                method["id"] == "q24"
                and values.get("D") is not None
                and values["D"] < 0
            ):
                raise ValueError("Deficit must be non-negative.")
            missing = sorted(key for key, value in values.items() if value is None)
            value = None if missing else walk(method["expression"], values)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"{i}: {exc}") from exc
        output.append(
            {
                "year": year,
                "month": month,
                "inputs": values,
                "value": value,
                "missing": missing,
            }
        )
    if not any(row["value"] is not None for row in output):
        raise ValueError("No calculable months.")
    return output


def calculate(method, rows, meta=None):
    if method.get("engine") == "comparison":
        output = comparison_rows(method, rows)
    elif method.get("engine") == "frequency":
        output = frequency_result(method, rows)
    elif "group" in method:
        p = method.get("parameters", {})
        if (
            "capacity" in p
            and (p["capacity"] <= 0 or not 0 <= p.get("initial", 0) <= p["capacity"])
            or any(not 0 <= p[k] <= 1 for k in ("direct", "runoff", "melt") if k in p)
            or ("rain_temp" in p and p["rain_temp"] <= p["snow_temp"])
            or any(
                p[k] <= 0 for k in ("seconds", "latent", "surface", "lower") if k in p
            )
        ):
            raise ValueError("Invalid method parameters.")
        output = formula_rows(method, rows, meta or {}, symbol_values)
    elif method["id"] == BALANCE["id"]:
        output = balance_rows(rows, method["parameters"])
    elif method["id"] == FREQUENCY["id"]:
        output = frequency_rows(rows, method["parameters"])
    else:
        prepared = (
            fao_inputs(rows, meta or {}, method["parameters"])
            if method["id"] == FAO["id"]
            else rows
        )
        output = scalar_results(method, prepared)
    signature = json.dumps(
        method, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    )
    return {
        "format_version": 1,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "method": dict(method),
        "formula_revision": hashlib.sha256(signature.encode()).hexdigest(),
        "rows": output,
    }


def store_result(project, result):
    folder = Path(project) / "results"
    folder.mkdir(exist_ok=True)
    path = folder / (uuid4().hex + ".json")
    save_json(path, result)
    return path


def export_result(path, result, tr=str):
    path = Path(path)
    method = result["method"]
    inputs = sorted({k for row in result["rows"] for k in row["inputs"]})
    outputs = sorted({k for row in result["rows"] for k in row.get("outputs", {})})
    headers = [
        "Year",
        "Month",
        *inputs,
        f"{method['name']} [{method['unit']}]",
        "Missing",
        *outputs,
        "Formula",
        "Method SHA256",
        "Source",
        "Parameters",
        "Station",
        "Input result",
        "Series",
        "Distribution",
        "Input period",
    ]
    rows = [[tr(h) for h in headers]]
    for row in result["rows"]:
        rows.append(
            [
                row["year"],
                row["month"],
                *(row["inputs"].get(key) for key in inputs),
                row["value"],
                ", ".join(row["missing"]),
                *(row.get("outputs", {}).get(k) for k in outputs),
                method["latex"],
                result["formula_revision"],
                method["source"],
                json.dumps(method.get("parameters", {})),
                result.get("station", ""),
                result.get("input_result", ""),
                method.get("series", ""),
                method.get("distribution", ""),
                " / ".join(result.get("input_period", [])),
            ]
        )
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as fp:
        temp = Path(fp.name)
    try:
        if path.suffix.lower() == ".xlsx":
            book = Workbook()
            sheet = book.active
            sheet.title = "results"
            for row in rows:
                sheet.append(row)
                for cell in sheet[sheet.max_row]:
                    if cell.data_type == "f":
                        cell.data_type = "s"
            from plambas.result_charts import add_result_charts

            add_result_charts(book, result, tr)
            book.save(temp)
        else:
            with temp.open("w", encoding="utf-8", newline="") as out:
                writer = csv.writer(
                    out, delimiter="," if path.suffix.lower() == ".csv" else "\t"
                )
                writer.writerows(rows)
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)
