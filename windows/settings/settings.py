# python standard modules
import os
# app modules and windows
from appdata import css

# pyqt5 modules
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QGroupBox, QVBoxLayout, QComboBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class SettingsWindow(QWidget):
    def __init__(self, language):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = language
        self.WindowGUI()

    def WindowGUI(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('Settings')
        self.setWindowIcon(QIcon(css.menu_about_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.listOfLanguages())
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def listOfLanguages(self):
        groupBox = QGroupBox('List of existing Projects...')
        self.combo_box = QComboBox()
        self.combo_box.addItems(next(os.walk(os.path.curdir + '/appdata/languages/'))[1])
        vbox = QVBoxLayout()
        vbox.addWidget(self.combo_box)
        groupBox.setLayout(vbox)
        return groupBox