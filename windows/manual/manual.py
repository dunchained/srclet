# python standard modules

# app modules and windows
from appdata import css

# pyqt5 modules
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class ManualWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.WindowGUI()

    def WindowGUI(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('Manual')
        self.setWindowIcon(QIcon(css.menu_about_icon))
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())