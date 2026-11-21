import json
from uuid import uuid4
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)
from mortys.language_morty import bind, events, tr
from plambas.monthly_data import ROOT, number, save_json


class ParameterCatalog(QDialog):
    def __init__(self, kind, parent=None):
        super().__init__(parent)
        self.kind = kind
        self.folder = ROOT / "parameters" / kind
        self.categories = json.loads(
            (
                ROOT
                / "srclet/languages/en"
                / (
                    "basic_parameter_types.json"
                    if kind == "basic"
                    else "changable_parameter_types.json"
                )
            ).read_text()
        )
        bind(
            self,
            "windowTitle",
            "Basic parameters" if kind == "basic" else "Changable parameters",
        )
        self.resize(800, 420)
        layout = QHBoxLayout(self)
        self.list = QListWidget()
        layout.addWidget(self.list)
        form = QFormLayout()
        layout.addLayout(form)
        self.fields = {}
        for key, title in (
            ("name", "Name"),
            ("symbol", "Symbol"),
            ("unit", "Unit"),
            ("description", "Description"),
            ("value", "Default value"),
        ):
            if key == "value" and kind == "basic":
                continue
            box = QLineEdit()
            form.addRow(bind(QLabel(), "text", title), box)
            self.fields[key] = box
        self.category = QComboBox()
        for k, title in self.categories.items():
            self.category.addItem(tr(title), k)
        form.addRow(bind(QLabel(), "text", "Category"), self.category)
        for title, fn in (
            ("New parameter", self.new),
            ("Save changes", self.save),
            ("Delete selected parameter", self.remove),
            ("Close", self.close),
        ):
            b = bind(QPushButton(), "text", title)
            b.clicked.connect(fn)
            form.addRow(b)
        self.status = QLabel()
        form.addRow(self.status)
        self.list.currentRowChanged.connect(self.select)
        self.reload()
        events.changed.connect(self.translate)

    def translate(self):
        for i, v in enumerate(self.categories.values()):
            self.category.setItemText(i, tr(v))
        for i, (_, d) in enumerate(self.items):
            self.list.item(i).setText(d["symbol"] + " · " + tr(d["name"]))
        # Keep user edits in progress when the interface language changes.
        for k, original in self.displayed.items():
            field = self.fields[k]
            if not field.isModified():
                field.setText(tr(original))

    def reload(self, path=None):
        self.items = sorted(
            (
                (p, json.loads(p.read_text(encoding="utf-8")))
                for p in self.folder.glob("*.json")
            ),
            key=lambda pair: pair[1]["symbol"],
        )
        self.list.clear()
        for _, d in self.items:
            self.list.addItem(d["symbol"] + " · " + tr(d["name"]))
        if self.items:
            self.list.setCurrentRow(
                next((i for i, (p, _) in enumerate(self.items) if p == path), 0)
            )
        else:
            self.new()

    def select(self, i):
        if i < 0:
            return
        self.path, d = self.items[i]
        self.displayed = {k: d.get(k, "") for k in ("name", "description")}
        for k, field in self.fields.items():
            field.setText(
                tr(str(d.get(k, ""))) if k in self.displayed else str(d.get(k, ""))
            )
        self.fields["symbol"].setReadOnly(True)
        self.category.setCurrentIndex(max(0, self.category.findData(d.get("category"))))
        self.status.clear()

    def new(self):
        self.path = None
        self.displayed = {}
        self.list.clearSelection()
        for field in self.fields.values():
            field.clear()
        self.fields["symbol"].setReadOnly(False)

    def save(self):
        try:
            d = {k: f.text().strip() for k, f in self.fields.items()}
            for k, v in self.displayed.items():
                if not self.fields[k].isModified():
                    d[k] = v
            if not d["name"] or not d["symbol"].isidentifier():
                raise ValueError("Enter a name and a valid symbol.")
            if any(
                old["symbol"] == d["symbol"] and path != self.path
                for path, old in self.items
            ):
                raise ValueError("Symbol already exists.")
            if "value" in d and number(d["value"], ",") is None:
                raise ValueError("Enter a numeric value.")
            path = self.path or self.folder / (uuid4().hex + ".json")
            save_json(path, {**d, "category": self.category.currentData(), "type": "a"})
            self.reload(path)
            events.catalogChanged.emit()
        except (ValueError, OSError) as exc:
            self.status.setText(tr(str(exc)))

    def remove(self):
        if (
            self.path
            and QMessageBox.question(
                self,
                tr("Delete selected parameter"),
                tr("Are you sure you want to delete selected parameter?"),
            )
            == QMessageBox.StandardButton.Yes
        ):
            self.path.unlink()
            self.reload()
            events.catalogChanged.emit()
