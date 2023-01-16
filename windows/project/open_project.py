# python standard modules
import os, json, shutil
cwd = os.path.curdir

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
        self.list_of_projects_groupbox = QGroupBox(self.language['open_project_caption'])
        self.project_list = QListWidget()
        self.project_list.addItems(next(os.walk(os.path.curdir + var.projects_folder))[1])
        self.project_list.currentItemChanged.connect(self.index_changed)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.project_list)
        self.list_of_projects_groupbox.setLayout(self.vbox)
        self.list_of_projects_groupbox.setMaximumWidth(350)
        return self.list_of_projects_groupbox
    
    def index_changed(self, i):
        self.json_path = cwd + var.projects_folder + i.text() + '/data.json'
        with open(self.json_path) as json_file:
            data = json.load(json_file)
        self.label_project_description.setText(data['project_description'])
        self.item_text = i.text()
    
    def project_description(self):
        self.project_description_groupbox = QGroupBox(self.language['open_project_description_caption'])
        self.label_project_description = QLabel()
        self.label_project_description.setWordWrap(True)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label_project_description)
        self.project_description_groupbox.setLayout(self.vbox)
        return self.project_description_groupbox

    def do_something_with_project(self):
        groupBox = QGroupBox(self.language['open_project_btn_caption'])
        buttonOpenProject = QPushButton(self.language['open_project_btn_open'])
        buttonOpenProject.clicked.connect(self.open_project)
        buttonDeleteProject = QPushButton(self.language['open_project_btn_delete'])
        buttonDeleteProject.clicked.connect(self.delete_procedure)
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
        self.project_path = cwd + var.projects_folder + self.item_text
        self.hide()
        self.next_window = ProjectWindow(project_path=self.project_path, language=self.language)
        self.next_window.show()
        
    def delete_procedure(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(self.language['open_project_delete_message'])
        msgBox.setWindowTitle(self.language['open_project_delete_message_title'])
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        buttonOK = msgBox.button(QMessageBox.Ok)
        buttonOK.setText(self.language['open_project_delete_ok'])
        buttonCancel = msgBox.button(QMessageBox.Cancel)
        buttonCancel.setText(self.language['open_project_delete_cancel'])
        msgBox.buttonClicked.connect(self.delete_project)

        returnValue = msgBox.exec()
        #if returnValue == QMessageBox.Ok:
            #self.delete_project()

    def delete_project(self, value):
        if value.text() == self.language['open_project_delete_ok']:
            shutil.rmtree(os.path.join(cwd + var.projects_folder + self.item_text), ignore_errors=True)
            self.refresh_project_list()
        else:
            pass
        
    def refresh_project_list(self):
        item_to_remove = self.project_list.selectedItems()
        if not item_to_remove: return
        for item in item_to_remove:
            self.project_list.takeItem(self.project_list.row(item))
        