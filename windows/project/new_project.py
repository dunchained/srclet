import os
from appdata import css
from windows.project.new_project_2 import NewProjectWindow2
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QGridLayout, QLabel, QFileDialog
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QPushButton, QGroupBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class NewProjectWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.WindowGUI()

    def WindowGUI(self):
        self.setFixedSize(300, 150)
        self.setWindowTitle('Create new project...')
        self.setWindowIcon(QIcon(css.new_project_window_icon))
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
        
        self.text_save_project = QLabel('Enter new project name:')
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
        
        self.lista_projekata = os.listdir(os.getcwd() + '/projects/')
        
        if self.project_name.text() in self.lista_projekata:
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText('There is a project with that name already...')
            self.msg.setWindowTitle('Project name...')
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            if not self.project_name.text():
                self.msg = QMessageBox()
                self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText('Project name can not be empty...')
                self.msg.setWindowTitle('Project name...')
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.buttonClicked.connect(self.msg.close)
                self.msg.show()
            else:
                os.mkdir(os.getcwd() + '/projects/' + self.project_name.text())
                self.hide()
                name_of_project = self.project_name.text()
                self.next_window = NewProjectWindow2(name_of_project)
                self.next_window.show()