from mortys.language_morty import bind_key
import os
cwd = os.path.curdir

from variables import css, var
from mortys.font_morty import read_text_font_size, read_input_font_size
from windows.project.new_project_2 import NewProjectWindow2
from PyQt6.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QGridLayout, QLabel
from PyQt6.QtWidgets import QMessageBox, QPushButton, QGroupBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
#

class NewProjectWindow(QWidget):
    def __init__(self, language):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowCloseButtonHint)
        self.language = language
        self.window_gui()

    def window_gui(self):
        self.setFixedSize(var.new_project_window_widith, var.new_project_window_height)
        bind_key(self, "windowTitle", 'new_project_title')
        self.setWindowIcon(QIcon(css.new_project_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.create_new_project())
        self.setLayout(self.grid)
        self.center_gui()
        self.show()
        
    def center_gui(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_new_project(self):
        self.groupBox = QGroupBox()
        self.font_text = self.groupBox.font()
        self.font_text.setPointSize(read_text_font_size())
        self.groupBox.setFont(self.font_text)
        
        self.text_save_project = bind_key(QLabel(), "text", 'new_project_caption')
        self.project_name = QLineEdit()
        
        self.font_input = self.project_name.font()
        self.font_input.setPointSize(read_input_font_size())
        self.project_name.setFont(self.font_input)
        
        self.buttonSaveProject = bind_key(QPushButton(), "text", 'new_project_btn_create')
        self.buttonSaveProject.clicked.connect(self.create_project)
        
        self.buttonCancel = bind_key(QPushButton(), "text", 'new_project_btn_cancel')
        self.buttonCancel.clicked.connect(self.close)
        
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.text_save_project)
        self.vbox.addWidget(self.project_name)
        self.vbox.addWidget(self.buttonSaveProject)
        self.vbox.addWidget(self.buttonCancel)
        self.vbox.addStretch(1)
        self.groupBox.setLayout(self.vbox)
        return self.groupBox

    def create_project(self):
        self.lista_projekata = os.listdir(cwd + var.projects_folder)
        if self.project_name.text() in self.lista_projekata:
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Icon.Information)
            bind_key(self.msg, "text", 'new_project_message_name')
            bind_key(self.msg, "windowTitle", 'new_project_message_name_title')
            self.msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            if not self.project_name.text():
                self.msg = QMessageBox()
                self.msg.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
                self.msg.setIcon(QMessageBox.Icon.Information)
                bind_key(self.msg, "text", 'new_project_message_empty')
                bind_key(self.msg, "windowTitle", 'new_project_message_empty_title')
                self.msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                self.msg.buttonClicked.connect(self.msg.close)
                self.msg.show()
            else:
                os.mkdir(cwd + var.projects_folder + self.project_name.text())
                self.hide()
                name_of_project = self.project_name.text()
                self.next_window = NewProjectWindow2(name_of_project, self.language)
                self.next_window.show()