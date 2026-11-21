import json
import tempfile
import unittest
from pathlib import Path

from plambas.formulas import Q24, walk
from plambas.monthly_data import ROOT, catalog, column_id, create_project, load_project, mapped_rows, read_table
from plambas.monthly_results import calculate, export_result, store_result


class MonthlyProjectTest(unittest.TestCase):
    def test_import_calculate_save_reopen_export(self):
        with tempfile.TemporaryDirectory() as temp:
            headers, raw = read_table(ROOT / "examples/mliniste.csv")
            mapping = [column_id(h, catalog()) for h in headers]
            rows = mapped_rows(mapping, raw)
            path = create_project(temp, "Mlinište", {"weather_station": "Mlinište"}, rows)
            meta, columns, loaded = load_project(path)
            self.assertEqual(columns, mapping)
            self.assertEqual(meta["format_version"], 2)
            result = calculate(Q24, loaded)
            self.assertAlmostEqual(result["rows"][0]["value"], 0.1269414576)
            self.assertEqual(json.loads(store_result(path, result).read_text()), result)
            for ext in ("csv", "txt", "xlsx"):
                dest = path / ("export." + ext)
                export_result(dest, result)
                saved_headers, data = read_table(dest)
                self.assertIn("q₂₄ [L/s/ha]", saved_headers)
                self.assertAlmostEqual(float(data[0][saved_headers.index("q₂₄ [L/s/ha]")]), 0.1269414576)
            with self.assertRaises(FileExistsError):
                create_project(temp, "Mlinište", {}, rows)

    def test_missing_values_calendar_and_duplicates(self):
        rows = mapped_rows(["Year", "Month", "Deficit"], [[2024, 2, "29,0"], [2024, 3, "-999,00"]], ",")
        result = calculate(Q24, rows)
        self.assertEqual(result["rows"][0]["inputs"]["d"], 29)
        self.assertIsNone(result["rows"][1]["value"])
        self.assertEqual(result["rows"][1]["missing"], ["D"])
        with self.assertRaises(ValueError):
            mapped_rows(["Year", "Month", "Deficit"], [[2024, 2, 1], [2024, 2, 2]])
        with self.assertRaises(ValueError):
            mapped_rows(["Year", "Month", "Deficit"], [[2024, 13, 1]])

    def test_formula_cases_and_groups(self):
        expr = ["Which", ["Greater", "D", 0], ["Divide", ["Set", "D"], ["Sqrt", 4]], "True", 0]
        self.assertEqual(walk(expr, {"D": 8}), 4)
        self.assertEqual(walk(expr, {"D": -8}), 0)
        with self.assertRaisesRegex(ValueError, "unknown|Unknown"):
            walk(expr, {}, check=True)
        with self.assertRaises(ValueError):
            walk(["Divide", 2, 0], {})

    def test_legacy_two_header_sheet(self):
        _, columns, rows = load_project(ROOT / "projects/project_test")
        self.assertIn("Tmax", columns)
        self.assertAlmostEqual(float(rows[0]["Tmax"]), 3.2)

