"""Regenerate screenshots of the interface using only temporary project data."""

import argparse
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--disable-gpu")

from PyQt6.QtCore import QCoreApplication, QEvent, QTimer
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication, QDialog
from mortys import language_morty as lang
from mortys.font_morty import apply_settings
from plambas.monthly_data import create_project, mapped_rows, read_table, save_json
from plambas.monthly_results import project_methods
from widgets.formula_editor import FormulaEditor
from windows.settings.settings import SettingsWindow
from windows.project.monthly_import import ProjectImport
from windows.project.method_selection import ROLE
from windows.project.project_opened import ProjectWindow
from windows.project.data_editor import DataEditor
from windows.methods.catalog import MethodCatalog
from windows.parameters.catalog import ParameterCatalog


def wait_for(predicate):
    for _ in range(250):
        if predicate():
            return
        QTest.qWait(30)
    raise RuntimeError("The interface did not finish rendering")


def capture(window, path, width, height):
    window.showNormal()
    QApplication.processEvents()
    QTest.qWait(50)
    window.resize(width, height)
    window.show()
    QApplication.processEvents()
    QTest.qWait(100)
    if not window.grab().save(str(path)):
        raise OSError(path)


def select(page, key):
    for i in range(page.tree.topLevelItemCount()):
        group = page.tree.topLevelItem(i)
        for j in range(group.childCount()):
            item = group.child(j)
            if item.data(0, ROLE) == key:
                page.tree.setCurrentItem(item)
                page.tree.scrollToItem(item)
                return
    raise KeyError(key)


def generate(code):
    destination = ROOT / "srclet/manual" / code
    with tempfile.TemporaryDirectory() as temp:
        home = Path(temp)
        local_settings = home / "settings.json"
        save_json(
            local_settings,
            {
                "menu_font_size": 12,
                "text_font_size": 12,
                "input_text_size": 12,
                "icon_size": 24,
                "language": code,
            },
        )
        with patch.object(lang, "SETTINGS", local_settings):
            lang.update_language(code)
            lang.qt_language()
            apply_settings()
            settings = SettingsWindow()
            capture(settings, destination / "settings.png", 560, 310)
            settings.close()
            wizard = ProjectImport()
            wizard.folder.setText(temp)
            wizard.name.setText("Sarajevo")
            wizard.next_page()
            wizard.file = Path("examples/methods/workflow.csv")
            wizard.preview()
            capture(wizard, destination / "import.png", 1180, 620)
            wizard.close()
            headers, raw = read_table(wizard.file)
            path = create_project(
                home,
                "Sarajevo",
                {
                    "weather_station": "Sarajevo",
                    "weather_station_latitude": "43.85",
                    "weather_station_elevation": "500",
                },
                mapped_rows(headers, raw),
            )
            data = DataEditor(path)
            capture(data, destination / "data.png", 1100, 560)
            data.close()
            params = ParameterCatalog("basic")
            params.list.setCurrentRow(
                next(
                    i for i, (_, d) in enumerate(params.items) if d["symbol"] == "Tmin"
                )
            )
            capture(params, destination / "parameters.png", 1000, 550)
            params.close()
            project = ProjectWindow(str(path), lang.language())
            page = project.central_widget
            select(page, "fao56")
            page.append_method()
            select(page, "mccabe2007")
            capture(project, destination / "selection.png", 1280, 850)
            page.append_method()
            select(page, "weibull_normal")

            def screenshot_options():
                dialog = QApplication.activeModalWidget()
                if isinstance(dialog, QDialog):
                    capture(dialog, destination / "frequency.png", 560, 300)
                    dialog.reject()

            QTimer.singleShot(120, screenshot_options)
            page.configure()
            page.execute()
            capture(project, destination / "results.png", 1240, 720)
            project.close()
            catalog = MethodCatalog("wb")
            catalog.list.setCurrentRow(
                next(i for i, m in enumerate(catalog.items) if m["id"] == "mccabe2007")
            )
            capture(catalog, destination / "catalog.png", 1220, 800)
            catalog.close()
            q = next(m for m in project_methods() if m["id"] == "q24")
            editor = FormulaEditor(
                q,
                {"D": "mm", "d": lang.tr("Days in month")},
                [("2000-08", {"D": 34, "d": 31})],
            )
            editor.show()
            wait_for(lambda: editor.ready)
            editor.read(False)
            wait_for(lambda: editor.last_value is not None)
            capture(editor, destination / "formula.png", 1000, 590)
            editor.close()
            for widget in (settings, wizard, data, params, project, catalog, editor):
                widget.deleteLater()
            QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
            QApplication.processEvents()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "language", choices=("ba", "en", "fr", "all"), default="all", nargs="?"
    )
    chosen = parser.parse_args().language
    os.chdir(ROOT)
    app = QApplication(["SRCLET-manual"])
    app.setQuitOnLastWindowClosed(False)
    for code in ("ba", "en", "fr") if chosen == "all" else (chosen,):
        generate(code)
