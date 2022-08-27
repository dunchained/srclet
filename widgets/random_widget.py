import os, random
cwd = os.path.curdir

from variables import var, css
from pathlib import Path

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class RandomWidget(QWidget):
    def __init__(self):
        super().__init__()
        #get_files = next(os.walk(cwd + var.random_images_folder), (None, None, []))[2]
        #self.file_list = []
        #for file in get_files:
            #self.file_list.append(file)
        #photo = random.choice(self.file_list)

        layout = QVBoxLayout()
        label = QLabel(self)
        pixmap = QPixmap(css.srclet_caption)
        #pixmap = pixmap.scaled(2048, 1024, Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        self.setLayout(layout)