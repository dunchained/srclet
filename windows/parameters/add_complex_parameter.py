# python standard modules
import sys, json, os
from pathlib import Path

# app modules and windows
from css import css

# pyqt5 modules
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QPushButton, QLineEdit
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

class AddComplexParameter(QWidget):
    clicked = pyqtSignal()
    def __init__(self, language):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = language
        self.WindowGUI()

    def WindowGUI(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle(self.language['add_complex_parameter_window_title'])
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
        groupBox = QGroupBox(self.language['add_complex_parameter_window_caption'])
        self.text_parameter_filename = QLabel(self.language['add_complex_parameter_window_filename'])
        self.text_parameter_filename1 = QLabel(self.language['add_complex_parameter_window_filename_exp'])
        self.parameter_filename = QLineEdit()
        self.text_parameter_name = QLabel(self.language['add_complex_parameter_window_name'])
        self.text_parameter_name1 = QLabel(self.language['add_complex_parameter_window_name_exp'])
        self.parameter_name = QLineEdit()
        self.text_parameter_symbol = QLabel(self.language['add_complex_parameter_window_symbol'])
        self.text_parameter_symbol1 = QLabel(self.language['add_complex_parameter_window_symbol_exp'])
        self.parameter_symbol = QLineEdit()
        self.text_parameter_unit = QLabel(self.language['add_complex_parameter_window_unit'])
        self.text_parameter_unit1 = QLabel(self.language['add_complex_parameter_window_unit_exp'])
        self.parameter_unit = QLineEdit()
        self.text_parameter_formula = QLabel(self.language['add_complex_parameter_window_formula'])
        self.text_parameter_formula1 = QLabel(self.language['add_complex_parameter_window_formula_exp'])
        self.parameter_formula = QTextEdit()
        self.text_parameter_descriprion = QLabel(self.language['add_complex_parameter_window_desc'])
        self.text_parameter_descriprion1 = QLabel(self.language['add_complex_parameter_window_desc_exp'])
        self.parameter_descriprion = QTextEdit()
        
        buttonSaveProject = QPushButton(self.language['add_complex_parameter_window_btn_add'])
        buttonSaveProject.clicked.connect(self.add_parameter)
        buttonCancel = QPushButton(self.language['add_complex_parameter_window_btn_cancel'])
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
        layout.addWidget(self.text_parameter_formula)
        layout.addWidget(self.text_parameter_formula1)
        layout.addWidget(self.parameter_formula)
        layout.addWidget(self.text_parameter_descriprion)
        layout.addWidget(self.text_parameter_descriprion1)
        layout.addWidget(self.parameter_descriprion)
        layout.addWidget(buttonSaveProject)
        layout.addWidget(buttonCancel)
        layout.addStretch(1)
        
        groupBox.setLayout(layout)
        
        return groupBox
    
    def add_parameter(self):
        get_files = next(os.walk(os.path.curdir + "/parameters/complex/"), (None, None, []))[2]
        self.file_list = []
        for file in get_files:
            self.file_list.append(Path(file).stem)
        
        if self.parameter_filename.text() in self.file_list:
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['add_complex_parameter_window_filename_message'])
            self.msg.setWindowTitle(self.language['add_complex_parameter_window_filename_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            if not self.parameter_formula.toPlainText() or not self.parameter_filename.text() or not self.parameter_unit.text() or not self.parameter_name.text() or not self.parameter_symbol:
                self.msg = QMessageBox()
                self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText(self.language['add_complex_parameter_window_save_message'])
                self.msg.setWindowTitle(self.language['add_complex_parameter_window_save_message_caption'])
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.buttonClicked.connect(self.msg.close)
                self.msg.show()
            else:
                parameter_dict = {
                    "name": self.parameter_name.text(),
                    "unit": self.parameter_unit.text(),
                    "symbol": self.parameter_symbol.text(),
                    "formula": self.parameter_formula.toPlainText(),
                    "description": self.parameter_descriprion.toPlainText(),
                    "type": "a"
                    }
                json_object = json.dumps(parameter_dict, indent = 4)
                with open(os.path.curdir + "/parameters/complex/" + self.parameter_filename.text() + ".json", "w") as outfile:
                    outfile.write(json_object)
                self.msg = QMessageBox()
                self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText(self.language['add_complex_parameter_window_saved_message'])
                self.msg.setWindowTitle(self.language['add_complex_parameter_window_saved_message_caption'])
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.buttonClicked.connect(self.clicked)
                self.msg.buttonClicked.connect(self.message_box_success)

                self.msg.show()
            
    def message_box_success(self):
        self.parameter_filename.clear()
        self.parameter_name.clear()
        self.parameter_symbol.clear()
        self.parameter_unit.clear()
        self.parameter_formula.clear()
        self.parameter_descriprion.clear()
        self.close()