from mortys.language_morty import bind_key
from pathlib import Path
from PyQt6.QtWidgets import QFileDialog
from mortys.language_morty import bind, tr
from windows.project.project_opened import ProjectWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox, QListWidget
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QGridLayout, QLabel, QPushButton, QGroupBox
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
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowCloseButtonHint)
        self.window_gui()

    def window_gui(self):
        self.setFixedSize(var.open_project_widith, var.open_project_height)
        bind_key(self, "windowTitle", 'open_project_title')
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
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def list_of_projects(self):
        self.list_of_projects_groupbox = bind_key(QGroupBox(), "title", 'open_project_caption')
        self.font_text = self.list_of_projects_groupbox.font()
        self.font_text.setPointSize(read_text_font_size())
        self.list_of_projects_groupbox.setFont(self.font_text)
        self.project_list = QListWidget()
        self.project_list.addItems(sorted(p.name for p in Path("projects").iterdir()
                                         if (p / "data.json").is_file() and (p / "data.xlsx").is_file()))
        self.project_list.currentItemChanged.connect(self.index_changed)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.project_list)
        self.list_of_projects_groupbox.setLayout(self.vbox)
        self.list_of_projects_groupbox.setFixedWidth(350)
        return self.list_of_projects_groupbox

    def index_changed(self, i):
        if i is None:
            return
        self.json_path = cwd + var.projects_folder + i.text() + '/data.json'
        try:
            data = json.loads(Path(self.json_path).read_text(encoding="utf-8-sig"))
            self.label_project_description.setText(str(data.get("project_description", "")))
        except (OSError, ValueError, AttributeError) as exc:
            self.label_project_description.setText(tr("Data error") + " · " + str(exc))
        self.item_text = i.text()

    def project_description(self):
        self.project_description_groupbox = bind_key(QGroupBox(), "title", 'open_project_description_caption')
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
        self.dswp_groupbox = bind_key(QGroupBox(), "title", 'open_project_btn_caption')
        self.font_text = self.dswp_groupbox.font()
        self.font_text.setPointSize(read_text_font_size())
        self.dswp_groupbox.setFont(self.font_text)
        self.buttonOpenProject = bind_key(QPushButton(), "text", 'open_project_btn_open')
        self.buttonOpenProject.clicked.connect(self.open_project)
        self.buttonDeleteProject = bind_key(QPushButton(), "text", 'open_project_btn_delete')
        self.buttonDeleteProject.clicked.connect(self.delete_procedure)
        self.buttonCancel = bind_key(QPushButton(), "text", 'open_project_btn_cancel')
        self.buttonCancel.clicked.connect(self.close)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.buttonOpenProject)
        browse = bind(QPushButton(), "text", "Open folder…")
        browse.clicked.connect(self.choose_folder)
        self.vbox.addWidget(browse)
        self.vbox.addWidget(self.buttonDeleteProject)
        self.vbox.addWidget(self.buttonCancel)
        self.vbox.addStretch(1)
        self.dswp_groupbox.setLayout(self.vbox)
        return self.dswp_groupbox

    def open_project(self):
        if self.project_list.currentItem():
            self.open_path(Path("projects") / self.project_list.currentItem().text())

    def choose_folder(self):
        path = QFileDialog.getExistingDirectory(self, tr("Project"))
        if path:
            self.open_path(Path(path))

    def open_path(self, path):
        from zipfile import BadZipFile
        try:
            self.next_window = ProjectWindow(str(path.resolve()), self.language)
        except (OSError, ValueError, KeyError, BadZipFile) as error:
            QMessageBox.warning(self, tr("Data error"), str(error))
            return
        self.hide()

    def delete_procedure(self):
        if not self.project_list.currentItem():
            return
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Information)
        bind_key(msgBox, "text", 'open_project_delete_message')
        bind_key(msgBox, "windowTitle", 'open_project_delete_message_title')
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        buttonOK = msgBox.button(QMessageBox.StandardButton.Ok)
        bind_key(buttonOK, "text", 'open_project_delete_ok')
        buttonCancel = msgBox.button(QMessageBox.StandardButton.Cancel)
        bind_key(buttonCancel, "text", 'open_project_delete_cancel')
        msgBox.buttonClicked.connect(self.delete_project)

        returnValue = msgBox.exec()
        # if returnValue == QMessageBox.StandardButton.Ok:
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
