from pathlib import Path
from zipfile import BadZipFile
import csv

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (QComboBox, QDialog, QFileDialog, QFormLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QStackedWidget, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)

from mortys.language_morty import bind, events, tr
from plambas.monthly_data import PROJECTS, catalog, column_id, create_project, mapped_rows, read_table
from widgets.formula_editor import LanguagePicker


class ProjectImport(QDialog):
    projectCreated = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        bind(self, "windowTitle", "New project")
        self.resize(820, 520)
        self.file = None
        self.rows = []
        self.headers = []
        self.fields = catalog()
        outer = QVBoxLayout(self)
        outer.addWidget(LanguagePicker())
        self.pages = QStackedWidget()
        outer.addWidget(self.pages)
        details = QWidget()
        form = QFormLayout(details)
        self.name = QLineEdit()
        self.folder = QLineEdit(str(PROJECTS))
        form.addRow(bind(QLabel(), "text", "Name"), self.name)
        line = QHBoxLayout()
        line.addWidget(self.folder)
        browse = bind(QPushButton(), "text", "Browse…")
        browse.clicked.connect(self.choose_folder)
        line.addWidget(browse)
        form.addRow(bind(QLabel(), "text", "Folder"), line)
        self.metadata = {}
        for key, label in [("weather_station", "Station"), ("weather_station_country", "Country"),
                           ("weather_station_latitude", "Latitude (°)"), ("weather_station_longitude", "Longitude (°)"),
                           ("weather_station_elevation", "Elevation (m)"), ("project_description", "Description")]:
            field = QLineEdit()
            form.addRow(bind(QLabel(), "text", label), field)
            self.metadata[key] = field
        self.pages.addWidget(details)

        page = QWidget()
        layout = QVBoxLayout(page)
        actions = QHBoxLayout()
        choose = bind(QPushButton(), "text", "Choose data file…")
        choose.clicked.connect(self.choose_file)
        actions.addWidget(choose)
        manual=bind(QPushButton(),"text","Enter data manually")
        manual.clicked.connect(self.manual_data)
        actions.addWidget(manual)
        self.delim = QComboBox()
        for label, value in [("Automatic", "auto"), ("Tab", "\t"), ("Semicolon", ";"), ("Comma", ","), ("Space", "space")]:
            self.delim.addItem(tr(label), value)
        self.delim.currentIndexChanged.connect(self.preview)
        actions.addWidget(bind(QLabel(), "text", "Delimiter"))
        actions.addWidget(self.delim)
        self.decimal = QComboBox()
        self.decimal.addItems([".", ","])
        actions.addWidget(bind(QLabel(), "text", "Decimal"))
        actions.addWidget(self.decimal)
        layout.addLayout(actions)
        self.filename = QLabel()
        layout.addWidget(self.filename)
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)
        self.pages.addWidget(page)
        self.error = QLabel()
        self.error.setWordWrap(True)
        outer.addWidget(self.error)
        nav = QHBoxLayout()
        outer.addLayout(nav)
        self.back = bind(QPushButton(), "text", "Back")
        self.back.clicked.connect(lambda: self.step(0))
        self.next = bind(QPushButton(), "text", "Next")
        self.next.clicked.connect(self.next_page)
        self.save_close = bind(QPushButton(), "text", "Save and close")
        self.save_close.clicked.connect(lambda: self.finish(False))
        self.save = bind(QPushButton(), "text", "Save and open")
        self.save.clicked.connect(lambda: self.finish(True))
        cancel = bind(QPushButton(), "text", "Cancel")
        cancel.clicked.connect(self.reject)
        for button in (self.back, self.next, self.save_close, self.save, cancel):
            nav.addWidget(button)
        self.step(0)
        events.changed.connect(self.retranslate)

    def step(self, page):
        self.pages.setCurrentIndex(page)
        self.back.setVisible(bool(page))
        self.next.setVisible(not page)
        self.save.setVisible(bool(page))
        self.save_close.setVisible(bool(page))
        self.error.clear()

    def choose_folder(self):
        name = QFileDialog.getExistingDirectory(self, tr("Folder"), self.folder.text())
        if name:
            self.folder.setText(name)

    def next_page(self):
        name = self.name.text().strip()
        if not name or name in (".", "..") or "/" in name or "\\" in name:
            self.error.setText(tr("Invalid project name."))
        elif (Path(self.folder.text()) / name).exists():
            self.error.setText(tr("Project folder already exists."))
        else:
            self.step(1)

    def manual_data(self):
        from windows.project.data_editor import DataEditor
        dialog=DataEditor(parent=self)
        if dialog.exec():
            try:
                path=create_project(self.folder.text(),self.name.text().strip(),
                                    {k:f.text().strip() for k,f in self.metadata.items()},dialog.rows)
                self.projectCreated.emit(str(path))
                self.accept()
            except (ValueError,OSError) as exc:self.error.setText(tr(str(exc)))

    def choose_file(self):
        name, _ = QFileDialog.getOpenFileName(self, tr("Monthly data"), "", "TXT / CSV / Excel (*.txt *.tsv *.csv *.xlsx)")
        if name:
            self.file = Path(name)
            self.preview()

    def retranslate(self):
        for i, label in enumerate(("Automatic", "Tab", "Semicolon", "Comma", "Space")):
            self.delim.setItemText(i, tr(label))
        for i in range(self.table.columnCount()):
            combo = self.table.cellWidget(0, i)
            if combo:
                for j in range(combo.count()):
                    key = combo.itemData(j)
                    combo.setItemText(j, self.field_label(key))

    def field_label(self, key):
        if not key:
            return tr("Skip column")
        name, unit = self.fields[key]
        return f"{tr(name)} ({unit})" if unit else tr(name)

    def preview(self):
        if not self.file:
            return
        self.rows = []
        self.table.clear()
        self.table.setRowCount(0)
        self.error.clear()
        self.filename.setText(str(self.file))
        try:
            self.headers, self.rows = read_table(self.file, self.delim.currentData())
        except (OSError, ValueError, BadZipFile, csv.Error) as error:
            self.error.setText(tr(str(error)))
            return
        self.table.setColumnCount(len(self.headers))
        self.table.setRowCount(1 + min(25, len(self.rows)))
        self.table.setHorizontalHeaderLabels(self.headers)
        for i, header in enumerate(self.headers):
            combo = QComboBox()
            combo.addItem(tr("Skip column"), None)
            for key in self.fields:
                combo.addItem(self.field_label(key), key)
            key = column_id(header, self.fields)
            combo.setCurrentIndex(combo.findData(key) if key else 0)
            self.table.setCellWidget(0, i, combo)
        for i, row in enumerate(self.rows[:25], 1):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem("" if val is None else str(val)))
        self.table.resizeColumnsToContents()

    def finish(self, open_after):
        if not self.rows:
            self.error.setText(tr("No data file selected."))
            return
        try:
            mapping = [self.table.cellWidget(0, col).currentData() for col in range(len(self.headers))]
            rows = mapped_rows(mapping, self.rows, self.decimal.currentText())
            metadata = {key: field.text().strip() for key, field in self.metadata.items()}
            metadata.update(skip_rows="1", source_file=self.file.name,
                            import_columns=[{"header": h, "id": k} for h, k in zip(self.headers, mapping)],
                            decimal=self.decimal.currentText(), delimiter=self.delim.currentData())
            path = create_project(self.folder.text(), self.name.text().strip(), metadata, rows)
        except (ValueError, OSError) as error:
            self.error.setText(tr(str(error)))
            return
        if open_after:
            self.projectCreated.emit(str(path))
        self.accept()

