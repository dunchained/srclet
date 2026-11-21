import json
from pathlib import Path

from PyQt6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from mortys.language_morty import bind, events, format_number, tr
from plambas.hydrology import PARAMETER_LABELS
from plambas.method_series import add_outputs, prepare
from plambas.formulas import symbols_used
from plambas.monthly_data import catalog, load_project, save_json
from plambas.monthly_results import (
    calculate,
    export_result,
    project_methods,
    store_result,
    symbol_values,
)
from widgets.formula_editor import FormulaEditor, LanguagePicker


class MonthlyCalculations(QWidget):
    def __init__(self, project, *, results_only=False):
        super().__init__()
        self.project = Path(project)
        self.meta, self.headers, self.rows = load_project(self.project)
        self.input_path = None
        self.base_rows = self.rows
        self.base_headers = self.headers
        self.fields = catalog()
        self.methods = project_methods()
        self.formulas_path = self.project / "formulas.json"
        overrides = self.read_overrides()
        self.methods = [
            {**method, **overrides.get(method["id"], {})} for method in self.methods
        ]
        self.result = None
        self.method = self.methods[0] if self.methods else {}
        layout = QVBoxLayout(self)
        top = QHBoxLayout()
        self.station = QLabel()
        top.addWidget(self.station, 1)
        top.addWidget(LanguagePicker())
        layout.addLayout(top)
        self.input_summary = QLabel()
        self.input_summary.setWordWrap(True)
        layout.addWidget(self.input_summary)
        controls = QWidget()
        settings_layout = QVBoxLayout(controls)
        layout.addWidget(controls)
        controls.setVisible(not results_only)
        form = QFormLayout()
        self.input_choice = QComboBox()
        self.input_choice.currentIndexChanged.connect(self.select_input)
        form.addRow(bind(QLabel(), "text", "Working data"), self.input_choice)
        self.choices = QComboBox()
        for method in self.methods:
            self.choices.addItem(method["name"])
        self.choices.currentIndexChanged.connect(self.select_method)
        method_row = QHBoxLayout()
        method_row.addWidget(self.choices, 1)
        refresh = bind(QPushButton(), "text", "Refresh methods list")
        refresh.clicked.connect(self.refresh_catalog)
        method_row.addWidget(refresh)
        form.addRow(bind(QLabel(), "text", "Method"), method_row)
        settings_layout.addLayout(form)
        self.parameter_form = QFormLayout()
        self.parameter_boxes = {}
        settings_layout.addLayout(self.parameter_form)
        self.equation = QLabel()
        self.equation.setWordWrap(True)
        settings_layout.addWidget(self.equation)
        actions = QHBoxLayout()
        self.edit = bind(QPushButton(), "text", "Edit formula…")
        self.edit.clicked.connect(self.edit_formula)
        actions.addWidget(self.edit)
        self.run = bind(QPushButton(), "text", "Calculate and save")
        self.run.clicked.connect(self.run_method)
        actions.addWidget(self.run)
        settings_layout.addLayout(actions)
        self.status = QLabel()
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        self.results_only = results_only
        bar = QHBoxLayout()
        bar.addWidget(bind(QLabel(), "text", "Saved results"))
        self.history = QComboBox()
        self.history.currentIndexChanged.connect(self.view_saved)
        bar.addWidget(self.history, 1)
        self.export = bind(QPushButton(), "text", "Export…")
        self.export.clicked.connect(self.export_file)
        bar.addWidget(self.export)
        layout.addLayout(bar)
        self.result_details = QLabel()
        self.result_details.setWordWrap(True)
        layout.addWidget(self.result_details)
        self.table = QTableWidget(0, 4)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)
        self.reload_history()
        self.configure_parameters()
        self.retranslate()
        events.changed.connect(self.retranslate)

    def read_overrides(self):
        if self.formulas_path.exists():
            return json.loads(self.formulas_path.read_text(encoding="utf-8"))
        return {}

    def retranslate(self):
        for index, method in enumerate(self.methods):
            self.choices.setItemText(index, tr(method["name"]))
        self.input_choice.setItemText(0, tr("Original inputs"))
        self.station.setText(
            f"{self.project.name}  ·  {self.meta.get('weather_station', '')}"
        )
        self.input_summary.setText(
            tr("Input columns") + " · " + ", ".join(self.headers)
        )
        if self.result:
            self.view_saved(self.history.currentIndex())
        for i, source in enumerate(("Year", "Month", "Result", "Missing")):
            if self.table.horizontalHeaderItem(i):
                self.table.horizontalHeaderItem(i).setText(tr(source))
        self.refresh_method()
        if self.results_only:
            self.status.clear()

    def select_method(self, index):
        self.method = self.methods[index] if self.methods else {}
        self.configure_parameters()
        self.refresh_method()

    def refresh_catalog(self):
        selected = self.method.get("id")
        overrides = self.read_overrides()
        self.methods = [{**m, **overrides.get(m["id"], {})} for m in project_methods()]
        self.choices.blockSignals(True)
        self.choices.clear()
        for method in self.methods:
            self.choices.addItem(method["name"])
        index = next((i for i, m in enumerate(self.methods) if m["id"] == selected), 0)
        self.choices.setCurrentIndex(index)
        self.choices.blockSignals(False)
        self.select_method(index)
        self.retranslate()

    def choose_symbol(self, symbol):
        self.refresh_catalog()
        if not symbol:
            return
        for i, method in enumerate(self.methods):
            if method.get("symbol") == symbol:
                self.choices.setCurrentIndex(i)
                return
        self.status.setText(
            symbol
            + " · "
            + tr("Save this catalog formula in the visual editor to calculate it.")
        )
        self.run.setEnabled(False)

    def configure_parameters(self):
        while self.parameter_form.rowCount():
            self.parameter_form.removeRow(0)
        self.parameter_boxes.clear()
        for key, default in self.method.get("parameters", {}).items():
            box = QDoubleSpinBox()
            box.setRange(-1e8, 1e8)
            box.setDecimals(0 if key in ("month", "years") else 6)
            if key in ("direct", "runoff", "melt"):
                box.setRange(0, 1)
                box.setSingleStep(0.01)
            elif key == "month":
                box.setRange(1, 12)
            elif key == "years":
                box.setRange(2, 1000)
            box.setValue(default)
            box.valueChanged.connect(self.refresh_method)
            self.parameter_boxes[key] = box
            self.parameter_form.addRow(
                bind(QLabel(), "text", PARAMETER_LABELS.get(key, key)), box
            )

    def select_input(self, index):
        self.input_path = self.input_choice.itemData(index)
        self.rows = self.base_rows
        self.headers = self.base_headers
        if self.input_path:
            try:
                path = Path(self.input_path)
                layers = []
                seen = set()
                while path:
                    if path.name in seen or path.parent != self.project / "results":
                        raise ValueError("Invalid result history.")
                    seen.add(path.name)
                    record = json.loads(path.read_text(encoding="utf-8"))
                    layers.append(record)
                    parent = record.get("input_result")
                    path = self.project / "results" / parent if parent else None
                self.rows = [dict(row) for row in self.base_rows]
                self.headers = list(self.base_headers)
                for record in reversed(layers):
                    self.rows = add_outputs(self.rows, record)
                self.headers = list(self.rows[0]) if self.rows else self.base_headers
            except (ValueError, KeyError, OSError) as exc:
                self.run.setEnabled(False)
                self.status.setText(str(exc))
                return
        self.retranslate()

    def refresh_method(self):
        if not self.method:
            self.equation.clear()
            self.edit.hide()
            self.run.setEnabled(False)
            self.status.setText(tr("No methods match these inputs."))
            return
        self.equation.setText(f"{self.method['source']}   ·   {self.method['unit']}")
        self.edit.setVisible(
            self.method.get("expression") is not None
            and not self.method.get("steps")
            and not self.method.get("engine")
        )
        try:
            calculate(self.active_method(), self.rows, self.meta)
        except (ValueError, TypeError, ArithmeticError, KeyError) as exc:
            self.status.setText(tr("Missing") + " · " + tr(str(exc)))
            self.run.setEnabled(False)
        else:
            self.status.setText(tr("Ready"))
            self.run.setEnabled(True)
        self.export.setEnabled(self.result is not None)

    def reload_data(self):
        self.meta, self.base_headers, self.base_rows = load_project(self.project)
        self.select_input(0)

    def active_method(self):
        method = dict(self.method)
        if self.parameter_boxes:
            method["parameters"] = {
                k: b.value() for k, b in self.parameter_boxes.items()
            }
        return method

    def edit_formula(self):
        symbols = {
            key: tr(self.fields.get(key, (key, ""))[0])
            for key in self.headers
            if key.isidentifier()
        }
        symbols.update({k: k for k in self.parameter_boxes})
        symbols.update(D=tr("Water deficit") + " (mm)", d=tr("Days in month"))
        symbols.update(
            {s: symbols.get(s, s) for s in symbols_used(self.method["expression"])}
        )
        samples = []
        try:
            rows = prepare(self.active_method(), self.rows, self.meta)
        except ValueError as exc:
            self.status.setText(str(exc))
            return
        for row in rows:
            try:
                y, m, values = symbol_values(
                    row, symbols, self.active_method().get("parameters")
                )
                samples.append((f"{y}-{m:02}", values))
            except (TypeError, ValueError):
                continue
        dialog = FormulaEditor(self.active_method(), symbols, samples, self)
        if dialog.exec():
            try:
                overrides = self.read_overrides()
                overrides[self.method["id"]] = dialog.definition
                save_json(self.formulas_path, overrides)
            except (OSError, ValueError) as exc:
                self.status.setText(str(exc))
                return
            self.method = self.methods[self.choices.currentIndex()] = dialog.definition
            self.refresh_method()

    def run_method(self):
        try:
            method = self.active_method()
            result = calculate(method, self.rows, self.meta)
            result["input_result"] = (
                Path(self.input_path).name if self.input_path else ""
            )
            result["station_metadata"] = self.meta
            result["station"] = self.meta.get("weather_station", "")
            path = store_result(self.project, result)
            self.reload_history(path)
        except (ValueError, TypeError, OSError) as exc:
            self.status.setText(tr("Data error") + " · " + tr(str(exc)))

    def reload_history(self, selected=None):
        self.history.blockSignals(True)
        self.history.clear()
        self.input_choice.blockSignals(True)
        self.input_choice.clear()
        self.input_choice.addItem(tr("Original inputs"), None)
        entries = []
        for path in (self.project / "results").glob("*.json"):
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
                entries.append(
                    (
                        record["timestamp"],
                        path,
                        record["method"]["name"],
                        record["method"].get("output"),
                    )
                )
            except (OSError, ValueError, KeyError, TypeError):
                continue
        for timestamp, path, name, output in sorted(entries, reverse=True):
            self.history.addItem(f"{timestamp}  ·  {tr(name)}", str(path))
            if output:
                self.input_choice.addItem(f"{output} · {timestamp} · {name}", str(path))
        if self.input_path:
            self.input_choice.setCurrentIndex(
                max(0, self.input_choice.findData(self.input_path))
            )
        self.input_choice.blockSignals(False)
        if selected:
            self.history.setCurrentIndex(self.history.findData(str(selected)))
        self.history.blockSignals(False)
        self.view_saved(self.history.currentIndex())

    def view_saved(self, index):
        self.result = None
        self.result_details.clear()
        self.table.setRowCount(0)
        self.export.setEnabled(False)
        if index < 0:
            return
        try:
            record = json.loads(
                Path(self.history.itemData(index)).read_text(encoding="utf-8")
            )
            method = record["method"]
            rows = record["rows"]
            extra = list(rows[0].get("outputs", {})) if rows else []
            self.table.setColumnCount(4 + len(extra))
            self.table.setHorizontalHeaderLabels(
                [tr("Year"), tr("Month"), tr("Result"), tr("Missing"), *extra]
            )
            self.table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                value = (
                    "—"
                    if row["value"] is None
                    else f"{format_number(row['value'])} {tr(method['unit'])}"
                )
                for j, obj in enumerate(
                    (
                        row["year"] or "—",
                        row["month"] or "—",
                        value,
                        ", ".join(row["missing"]),
                        *(format_number(row["outputs"][key]) for key in extra),
                    )
                ):
                    self.table.setItem(i, j, QTableWidgetItem(str(obj)))
            self.table.resizeColumnsToContents()
            params = ", ".join(
                f"{k}={v:g}" for k, v in method.get("parameters", {}).items()
            )
            self.result_details.setText(
                " · ".join(
                    filter(
                        None,
                        (
                            tr(method["name"]),
                            tr(method["unit"]),
                            params,
                            method.get("series", ""),
                            tr(method.get("distribution", "").title()),
                            method["source"],
                        ),
                    )
                )
            )
            self.result = record
            self.export.setEnabled(True)
        except (OSError, KeyError, ValueError, TypeError) as exc:
            self.status.setText(tr("Data error") + " · " + str(exc))

    def export_file(self):
        if self.result:
            path, fmt = QFileDialog.getSaveFileName(
                self,
                tr("Export…"),
                str(self.project / "results.xlsx"),
                "Excel (*.xlsx);;CSV (*.csv);;TSV (*.tsv);;TXT (*.txt)",
            )
            if path:
                suffix = fmt.split("*.")[-1].rstrip(")")
                dest = Path(path)
                if not dest.suffix:
                    dest = dest.with_suffix("." + suffix)
                try:
                    if dest.resolve() == (self.project / "data.xlsx").resolve():
                        raise ValueError(tr("Choose a separate result file."))
                    export_result(dest, self.result, tr)
                    self.status.setText(str(dest))
                except (ValueError, OSError) as exc:
                    self.status.setText(str(exc))
