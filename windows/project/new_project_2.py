from mortys.language_morty import bind_key
from windows.project.project_opened import ProjectWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox, QPushButton, QGroupBox, QTextEdit
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QGridLayout, QLabel, QFileDialog
from mortys.project_description_morty import update_project_description
from mortys.font_morty import read_text_font_size, read_input_font_size
from windows.data.check_data import CheckDataTypeWidget
from variables import css, var
import os
import shutil
cwd = os.path.curdir


class NewProjectWindow2(QWidget):
    def __init__(self, name_of_project, language):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
        self.language = language
        self.project_name = name_of_project
        self.project_path = cwd + var.projects_folder + name_of_project
        self.window_gui(name_of_project)

    def window_gui(self, name_of_project):
        self.setFixedSize(var.new_project_window_2_widith,
                          var.new_project_window_2_height)
        self.setWindowTitle(
            self.language['new_project_2_title'] + ' ' + name_of_project)
        self.setWindowIcon(QIcon(css.new_project_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.load_and_check_data(), 0, 0, 1, 1)
        self.grid.addWidget(self.project_description(), 0, 1, 1, 1)
        self.grid.addWidget(self.save_project(), 1, 0, 1, 2)
        self.setLayout(self.grid)
        self.center_gui()
        self.show()

    def center_gui(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def refresh_after_data_check(self):
        self.buttonSaveAndExit.setEnabled(True)
        self.buttonSaveAndOpen.setEnabled(True)
        bind_key(self.text_data_status, "text", 'new_project_2_label_loaded')

    def load_and_check_data(self):
        self.groupBox = bind_key(QGroupBox(), "title", 'new_project_2_data_caption')
        self.font = self.groupBox.font()
        self.font.setPointSize(read_text_font_size())
        self.groupBox.setFont(self.font)

        self.buttonBrowse = bind_key(QPushButton(), "text", 'new_project_2_btn_browse')
        self.text_data_selected = QLabel()
        self.text_data_selected.setWordWrap(True)
        bind_key(self.text_data_selected, "text", 'new_project_2_label_browse')
        self.buttonBrowse.clicked.connect(self.browse)

        self.buttonLoadFile = bind_key(QPushButton(), "text", 'new_project_2_btn_loadandcheck')
        self.buttonLoadFile.clicked.connect(self.load_file)
        self.text_data_status = QLabel()
        bind_key(self.text_data_status, "text", 'new_project_2_label_loadandcheck')

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.buttonBrowse)
        self.vbox.addWidget(self.text_data_selected)
        self.vbox.addWidget(self.buttonLoadFile)
        self.vbox.addWidget(self.text_data_status)
        self.vbox.addStretch(1)
        self.groupBox.setLayout(self.vbox)
        self.groupBox.setFixedWidth(400)

        return self.groupBox

    def browse(self):
        self.fileName, _ = QFileDialog.getOpenFileName(
            self, self.language['new_project_2_file_dialog'], os.path.curdir, '*.txt')

        with open(self.fileName) as f:
            lines = f.readlines()

        tabs = []
        letabs = []
        for line in lines:
            lineContains = line.split('\t')
            lineLength = len(lineContains)  # calculate elements

            if lineLength < 3:
                letabs.append(line)
            else:
                tabs.append(lineContains)

        if len(letabs) != 0:
            print('file not supported warning')
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Icon.Information)
            bind_key(self.msg, "text", 'new_project_2_browse_message')
            bind_key(self.msg, "windowTitle", 'new_project_2_browse_message_caption')
            self.msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            # print('napravi izmjene koje trebs na gui i idi dalje')
            self.text_data_selected.setText(self.fileName)

    def load_file(self):
        if not self.text_data_selected.text() or self.text_data_selected.text() == self.language['new_project_2_label_browse']:
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Icon.Information)
            bind_key(self.msg, "text", 'new_project_2_load_message')
            bind_key(self.msg, "windowTitle", 'new_project_2_load_message_caption')
            self.msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            self.window = CheckDataTypeWidget(file_path=self.text_data_selected.text(
            ), project_path=self.project_path, language=self.language)
            self.window.clicked.connect(self.refresh_after_data_check)

    def project_description(self):
        self.groupBox = bind_key(QGroupBox(), "title", 'new_project_2_description_caption')
        self.font = self.groupBox.font()
        self.font.setPointSize(read_input_font_size())
        self.groupBox.setFont(self.font)

        self.text_project_description = QTextEdit(
            self.language['new_project_2_description_initial'])

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.text_project_description)
        self.vbox.addStretch(1)

        self.groupBox.setLayout(self.vbox)

        return self.groupBox

    def save_project(self):
        self.groupBox = QGroupBox()
        self.font = self.groupBox.font()
        self.font.setPointSize(read_text_font_size())
        self.groupBox.setFont(self.font)

        self.buttonSaveAndExit = bind_key(QPushButton(), "text", 'new_project_2_btn_save_and_exit')
        self.buttonSaveAndExit.clicked.connect(self.save_and_exit)
        self.buttonSaveAndExit.setEnabled(False)

        self.buttonSaveAndOpen = bind_key(QPushButton(), "text", 'new_project_2_btn_save_and_open')
        self.buttonSaveAndOpen.clicked.connect(self.save_and_open)
        self.buttonSaveAndOpen.setEnabled(False)
        self.buttonCancel = bind_key(QPushButton(), "text", 'new_project_2_btn_cancel')
        self.buttonCancel.clicked.connect(self.cancel)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.buttonSaveAndExit)
        self.vbox.addWidget(self.buttonSaveAndOpen)
        self.vbox.addWidget(self.buttonCancel)

        self.vbox.addStretch(1)
        self.groupBox.setLayout(self.vbox)
        return self.groupBox

    def save_and_exit(self):
        self.file_path = self.project_path + '/' + 'data.json'
        update_project_description(data_file_path=self.file_path,
                                   updated_data=self.text_project_description.toPlainText())
        self.msg = QMessageBox()
        self.msg.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.msg.setIcon(QMessageBox.Icon.Information)
        bind_key(self.msg, "text", 'new_project_2_save_and_exit_message')
        bind_key(self.msg, "windowTitle", 'new_project_2_save_and_exit_message_caption')
        self.msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.msg.buttonClicked.connect(self.close)
        self.msg.show()

    def save_and_open(self):
        self.file_path = self.project_path + '/' + 'data.json'
        update_project_description(data_file_path=self.file_path,
                                   updated_data=self.text_project_description.toPlainText())
        self.msg = QMessageBox()
        self.msg.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.msg.setIcon(QMessageBox.Icon.Information)
        bind_key(self.msg, "text", 'new_project_2_save_and_open_message')
        bind_key(self.msg, "windowTitle", 'new_project_2_save_and_open_message_caption')
        self.msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.msg.buttonClicked.connect(self.message_close)
        self.msg.show()

    def message_close(self):
        self.hide()
        self.next_window = ProjectWindow(
            project_path=self.project_path, language=self.language)
        self.next_window.show()

    def cancel(self):
        shutil.rmtree(os.path.join(cwd + var.projects_folder +
                      self.project_name), ignore_errors=True)
        self.hide()
