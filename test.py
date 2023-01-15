from PyQt5 import QtWebEngineWidgets, QtCore
import sys
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QDesktopWidget, QMenu

class PDFViewer(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, pdf_path, parent=None):
        super().__init__(parent)
        self.load(QtCore.QUrl.fromLocalFile(pdf_path))
        self.show()

pdf_path = "srclet/sample.pdf"
app = QApplication(sys.argv)
viewer = PDFViewer(pdf_path)
sys.exit(app.exec_())
