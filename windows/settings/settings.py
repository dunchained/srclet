from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QWidget,
)
from mortys.font_morty import SIZES, settings, set_preference
from mortys.language_morty import bind, bind_key, events, tr
from widgets.formula_editor import LanguagePicker


class SettingsWindow(QWidget):
    def __init__(self, language=None):
        super().__init__()
        bind_key(self, "windowTitle", "settings_window_title")
        form = QFormLayout(self)
        self.boxes = {}
        for key, label in (
            ("menu_font_size", "Menu font size"),
            ("text_font_size", "Text font size"),
            ("input_text_size", "Input font size"),
        ):
            combo = QComboBox()
            for text, size in SIZES.items():
                combo.addItem(tr(text.title()), size)
            self.boxes[key] = combo
            form.addRow(bind(QLabel(), "text", label), combo)
            combo.currentIndexChanged.connect(
                lambda _, k=key, c=combo: set_preference(k, c.currentData())
            )
        self.icons = QSpinBox()
        self.icons.setRange(12, 96)
        self.icons.setSuffix(" px")
        form.addRow(bind(QLabel(), "text", "Icon size"), self.icons)
        self.icons.valueChanged.connect(lambda v: set_preference("icon_size", v))
        self.combo_box = LanguagePicker()
        form.addRow(bind(QLabel(), "text", "Language"), self.combo_box)
        close = bind(QPushButton(), "text", "Close")
        close.clicked.connect(self.close)
        form.addRow(close)
        events.changed.connect(self.sync)
        events.appearanceChanged.connect(self.sync)
        self.sync()
        self.show()

    def sync(self):
        data = settings()
        for key, combo in self.boxes.items():
            combo.blockSignals(True)
            for i, label in enumerate(SIZES):
                combo.setItemText(i, tr(label.title()))
            combo.setCurrentIndex(combo.findData(int(data[key])))
            combo.blockSignals(False)
        self.icons.blockSignals(True)
        self.icons.setValue(int(data["icon_size"]))
        self.icons.blockSignals(False)
