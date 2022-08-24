# python standard modules
import sys, json, os
from pathlib import Path

# app modules and windows
#from css import css
#from parameters.ParametersWindow import *

# pyqt5 modules
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QPushButton, QLineEdit
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

class AddParameter(QWidget):
    clicked = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = {
            "add_parameter_window_title": "Add new parameter",
            "add_parameter_window_caption": "Parameter information:",
            "add_parameter_window_filename": "Filename:",
            "add_parameter_window_filename_exp": "Text to be used as parameter filename.",
            "add_parameter_window_name": "Parameter name:",
            "add_parameter_window_name_exp": "Text to be used as parameter short description",
            "add_parameter_window_unit": "Parameter unit:",
            "add_parameter_window_unit_exp": "Unit to be used...",
            "add_parameter_window_symbol": "Parameter symbol:",
            "add_parameter_window_symbol_exp": "Text to be used as parameter symbol in forulas.",
            "add_parameter_window_desc": "Parameter description:",
            "add_parameter_window_desc_exp": "Text to be used for short explinations.",
            "add_parameter_window_btn_add": "Save",
            "add_parameter_window_btn_cancel": "Cancel",
            "add_parameter_window_save_message": "Parameter name or unit empty...",
            "add_parameter_window_save_message_caption": "Missing data...",
            "add_parameter_window_saved_message": "Parameter saved...",
            "add_parameter_window_saved_message_caption": "Successuful...",
            "add_parameter_window_filename_message": "Parameter with this filename already exists.",
            "add_parameter_window_filename_message_caption": "Filename..."
        }
        self.WindowGUI()

    def WindowGUI(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle(self.language['add_parameter_window_title'])
        #self.setWindowIcon(QIcon(css.menu_about_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.addParameterGroupBox())
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def addParameterGroupBox(self):
        groupBox = QGroupBox(self.language['add_parameter_window_caption'])
        self.text_parameter_filename = QLabel(self.language['add_parameter_window_filename'])
        self.text_parameter_filename1 = QLabel(self.language['add_parameter_window_filename_exp'])
        self.parameter_filename = QLineEdit()
        self.text_parameter_name = QLabel(self.language['add_parameter_window_name'])
        self.text_parameter_name1 = QLabel(self.language['add_parameter_window_name_exp'])
        self.parameter_name = QLineEdit()
        self.text_parameter_symbol = QLabel(self.language['add_parameter_window_symbol'])
        self.text_parameter_symbol1 = QLabel(self.language['add_parameter_window_symbol_exp'])
        self.parameter_symbol = QLineEdit()
        self.text_parameter_unit = QLabel(self.language['add_parameter_window_unit'])
        self.text_parameter_unit1 = QLabel(self.language['add_parameter_window_unit_exp'])
        self.parameter_unit = QLineEdit()
        self.text_parameter_descriprion = QLabel(self.language['add_parameter_window_desc'])
        self.text_parameter_descriprion1 = QLabel(self.language['add_parameter_window_desc_exp'])
        self.parameter_descriprion = QTextEdit()
        
        buttonSaveProject = QPushButton(self.language['add_parameter_window_btn_add'])
        buttonSaveProject.clicked.connect(self.add_parameter)
        buttonCancel = QPushButton(self.language['add_parameter_window_btn_cancel'])
        buttonCancel.clicked.connect(self.close)
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_parameter_filename)
        layout.addWidget(self.text_parameter_filename1)
        layout.addWidget(self.parameter_filename)
        layout.addWidget(self.text_parameter_name)
        layout.addWidget(self.text_parameter_name1)
        layout.addWidget(self.parameter_name)
        layout.addWidget(self.text_parameter_symbol)
        layout.addWidget(self.text_parameter_symbol1)
        layout.addWidget(self.parameter_symbol)
        layout.addWidget(self.text_parameter_unit)
        layout.addWidget(self.text_parameter_unit1)
        layout.addWidget(self.parameter_unit)
        layout.addWidget(self.text_parameter_descriprion)
        layout.addWidget(self.text_parameter_descriprion1)
        layout.addWidget(self.parameter_descriprion)
        layout.addWidget(buttonSaveProject)
        layout.addWidget(buttonCancel)
        layout.addStretch(1)
        
        groupBox.setLayout(layout)
        
        return groupBox
    
    def add_parameter(self):
        get_files = next(os.walk(os.path.curdir + "/parameters/basic/"), (None, None, []))[2]
        self.file_list = []
        for file in get_files:
            self.file_list.append(Path(file).stem)
        
        if self.parameter_filename.text() in self.file_list:
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['add_parameter_window_filename_message'])
            self.msg.setWindowTitle(self.language['add_parameter_window_filename_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            if not self.parameter_filename.text() or not self.parameter_unit.text() or not self.parameter_name.text():
                self.msg = QMessageBox()
                self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText(self.language['add_parameter_window_save_message'])
                self.msg.setWindowTitle(self.language['add_parameter_window_save_message_caption'])
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.buttonClicked.connect(self.msg.close)
                self.msg.show()
            else:
                parameter_dict = {
                    "name": self.parameter_name.text(),
                    "unit": self.parameter_unit.text(),
                    "symbol": self.parameter_symbol.text(),
                    "description": self.parameter_descriprion.toPlainText(),
                    "type": "a"
                    }
                json_object = json.dumps(parameter_dict, indent = 4)
                with open(os.path.curdir + "/parameters/basic/" + self.parameter_filename.text() + ".json", "w") as outfile:
                    outfile.write(json_object)
                self.msg = QMessageBox()
                self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText(self.language['add_parameter_window_saved_message'])
                self.msg.setWindowTitle(self.language['add_parameter_window_saved_message_caption'])
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.buttonClicked.connect(self.message_box_success)
                self.msg.show()
            
    def message_box_success(self):
       self.clicked
       self.close()
        
        
        
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = AddParameter()
    sys.exit(mainApplication.exec_())