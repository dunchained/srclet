import os
cwd = os.path.curdir

from variables import css, var
from mortys.font_morty import read_text_font_size, read_input_font_size
from windows.project.new_project_2 import NewProjectWindow2
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QGridLayout, QLabel, QFileDialog
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QPushButton, QGroupBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
#

class NewProjectWindow(QWidget):
    def __init__(self, language):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = language
        self.window_gui()

    def window_gui(self):
        self.setFixedSize(var.new_project_window_widith, var.new_project_window_height)
        self.setWindowTitle(self.language['new_project_title'])
        self.setWindowIcon(QIcon(css.new_project_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.create_new_project())
        self.setLayout(self.grid)
        self.center_gui()
        self.show()
        
    def center_gui(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_new_project(self):
        self.groupBox = QGroupBox()
        self.font_text = self.groupBox.font()
        self.font_text.setPointSize(read_text_font_size())
        self.groupBox.setFont(self.font_text)
        
        self.text_save_project = QLabel(self.language['new_project_caption'])
        self.project_name = QLineEdit()
        
        self.font_input = self.project_name.font()
        self.font_input.setPointSize(read_input_font_size())
        self.project_name.setFont(self.font_input)
        
        self.buttonSaveProject = QPushButton(self.language['new_project_btn_create'])
        self.buttonSaveProject.clicked.connect(self.create_project)
        
        self.buttonCancel = QPushButton(self.language['new_project_btn_cancel'])
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
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['new_project_message_name'])
            self.msg.setWindowTitle(self.language['new_project_message_name_title'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            if not self.project_name.text():
                self.msg = QMessageBox()
                self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText(self.language['new_project_message_empty'])
                self.msg.setWindowTitle(self.language['new_project_message_empty_title'])
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.buttonClicked.connect(self.msg.close)
                self.msg.show()
            else:
                os.mkdir(cwd + var.projects_folder + self.project_name.text())
                self.hide()
                name_of_project = self.project_name.text()
                self.next_window = NewProjectWindow2(name_of_project, self.language)
                self.next_window.show()