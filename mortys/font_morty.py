import json

from PyQt6.QtWidgets import QApplication
from mortys import language_morty as i18n
from plambas.monthly_data import save_json

SIZES = {"small": 12, "medium": 14, "large": 16}


def settings():
    return json.loads(i18n.SETTINGS.read_text(encoding="utf-8"))


def read_menu_font_size():
    return int(settings()["menu_font_size"])


def read_text_font_size():
    return int(settings()["text_font_size"])


def read_input_font_size():
    return int(settings()["input_text_size"])


def apply_settings():
    app = QApplication.instance()
    if not app:
        return
    data = settings()
    menu, text, entry, icon = (
        int(data[k])
        for k in ("menu_font_size", "text_font_size", "input_text_size", "icon_size")
    )
    app.setStyleSheet(
        f"QWidget {{ font-size: {text}pt; }} QMenuBar, QMenu {{ font-size: {menu}pt; }} "
        f"QLineEdit,QTextEdit,QPlainTextEdit,QComboBox,QAbstractSpinBox,QAbstractItemView {{font-size:{entry}pt;}} "
        f"QToolBar {{qproperty-iconSize:{icon}px {icon}px;}}"
    )
    for obj in app.allWidgets():
        if obj.inherits("QWebEngineView"):
            obj.setZoomFactor(entry / 14.0)
    i18n.events.appearanceChanged.emit()


def set_preference(key, value):
    data = settings()
    if data.get(key) == value:
        return
    save_json(i18n.SETTINGS, {**data, key: value})
    apply_settings()


def update_fonts(menu_font_size, text_font_size, input_font_size):
    data = settings()
    save_json(
        i18n.SETTINGS,
        {
            **data,
            "menu_font_size": SIZES[menu_font_size],
            "text_font_size": SIZES[text_font_size],
            "input_text_size": SIZES[input_font_size],
        },
    )
    apply_settings()
