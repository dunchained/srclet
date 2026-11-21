import json

from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (QComboBox, QDialog, QFormLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QWidget)

from mortys.language_morty import LANGUAGES, bind, events, format_number, read_language, tr, update_language
from plambas.formulas import legacy_expression, symbols_used, walk
from plambas.monthly_data import ROOT, catalog


class LanguagePicker(QComboBox):
    def __init__(self):
        super().__init__()
        for code, name in LANGUAGES.items():
            self.addItem(name, code)
        self.sync()
        self.currentIndexChanged.connect(self.select_language)
        events.changed.connect(self.sync)

    def select_language(self, index):
        update_language(self.itemData(index))

    def sync(self):
        self.setCurrentIndex(self.findData(read_language()))


class FormulaEditor(QDialog):
    def __init__(self, definition, symbols, samples=(), parent=None):
        super().__init__(parent)
        self.resize(800, 530)
        bind(self, "windowTitle", "Formula editor")
        self.definition = dict(definition)
        self.symbols = dict(symbols)
        self.samples = list(samples)
        self.ready = False
        layout = QVBoxLayout(self)
        bar = QHBoxLayout()
        picker = LanguagePicker()
        bar.addWidget(picker)
        self.symbol = QComboBox()
        for key, label in self.symbols.items():
            self.symbol.addItem(f"{key}  ·  {label}", key)
        bar.addWidget(self.symbol, 1)
        insert_symbol = bind(QPushButton(), "text", "Insert symbol")
        insert_symbol.clicked.connect(self.insert_symbol)
        bar.addWidget(insert_symbol)
        layout.addLayout(bar)
        bar = QHBoxLayout()
        for label, template in [("Fraction", r"\frac{#0}{#?}"), ("Root", r"\sqrt{#0}"),
                                ("Power", "#0^{#?}"), ("Subscript", "#0_{#?}"),
                                ("Braces", r"\left\{#0\right\}"),
                                ("Cases", r"\begin{cases}#? & #? \\ #? & \mathrm{otherwise}\end{cases}")]:
            button = bind(QPushButton(), "text", label)
            button.clicked.connect(lambda _, value=template: self.insert(value))
            bar.addWidget(button)
        layout.addLayout(bar)
        self.web = QWebEngineView()
        from mortys.font_morty import read_input_font_size
        self.web.setZoomFactor(read_input_font_size()/14.)
        layout.addWidget(self.web, 2)
        self.web.loadFinished.connect(self.loaded)
        self.web.load(QUrl.fromLocalFile(str(ROOT / "srclet/formula/editor.html")))

        self.period = QComboBox()
        for label, _ in self.samples:
            self.period.addItem(label)
        if self.samples:
            form = QFormLayout()
            form.addRow(bind(QLabel(), "text", "Sample month"), self.period)
            layout.addLayout(form)
        self.values = QTableWidget(len(self.symbols), 2)
        self.values.horizontalHeader().hide()
        self.values.verticalHeader().hide()
        for i, key in enumerate(self.symbols):
            label = QTableWidgetItem(key)
            label.setFlags(label.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.values.setItem(i, 0, label)
            self.values.setItem(i, 1, QTableWidgetItem(""))
        self.values.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.values, 1)
        self.period.currentIndexChanged.connect(self.show_sample)
        self.show_sample(self.period.currentIndex())
        self.last_value = None
        self.status = QLabel()
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        bar = QHBoxLayout()
        for label, fn in [("Test formula", lambda: self.read(False)), ("Apply", lambda: self.read(True)),
                          ("Cancel", self.reject)]:
            button = bind(QPushButton(), "text", label)
            button.setAutoDefault(False)
            button.clicked.connect(fn)
            bar.addWidget(button)
        layout.addLayout(bar)
        picker.activated.connect(self.focus_formula)
        events.changed.connect(self.retranslate)

    def focus_formula(self):
        if self.ready:
            self.web.setFocus()
            self.web.page().runJavaScript("field.focus()")

    def retranslate(self):
        if self.ready:
            self.web.page().runJavaScript("MathfieldElement.locale="+json.dumps({"ba":"bs","fr":"fr","en":"en"}[read_language()]))
        if self.last_value is not None:
            self.status.setText(f"{tr('Result')} = {format_number(self.last_value, 8)}")

    def show_sample(self, index):
        if index < 0:
            return
        values = self.samples[index][1]
        for i, key in enumerate(self.symbols):
            val = values.get(key)
            self.values.item(i, 1).setText("" if val is None else str(val))

    def loaded(self, ok):
        if not ok:
            self.status.setText(tr("Formula editor") + " · " + tr("Missing"))
            return
        self.web.page().runJavaScript("typeof openFormula === 'function'", self.initialize)

    def initialize(self, available):
        self.ready = bool(available)
        if self.ready:
            self.retranslate()
            args = [self.definition.get("latex", ""), self.definition.get("expression")]
            self.web.page().runJavaScript("openFormula(..." + json.dumps(args) + ")")

    def insert(self, template):
        if self.ready:
            self.web.page().runJavaScript("insertMath(" + json.dumps(template) + ")")

    def insert_symbol(self):
        key = self.symbol.currentData()
        if key and key.isidentifier():
            self.insert(key if len(key) == 1 else r"\mathrm{" + key + "}")

    def read(self, apply):
        if self.ready:
            self.web.page().runJavaScript("readFormula()", lambda result: self.handle(result, apply))

    def handle(self, result, apply):
        if not result:
            return
        try:
            data = json.loads(result)
            if data.get("error"):
                raise ValueError(data["error"])
            expr = data["expression"]
            walk(expr, self.symbols, check=True)
            if not data["latex"].strip():
                raise ValueError(tr("Missing"))
            if apply:
                self.definition.update(data)
                self.accept()
            else:
                values = {}
                for i, key in enumerate(self.symbols):
                    if key in symbols_used(expr):
                        raw = self.values.item(i, 1).text().strip()
                        if not raw:
                            raise ValueError(tr("Missing") + " · " + key)
                        values[key] = float(raw.replace(",", "."))
                self.last_value = walk(expr, values)
                self.retranslate()
        except (TypeError, KeyError, ValueError, ArithmeticError) as error:
            self.last_value = None
            message, sep, detail = str(error).partition(":")
            self.status.setText(tr(message) + sep + detail)
            if message == "Unknown symbol":
                self.web.page().runJavaScript("selectUnknownSymbol(" + json.dumps(detail.strip()) + ")")


class FormulaField(QWidget):
    """Catalog field for both historical text and visually edited expressions."""
    def __init__(self, text=""):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.text = QLineEdit(text)
        layout.addWidget(self.text)
        button = bind(QPushButton(), "text", "Edit formula…")
        layout.addWidget(button)
        self.tree = None
        self.text.textChanged.connect(self.clear_tree)
        button.clicked.connect(self.edit)

    def clear_tree(self):
        self.tree = None

    def setText(self, value):
        self.text.setText(value)

    setPlainText = setText

    def toPlainText(self):
        return self.text.text()

    def edit(self):
        original = self.toPlainText()
        definition = {"latex": original}
        if original and "\\" not in original:
            try:
                definition = {"expression": legacy_expression(original)}
            except (SyntaxError, ValueError):
                pass
        symbols = {key: name for key, (name, _) in catalog().items() if key.isidentifier()}
        symbols.update({"D": "Deficit (mm)", "d": "Days"})
        for folder in ("parameters/changable", "methods/others", "methods/eto", "methods/wb"):
            for path in (ROOT / folder).glob("*.json"):
                item = json.loads(path.read_text(encoding="utf-8"))
                symbols[item["symbol"]] = item["name"]
        dialog = FormulaEditor(definition, symbols, parent=self)
        if dialog.exec():
            self.setText(dialog.definition["latex"])
            self.tree = dialog.definition["expression"]

