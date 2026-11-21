import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PyQt6.QtCore import QCoreApplication, QEvent
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication
from mortys import language_morty as lang
from windows.manual.manual import ManualWindow


class ManualTest(unittest.TestCase):
    def wait(self, condition):
        for _ in range(200):
            if condition():
                return
            QTest.qWait(25)
        self.fail("Manual did not finish loading")

    def js(self, manual, script):
        result = []
        manual.page.page().runJavaScript(script, result.append)
        self.wait(lambda: len(result) > 0)
        return result[0]

    def test_manual_screenshots_chapters_languages_and_video_file(self):
        self.app = QApplication.instance() or QApplication(["SRCLET-manual-test"])
        with tempfile.TemporaryDirectory() as tmp:
            settings = Path(tmp) / "settings.json"
            settings.write_bytes(lang.SETTINGS.read_bytes())
            video = Path(tmp) / "video_url.txt"
            video.write_text("https://example.org/guide", encoding="utf-8")
            original = lang.read_language()
            with (
                patch.object(lang, "SETTINGS", settings),
                patch("windows.manual.manual.VIDEO_FILE", video),
            ):
                window = ManualWindow()
                try:
                    self.wait(lambda: window.ready)
                    self.assertIn("https://example.org/guide", window.video.text())
                    self.js(window, "document.getElementById('formula').open=true")
                    for code, html_lang in (("ba", "bs"), ("en", "en"), ("fr", "fr")):
                        lang.update_language(code)
                        self.wait(
                            lambda: (
                                window.ready
                                and window.page.url()
                                .path()
                                .endswith("/" + code + "/index.html")
                            )
                        )
                        self.wait(
                            lambda: (
                                self.js(window, "document.documentElement.lang")
                                == html_lang
                            )
                        )
                        self.assertEqual(
                            self.js(
                                window, "document.querySelectorAll('details').length"
                            ),
                            9,
                        )
                        self.assertTrue(
                            self.js(
                                window,
                                "Array.from(document.querySelectorAll('figure img')).every(i=>i.complete && i.naturalWidth>0)",
                            )
                        )
                        self.assertTrue(
                            self.js(window, "document.getElementById('formula').open")
                        )
                        self.js(
                            window, "document.querySelector('#formula button').click()"
                        )
                        self.assertTrue(
                            self.js(window, "document.querySelector('dialog').open")
                        )
                        self.js(window, "document.querySelector('dialog').close()")
                    new = video.with_suffix(".tmp")
                    new.write_text("https://example.org/new", encoding="utf-8")
                    new.replace(video)
                    self.wait(lambda: "https://example.org/new" in window.video.text())
                finally:
                    window.close()
                    window.deleteLater()
                    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
                    lang.update_language(original)
