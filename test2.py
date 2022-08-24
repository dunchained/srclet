from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout


class win02(QWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(win02, self).__init__(parent)
        self.button = QPushButton("call to func")
        self.button.clicked.connect(self.clicked)
        lay = QVBoxLayout(self)
        lay.addWidget(self.button)