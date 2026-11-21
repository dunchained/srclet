from html import escape
from PyQt6.QtCore import QFileSystemWatcher, QUrl
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from mortys.font_morty import read_input_font_size
from mortys.language_morty import bind, events, read_language, tr
from plambas.monthly_data import ROOT
import json

VIDEO_FILE = ROOT / "video_url.txt"


class ManualWindow(QWidget):
    def __init__(self, language=None):
        super().__init__()
        bind(self, "windowTitle", "Manual")
        self.resize(1080, 770)
        self.video_file = VIDEO_FILE
        self.watch = QFileSystemWatcher(self)
        self.watch.addPath(str(self.video_file.parent))
        self.watch.fileChanged.connect(self.video_link)
        self.watch.directoryChanged.connect(self.video_link)
        self.page = QWebEngineView()
        self.page.setZoomFactor(read_input_font_size() / 14)
        self.video = QLabel()
        self.video.setOpenExternalLinks(True)
        self.video.setWordWrap(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.page, 1)
        layout.addWidget(self.video)
        self.ready = False
        self.chapters = None
        self.page.loadFinished.connect(self.loaded)
        events.changed.connect(self.change_language)
        self.load()
        self.show()

    def video_link(self, *_):
        try:
            raw = self.video_file.read_text(encoding="utf-8-sig").strip()
        except OSError:
            raw = ""
        url = QUrl(raw)
        if self.video_file.exists() and str(self.video_file) not in self.watch.files():
            self.watch.addPath(str(self.video_file))
        self.video.setVisible(
            url.isValid() and url.scheme() in ("https", "http") and bool(url.host())
        )
        self.video.setText(
            f'{tr("Video guide")} · <a href="{escape(raw, quote=True)}">{escape(raw)}</a>'
        )

    def load(self, chapters=None):
        self.ready = False
        self.chapters = chapters
        self.video_link()
        self.page.load(
            QUrl.fromLocalFile(
                str(ROOT / "srclet/manual" / read_language() / "index.html")
            )
        )

    def loaded(self, ok):
        self.ready = ok
        if ok and self.chapters is not None:
            self.page.page().runJavaScript(
                "openChapters(" + json.dumps(self.chapters) + ")"
            )

    def change_language(self):
        if self.ready:
            self.page.page().runJavaScript(
                "Array.from(document.querySelectorAll('details[open]'), el=>el.id)",
                self.load,
            )
        else:
            self.load()
