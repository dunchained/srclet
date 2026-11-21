import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from openpyxl import load_workbook
from PyQt6.QtWidgets import QApplication

from mortys import language_morty as lang
from plambas.frequency import DISTRIBUTIONS
from plambas.monthly_data import (
    ROOT,
    catalog,
    column_id,
    create_project,
    load_project,
    mapped_rows,
    read_table,
)
from plambas.monthly_results import calculate, export_result, project_methods
from windows.methods.catalog import MethodCatalog
from windows.project.project_opened import ProjectWindow
from windows.project.method_selection import ROLE
from windows.settings.settings import SettingsWindow


def example(name):
    headers, raw = read_table(ROOT / "examples/methods" / (name + ".csv"))
    fields = catalog()
    return mapped_rows([column_id(k, fields) for k in headers], raw)


class MethodWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(["tests"])

    def test_catalog_examples_and_excel_charts(self):
        with tempfile.TemporaryDirectory() as tmp:
            for method in project_methods():
                with self.subTest(method=method["id"]):
                    output = calculate(method, example(method["id"]))
                    path = Path(tmp) / (method["id"] + ".xlsx")
                    export_result(path, output)
                    book = load_workbook(path)
                    self.assertEqual(len(book["Charts"]._charts), 1)
                    self.assertGreaterEqual(book.active.max_row, 2)
                    book.close()

    def test_all_probability_methods_and_distributions(self):
        rows = example("weibull_normal")
        for method in [m for m in project_methods() if m.get("engine") == "frequency"]:
            for dist in DISTRIBUTIONS:
                rec = calculate({**method, "distribution": dist}, rows)["rows"][0]
                self.assertEqual(len(rec["plotting_positions"]), 12)
                self.assertGreater(rec["value"], 0)

    def test_gui_selection_by_inputs_then_chained_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            rows = example("workflow")
            path = create_project(tmp, "Station", {}, rows)
            project = ProjectWindow(str(path), lang.language())
            page = project.central_widget
            self.assertIs(project.tabs.currentWidget(), page)
            self.assertIn("fao56", page.preview)
            self.assertNotIn("mccabe2007", page.preview)
            self.assertNotIn("q24", page.preview)
            for method in ("fao56", "mccabe2007", "q24"):
                for i in range(page.tree.topLevelItemCount()):
                    group = page.tree.topLevelItem(i)
                    for j in range(group.childCount()):
                        if group.child(j).data(0, ROLE) == method:
                            page.tree.setCurrentItem(group.child(j))
                self.assertEqual(page.key(), method)
                page.add.click()
            page.save.click()
            self.assertEqual(len(list((path / "results").glob("*.json"))), 3)
            final = project.calculations.result
            self.assertEqual(final["method"]["id"], "q24")
            parent = json.loads((path / "results" / final["input_result"]).read_text())
            self.assertEqual(parent["method"]["id"], "mccabe2007")
            self.assertTrue(parent["input_result"])
            self.assertEqual(load_project(path)[2], rows)
            project.close()

    def test_same_editor_for_builtin_and_new_method(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / "methods", root / "methods")
            shutil.copytree(ROOT / "parameters", root / "parameters")
            with (
                patch("windows.methods.catalog.ROOT", root),
                patch("plambas.monthly_results.ROOT", root),
            ):
                editor = MethodCatalog("eto")
                editor.new()
                for k, v in {
                    "name": "Example ET",
                    "symbol": "ExampleET",
                    "unit": "mm/month",
                    "output": "ET0",
                }.items():
                    editor.fields[k].setText(v)
                editor.formula.setText("2*Tmean")
                editor.write()
                self.assertEqual(editor.status.text(), "")
                method = next(
                    m for m in project_methods() if m["symbol"] == "ExampleET"
                )
                self.assertEqual(
                    calculate(method, [{"Year": 2020, "Month": 1, "Tmean": 8}])["rows"][
                        0
                    ]["value"],
                    16,
                )
                for method in project_methods():
                    editor.fill(method)
                    editor.write()
                    self.assertEqual(editor.status.text(), "", method["id"])
                editor.close()

    def test_settings_apply_without_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = Path(tmp) / "settings.json"
            settings.write_bytes(lang.SETTINGS.read_bytes())
            original = lang.read_language()
            old_style = self.app.styleSheet()
            with patch.object(lang, "SETTINGS", settings):
                window = SettingsWindow()
                try:
                    for code, text in (
                        ("ba", "Zatvori"),
                        ("fr", "Fermer"),
                        ("en", "Close"),
                    ):
                        window.combo_box.setCurrentIndex(
                            window.combo_box.findData(code)
                        )
                        self.assertEqual(lang.tr("Close"), text)
                    window.boxes["input_text_size"].setCurrentIndex(2)
                    window.icons.setValue(28)
                    self.assertEqual(
                        json.loads(settings.read_text())["input_text_size"], 16
                    )
                    self.assertIn("16pt", self.app.styleSheet())
                    self.assertEqual(json.loads(settings.read_text())["icon_size"], 28)
                finally:
                    window.close()
                    lang.update_language(original)
                    self.app.setStyleSheet(old_style)
