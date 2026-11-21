"""Time and station variables shared by the method catalog."""

import math
import csv
from functools import lru_cache
from collections import defaultdict
from datetime import date
from statistics import correlation, mean

from plambas.formulas import symbols_used, walk
from plambas.hydrology import fao_inputs, mean_temperature
from plambas.monthly_data import ROOT, number, period_values


@lru_cache
def station_coefficients():
    with (ROOT / "parameters/station_coefficients.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        return {
            row["Station"].casefold(): {
                key: float(row[key]) for key in ("kRs", "offset")
            }
            for row in csv.DictReader(handle)
        }


@lru_cache(maxsize=16384)
def day_geometry(year, month, latitude, day=15):
    j = date(year, month, day).timetuple().tm_yday
    angle = 2 * math.pi * j / 365
    phi = math.radians(latitude)
    decl = 0.409 * math.sin(angle - 1.39)
    sunset = math.acos(max(-1, min(1, -math.tan(phi) * math.tan(decl))))
    ra = (
        1440
        / math.pi
        * 0.0820
        * (1 + 0.033 * math.cos(angle))
        * (
            sunset * math.sin(phi) * math.sin(decl)
            + math.cos(phi) * math.cos(decl) * math.sin(sunset)
        )
    )
    return ra, 24 * sunset / math.pi


def method_inputs(method):
    local = set(method.get("parameters", {})) | set(method.get("state", {}))
    needed = set(method.get("inputs", []))
    for step in method.get("steps", []):
        needed.update(symbols_used(step["expression"]) - local)
        local.add(step["symbol"])
    if method.get("expression") is not None and method.get("engine") not in (
        "frequency",
        "comparison",
    ):
        needed.update(symbols_used(method["expression"]) - local)
    return needed


def comparison_rows(method, rows):
    pairs = []
    for row in rows:
        observed, estimated = (number(row.get(k), ",") for k in ("FAOPM", "EstimateET"))
        if observed is not None and estimated is not None:
            days = period_values(row)[2]
            pairs.append((observed / days, estimated / days))
    if len(pairs) < 2:
        raise ValueError("At least two paired months are required.")
    observed, estimated = zip(*pairs)
    diffs = [a - b for a, b in pairs]
    bias = mean(diffs)
    scope = dict(
        meanDiff=bias,
        varianceTerm=sum((-v - bias) ** 2 for v in diffs) / (len(diffs) - 1),
        meanSquare=mean(v * v for v in diffs),
        meanAbs=mean(abs(v) for v in diffs),
    )
    if "correlation" in symbols_used(method["expression"]):
        if len(set(observed)) < 2 or len(set(estimated)) < 2:
            raise ValueError("Correlation requires two varying series.")
        scope["correlation"] = correlation(observed, estimated)
    return [
        {
            "year": None,
            "month": None,
            "inputs": {"n": len(pairs)},
            "value": walk(method["expression"], scope),
            "missing": [],
            "series": pairs,
        }
    ]


def prepare(method, rows, meta):
    if method.get("prepare") == "fao":
        return fao_inputs(rows, meta, method["parameters"])
    required = method_inputs(method)
    calibration = station_coefficients().get(
        str(meta.get("weather_station", "")).strip().casefold(), {}
    )
    temps = defaultdict(dict)
    out = []
    for row in rows:
        y, m, days = period_values(row)
        row = dict(row)
        for key, value in calibration.items():
            if key in required and row.get(key) is None:
                row[key] = value
        for key, field in (
            ("Φ", "weather_station_latitude"),
            ("z", "weather_station_elevation"),
        ):
            if row.get(key) is None:
                row[key] = number(meta.get(field), ",")
        row["Tmean"] = mean_temperature(row)
        if row["Tmean"] is not None:
            temps[y][m] = row["Tmean"]
        if required.intersection({"Ra", "daylight"}) and row["Φ"] is not None:
            if not -90 <= row["Φ"] <= 90:
                raise ValueError("Invalid latitude.")
            ra, daylight = day_geometry(y, m, row["Φ"])
            if row.get("Ra") is None:
                row["Ra"] = ra
            if row.get("daylight") is None:
                row["daylight"] = (
                    mean(day_geometry(y, m, row["Φ"], i)[1] for i in range(1, days + 1))
                    if "daylight" in required
                    else daylight
                )
        out.append(row)
    if "heatIndex" in required:
        indices = {
            y: sum((max(0, t) / 5) ** 1.514 for t in data.values())
            for y, data in temps.items()
            if len(data) == 12
        }
        for row in out:
            if row.get("heatIndex") is None:
                row["heatIndex"] = indices.get(period_values(row)[0])
    return out


def formula_rows(method, rows, meta, symbol_values):
    required = method_inputs(method)
    params = method.get("parameters", {})
    state = {key: walk(init, params) for key, init in method.get("state", {}).items()}
    steps = method.get("steps", [])
    output = []
    previous = None
    ordered = sorted(rows, key=lambda r: period_values(r)[:2]) if state else rows
    for row in prepare(method, ordered, meta):
        y, m, values = symbol_values(row, required, params)
        missing = sorted(key for key, value in values.items() if value is None)
        if state and (missing or (previous is not None and y * 12 + m != previous + 1)):
            raise ValueError(
                f"{y}-{m:02} · "
                + (", ".join(missing) if missing else "Consecutive months required.")
            )
        previous = y * 12 + m
        calculated = None
        extra = {}
        if not missing:
            scope = {**values, **params, **state}
            if method["id"] == "q24" and scope.get("D", 0) < 0:
                raise ValueError("Deficit must be non-negative.")
            if "RHmean" in scope and not 0 <= scope["RHmean"] <= 100:
                raise ValueError(f"{y}-{m:02} · RH (0–100%)")
            if method.get("group") == "wb" and any(
                scope.get(key, 0) < 0 for key in ("ET0", "PRCP")
            ):
                raise ValueError(f"{y}-{m:02} · ET0 / PRCP < 0")
            for step in steps:
                scope[step["symbol"]] = walk(step["expression"], scope)
                if step.get("publish"):
                    extra[step["symbol"]] = scope[step["symbol"]]
            calculated = walk(method["expression"], scope)
            state = {k: scope[k] for k in state}
        entry = {
            "year": y,
            "month": m,
            "inputs": values,
            "value": calculated,
            "missing": missing,
        }
        if extra:
            entry["outputs"] = extra
        output.append(entry)
    if not any(item["value"] is not None for item in output):
        raise ValueError("No calculable months.")
    return output


def add_outputs(rows, record):
    method = record["method"]
    if method.get("engine") == "frequency" or all(
        r["year"] is None for r in record["rows"]
    ):
        return rows
    by_date = {(r["year"], r["month"]): r for r in record["rows"]}
    names = set(filter(None, (method.get("output"), method.get("symbol"))))
    if (
        method.get("group") == "eto"
        and method.get("output") == "ET0"
        and method.get("prepare") != "fao"
    ):
        names.add("EstimateET")
    extra = {k for r in record["rows"] for k in r.get("outputs", {})}
    result = []
    for row in rows:
        item = by_date.get(period_values(row)[:2], {})
        derived = {key: item.get("value") for key in names}
        derived.update({key: item.get("outputs", {}).get(key) for key in extra})
        result.append({**row, **derived})
    return result
