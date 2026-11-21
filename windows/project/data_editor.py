from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)
from mortys.language_morty import bind, events, tr
from plambas.monthly_data import catalog, load_project, mapped_rows, save_json


class DataEditor(QDialog):
    def __init__(self, project=None, parent=None):
        super().__init__(parent)
        self.project = project
        bind(self, "windowTitle", "Edit project data")
        self.resize(850, 550)
        meta, self.headers, rows = (
            load_project(project) if project else ({}, ["Year", "Month"], [{}])
        )
        self.metadata = {}
        self.rows = []
        layout = QVBoxLayout(self)
        form = QFormLayout()
        if project:
            for key, label in (
                ("weather_station_latitude", "Latitude (°)"),
                ("weather_station_elevation", "Elevation (m)"),
            ):
                field = QLineEdit(str(meta.get(key) or ""))
                self.metadata[key] = field
                form.addRow(bind(QLabel(), "text", label), field)
        layout.addLayout(form)
        self.table = QTableWidget(len(rows), len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        for i, row in enumerate(rows):
            for j, key in enumerate(self.headers):
                value = row.get(key)
                self.table.setItem(
                    i, j, QTableWidgetItem("" if value is None else str(value))
                )
        layout.addWidget(self.table)
        bar = QHBoxLayout()
        self.field = QComboBox()
        bar.addWidget(self.field)
        for label, fn in (
            ("Add column", self.column),
            ("Add row", lambda: self.table.insertRow(self.table.rowCount())),
            ("Remove row", lambda: self.table.removeRow(self.table.currentRow())),
        ):
            b = bind(QPushButton(), "text", label)
            b.clicked.connect(fn)
            bar.addWidget(b)
        layout.addLayout(bar)
        self.error = QLabel()
        layout.addWidget(self.error)
        action = bind(QPushButton(), "text", "Save data")
        action.clicked.connect(self.save)
        layout.addWidget(action)
        events.changed.connect(self.translate)
        self.translate()

    def translate(self):
        key = self.field.currentData()
        self.field.clear()
        for k, (name, unit) in catalog().items():
            if k not in self.headers:
                self.field.addItem(tr(name) + " · " + k + " " + unit, k)
        if self.field.findData(key) >= 0:
            self.field.setCurrentIndex(self.field.findData(key))

    def column(self):
        key = self.field.currentData()
        if key:
            self.headers.append(key)
            self.table.insertColumn(len(self.headers) - 1)
            self.table.setHorizontalHeaderLabels(self.headers)
            self.translate()

    def save(self):
        try:
            raw = [
                [
                    self.table.item(i, j).text() if self.table.item(i, j) else ""
                    for j in range(len(self.headers))
                ]
                for i in range(self.table.rowCount())
            ]
            if not raw:
                raise ValueError("At least one valid month is required.")
            self.rows = mapped_rows(self.headers, raw, ",")
            meta = {k: w.text().strip() for k, w in self.metadata.items()}
            for k, v in meta.items():
                if v:
                    n = float(v.replace(",", "."))
                    if not (
                        (-90 <= n <= 90)
                        if k.endswith("latitude")
                        else (-500 <= n <= 9000)
                    ):
                        raise ValueError("Invalid station coordinates.")
            if self.project:
                save_json(
                    self.project / "inputs.json",
                    {"rows": self.rows, "columns": self.headers, "metadata": meta},
                )
            self.accept()
        except (ValueError, OSError) as exc:
            self.error.setText(tr(str(exc)))
