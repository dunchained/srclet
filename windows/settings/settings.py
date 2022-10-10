import json, os
cwd = os.path.curdir

from variables import css, var
from mortys.language_morty import read_language, update_language
from mortys.reader_morty import read_font_size_text, read_font_size_key, read_menu_font_size_current_text
from mortys.reader_morty import read_text_font_size_current_text, read_input_font_size_current_text
from mortys.font_morty import read_text_font_size, update_fonts
#
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
        self.setFixedSize(var.settings_window_widith, var.settings_window_height)
        self.setWindowTitle(self.language['settings_window_title'])
        self.setWindowIcon(QIcon(css.settings_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.settings(), 0, 0)
        self.setLayout(self.grid)
        self.center_gui()
        self.show()
        
    def center_gui(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def settings(self):
        self.font_sizes_list = read_font_size_text()
        
        ########## Menu font size:
        self.menu_font_sizeGroupBox = QGroupBox(self.language['settings_window_menu_font'])
        self.font = self.menu_font_sizeGroupBox.font()
        self.font.setPointSize(read_text_font_size())
        self.menu_font_sizeGroupBox.setFont(self.font)
        
        self.menu_font_sizeGroupBoxLayout = QVBoxLayout()
        self.menu_font_sizeComboBox = QComboBox()
        self.menu_font_sizeComboBox.addItems(self.font_sizes_list)
        self.menu_font_sizeComboBox.setCurrentText(read_menu_font_size_current_text())

        self.menu_font_sizeGroupBoxLayout.addWidget(self.menu_font_sizeComboBox)
        self.menu_font_sizeGroupBox.setLayout(self.menu_font_sizeGroupBoxLayout)
        
        ########## Text font size:
        self.text_font_sizeGroupBox = QGroupBox(self.language['settings_window_text_font'])
        self.text_font_sizeGroupBox.setFont(self.font)
        self.text_font_sizeGroupBoxLayout = QVBoxLayout()
        self.text_font_sizeComboBox = QComboBox()
        self.text_font_sizeComboBox.addItems(self.font_sizes_list)
        self.text_font_sizeComboBox.setCurrentText(read_text_font_size_current_text())
        
        self.text_font_sizeGroupBoxLayout.addWidget(self.text_font_sizeComboBox)
        self.text_font_sizeGroupBox.setLayout(self.text_font_sizeGroupBoxLayout)
        
        ########## Input font size:
        self.input_font_sizeGroupBox = QGroupBox(self.language['settings_window_input_font'])
        self.input_font_sizeGroupBox.setFont(self.font)
        self.input_font_sizeGroupBoxLayout = QVBoxLayout()
        self.input_font_sizeComboBox = QComboBox()
        self.input_font_sizeComboBox.addItems(self.font_sizes_list)
        self.input_font_sizeComboBox.setCurrentText(read_input_font_size_current_text())
        
        self.input_font_sizeGroupBoxLayout.addWidget(self.input_font_sizeComboBox)
        self.input_font_sizeGroupBox.setLayout(self.input_font_sizeGroupBoxLayout)
        
        ########## Language:
        self.languageGroupBox = QGroupBox(self.language['settings_window_language'])
        self.languageGroupBox.setFont(self.font)
        self.combo_box = QComboBox()
        self.combo_box.addItems(next(os.walk(cwd + var.language_folder))[1])
        self.combo_box.setCurrentText(read_language())
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.combo_box)
        self.languageGroupBox.setLayout(self.vbox)
        
        ########## All:
        self.fontsGroupBox = QGroupBox(self.language['settings_window_groupbox'])
        self.fontsGroupBox.setFont(self.font)
        self.buttonSave = QPushButton(self.language['settings_window_btn_save'])
        self.buttonSave.clicked.connect(self.save)
        self.buttonClose = QPushButton(self.language['settings_window_btn_close'])
        self.buttonClose.clicked.connect(self.close)
        
        self.fontsGroupBoxLayout = QGridLayout()
        
        self.fontsGroupBoxLayout.addWidget(self.menu_font_sizeGroupBox, 0, 1, 1, 1)
        self.fontsGroupBoxLayout.addWidget(self.text_font_sizeGroupBox, 0, 2, 1, 1)
        self.fontsGroupBoxLayout.addWidget(self.input_font_sizeGroupBox, 0, 3, 1, 1)
        self.fontsGroupBoxLayout.addWidget(self.languageGroupBox, 0, 4, 1, 1)
        self.fontsGroupBoxLayout.addWidget(self.buttonSave, 1, 1, 1, 4)
        self.fontsGroupBoxLayout.addWidget(self.buttonClose, 2, 1, 1, 4)
                
        self.fontsGroupBox.setLayout(self.fontsGroupBoxLayout)
  
        return self.fontsGroupBox
        
    def save(self):
        update_fonts(
            menu_font_size=read_font_size_key(font_size_text=self.menu_font_sizeComboBox.currentText()),
            text_font_size=read_font_size_key(font_size_text=self.text_font_sizeComboBox.currentText()),
            input_font_size=read_font_size_key(font_size_text=self.input_font_sizeComboBox.currentText())
            )
        update_language(new_language=self.combo_box.currentText())
               
        self.msg = QMessageBox()
        self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText(self.language['settings_window_message'])
        self.msg.setWindowTitle(self.language['settings_window_message_caption'])
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.msg.close)
        self.msg.show()
        
    def close(self):
        self.hide()