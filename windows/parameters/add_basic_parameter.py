# python standard modules
import sys, json, os, random
from pathlib import Path
cwd = os.path.curdir

# app modules and windows
#from css import css, var
#
language_folder = '/srclet/languages/'
language_file = 'language.json'
categories_file = 'parameter_types.json'
projects_folder = '/projects/'
parameters_folder = '/parameters/basic/'
complex_parameters_folder = '/parameters/complex/'
random_images_folder = '/srclet/images/random_image/'
eto_methods_folder = '/methods/eto/'
wb_methods_folder = '/methods/wb/'
other_methods_folder = '/methods/others/'

# pyqt5 modules
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QPushButton, QLineEdit
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QTextEdit, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

class AddParameter(QWidget):
    clicked = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = {

            "language_description": "en",


            "//": "Add Parameter Window",
            "add_parameter_window_title": "Add new parameter",
            "add_parameter_window_caption": "Parameter information:",
            "add_parameter_window_filename": "Filename:",
            "add_parameter_window_filename_exp": "Text to be used as parameter filename.",
            "add_parameter_window_category": "Parameter category:",
            "add_parameter_window_category_exp": "Paremeter category...",
            "add_parameter_window_name": "Parameter name:",
            "add_parameter_window_name_exp": "Text to be used as parameter short description.",
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
            "add_parameter_window_filename_message_caption": "Filename...",
        }
        self.WindowGUI()

    def WindowGUI(self):
        self.setFixedSize(800, 800)
        #self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle(self.language['add_parameter_window_title'])
        #self.setWindowIcon(QIcon(css.menu_about_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.centralGroupBox())
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def centralGroupBox(self):
        groupBox = QGroupBox()
        grid = QGridLayout()
        grid.addWidget(self.parameterNameGroupBox(), 0, 0, 1, 1)
        grid.addWidget(self.parameterCategoryGroupBox(), 0, 1, 1, 1)
        grid.addWidget(self.parameterSymbolGroupBox(), 1, 0, 1, 1)
        grid.addWidget(self.parameterUnitGroupBox(), 1, 1, 1, 1)
        grid.addWidget(self.parameterDescriptionGroupBox(), 2, 0, 2, 2)
        grid.addWidget(self.buttonGroupBox(), 4, 0, 1, 2)
        groupBox.setLayout(grid)
        return groupBox
        

    def file_name(self):
        lista = ['q','w','e','r','t','z','u','i','o','p',
                'a','s','d','d','f','g','h','j','k','l',
                'y','x','c','v','b','n','m']

        p = random.choice(lista)
        d = str(random.choice(range(0,9)))
        t = random.choice(lista)
        c = str(random.choice(range(0,9)))
        p2 = random.choice(lista)
        s = str(random.choice(range(0,9)))
        p3 = random.choice(lista)
        d2 = str(random.choice(range(0,9)))


        filename = p + d + t + c + p2 + s + p3 + d2
        
        return filename
        
    
    def parameterCategoryGroupBox(self):
        categoriess_file = 'parameter_types.json'
        groupBox = QGroupBox(self.language['add_parameter_window_category'])
        self.text_parameter_category = QLabel(self.language['add_parameter_window_category_exp'])
        categories_file = open(os.path.join(cwd + language_folder + self.language['language_description'] + '/' + categoriess_file))
        self.categories_file_data = json.load(categories_file)
        self.categories_list = []
        for category in self.categories_file_data:
            self.categories_list.append(self.categories_file_data[category])
        self.comboBox = QComboBox()
        self.comboBox.addItems(self.categories_list)

        layout = QVBoxLayout()
        layout.addWidget(self.text_parameter_category)
        layout.addWidget(self.comboBox)
        layout.addStretch(1)

        groupBox.setLayout(layout)

        return groupBox

    def parameterNameGroupBox(self):
        groupBox = QGroupBox(self.language['add_parameter_window_name'])
        self.text_parameter_name = QLabel(self.language['add_parameter_window_name_exp'])
        self.parameter_name = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.text_parameter_name)
        layout.addWidget(self.parameter_name)
        layout.addStretch(1)
        
        groupBox.setLayout(layout)

        return groupBox

    def parameterSymbolGroupBox(self):
        groupBox = QGroupBox(self.language['add_parameter_window_symbol'])
        self.text_parameter_symbol = QLabel(self.language['add_parameter_window_symbol_exp'])
        self.parameter_symbol = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.text_parameter_symbol)
        layout.addWidget(self.parameter_symbol)
        layout.addStretch(1)
        
        groupBox.setLayout(layout)

        return groupBox

    def parameterUnitGroupBox(self):
        groupBox = QGroupBox(self.language['add_parameter_window_unit'])
        self.text_parameter_unit = QLabel(self.language['add_parameter_window_unit_exp'])
        self.parameter_unit = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.text_parameter_unit)
        layout.addWidget(self.parameter_unit)
        layout.addStretch(1)
        
        groupBox.setLayout(layout)

        return groupBox

    def parameterDescriptionGroupBox(self):
        groupBox = QGroupBox(self.language['add_parameter_window_desc'])
        self.text_parameter_descriprion = QLabel(self.language['add_parameter_window_desc_exp'])
        self.parameter_descriprion = QTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.text_parameter_descriprion)
        layout.addWidget(self.parameter_descriprion)
        layout.addStretch(1)
        
        groupBox.setLayout(layout)

        return groupBox
        
    def buttonGroupBox(self):
        groupBox = QGroupBox()
        
        buttonSaveParameter = QPushButton(self.language['add_parameter_window_btn_add'])
        buttonSaveParameter.clicked.connect(self.add_parameter)
        buttonCancel = QPushButton(self.language['add_parameter_window_btn_cancel'])
        buttonCancel.clicked.connect(self.close)
        
        layout = QHBoxLayout()

        layout.addWidget(buttonSaveParameter)
        layout.addWidget(buttonCancel)
        
        groupBox.setLayout(layout)
        
        return groupBox
    
    def add_parameter(self):
        self.file_name_to_save = self.file_name()
        get_files = next(os.walk(cwd + parameters_folder), (None, None, []))[2]
        self.file_list = []
        for file in get_files:
            self.file_list.append(Path(file).stem)
        
        if self.file_name_to_save in self.file_list:
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['add_parameter_window_filename_message'])
            self.msg.setWindowTitle(self.language['add_parameter_window_filename_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            if not self.parameter_symbol.text() or not self.parameter_unit.text() or not self.parameter_name.text():
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
                    "category": list(self.categories_file_data.keys())[list(self.categories_file_data.values()).index(self.comboBox.currentText())],
                    "unit": self.parameter_unit.text(),
                    "symbol": self.parameter_symbol.text(),
                    "description": self.parameter_descriprion.toPlainText(),
                    "type": "a"
                    }
                json_object = json.dumps(parameter_dict, indent = 4)
                with open(cwd + parameters_folder + self.file_name_to_save + ".json", "w") as outfile:
                    outfile.write(json_object)
                self.msg = QMessageBox()
                self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText(self.language['add_parameter_window_saved_message'])
                self.msg.setWindowTitle(self.language['add_parameter_window_saved_message_caption'])
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.buttonClicked.connect(self.clicked)
                self.msg.buttonClicked.connect(self.message_box_success)

                self.msg.show()
            
    def message_box_success(self):
        self.parameter_name.clear()
        self.parameter_symbol.clear()
        self.parameter_unit.clear()
        self.parameter_descriprion.clear()
        self.close()

if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = AddParameter()
    sys.exit(mainApplication.exec_())