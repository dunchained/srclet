from variables import css
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class ImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(self)
        pixmap = QPixmap(css.srclet_caption)
        label.setPixmap(pixmap)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)