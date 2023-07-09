from windows.project.project_opened import ProjectWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QListWidget
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGridLayout, QLabel, QPushButton, QGroupBox
from mortys.font_morty import read_text_font_size
from variables import css, var
import os
import json
import shutil
cwd = os.path.curdir
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
        self.list_of_projects_groupbox = QGroupBox(
            self.language['open_project_caption'])
        self.font_text = self.list_of_projects_groupbox.font()
        self.font_text.setPointSize(read_text_font_size())
        self.list_of_projects_groupbox.setFont(self.font_text)
        self.project_list = QListWidget()
        self.project_list.addItems(
            next(os.walk(os.path.curdir + var.projects_folder))[1])
        self.project_list.currentItemChanged.connect(self.index_changed)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.project_list)
        self.list_of_projects_groupbox.setLayout(self.vbox)
        self.list_of_projects_groupbox.setFixedWidth(350)
        return self.list_of_projects_groupbox

    def index_changed(self, i):
        self.json_path = cwd + var.projects_folder + i.text() + '/data.json'
        with open(self.json_path) as json_file:
            data = json.load(json_file)
        self.label_project_description.setText(data['project_description'])
        self.item_text = i.text()

    def project_description(self):
        self.project_description_groupbox = QGroupBox(
            self.language['open_project_description_caption'])
        self.font_text = self.project_description_groupbox.font()
        self.font_text.setPointSize(read_text_font_size())
        self.project_description_groupbox.setFont(self.font_text)
        self.label_project_description = QLabel()
        self.label_project_description.setWordWrap(True)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label_project_description)
        self.project_description_groupbox.setLayout(self.vbox)
        return self.project_description_groupbox

    def do_something_with_project(self):
        self.dswp_groupbox = QGroupBox(
            self.language['open_project_btn_caption'])
        self.font_text = self.dswp_groupbox.font()
        self.font_text.setPointSize(read_text_font_size())
        self.dswp_groupbox.setFont(self.font_text)
        self.buttonOpenProject = QPushButton(
            self.language['open_project_btn_open'])
        self.buttonOpenProject.clicked.connect(self.open_project)
        self.buttonDeleteProject = QPushButton(
            self.language['open_project_btn_delete'])
        self.buttonDeleteProject.clicked.connect(self.delete_procedure)
        self.buttonCancel = QPushButton(
            self.language['open_project_btn_cancel'])
        self.buttonCancel.clicked.connect(self.close)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.buttonOpenProject)
        self.vbox.addWidget(self.buttonDeleteProject)
        self.vbox.addWidget(self.buttonCancel)
        self.vbox.addStretch(1)
        self.dswp_groupbox.setLayout(self.vbox)
        return self.dswp_groupbox

    def open_project(self):
        self.project_path = cwd + var.projects_folder + self.item_text
        self.hide()
        self.next_window = ProjectWindow(
            project_path=self.project_path, language=self.language)
        self.next_window.show()

    def delete_procedure(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(self.language['open_project_delete_message'])
        msgBox.setWindowTitle(
            self.language['open_project_delete_message_title'])
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        buttonOK = msgBox.button(QMessageBox.Ok)
        buttonOK.setText(self.language['open_project_delete_ok'])
        buttonCancel = msgBox.button(QMessageBox.Cancel)
        buttonCancel.setText(self.language['open_project_delete_cancel'])
        msgBox.buttonClicked.connect(self.delete_project)

        returnValue = msgBox.exec()
        # if returnValue == QMessageBox.Ok:
        # self.delete_project()

    def delete_project(self, value):
        if value.text() == self.language['open_project_delete_ok']:
            shutil.rmtree(os.path.join(cwd + var.projects_folder +
                          self.item_text), ignore_errors=True)
            self.refresh_project_list()
        else:
            pass

    def refresh_project_list(self):
        item_to_remove = self.project_list.selectedItems()
        if not item_to_remove:
            return
        for item in item_to_remove:
            self.project_list.takeItem(self.project_list.row(item))
