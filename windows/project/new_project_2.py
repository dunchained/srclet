# python standard modules
import os

# app modules and windows
from appdata import css
from windows.data.check_data import CheckDataTypeWidget

# pyqt5 modules
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QGridLayout, QLabel, QFileDialog, QPushButton, QGroupBox
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class NewProjectWindow2(QWidget):
    
    def __init__(self, name_of_project):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.WindowGUI(name_of_project)
        self.project_path = os.getcwd() + '/projects/' + name_of_project

    def WindowGUI(self, name_of_project):
        self.setFixedSize(400, 300)
        self.setWindowTitle('Create New Project: ' + name_of_project)
        self.setWindowIcon(QIcon(css.menu_about_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.loadAndCheckData())
        self.grid.addWidget(self.saveProject())
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())    

    def loadAndCheckData(self):
        groupBox = QGroupBox('Browse for data file...')
        buttonBrowse = QPushButton('Browse')
        self.text_data_selected = QLabel()
        self.text_data_selected.setText('No file selected.')
        buttonBrowse.clicked.connect(self.buttonBrowse)
        buttonLoadFile = QPushButton('Load file and check data')
        buttonLoadFile.clicked.connect(self.buttonLoadFile)
        self.text_data_status = QLabel()
        self.text_data_status.setText('File not checked.')
        vbox = QVBoxLayout()
        vbox.addWidget(buttonBrowse)
        vbox.addWidget(self.text_data_selected)
        vbox.addWidget(buttonLoadFile)
        vbox.addWidget(self.text_data_status)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def saveProject(self):
        groupBox = QGroupBox()
        buttonSaveAndExit = QPushButton('Save project and Exit')
        buttonSaveAndExit.clicked.connect(self.saveAndExit)
        buttonSaveAndOpen = QPushButton('Save project and Open')
        buttonSaveAndOpen.clicked.connect(self.saveAndOpen)

        vbox = QVBoxLayout()
        vbox.addWidget(buttonSaveAndExit)
        vbox.addWidget(buttonSaveAndOpen)
        
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def buttonBrowse(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, 'Open data file...', os.path.curdir, '*.*')
        self.text_data_selected.setText(self.fileName)

    def buttonLoadFile(self):
        if self.text_data_selected.text() == 'No file selected.':
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText('Please select data file...')
            self.msg.setWindowTitle('Data file...')
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            project_path_to_forward = self.project_path
            file_path_from_other_window = self.text_data_selected.text()
            self.window = CheckDataTypeWidget(file_path_from_other_window, project_path_to_forward)
    
    def saveAndExit(self):
        pass

    def saveAndOpen(self):
        pass