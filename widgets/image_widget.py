from variables import css
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class ImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(self)
        pixmap = QPixmap(css.srclet_caption)
        label.setPixmap(pixmap)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        self.setLayout(layout)