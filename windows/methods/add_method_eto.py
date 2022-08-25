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
from PyQt5.QtWidgets import QScrollArea, QFormLayout, QBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

class AddETOMethod(QWidget):
    clicked = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = {
            "//": "Add ETO methods Window",
            "add_eto_methods_window_title": "Add new ETO method",
            "add_eto_methods_window_caption": "Method information:",
            "add_eto_methods_window_filename": "Filename:",
            "add_eto_methods_window_filename_exp": "Text to be used as method filename.",
            "add_eto_methods_window_name": "Method name:",
            "add_eto_methods_window_name_exp": "Text to be used as method short description.",
            "add_eto_methods_window_conditions": "Method conditions:",
            "add_eto_methods_window_conditions_exp": "Conditions to be used...",
            "add_eto_methods_window_formula": "Method formula:",
            "add_eto_methods_window_formula_exp": "Formula used to calculate method...",
            "add_eto_methods_window_desc": "Method description:",
            "add_eto_methods_window_desc_exp": "Text to be used for short explinations.",
            "add_eto_methods_window_btn_add": "Save",
            "add_eto_methods_window_btn_cancel": "Cancel",
            "add_eto_methods_window_save_message": "Method name or unit empty...",
            "add_eto_methods_window_save_message_caption": "Missing data...",
            "add_eto_methods_window_saved_message": "Method saved...",
            "add_eto_methods_window_saved_message_caption": "Successuful...",
            "add_eto_methods_window_filename_message": "Method with this filename already exists.",
            "add_eto_methods_window_filename_message_caption": "Filename...",
            "":""
        }
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
        
        ###
        self.groupBox_name_and_filename = QGroupBox('Name and filename of the method:')
        
        self.text_method_filename = QLabel(self.language['add_eto_methods_window_filename'])
        self.text_method_filename1 = QLabel(self.language['add_eto_methods_window_filename_exp'])
        self.method_filename = QLineEdit()
        
        self.text_method_name = QLabel(self.language['add_eto_methods_window_name'])
        self.text_method_name1 = QLabel(self.language['add_eto_methods_window_name_exp'])
        self.method_name = QLineEdit()
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_method_filename)
        self.layout.addWidget(self.text_method_filename1)
        self.layout.addWidget(self.method_filename)
        self.layout.addWidget(self.text_method_name)
        self.layout.addWidget(self.text_method_name1)
        self.layout.addWidget(self.method_name)
        self.groupBox_name_and_filename.setLayout(self.layout)
        ###
        
        ###
        self.groupBox_basic_parameters = QGroupBox('Basic parameters to be used by method:')
        self.scrollLayout = QVBoxLayout()
        self.parameters_scroll = QWidget()
        self.basic_parameters_list = []
        get_parameters = next(os.walk(cwd + parameters_folder), (None, None, []))[2]
        self.parameters_list = []
        for file in get_parameters:
            self.parameters_list.append(Path(file).stem)
            #abecedno urediti listu
        i = 0
        for item in range(0, len(self.parameters_list)):
            #for parameter in self.parameters_list:
            #print(f'{self.parameters_list[item]}')
            self.json_path = cwd + parameters_folder + f'{self.parameters_list[item]}' + '.json'
            #print(self.json_path)
            with open(self.json_path) as json_file:
                parameter_data = json.load(json_file)
            
            card = QGroupBox(f'{self.parameters_list[item]}')
            card.setCheckable(True)
            card.setChecked(False)
            card.clicked.connect(self.onStateChangeBasicParameters)
            layout = QGridLayout()
            
            label_name_text = QLabel('Parameter name:')
            label_name = QLabel(parameter_data['name'])
           
            label_unit_text = QLabel('Parameter unit:')
            label_unit = QLabel(parameter_data['unit'])
            
            label_symbol_text = QLabel('Parameter symbol:')
            label_symbol = QLabel(parameter_data['name'])
            
            label_desc_text = QLabel('Parameter Description:')
            label_desc = QLabel(parameter_data['name'])
            
            #layout.addWidget(label_name_text, 0, 0)
            #layout.addWidget(label_unit_text, 0, 1)
            #layout.addWidget(label_symbol_text, 0, 2)
            layout.addWidget(label_name, 0, 1)
            #layout.addWidget(label_unit, 1, 1)
            #layout.addWidget(label_symbol, 1, 2)
            
            #layout.addWidget(label_desc_text, 0, 2)
            layout.addWidget(label_desc, 0, 2)
            
            card.setLayout(layout)
            
            #button = QCheckBox(f'{self.parameters_list[item]}', self)
            #self.scrollLayout.addWidget(button)
            self.scrollLayout.addWidget(card)
        self.parameters_scroll.setLayout(self.scrollLayout)
        
        scroll = QScrollArea()
        scroll.setWidget(self.parameters_scroll)
        scroll.setWidgetResizable(1)

        self.layout = QVBoxLayout()
        self.layout.addWidget(scroll)
        self.groupBox_basic_parameters.setLayout(self.layout)
        ###
        
        ###
        self.groupBox_complex_parameters = QGroupBox('Complex parameters to be used by method:')
        self.scrollLayout = QVBoxLayout()
        self.parameters_scroll = QWidget()
        
        get_parameters = next(os.walk(cwd + complex_parameters_folder), (None, None, []))[2]
        self.parameters_list = []
        for file in get_parameters:
            self.parameters_list.append(Path(file).stem)
        i = 0
        for item in range(0, len(self.parameters_list)):
            button = QCheckBox(f'{self.parameters_list[item]}', self)
            self.scrollLayout.addWidget(button)
        self.parameters_scroll.setLayout(self.scrollLayout)
        
        scroll = QScrollArea()
        scroll.setWidget(self.parameters_scroll)
        scroll.setWidgetResizable(1)

        self.layout = QVBoxLayout()
        self.layout.addWidget(scroll)
        self.groupBox_complex_parameters.setLayout(self.layout)
        ###
               
        layout = QVBoxLayout()
        layout.addWidget(self.groupBox_name_and_filename)
        layout.addWidget(self.groupBox_basic_parameters)
        layout.addWidget(self.groupBox_complex_parameters)
        layout.addStretch(1)
        groupBox.setLayout(layout)
        return groupBox
    
    def onStateChangeBasicParameters(self):
        change = self.sender().title()
        #change = change.title()
        if change not in self.basic_parameters_list:
            self.basic_parameters_list.append(change)
        else:
            if change in self.basic_parameters_list:
                self.basic_parameters_list.remove(change)
        
        print(self.basic_parameters_list)
    
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
        
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = AddETOMethod()
    sys.exit(mainApplication.exec_())