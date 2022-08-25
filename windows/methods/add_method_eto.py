# python standard modules
import sys, json, os
from pathlib import Path
cwd = os.path.curdir

# app modules and windows
#from css import css, var
eto_methods_folder = '/methods/eto/'
parameters_folder = '/parameters/basic/'
complex_parameters_folder = '/parameters/complex/'


# pyqt5 modules
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QPushButton, QLineEdit
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QTextEdit, QCheckBox
from PyQt5.QtWidgets import QScrollArea, QFormLayout, QBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

class AddETOMethod(QWidget):
    clicked = pyqtSignal()
    def __init__(self, language):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = language
        self.WindowGUI()

    def WindowGUI(self):
        #self.setFixedSize(800, 600)
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle(self.language['add_eto_methods_window_title'])
        #self.setWindowIcon(QIcon(css.menu_about_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.addMethodGroupBoxLeft(), 0, 0)
        self.grid.addWidget(self.addMethodGroupBoxRight(), 0, 1)
        self.grid.addWidget(self.addMethodGroupBoxDown(), 1, 0, 1, 2)
        #self.grid.addWidget(a0, row, column, rowSpan, columnSpan)
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def addMethodGroupBoxLeft(self):
        groupBox = QGroupBox(self.language['add_eto_methods_window_caption'])
        self.text_method_filename = QLabel(self.language['add_eto_methods_window_filename'])
        self.text_method_filename1 = QLabel(self.language['add_eto_methods_window_filename_exp'])
        self.method_filename = QLineEdit()
        
        self.text_method_name = QLabel(self.language['add_eto_methods_window_name'])
        self.text_method_name1 = QLabel(self.language['add_eto_methods_window_name_exp'])
        self.method_name = QLineEdit()
        
        #####
        self.formLayout = QVBoxLayout()
        self.parameters_GroupBox = QGroupBox('GroupBox')
        #self.parameters_GroupBox.setFixedHeight(200)
        
        parameters = ['Temp', 'Hum', 'Tmin', 'Tmax', 'n', 'Ta', 'kg', 'cm', 'ta', 'Don\'t use', 'Temp', 'Hum', 'Tmin', 'Tmax', 'n', 'Ta', 'kg', 'cm', 'ta', 'Don\'t use', 'Temp', 'Hum', 'Tmin', 'Tmax', 'n', 'Ta', 'kg', 'cm', 'ta', 'Don\'t use', 'Temp', 'Hum', 'Tmin', 'Tmax', 'n', 'Ta', 'kg', 'cm', 'ta', 'Don\'t use']
        i = 0
        for item in range(0, len(parameters)):
            #print(item)
            #print(f'{parameters[item]}')
            button = QCheckBox(f'{parameters[item]}', self)
            self.formLayout.addWidget(button)
        
        self.parameters_GroupBox.setLayout(self.formLayout)
        
        scroll = QScrollArea()
        scroll.setWidget(self.parameters_GroupBox)
        scroll.setWidgetResizable(1)
                
        layout = QVBoxLayout()
        #layout.addWidget(self.text_method_filename)
        #layout.addWidget(self.text_method_filename1)
        #layout.addWidget(self.method_filename)
        #layout.addWidget(self.text_method_name)
        #layout.addWidget(self.text_method_name1)
        #layout.addWidget(self.method_name)
        #layout.addWidget(self.parameters_GroupBox)
        layout.addWidget(scroll)
        #layout.addWidget(self.complex_parameters_GroupBox)
        layout.addStretch(1)
        
        groupBox.setLayout(layout)
        
        return groupBox
    
    def addMethodGroupBoxRight(self):
        groupBox = QGroupBox(self.language['add_eto_methods_window_caption'])
        
        self.text_method_formula = QLabel(self.language['add_eto_methods_window_formula'])
        self.text_method_formula1 = QLabel(self.language['add_eto_methods_window_formula_exp'])
        self.method_formula = QTextEdit()
        
        self.text_method_conditions = QLabel(self.language['add_eto_methods_window_conditions'])
        self.text_method_conditions1 = QLabel(self.language['add_eto_methods_window_conditions_exp'])
        self.method_conditions = QTextEdit()
        
        self.text_method_descriprion = QLabel(self.language['add_eto_methods_window_desc'])
        self.text_method_descriprion1 = QLabel(self.language['add_eto_methods_window_desc_exp'])
        self.method_descriprion = QTextEdit()
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_method_formula)
        layout.addWidget(self.text_method_formula1)
        layout.addWidget(self.method_formula)
        layout.addWidget(self.text_method_conditions)
        layout.addWidget(self.text_method_conditions1)
        layout.addWidget(self.method_conditions)
        layout.addWidget(self.text_method_descriprion)
        layout.addWidget(self.text_method_descriprion1)
        layout.addWidget(self.method_descriprion)
        #layout.addWidget(buttonSaveProject)
        #layout.addWidget(buttonCancel)
        layout.addStretch(1)
        
        groupBox.setLayout(layout)
        
        return groupBox
    
    def addMethodGroupBoxDown(self):
        groupBox = QGroupBox(self.language['add_eto_methods_window_caption'])
              
        buttonSaveProject = QPushButton(self.language['add_eto_methods_window_btn_add'])
        buttonSaveProject.clicked.connect(self.add_method)
        buttonCancel = QPushButton(self.language['add_eto_methods_window_btn_cancel'])
        buttonCancel.clicked.connect(self.close)
        
        layout = QVBoxLayout()
        
        layout.addWidget(buttonSaveProject)
        layout.addWidget(buttonCancel)
        layout.addStretch(1)
        
        groupBox.setLayout(layout)
        
        return groupBox
    
    
    def add_method(self):
        get_files = next(os.walk(cwd + eto_methods_folder), (None, None, []))[2]
        self.file_list = []
        for file in get_files:
            self.file_list.append(Path(file).stem)
        
        if self.method_filename.text() in self.file_list:
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['add_eto_methods_window_filename_message'])
            self.msg.setWindowTitle(self.language['add_eto_methods_window_filename_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            if not self.method_symbol.text() or not self.method_filename.text() or not self.method_unit.text() or not self.method_name.text():
                self.msg = QMessageBox()
                self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText(self.language['add_eto_methods_window_save_message'])
                self.msg.setWindowTitle(self.language['add_eto_methods_window_save_message_caption'])
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.buttonClicked.connect(self.msg.close)
                self.msg.show()
            else:
                method_dict = {
                    "name": self.method_name.text(),
                    "unit": self.method_unit.text(),
                    "symbol": self.method_symbol.text(),
                    "description": self.method_descriprion.toPlainText(),
                    "type": "a"
                    }
                json_object = json.dumps(method_dict, indent = 4)
                with open(cwd + eto_methods_folder + self.method_filename.text() + ".json", "w") as outfile:
                    outfile.write(json_object)
                self.msg = QMessageBox()
                self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText(self.language['add_eto_methods_window_saved_message'])
                self.msg.setWindowTitle(self.language['add_eto_methods_window_saved_message_caption'])
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.buttonClicked.connect(self.clicked)
                self.msg.buttonClicked.connect(self.message_box_success)

                self.msg.show()
            
    def message_box_success(self):
        self.method_filename.clear()
        self.method_name.clear()
        self.method_symbol.clear()
        self.method_unit.clear()
        self.method_descriprion.clear()
        self.close()