import os, json
cwd = os.path.curdir

from css import css, var
from windows.data.check_data import CheckDataTypeWidget
from windows.project.project_opened import ProjectWindow

from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QGridLayout, QLabel, QFileDialog
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QPushButton, QGroupBox, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class NewProjectWindow2(QWidget):
    
    def __init__(self, name_of_project, language):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = language
        self.project_name = name_of_project
        self.project_path = cwd + var.projects_folder + name_of_project
        self.WindowGUI(name_of_project)
        
    def WindowGUI(self, name_of_project):
        #self.setFixedSize(800, 600)
        self.setWindowTitle(self.language['new_project_2_title'] + name_of_project)
        self.setWindowIcon(QIcon(css.new_project_window2_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.loadAndCheckData(), 0, 0, 1, 1)
        self.grid.addWidget(self.projectDescription(), 0, 1, 1, 1)
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
        groupBox = QGroupBox(self.language['new_project_2_data_caption'])
        buttonBrowse = QPushButton(self.language['new_project_2_btn_browse'])
        self.text_data_selected = QLabel()
        self.text_data_selected.setText(self.language['new_project_2_label_browse'])
        buttonBrowse.clicked.connect(self.buttonBrowse)
        buttonLoadFile = QPushButton(self.language['new_project_2_btn_loadandcheck'])
        buttonLoadFile.clicked.connect(self.buttonLoadFile)
        self.text_data_status = QLabel()
        self.text_data_status.setText(self.language['new_project_2_label_loadandcheck'])
        vbox = QVBoxLayout()
        vbox.addWidget(buttonBrowse)
        vbox.addWidget(self.text_data_selected)
        vbox.addWidget(buttonLoadFile)
        vbox.addWidget(self.text_data_status)
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
            self.window = CheckDataTypeWidget(file_path=file_path, project_path=project_path, language=self.language)
    
    
    def projectDescription(self):
        groupBox = QGroupBox(self.language['new_project_2_description_caption'])
        self.textDescription = QTextEdit()
        vbox = QVBoxLayout()
        vbox.addWidget(self.textDescription)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def saveProject(self):
        groupBox = QGroupBox()
        buttonSaveAndExit = QPushButton(self.language['new_project_2_btn_save_and_exit'])
        buttonSaveAndExit.clicked.connect(self.saveAndExit)
        buttonSaveAndOpen = QPushButton(self.language['new_project_2_btn_save_and_open'])
        buttonSaveAndOpen.clicked.connect(self.saveAndOpen)
        buttonCancel = QPushButton(self.language['new_project_2_btn_cancel'])
        buttonCancel.clicked.connect(self.cancel)

        vbox = QVBoxLayout()
        vbox.addWidget(buttonSaveAndExit)
        vbox.addWidget(buttonSaveAndOpen)
        vbox.addWidget(buttonCancel)
        
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def saveAndExit(self):
        # provjeriti je li sve upisano i mesege         
        # snimiti project description   
        self.msg = QMessageBox()
        self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText(self.language['new_project_2_save_and_exit_message'])
        self.msg.setWindowTitle(self.language['new_project_2_save_and_exit_message_caption'])
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.close)
        self.msg.show()
        

    def saveAndOpen(self):
        # provjeriti je li sve upisano    
        # snimiti project description        
        self.msg = QMessageBox()
        self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText(self.language['new_project_2_save_and_open_message'])
        self.msg.setWindowTitle(self.language['new_project_2_save_and_open_message_caption'])
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.messageClose)
        self.msg.show()

    def messageClose(self):
        self.hide()
        self.next_window = ProjectWindow(project_path=self.project_path, language=self.language)
        self.next_window.show()
        
    def cancel(self):
        # izbrisati direktorij projekta i poruku zadat
        pass