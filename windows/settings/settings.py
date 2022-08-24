# python standard modules
import json
import os
# app modules and windows
from css import css, var

# pyqt5 modules
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QGroupBox, QVBoxLayout, QComboBox
from PyQt5.QtWidgets import QGridLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class SettingsWindow(QWidget):
    def __init__(self, language):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = language
        self.WindowGUI()

    def WindowGUI(self):
        #self.setFixedSize(800, 600)
        self.setWindowTitle(self.language['settings_window_title'])
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
        groupBox = QGroupBox(self.language['settings_window_language'])
        self.combo_box = QComboBox()
        self.combo_box.addItems(next(os.walk(os.path.curdir + var.language_folder))[1])
        vbox = QVBoxLayout()

        self.buttonSave = QPushButton(self.language['settings_window_language_save'])
        self.buttonSave.clicked.connect(self.saveLanguage)

        vbox.addWidget(self.combo_box)
        vbox.addWidget(self.buttonSave)
        groupBox.setLayout(vbox)
        return groupBox

    def saveLanguage(self):
        language = {
            "language": self.combo_box.currentText()
        }
        with open(os.path.curdir + var.language_folder + var.language_file, "w") as outfile:
            json.dump(language, outfile)

        self.msg = QMessageBox()
        self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText(self.language['settings_window_message'])
        self.msg.setWindowTitle(self.language['settings_window_message_caption'])
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.msg.close)
        self.msg.show()
        self.hide()
    
    def closeLanguage(self):
        self.hide()