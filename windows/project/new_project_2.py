import os, json
from appdata import css
from windows.data.check_data import CheckDataTypeWidget
from windows.project.project_opened import ProjectWindow

from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QGridLayout, QLabel, QFileDialog
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QPushButton, QGroupBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class NewProjectWindow2(QWidget):
    
    def __init__(self, name_of_project):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.WindowGUI(name_of_project)
        self.project_path = os.getcwd() + '/projects/' + name_of_project
        self.project_name = name_of_project
        print(self.project_path)

    def WindowGUI(self, name_of_project):
        self.setFixedSize(800, 600)
        self.setWindowTitle('Create New Project: ' + name_of_project)
        self.setWindowIcon(QIcon(css.new_project_window2_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.loadAndCheckData(), 0, 0, 1, 1)
        self.grid.addWidget(self.projectParameters(), 0, 1, 1, 1)
        self.grid.addWidget(self.saveProject(), 1, 0, -1, 2)
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())    

    def loadAndCheckData(self):
        groupBox = QGroupBox('project data file...')
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
    
    def projectParameters(self):
        groupBox = QGroupBox('Project settings and parameters...')
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
            project_path = self.project_path
            file_path = self.text_data_selected.text()
            self.window = CheckDataTypeWidget(file_path, project_path)
    
    def saveAndExit(self):
        print(self.project_path)
        project_settings_dict = {
            "name": 'parametar1',
            "unit": 'parametar2',
            "description": 'parametar3'
            }
        
        json_object = json.dumps(project_settings_dict, indent = 4)
        with open(self.project_path + '/' + "settings.json", "w") as outfile:
            outfile.write(json_object)
            
        self.msg = QMessageBox()
        self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText('Project saved...')
        self.msg.setWindowTitle('Successuful...')
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.close)
        self.msg.show()
        

    def saveAndOpen(self):
        print(self.project_path)
        project_settings_dict = {
            "name": 'parametar1',
            "unit": 'parametar2',
            "description": 'parametar3'
            }
        
        json_object = json.dumps(project_settings_dict, indent = 4)
        with open(self.project_path + '/' + "settings.json", "w") as outfile:
            outfile.write(json_object)
            
        self.msg = QMessageBox()
        self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText('Project saved...')
        self.msg.setWindowTitle('Successuful...')
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.messageClose)
        self.msg.show()

    def messageClose(self):
        self.hide()
        self.next_window = ProjectWindow(project_path=self.project_path)
        self.next_window.show()