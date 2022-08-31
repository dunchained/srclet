from asyncore import read
import json, os
cwd = os.path.curdir
from variables import css, var
from mortys.language_morty import read_language, update_language
from mortys.reader_morty import read_font_sizes
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QGroupBox, QVBoxLayout, QComboBox
from PyQt5.QtWidgets import QGridLayout, QPushButton, QMessageBox, QHBoxLayout
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
        self.grid.addWidget(self.font_sizes(), 1, 0)
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
        self.font_sizes_list = read_font_sizes()
        
        ##########
        self.menu_font_sizeGroupBox = QGroupBox()
        self.menu_font_sizeGroupBoxLayout = QVBoxLayout()
        self.menu_font_sizeComboBox = QComboBox()
        self.menu_font_sizeComboBox.addItems(self.font_sizes_list)
        
        self.menu_font_sizeGroupBoxLayout.addWidget(self.menu_font_sizeComboBox)
        self.menu_font_sizeGroupBox.setLayout(self.menu_font_sizeGroupBoxLayout)
        
        ##########
        self.text_font_sizeGroupBox = QGroupBox()
        self.text_font_sizeGroupBoxLayout = QVBoxLayout()
        self.text_font_sizeComboBox = QComboBox()
        self.text_font_sizeComboBox.addItems(self.font_sizes_list)
        
        self.text_font_sizeGroupBoxLayout.addWidget(self.text_font_sizeComboBox)
        self.text_font_sizeGroupBox.setLayout(self.text_font_sizeGroupBoxLayout)
        
        ##########
        self.input_font_sizeGroupBox = QGroupBox()
        self.input_font_sizeGroupBoxLayout = QVBoxLayout()
        self.input_font_sizeComboBox = QComboBox()
        self.input_font_sizeComboBox.addItems(self.font_sizes_list)
        
        self.input_font_sizeGroupBoxLayout.addWidget(self.input_font_sizeComboBox)
        self.input_font_sizeGroupBox.setLayout(self.input_font_sizeGroupBoxLayout)
        
        ##########
        self.fontsGroupBox = QGroupBox(self.language['settings_window_language'])
        
        self.fontsGroupBoxLayout = QHBoxLayout()

        self.fontsGroupBoxLayout.addWidget(self.menu_font_sizeGroupBox)
        self.fontsGroupBoxLayout.addWidget(self.text_font_sizeGroupBox)
        self.fontsGroupBoxLayout.addWidget(self.input_font_sizeGroupBox)
        
        
        self.fontsGroupBox.setLayout(self.fontsGroupBoxLayout)
        return self.fontsGroupBox

    
    def closeLanguage(self):
        self.hide()