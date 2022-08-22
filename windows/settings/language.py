# python standard modules
import json
import os
# app modules and windows
from css import css

# pyqt5 modules
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QGroupBox, QVBoxLayout, QComboBox
from PyQt5.QtWidgets import QGridLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class LanguageWindow(QWidget):
    def __init__(self, language):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = language
        self.WindowGUI()

    def WindowGUI(self):
        #self.setFixedSize(800, 600)
        self.setWindowTitle('Language...')
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
        groupBox = QGroupBox('List of available languages...')
        self.combo_box = QComboBox()
        self.combo_box.addItems(next(os.walk(os.path.curdir + '/appdata/languages/'))[1])
        vbox = QVBoxLayout()

        self.buttonSave = QPushButton('Save')
        self.buttonSave.clicked.connect(self.saveLanguage)

        vbox.addWidget(self.combo_box)
        vbox.addWidget(self.buttonSave)
        groupBox.setLayout(vbox)
        return groupBox

    def saveLanguage(self):
        language = {
            "language": self.combo_box.currentText()
        }
        with open("appdata/languages/language.json", "w") as outfile:
            json.dump(language, outfile)

        self.msg = QMessageBox()
        self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText(self.language['message_language'])
        self.msg.setWindowTitle('Language...')
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.msg.close)
        self.msg.show()
        self.hide()
    
    def closeLanguage(self):
        self.hide()