from copy import deepcopy
from pathlib import Path
from uuid import uuid4

from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from mortys.language_morty import bind, events, tr
from plambas.formulas import legacy_expression, walk
from plambas.frequency import DISTRIBUTIONS
from plambas.method_series import method_inputs
from plambas.monthly_data import ROOT, catalog, read_table, save_json
from plambas.monthly_results import project_methods
from widgets.formula_editor import FormulaEditor
from windows.project.method_selection import GROUPS, ROLE


def button(title, fn, layout):
    obj = bind(QPushButton(), "text", title)
    obj.clicked.connect(fn)
    layout.addWidget(obj)
    return obj


class Pairs(QWidget):
    def __init__(self, first, second):
        super().__init__()
        layout = QVBoxLayout(self)
        self.table = QTableWidget(0, 2)
        self.labels = (first, second)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        line = QHBoxLayout()
        button("Add row", lambda: self.add("", ""), line)
        button(
            "Remove row", lambda: self.table.removeRow(self.table.currentRow()), line
        )
        layout.addLayout(line)
        events.changed.connect(self.translate)
        self.translate()

    def translate(self):
        self.table.setHorizontalHeaderLabels([tr(x) for x in self.labels])

    def add(self, k, v):
        i = self.table.rowCount()
        self.table.insertRow(i)
        for col, x in enumerate((k, v)):
            self.table.setItem(i, col, QTableWidgetItem(str(x)))

    def fill(self, values):
        self.table.setRowCount(0)
        for k, v in values.items():
            self.add(k, v)

    def values(self):
        result = {}
        for i in range(self.table.rowCount()):
            k, v = (self.table.item(i, j).text().strip() for j in range(2))
            if not k.isidentifier() or k in result or not v:
                raise ValueError("Enter a unique symbol and a value.")
            result[k] = v
        return result


class MethodCatalog(QDialog):
    def __init__(self, group=None, parent=None):
        super().__init__(parent)
        bind(self, "windowTitle", "Method catalog")
        self.resize(950, 690)
        outer = QHBoxLayout(self)
        left = QVBoxLayout()
        self.filter = QComboBox()
        for key, label in {"": "All methods", **GROUPS}.items():
            self.filter.addItem(tr(label), key)
        self.filter.setCurrentIndex(max(0, self.filter.findData(group)))
        left.addWidget(self.filter)
        self.list = QListWidget()
        left.addWidget(self.list)
        button("New method", self.new, left)
        button("Duplicate method", self.duplicate, left)
        self.delete = button("Delete selected method", self.remove, left)
        outer.addLayout(left, 1)
        right = QVBoxLayout()
        form = QFormLayout()
        self.fields = {}
        for k, label in (
            ("name", "Name"),
            ("symbol", "Symbol"),
            ("unit", "Unit"),
            ("output", "Output"),
            ("source", "Description"),
        ):
            field = QLineEdit()
            self.fields[k] = field
            form.addRow(bind(QLabel(), "text", label), field)
        self.group = QComboBox()
        for k, name in GROUPS.items():
            self.group.addItem(tr(name), k)
        form.addRow(bind(QLabel(), "text", "Method group"), self.group)
        self.prepare = QComboBox()
        self.prepare.addItem(tr("Monthly inputs"), "")
        self.prepare.addItem("FAO-56", "fao")
        self.prepare.addItem(tr("Method comparison"), "comparison")
        form.addRow(bind(QLabel(), "text", "Input preparation"), self.prepare)
        self.dist = QComboBox()
        for key, label in DISTRIBUTIONS.items():
            self.dist.addItem(tr(label), key)
        form.addRow(bind(QLabel(), "text", "Distribution"), self.dist)
        self.group.currentIndexChanged.connect(
            lambda: self.dist.setEnabled(self.group.currentData() == "frequency")
        )
        right.addLayout(form)
        self.tabs = QTabWidget()
        eq = QWidget()
        eql = QVBoxLayout(eq)
        self.formula = QLineEdit()
        self.formula.textEdited.connect(self.clear_expression)
        eql.addWidget(self.formula)
        button("Edit formula…", self.edit_formula, eql)
        self.steps = QListWidget()
        eql.addWidget(self.steps)
        line = QHBoxLayout()
        button("Add formula step", lambda: self.step_editor(-1), line)
        button(
            "Edit step",
            lambda: (
                self.step_editor(self.steps.currentRow())
                if self.steps.currentRow() >= 0
                else None
            ),
            line,
        )
        button("Remove row", self.remove_step, line)
        eql.addLayout(line)
        self.params = Pairs("Symbol", "Default value")
        self.coefficients = QComboBox()
        import json

        for path in sorted((ROOT / "parameters/changable").glob("*.json")):
            param = json.loads(path.read_text(encoding="utf-8"))
            self.coefficients.addItem(
                param["symbol"] + " · " + tr(param["name"]),
                (param["symbol"], param["value"]),
            )
            self.coefficients.setItemData(
                self.coefficients.count() - 1, param["name"], ROLE + 1
            )
        line = QHBoxLayout()
        line.addWidget(self.coefficients)
        button("Use catalog coefficient", self.add_coefficient, line)
        self.params.layout().addLayout(line)
        self.state = Pairs("State symbol", "Initial value or parameter")
        sample_page = QWidget()
        sample_layout = QVBoxLayout(sample_page)
        self.required = QLabel()
        self.required.setWordWrap(True)
        sample_layout.addWidget(self.required)
        self.samples = QTableWidget(0, 0)
        self.samples.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        sample_layout.addWidget(self.samples)
        for tab, label in (
            (eq, "Formula"),
            (self.params, "Method parameters"),
            (self.state, "Previous month"),
            (sample_page, "Input data"),
        ):
            self.tabs.addTab(tab, tr(label))
        right.addWidget(self.tabs, 1)
        self.status = QLabel()
        self.status.setWordWrap(True)
        right.addWidget(self.status)
        line = QHBoxLayout()
        self.example = button("Export example data…", self.export_example, line)
        self.save = button("Save changes", self.write, line)
        button("Close", self.close, line)
        right.addLayout(line)
        outer.addLayout(right, 2)
        self.filter.currentIndexChanged.connect(self.reload)
        self.list.currentRowChanged.connect(self.select)
        self.reload()
        events.changed.connect(self.translate)

    def add_coefficient(self):
        pair = self.coefficients.currentData()
        if pair:
            for i in range(self.params.table.rowCount()):
                if self.params.table.item(i, 0).text() == pair[0]:
                    return
            self.params.add(*pair)

    def translate(self):
        for k in ("name", "source"):
            if not self.fields[k].isModified():
                self.fields[k].setText(tr(self.model.get(k, "")))
        for i in range(self.coefficients.count()):
            sym, _ = self.coefficients.itemData(i)
            self.coefficients.setItemText(
                i, sym + " · " + tr(self.coefficients.itemData(i, ROLE + 1) or sym)
            )
        for i, label in enumerate(("All methods", *GROUPS.values())):
            self.filter.setItemText(i, tr(label))
        for i, label in enumerate(GROUPS.values()):
            self.group.setItemText(i, tr(label))
        for i, label in enumerate(
            ("Formula", "Method parameters", "Previous month", "Input data")
        ):
            self.tabs.setTabText(i, tr(label))
        for i, label in enumerate(DISTRIBUTIONS.values()):
            self.dist.setItemText(i, tr(label))
        self.show_inputs()
        self.prepare.setItemText(0, tr("Monthly inputs"))
        self.prepare.setItemText(2, tr("Method comparison"))
        for i, m in enumerate(self.items):
            self.list.item(i).setText(tr(m["name"]))

    def reload(self, *_, selected=None):
        g = self.filter.currentData()
        self.items = [m for m in project_methods() if not g or m["group"] == g]
        self.list.blockSignals(True)
        self.list.clear()
        self.list.addItems([tr(m["name"]) for m in self.items])
        self.list.blockSignals(False)
        if self.items:
            self.list.setCurrentRow(
                next((i for i, m in enumerate(self.items) if m["id"] == selected), 0)
            )
        else:
            self.new()

    def select(self, i):
        if i >= 0:
            self.fill(deepcopy(self.items[i]))

    def new(self):
        self.list.clearSelection()
        group = self.filter.currentData() or "others"
        self.fill(
            dict(
                group=group,
                name="",
                symbol="",
                source="",
                unit="",
                output={"eto": "ET0", "wb": "Deficit"}.get(group, ""),
                latex="",
                expression=None,
            )
        )

    def duplicate(self):
        self.model.pop("id", None)
        self.fields["name"].setText(self.fields["name"].text() + " · " + tr("Copy"))
        self.fields["symbol"].clear()
        self.delete.setEnabled(False)

    def fill(self, m):
        self.model = m
        for k, field in self.fields.items():
            field.setText(
                tr(str(m.get(k) or ""))
                if k in ("name", "source")
                else str(m.get(k) or "")
            )
        self.group.setCurrentIndex(self.group.findData(m["group"]))
        self.dist.setEnabled(m["group"] == "frequency")
        self.dist.setCurrentIndex(
            max(0, self.dist.findData(m.get("distribution", "normal")))
        )
        self.prepare.setCurrentIndex(
            max(
                0,
                self.prepare.findData(
                    "comparison"
                    if m.get("engine") == "comparison"
                    else m.get("prepare", "")
                ),
            )
        )
        self.formula.setText(m.get("latex", ""))
        self.params.fill(m.get("parameters", {}))
        self.state.fill(m.get("state", {}))
        self.show_inputs()
        self.delete.setEnabled("id" in m)
        self.example.setEnabled(
            (ROOT / "examples/methods" / (m.get("id", "") + ".csv")).is_file()
        )
        self.display_steps()
        self.status.clear()

    def show_inputs(self):
        m = self.model
        self.required.setText(
            tr("Inputs to formula") + " · " + ", ".join(sorted(method_inputs(m)))
        )
        source = ROOT / "examples/methods" / (m.get("id", "") + ".csv")
        self.samples.clear()
        if not source.is_file():
            self.samples.setRowCount(0)
            self.samples.setColumnCount(0)
            return
        headers, rows = read_table(source)
        self.samples.setColumnCount(len(headers))
        self.samples.setHorizontalHeaderLabels(headers)
        self.samples.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                self.samples.setItem(i, j, QTableWidgetItem(str(cell)))
        self.samples.resizeColumnsToContents()

    def display_steps(self):
        self.steps.clear()
        for step in self.model.get("steps", []):
            self.steps.addItem(step["symbol"] + " = " + step.get("latex", ""))

    def clear_expression(self):
        self.model["expression"] = None

    def symbols(self):
        available = {k: tr(name) for k, (name, _) in catalog().items()}
        for method in project_methods():
            for k in (method.get("symbol"), method.get("output")):
                if k:
                    available[k] = tr(method["name"])
            available.update(
                {
                    s["symbol"]: s["symbol"]
                    for s in method.get("steps", [])
                    if s.get("publish")
                }
            )
        for table in (self.state, self.params):
            for i in range(table.table.rowCount()):
                key = table.table.item(i, 0).text()
                available[key] = key
        available.update(
            {
                k: k
                for k in (
                    "d",
                    "D",
                    "M",
                    "Y",
                    "r",
                    "n",
                    "daylight",
                    "slope",
                    "gamma",
                    "es",
                    "T",
                    "meanDiff",
                    "varianceTerm",
                    "meanSquare",
                    "meanAbs",
                    "correlation",
                )
            }
        )
        available.update(
            {s["symbol"]: s["symbol"] for s in self.model.get("steps", [])}
        )
        return available

    def edit_formula(self):
        expression = self.model.get("expression")
        latex = self.formula.text()
        if expression is None and latex:
            try:
                expression = legacy_expression(latex)
                latex = ""
            except (SyntaxError, ValueError):
                pass
        dialog = FormulaEditor(
            {"expression": expression, "latex": latex}, self.symbols(), parent=self
        )
        if dialog.exec():
            self.model["expression"] = dialog.definition["expression"]
            self.formula.setText(dialog.definition["latex"])

    def step_editor(self, i):
        steps = self.model.setdefault("steps", [])
        step = steps[i].copy() if i >= 0 else {}
        dialog = QDialog(self)
        form = QFormLayout(dialog)
        symbol = QLineEdit(step.get("symbol", ""))
        text = QLineEdit(step.get("latex", ""))
        publish = bind(QCheckBox(), "text", "Publish as a result")
        publish.setChecked(step.get("publish", False))
        form.addRow(bind(QLabel(), "text", "Symbol"), symbol)
        form.addRow(bind(QLabel(), "text", "Formula"), text)
        form.addRow(publish)
        status = QLabel()
        form.addRow(status)

        def edit():
            popup = FormulaEditor(
                {"latex": text.text(), "expression": step.get("expression")},
                self.symbols(),
                parent=dialog,
            )
            if popup.exec():
                step["expression"] = popup.definition["expression"]
                text.setText(popup.definition["latex"])

        text.textEdited.connect(lambda: step.pop("expression", None))
        action = bind(QPushButton(), "text", "Edit formula…")
        action.clicked.connect(edit)
        form.addRow(action)

        def accept():
            try:
                if not symbol.text().isidentifier():
                    raise ValueError("Invalid symbol.")
                if step.get("expression") is None:
                    step["expression"] = legacy_expression(text.text())
                step.update(
                    symbol=symbol.text(), latex=text.text(), publish=publish.isChecked()
                )
            except (ValueError, SyntaxError) as err:
                status.setText(tr(str(err)))
                return
            if i < 0:
                steps.append(step)
            else:
                steps[i] = step
            dialog.accept()

        action = bind(QPushButton(), "text", "Apply")
        action.clicked.connect(accept)
        form.addRow(action)
        if dialog.exec():
            self.display_steps()

    def remove_step(self):
        i = self.steps.currentRow()
        if i >= 0:
            self.model["steps"].pop(i)
            self.display_steps()

    def path(self, m):
        folder = {"eto": "eto", "wb": "wb"}.get(m["group"], "others")
        return ROOT / "methods" / folder / (m["id"] + ".json")

    def write(self):
        try:
            m = {**self.model, **{k: w.text().strip() for k, w in self.fields.items()}}
            for k in ("name", "source"):
                if not self.fields[k].isModified() and self.fields[k].text() == tr(
                    self.model.get(k, "")
                ):
                    m[k] = self.model.get(k, "")
            group = self.group.currentData()
            if not m["name"] or not m["symbol"].isidentifier() or not m["unit"]:
                raise ValueError("Enter a name, a symbol and a unit.")
            if m["output"] and not m["output"].isidentifier():
                raise ValueError("Invalid symbol.")
            if m.get("expression") is None:
                m["expression"] = legacy_expression(self.formula.text())
            m.update(
                group=group,
                latex=self.formula.text(),
                version=1,
                parameters={
                    k: float(v.replace(",", "."))
                    for k, v in self.params.values().items()
                },
                state={k: legacy_expression(v) for k, v in self.state.values().items()},
            )
            m["prepare"] = self.prepare.currentData()
            if group == "frequency":
                m.update(
                    engine="frequency",
                    distribution=self.dist.currentData(),
                    output=None,
                    inputs=["Deficit"],
                )
                m["parameters"].setdefault("month", 8)
                m["parameters"].setdefault("years", 10)
                walk(m["expression"], {"r": 1, "n": 10}, check=True)
            elif m["prepare"] == "comparison":
                m.update(
                    engine="comparison",
                    prepare="",
                    output=None,
                    inputs=["FAOPM", "EstimateET"],
                )
                walk(m["expression"], self.symbols(), check=True)
            else:
                m.pop("engine", None)
                m.pop("distribution", None)
                m["output"] = m["output"] or {"eto": "ET0", "wb": "Deficit"}.get(
                    group, m["symbol"]
                )
                m[
                    "inputs"
                ] = []  # External formula symbols determine data dependencies.
                for step in m.get("steps", []):
                    walk(step["expression"], self.symbols(), check=True)
                walk(m["expression"], self.symbols(), check=True)
            for initial in m["state"].values():
                walk(initial, m["parameters"])
            if any(
                item["symbol"] == m["symbol"] and item["id"] != m.get("id")
                for item in project_methods()
            ):
                raise ValueError("Symbol already exists.")
            m.setdefault("id", uuid4().hex)
            m.update(
                type="a",
                description=m["source"],
                method_conditions="",
                formula_math=m["expression"],
                method_formula=m["latex"],
                basic_parameters=", ".join(sorted(method_inputs(m))),
                changable_parameters=", ".join(m["parameters"]),
                other_methods="",
                eto_methods="",
                category="other",
            )
            path = self.path(m)
            path.parent.mkdir(exist_ok=True)
            save_json(path, m)
            if "id" in self.model and self.path(self.model) != path:
                self.path(self.model).unlink(missing_ok=True)
            events.catalogChanged.emit()
            self.reload(selected=m["id"])
        except (ValueError, TypeError, SyntaxError, OSError) as err:
            self.status.setText(tr(str(err)))

    def export_example(self):
        from PyQt6.QtWidgets import QFileDialog

        source = ROOT / "examples/methods" / (self.model.get("id", "") + ".csv")
        if not source.exists():
            return
        dest, _ = QFileDialog.getSaveFileName(
            self, tr("Export example data…"), source.name, "CSV (*.csv)"
        )
        if dest and Path(dest).resolve() != source.resolve():
            try:
                Path(dest).write_bytes(source.read_bytes())
            except OSError as exc:
                self.status.setText(str(exc))

    def remove(self):
        if (
            QMessageBox.question(
                self,
                tr("Delete selected method"),
                tr("Are you sure you want to delete selected method?"),
            )
            == QMessageBox.StandardButton.Yes
        ):
            self.path(self.model).unlink()
            events.catalogChanged.emit()
            self.reload()
