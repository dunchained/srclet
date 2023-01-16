# python standard modules
import os

# app modules and windows
from variables import css, var
from windows.project.project_opened import ProjectWindow

# pyqt5 modules
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QGridLayout, QLabel, QPushButton, QGroupBox
from PyQt5.QtWidgets import QMessageBox, QComboBox, QDesktopWidget, QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QLineF, Qt
#
class OpenProjectWindow(QWidget):
    def __init__(self, language):
        super().__init__()
        self.language = language
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.window_gui()

    def window_gui(self):
        self.setFixedSize(var.open_project_widith, var.open_project_height)
        self.setWindowTitle(self.language['open_project_title'])
        self.setWindowIcon(QIcon(css.open_project_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.list_of_projects(), 0, 0, 1, 1)
        self.grid.addWidget(self.project_description(), 0, 1, 1, 1)
        self.grid.addWidget(self.do_something_with_project(), 1, 0, 1, 2)
        self.setLayout(self.grid)
        self.center_gui()
        self.show()
        
    def center_gui(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def list_of_projects(self):
        groupBox = QGroupBox(self.language['open_project_caption'])
        self.combo_box = QComboBox()
        self.combo_box.addItems(next(os.walk(os.path.curdir + var.projects_folder))[1])
        
        self.project_list = QListWidget()
        self.project_list.addItems(next(os.walk(os.path.curdir + var.projects_folder))[1])
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.combo_box)
        vbox.addWidget(self.project_list)
        groupBox.setLayout(vbox)
        return groupBox
    
    def project_description(self):
        groupBox = QGroupBox(self.language['open_project_caption'])
        self.combo_box = QComboBox()
        self.combo_box.addItems(next(os.walk(os.path.curdir + var.projects_folder))[1])
        vbox = QVBoxLayout()
        vbox.addWidget(self.combo_box)
        groupBox.setLayout(vbox)
        return groupBox

    def do_something_with_project(self):
        groupBox = QGroupBox(self.language['open_project_btn_caption'])
        buttonOpenProject = QPushButton(self.language['open_project_btn_open'])
        buttonOpenProject.clicked.connect(self.open_project)
        buttonDeleteProject = QPushButton(self.language['open_project_btn_delete'])
        buttonDeleteProject.clicked.connect(self.delete_project)
        buttonCancel = QPushButton(self.language['open_project_btn_cancel'])
        buttonCancel.clicked.connect(self.close)
        vbox = QVBoxLayout()
        vbox.addWidget(buttonOpenProject)
        vbox.addWidget(buttonDeleteProject)
        vbox.addWidget(buttonCancel)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox
    
    def open_project(self):
        self.project_path = os.path.curdir + var.projects_folder + self.combo_box.currentText()
        print(self.project_path)
        self.hide()
        self.next_window = ProjectWindow(project_path=self.project_path, language=self.language)
        self.next_window.show()

    def delete_project(self):
        pass