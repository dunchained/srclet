from collections import Counter
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from mortys.language_morty import bind, events, tr
from plambas.frequency import DISTRIBUTIONS
from plambas.hydrology import PARAMETER_LABELS
from plambas.method_series import add_outputs
from plambas.monthly_data import period_values
from plambas.monthly_results import calculate, store_result

GROUPS = {
    "eto": "Evapotranspiration methods",
    "wb": "Water balance methods",
    "frequency": "Frequency analysis",
    "hydro": "Irrigation hydromodule",
    "others": "Other methods",
}
ROLE = Qt.ItemDataRole.UserRole


class MethodSelection(QWidget):
    def __init__(self, panel, parent):
        super().__init__(parent)
        self.panel = panel
        self.plan = []
        self.preview = {}
        self.options = {}
        outer = QVBoxLayout(self)
        self.inputs = QLabel()
        self.inputs.setWordWrap(True)
        outer.addWidget(self.inputs)
        bar = QHBoxLayout()
        self.sources = QComboBox()
        self.sources.currentIndexChanged.connect(self.source_changed)
        bar.addWidget(bind(QLabel(), "text", "Working data"))
        bar.addWidget(self.sources, 1)
        self.series = QComboBox()
        self.series.currentIndexChanged.connect(self.refresh)
        bar.addWidget(bind(QLabel(), "text", "Series for frequency analysis"))
        bar.addWidget(self.series)
        outer.addLayout(bar)
        dates = QHBoxLayout()
        self.first = QComboBox()
        self.last = QComboBox()
        for label, box in (("From month", self.first), ("To month", self.last)):
            dates.addWidget(bind(QLabel(), "text", label))
            dates.addWidget(box)
            box.currentIndexChanged.connect(self.range_changed)
        outer.addLayout(dates)
        self.tree = QTreeWidget()
        self.tree.setColumnCount(4)
        self.tree.itemDoubleClicked.connect(lambda *_: self.append_method())
        self.tree.currentItemChanged.connect(self.buttons)
        outer.addWidget(self.tree, 3)
        line = QGridLayout()
        self.editors = bind(QPushButton(), "text", "Method catalog")
        self.editors.clicked.connect(self.open_catalog)
        line.addWidget(self.editors, 0, 0)
        self.data_button = bind(QPushButton(), "text", "Edit project data")
        self.data_button.clicked.connect(self.open_data)
        line.addWidget(self.data_button, 0, 1)
        self.config = bind(QPushButton(), "text", "Method parameters")
        self.config.clicked.connect(self.configure)
        line.addWidget(self.config, 1, 0)
        self.add = bind(QPushButton(), "text", "Select method")
        self.add.clicked.connect(self.append_method)
        line.addWidget(self.add, 1, 1)
        outer.addLayout(line)
        outer.addWidget(bind(QLabel(), "text", "Selected calculation sequence"))
        self.queue = QListWidget()
        outer.addWidget(self.queue, 1)
        self.message = QLabel()
        self.message.setWordWrap(True)
        outer.addWidget(self.message)
        line = QHBoxLayout()
        self.undo = bind(QPushButton(), "text", "Remove last method")
        self.undo.clicked.connect(self.pop)
        line.addWidget(self.undo)
        self.save = bind(QPushButton(), "text", "Calculate and save")
        self.save.clicked.connect(self.execute)
        line.addWidget(self.save)
        outer.addLayout(line)
        events.changed.connect(self.refresh)
        self.sync_sources()

    def sync_sources(self, selected=None):
        self.sources.blockSignals(True)
        self.sources.clear()
        for i in range(self.panel.input_choice.count()):
            self.sources.addItem(
                self.panel.input_choice.itemText(i), self.panel.input_choice.itemData(i)
            )
        self.sources.setCurrentIndex(max(0, self.sources.findData(selected)))
        self.sources.blockSignals(False)
        self.source_changed()

    def source_changed(self):
        index = self.panel.input_choice.findData(self.sources.currentData())
        self.panel.input_choice.setCurrentIndex(max(0, index))
        self.plan.clear()
        dates = []
        for row in self.panel.rows:
            try:
                y, m, _ = period_values(row)
                dates.append(f"{y:04}-{m:02}")
            except ValueError:
                continue
        dates = sorted(set(dates))
        for box in (self.first, self.last):
            box.blockSignals(True)
            box.clear()
            box.addItems(dates)
            box.setCurrentIndex(0 if box is self.first else len(dates) - 1)
            box.blockSignals(False)
        self.refresh()

    def range_changed(self):
        self.plan.clear()
        self.refresh()

    def refresh(self, *_):
        if self.plan:
            rows = self.plan[-1][1]
        else:
            rows = []
            for row in self.panel.rows:
                try:
                    y, m, _ = period_values(row)
                except ValueError:
                    continue
                if (
                    self.first.currentText()
                    <= f"{y:04}-{m:02}"
                    <= self.last.currentText()
                ):
                    rows.append(row)
        self.rows = rows
        headers = list(rows[0]) if rows else []
        old = self.series.currentData()
        self.series.blockSignals(True)
        self.series.clear()
        for key in headers:
            if key not in ("Year", "Month") and any(
                r.get(key) is not None for r in rows
            ):
                self.series.addItem(key, key)
        pos = self.series.findData(old)
        self.series.setCurrentIndex(
            pos if pos >= 0 else max(0, self.series.findData("Deficit"))
        )
        self.series.blockSignals(False)
        self.sources.setItemText(0, tr("Original inputs"))
        self.inputs.setText(
            self.panel.project.name
            + "  ·  "
            + tr("Input columns")
            + "  ·  "
            + ", ".join(headers)
        )
        selected = self.key()
        self.tree.clear()
        self.tree.setHeaderLabels(
            [tr("Method"), tr("Output"), tr("Unit"), tr("Valid months / sample size")]
        )
        self.preview.clear()
        groups = {}
        used = {record["method"]["id"] for record, _ in self.plan}
        for base in self.panel.methods:
            if base["id"] in used:
                continue
            method = {**base, **self.options.get(base["id"], {})}
            if method.get("engine") == "frequency":
                field = self.series.currentData()
                if not field:
                    continue
                method = dict(
                    method,
                    series=field,
                    unit=self.panel.fields.get(field, ("", method["unit"]))[1],
                )
                counts = Counter(
                    r.get("Month") for r in rows if r.get(field) is not None
                )
                if not counts or max(counts.values()) < 2:
                    continue
                if base["id"] not in self.options:
                    month = int(method["parameters"]["month"])
                    if counts[month] < 2:
                        month = max(counts, key=counts.get)
                    method["parameters"] = {
                        **method["parameters"],
                        "month": month,
                        "years": min(method["parameters"]["years"], counts[month]),
                    }
            try:
                record = calculate(method, rows, self.panel.meta)
            except (ValueError, TypeError, ArithmeticError, KeyError):
                continue
            record["input_period"] = [self.first.currentText(), self.last.currentText()]
            self.preview[method["id"]] = record
            group = method.get("group", "others")
            if group not in groups:
                groups[group] = QTreeWidgetItem([tr(GROUPS[group])])
                self.tree.addTopLevelItem(groups[group])
            item = QTreeWidgetItem(
                [
                    tr(method["name"]),
                    method.get("output") or method.get("series", ""),
                    tr(method["unit"]),
                    str(record["rows"][0]["inputs"].get("n", 0))
                    if method.get("engine")
                    else f"{sum(r['value'] is not None for r in record['rows'])} / {len(rows)}",
                ]
            )
            item.setData(0, ROLE, method["id"])
            groups[group].addChild(item)
            if selected == method["id"]:
                self.tree.setCurrentItem(item)
        self.tree.expandAll()
        self.tree.resizeColumnToContents(0)
        for col in range(1, 4):
            self.tree.resizeColumnToContents(col)
        self.queue.clear()
        for result, _ in self.plan:
            method = result["method"]
            self.queue.addItem(
                tr(method["name"])
                + "  →  "
                + (method.get("output") or method.get("series", ""))
            )
        if not self.preview:
            self.message.setText(tr("No methods match these inputs."))
        else:
            self.message.clear()
        self.buttons()

    def key(self):
        item = self.tree.currentItem()
        return item.data(0, ROLE) if item else None

    def buttons(self, *_):
        key = self.key()
        self.add.setEnabled(key in self.preview)
        self.config.setEnabled(
            bool(
                key
                and key in self.preview
                and self.preview[key]["method"].get("parameters")
            )
        )
        self.undo.setEnabled(bool(self.plan))
        self.save.setEnabled(bool(self.plan))

    def configure(self):
        key = self.key()
        if key not in self.preview:
            return
        method = self.preview[key]["method"]
        dialog = QDialog(self)
        bind(dialog, "windowTitle", "Method parameters")
        form = QFormLayout(dialog)
        boxes = {}
        for k, val in method["parameters"].items():
            box = QDoubleSpinBox()
            box.setRange(
                1 if k == "month" else 2 if k == "years" else -1e8,
                12 if k == "month" else 1e8,
            )
            box.setDecimals(0 if k in ("month", "years") else 6)
            box.setValue(val)
            form.addRow(bind(QLabel(), "text", PARAMETER_LABELS.get(k, k)), box)
            boxes[k] = box
        dist = QComboBox()
        if method.get("engine") == "frequency":
            for k, name in DISTRIBUTIONS.items():
                dist.addItem(tr(name), k)
            dist.setCurrentIndex(dist.findData(method.get("distribution", "normal")))
            form.addRow(bind(QLabel(), "text", "Distribution"), dist)
        error = QLabel()
        form.addRow(error)
        apply = bind(QPushButton(), "text", "Apply")

        def accept():
            opts = {"parameters": {k: box.value() for k, box in boxes.items()}}
            if dist.count():
                opts["distribution"] = dist.currentData()
            try:
                calculate({**method, **opts}, self.rows, self.panel.meta)
            except (ValueError, ArithmeticError, KeyError) as exc:
                error.setText(tr(str(exc)))
                return
            self.options[key] = opts
            dialog.accept()

        apply.clicked.connect(accept)
        form.addRow(apply)
        if dialog.exec():
            self.refresh()

    def append_method(self):
        if self.key() in self.preview:
            record = self.preview[self.key()]
            combined = add_outputs(self.rows, record)
            self.plan.append((record, combined))
            if record["method"].get("group") == "wb" and "Deficit" in combined[0]:
                self.series.blockSignals(True)
                if self.series.findData("Deficit") < 0:
                    self.series.addItem("Deficit", "Deficit")
                self.series.setCurrentIndex(self.series.findData("Deficit"))
                self.series.blockSignals(False)
            self.refresh()

    def pop(self):
        if self.plan:
            self.plan.pop()
        self.refresh()

    def execute(self):
        if not self.plan:
            return
        parent = self.sources.currentData()
        written = []
        try:
            for record, _ in self.plan:
                record.update(
                    input_result=Path(parent).name if parent else "",
                    station_metadata=self.panel.meta,
                    station=self.panel.meta.get("weather_station", ""),
                )
                parent = store_result(self.panel.project, record)
                written.append(parent)
        except OSError as exc:
            for path in reversed(written):
                path.unlink(missing_ok=True)
            self.message.setText(str(exc))
            return
        self.panel.reload_history(parent)
        # A statistical result is a summary, not a monthly input layer.
        self.sync_sources(
            str(parent)
            if self.panel.input_choice.findData(str(parent)) >= 0
            else self.sources.currentData()
        )
        self.panel.view_saved(self.panel.history.findData(str(parent)))
        self.window().tabs.setCurrentWidget(self.panel)

    def open_catalog(self):
        from windows.methods.catalog import MethodCatalog

        dialog = MethodCatalog(parent=self)
        dialog.exec()

    def open_data(self):
        from windows.project.data_editor import DataEditor

        if DataEditor(self.panel.project, self).exec():
            self.panel.reload_data()
            self.sync_sources()
