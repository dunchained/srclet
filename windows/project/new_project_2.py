import os, shutil
cwd = os.path.curdir

from variables import css, var
from windows.data.check_data import CheckDataTypeWidget
from windows.project.project_opened import ProjectWindow
from mortys.font_morty import read_text_font_size, read_input_font_size

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGridLayout, QLabel, QFileDialog
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QPushButton, QGroupBox, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

#
class NewProjectWindow2(QWidget):
    def __init__(self, name_of_project, language):
        super().__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.language = language
        self.project_name = name_of_project
        self.project_path = cwd + var.projects_folder + name_of_project
        self.window_gui(name_of_project)
        
    def window_gui(self, name_of_project):
        self.setFixedSize(var.new_project_window_2_widith, var.new_project_window_2_height)
        self.setWindowTitle(self.language['new_project_2_title'] + ' ' + name_of_project)
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
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())    
        
    def refresh_after_data_check(self):
        self.buttonSaveAndExit.setEnabled(True)
        self.buttonSaveAndOpen.setEnabled(True)
        self.text_data_status.setText(self.language['new_project_2_label_loaded'])
        
    def load_and_check_data(self):
        self.groupBox = QGroupBox(self.language['new_project_2_data_caption'])
        self.font = self.groupBox.font()
        self.font.setPointSize(read_text_font_size())
        self.groupBox.setFont(self.font)
        
        self.buttonBrowse = QPushButton(self.language['new_project_2_btn_browse'])
        self.text_data_selected = QLabel()
        self.text_data_selected.setText(self.language['new_project_2_label_browse'])
        self.buttonBrowse.clicked.connect(self.browse)
        
        self.buttonLoadFile = QPushButton(self.language['new_project_2_btn_loadandcheck'])
        self.buttonLoadFile.clicked.connect(self.load_file)
        self.text_data_status = QLabel()
        self.text_data_status.setText(self.language['new_project_2_label_loadandcheck'])
        
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.buttonBrowse)
        self.vbox.addWidget(self.text_data_selected)
        self.vbox.addWidget(self.buttonLoadFile)
        self.vbox.addWidget(self.text_data_status)
        self.vbox.addStretch(1)
        self.groupBox.setLayout(self.vbox)
        
        return self.groupBox
    
    def browse(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, self.language['new_project_2_file_dialog'], os.path.curdir, '*.*')
        self.text_data_selected.setText(self.fileName)
        
    def load_file(self):
        if not self.text_data_selected.text() or self.text_data_selected.text() == 'No file selected.':
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['new_project_2_load_message'])
            self.msg.setWindowTitle(self.language['new_project_2_load_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            self.window = CheckDataTypeWidget(file_path=self.text_data_selected.text(),
                                                   project_path=self.project_path,
                                                   language=self.language)
            self.window.clicked.connect(self.refresh_after_data_check)
        
    def project_description(self):
        self.groupBox = QGroupBox(self.language['new_project_2_description_caption'])
        self.font = self.groupBox.font()
        self.font.setPointSize(read_text_font_size())
        self.groupBox.setFont(self.font)
        
        self.text_project_description = QTextEdit(self.language['new_project_2_description_initial'])
        
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
                
        self.buttonSaveAndExit = QPushButton(self.language['new_project_2_btn_save_and_exit'])
        self.buttonSaveAndExit.clicked.connect(self.save_and_exit)
        self.buttonSaveAndExit.setEnabled(False)
        
        self.buttonSaveAndOpen = QPushButton(self.language['new_project_2_btn_save_and_open'])
        self.buttonSaveAndOpen.clicked.connect(self.save_and_open)
        self.buttonSaveAndOpen.setEnabled(False)
        self.buttonCancel = QPushButton(self.language['new_project_2_btn_cancel'])
        self.buttonCancel.clicked.connect(self.cancel)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.buttonSaveAndExit)
        self.vbox.addWidget(self.buttonSaveAndOpen)
        self.vbox.addWidget(self.buttonCancel)
        
        self.vbox.addStretch(1)
        self.groupBox.setLayout(self.vbox)
        return self.groupBox

    def save_and_exit(self):
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
        

    def save_and_open(self):
        # provjeriti je li sve upisano    
        # snimiti project description        
        self.msg = QMessageBox()
        self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText(self.language['new_project_2_save_and_open_message'])
        self.msg.setWindowTitle(self.language['new_project_2_save_and_open_message_caption'])
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.message_close)
        self.msg.show()

    def message_close(self):
        self.hide()
        self.next_window = ProjectWindow(project_path=self.project_path, language=self.language)
        self.next_window.show()
        
    def cancel(self):
        shutil.rmtree(os.path.join(cwd + var.projects_folder + self.project_name), ignore_errors=True)	
        #os.rmdir(os.path.join(cwd + var.projects_folder + self.project_name))
        self.hide()
     