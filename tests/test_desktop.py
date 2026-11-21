import os
import shutil
import tempfile
import unittest
from contextlib import chdir
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication, QDialog

from mortys import language_morty as i18n
from plambas.monthly_data import ROOT, create_project
from plambas.monthly_results import calculate, project_methods
from srclet import MainWindow
from widgets.formula_editor import FormulaEditor
from windows.methods.eto_methods_add import AddET0Method
from windows.project.project_opened import ProjectWindow


class DesktopWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(["SRCLET-tests"])

    def wait_for(self, condition):
        for _ in range(160):
            if condition():
                return
            QTest.qWait(50)
        self.fail("Qt did not complete the operation")

    def test_mliniste_desktop(self):
        with tempfile.TemporaryDirectory() as temp:
            settings = Path(temp) / "settings.json"
            settings.write_bytes(i18n.SETTINGS.read_bytes())
            original = i18n.read_language()
            with patch.object(i18n, "SETTINGS", settings):
                try:
                    window = MainWindow()
                    window.new_project_window()
                    wizard = window.window
                    wizard.name.setText("Mlinište")
                    wizard.folder.setText(temp)
                    wizard.metadata["weather_station"].setText("Mlinište")
                    wizard.next.click()
                    wizard.file = ROOT / "examples/mliniste.csv"
                    wizard.preview()
                    self.assertEqual(wizard.table.cellWidget(0, 2).currentData(), "Deficit")
                    wizard.save.click()
                    project = window.project_window
                    panel = project.calculations
                    editor = FormulaEditor(panel.method, {"D": "mm", "d": "days"},
                                           [("2000-08", {"D": 34, "d": 31})], project)
                    editor.show()
                    self.wait_for(lambda: editor.ready)
                    editor.web.page().runJavaScript(r'openFormula("\\frac{10000D}{86400d}", null)')
                    i18n.update_language("ba")
                    self.assertEqual(editor.windowTitle(), "Editor formula")
                    self.assertEqual(panel.run.text(), "Izračunaj i sačuvaj")
                    self.assertEqual(editor.values.item(0, 1).text(), "34")
                    editor.read(False)
                    self.wait_for(lambda: "0,126941" in editor.status.text())
                    editor.read(True)
                    self.wait_for(lambda: editor.result() == QDialog.DialogCode.Accepted)
                    # Pass the real editor output through the project dialog acceptance path.
                    with patch("windows.project.calculations.FormulaEditor", return_value=editor), patch.object(editor, "exec", return_value=1):
                        panel.edit_formula()
                    panel.run.click()
                    self.assertAlmostEqual(panel.result["rows"][0]["value"], .1269414576)
                    reopened = ProjectWindow(str(Path(temp) / "Mlinište"), i18n.language())
                    self.assertEqual(reopened.calculations.method["latex"], editor.definition["latex"])
                    self.assertEqual(reopened.calculations.result, panel.result)
                    i18n.update_language("fr")
                    self.assertEqual(reopened.calculations.run.text(), "Calculer et enregistrer")
                    reopened.close()
                    project.close()
                    window.close()
                    editor.deleteLater()
                finally:
                    i18n.update_language(original)


    def test_catalog_method_can_be_saved_and_run(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / "methods", root / "methods")
            for folder in ("parameters", "srclet"):
                shutil.copytree(ROOT / folder, root / folder)
            with chdir(root), patch("plambas.monthly_results.ROOT", root):
                window = AddET0Method(i18n.language(), None)
                window.method_name.setText("Test temperature")
                window.method_unit.setText("°C")
                window.method_symbol.setText("Tplus")
                box = next(window.bp_layout.itemAt(i).widget() for i in range(window.bp_layout.count())
                           if window.bp_layout.itemAt(i).widget().text() == "Tmax")
                box.click()
                self.assertEqual(window.selected_bp_list.text(), "Tmax")
                window.method_formula.setText(r"\mathrm{Tmax}+1")
                window.method_formula.tree = ["Add", "Tmax", 1]
                window.btn_save.click()
                method = next(m for m in project_methods() if m.get("symbol") == "Tplus")
                run = calculate(method, [{"Year": 2000, "Month": 8, "Tmax": 21}])
                self.assertEqual(run["rows"][0]["value"], 22)
                window.msg.close()
                window.close()

    def test_existing_projects_open(self):
        for path in sorted((ROOT / "projects").iterdir()):
            if not (path / "data.xlsx").is_file():
                continue
            with self.subTest(project=path.name):
                window = ProjectWindow(str(path.resolve()), i18n.language())
                self.assertTrue(window.calculations.rows)
                window.close()

    def test_saved_series_chain(self):
        with tempfile.TemporaryDirectory() as temp:
            rows = [{"Year": yr, "Month": mo, "Tmin": 10., "Tmax": 25., "Tmean": 17.5,
                     "u2": 2., "RHmean": 70., "G": 0., "Rn": 13., "PRCP": 40.}
                    for yr in range(2001, 2011) for mo in range(1, 13)]
            path = create_project(temp, "Station", {"weather_station_elevation": "500"}, rows)
            from windows.project.calculations import MonthlyCalculations
            panel = MonthlyCalculations(path)
            for idx, key in ((1, "ET0"), (2, "Deficit")):
                panel.choices.setCurrentIndex(idx)
                self.assertTrue(panel.run.isEnabled(), panel.status.text())
                panel.run.click()
                self.assertEqual(panel.result["method"]["output"], key)
                panel.input_choice.setCurrentIndex(1 if idx == 1 else next(i for i in
                    range(panel.input_choice.count()) if panel.input_choice.itemText(i).startswith(key)))
                self.assertIn(key, panel.headers)
            panel.choices.setCurrentIndex(3)
            panel.run.click()
            self.assertEqual(panel.result["rows"][0]["inputs"]["n"], 10)
            self.assertGreater(panel.result["rows"][0]["value"], 0)
            self.assertTrue(panel.result["input_result"])
            self.assertEqual(len(list((path / "results").glob("*.json"))), 3)
