# python standard modules
import os

# app modules and windows
from appdata import css
from windows.project.new_project_2 import NewProjectWindow2

# pyqt5 modules
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QGridLayout, QLabel, QFileDialog, QPushButton, QGroupBox
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class NewProjectWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.WindowGUI()

    def WindowGUI(self):
        self.setFixedSize(300, 150)
        self.setWindowTitle('Create New Project')
        self.setWindowIcon(QIcon(css.menu_about_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.createNewProject())
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def createNewProject(self):
        groupBox = QGroupBox()
        self.text_save_project = QLabel()
        self.text_save_project.setText('Project name:')
        self.project_name = QLineEdit()
        buttonSaveProject = QPushButton('Create project')
        buttonSaveProject.clicked.connect(self.createProject)
        buttonCancel = QPushButton('Cancel')
        buttonCancel.clicked.connect(self.close)
        vbox = QVBoxLayout()
        vbox.addWidget(self.text_save_project)
        vbox.addWidget(self.project_name)
        vbox.addWidget(buttonSaveProject)
        vbox.addWidget(buttonCancel)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def createProject(self):
        self.project_name = self.project_name.text()
        
        if not self.project_name:
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText('Project name can not be empty...')
            self.msg.setWindowTitle('Project name...')
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            # ovdje treba još jedan uslov da provjeri da li ima već projekat sa istim imenom
            os.mkdir(os.getcwd() + '/projects/' + self.project_name)
            self.hide()
            name_of_project = self.project_name
            self.next_window = NewProjectWindow2(name_of_project)
            self.next_window.show()
            
            # poruka da li želite otvoriti kreirani projekat