from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QDesktopWidget, QMenu
import sys


class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a QWebEngineView widget
        self.viewer = QWebEngineView(self)
        self.setCentralWidget(self.viewer)

        # Load the PDF file into the widget
        self.viewer.load(QUrl.fromLocalFile("sample.pdf"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pdf_viewer = PDFViewer()
    pdf_viewer.show()
    sys.exit(app.exec_())