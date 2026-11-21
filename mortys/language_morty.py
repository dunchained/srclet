"""Shared translations and in-place updates of labelled Qt objects."""

import json

from PyQt6.QtCore import QLocale, QObject, pyqtSignal, QTranslator, QLibraryInfo, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication

from plambas.monthly_data import ROOT, save_json

BASE = ROOT / "srclet/languages"
SETTINGS = ROOT / "srclet/settings/settings.json"
SOURCES = json.loads((BASE / "en/en.json").read_text(encoding="utf-8"))
MESSAGES = json.loads((BASE / "interface.json").read_text(encoding="utf-8"))
LANGUAGES = {"ba": "Bosanski", "en": "English", "fr": "Français"}


class LanguageEvents(QObject):
    changed = pyqtSignal()
    catalogChanged = pyqtSignal()
    appearanceChanged = pyqtSignal()


events = LanguageEvents()
_current = json.loads(SETTINGS.read_text(encoding="utf-8"))["language"]
_strings = {}


_translators = []


class InterfaceTranslator(QTranslator):
    def translate(self, context, source, disambiguation=None, n=-1):
        if _current != "en" and source.strip() in MESSAGES:
            return tr(source)
        if (
            _current != "en"
            and "&" in source
            and source.replace("&", "").strip() in MESSAGES
        ):
            return tr(source.replace("&", ""))
        return None


def qt_language():
    app = QApplication.instance()
    if app is None:
        return
    for translator in _translators:
        app.removeTranslator(translator)
    _translators.clear()
    locale = QLocale({"en": "en_GB", "ba": "bs_BA", "fr": "fr_FR"}[_current])
    QLocale.setDefault(locale)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
    if _current == "fr":
        qt = QTranslator()
        if qt.load(
            "qtbase_fr", QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
        ):
            app.installTranslator(qt)
            _translators.append(qt)
    if _current != "en":
        qt = InterfaceTranslator()
        app.installTranslator(qt)
        _translators.append(qt)


def read_language():
    return _current


def format_number(value, digits=6):
    locale = QLocale(
        {"ba": "bs_BA", "en": "en_GB", "fr": "fr_FR"}.get(_current, "en_GB")
    )
    return locale.toString(float(value), "g", digits)


# Older project workbooks use these original strings as column identifiers.
# Correct their displayed English while preserving project and translation keys.
_ENGLISH = {
    "Changable": "Adjustable",
    "changable": "adjustable",
    "reletive": "relative",
    "Reletive": "Relative",
    "procentages": "percent",
    "procentage": "percent",
    "Celsious": "Celsius",
    "Wather": "Weather",
    "Disclamair": "Disclaimer",
    "Abouta SRCLET": "About SRCLET",
    "Mathod": "Method",
    "softwere": "software",
    "prodact": "product",
    "Food scenes": "Food Sciences",
    "Authors also declines": "The authors also decline",
    "data and assumes": "data and assume",
    "you vant": "you want",
}


def tr(source):
    if _current == "en":
        for original, corrected in _ENGLISH.items():
            source = source.replace(original, corrected)
        return source
    stripped = source.strip()
    options = MESSAGES.get(stripped)
    if options:
        return source.replace(stripped, options[0 if _current == "ba" else 1])
    if source.startswith("Tooltip "):
        return tr(source[8:])
    for separator in (" · ", ": "):
        if separator in source:
            return separator.join(tr(part) for part in source.split(separator))
    if source.endswith(" years"):
        return source[:-5] + tr("years")
    return source


def language():
    if not _strings:
        _strings.update({key: tr(value) for key, value in SOURCES.items()})
        # The original category files contain stable catalog values in English.
        _strings["language_description"] = "en"
    return _strings


def bind(obj, prop, source):
    keys = obj.property("srcletMessages") or {}
    keys[prop] = source
    obj.setProperty("srcletMessages", keys)
    obj.setProperty(prop, tr(source))
    return obj


def bind_key(obj, prop, key):
    return bind(obj, prop, SOURCES[key])


def update_language(new_language):
    global _current
    if new_language not in LANGUAGES or new_language == _current:
        return
    settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
    save_json(SETTINGS, {**settings, "language": new_language})
    _current = new_language
    qt_language()
    _strings.clear()
    language()
    app = QApplication.instance()
    if app:
        objects = list(app.allWidgets())
        for window in app.topLevelWidgets():
            objects.extend(window.findChildren(QAction))
        for obj in objects:
            for prop, source in (obj.property("srcletMessages") or {}).items():
                obj.setProperty(prop, tr(source))
    events.changed.emit()
