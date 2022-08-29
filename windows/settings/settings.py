from asyncore import read
import json, os
cwd = os.path.curdir
from variables import css, var
from mortys.language_morty import read_language, update_language
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QGroupBox, QVBoxLayout, QComboBox
from PyQt5.QtWidgets import QGridLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class SettingsWindow(QWidget):
    def __init__(self, language):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = language
        self.window_gui()

    def window_gui(self):
        self.setFixedSize(400, 300)
        self.setWindowTitle(self.language['settings_window_title'])
        self.setWindowIcon(QIcon(css.settings_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.list_of_languages(), 0, 0)
        #self.grid.addWidget(self.font_sizes(), 0, 1)
        self.setLayout(self.grid)
        self.center_user_interface()
        self.show()
        
    def center_user_interface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def list_of_languages(self):
        groupBox = QGroupBox(self.language['settings_window_language'])
        self.combo_box = QComboBox()
        self.combo_box.addItems(next(os.walk(os.path.curdir + var.language_folder))[1])
        self.combo_box.setCurrentText(read_language())
        vbox = QVBoxLayout()

        self.buttonSave = QPushButton(self.language['settings_window_language_save'])
        self.buttonSave.clicked.connect(self.save_language)

        vbox.addWidget(self.combo_box)
        vbox.addWidget(self.buttonSave)
        groupBox.setLayout(vbox)
        return groupBox

    def save_language(self):
        update_language(new_language=self.combo_box.currentText())
        self.msg = QMessageBox()
        self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText(self.language['settings_window_message'])
        self.msg.setWindowTitle(self.language['settings_window_message_caption'])
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.msg.close)
        self.msg.show()
        #self.hide()

    def font_sizes(self):
        groupBox = QGroupBox(self.language['settings_window_language'])
        self.combo_box = QComboBox()
        self.combo_box.addItems(next(os.walk(os.path.curdir + var.language_folder))[1])
        self.language_settings = open(os.path.join(cwd + var.language_folder + var.language_file))
        self.language_settings_data = json.load(self.language_settings)
        self.selected_language = self.language_settings_data['language']
        self.combo_box.setCurrentText(self.selected_language)
        self.language_settings.close()
        vbox = QVBoxLayout()

        self.buttonSave = QPushButton(self.language['settings_window_language_save'])
        self.buttonSave.clicked.connect(self.save_language)

        vbox.addWidget(self.combo_box)
        vbox.addWidget(self.buttonSave)
        groupBox.setLayout(vbox)
        return groupBox

    
    def closeLanguage(self):
        self.hide()