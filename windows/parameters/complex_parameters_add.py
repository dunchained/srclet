import sys, json, os, random
from pathlib import Path
cwd = os.path.curdir
#
language_folder = '/srclet/languages/'
language_file = 'language.json'
categories_file = 'parameter_types.json'
projects_folder = '/projects/'
basic_parameters_folder = '/parameters/basic/'
complex_parameters_folder = '/parameters/complex/'
random_images_folder = '/srclet/images/random_image/'
eto_methods_folder = '/methods/eto/'
wb_methods_folder = '/methods/wb/'
other_methods_folder = '/methods/others/'

from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QPushButton, QLineEdit
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QTextEdit, QComboBox, QHBoxLayout
from parameters_morty import read_characters, get_filename, read_basic_parameters
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class AddComplexParameter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = {

            "language_description": "en",


            "//": "Add Parameter Window",
            "add_complex_parameter_window_title": "Add complex parameter",
            "add_complex_parameter_window_caption": "Parameter information:",
            "add_complex_parameter_window_category": "Parameter category:",
            "add_complex_parameter_window_category_exp": "Paremeter category.",
            "add_complex_parameter_window_name": "Parameter name:",
            "add_complex_parameter_window_name_exp": "Text to be used as parameter short description.",
            "add_complex_parameter_window_unit": "Parameter unit:",
            "add_complex_parameter_window_unit_exp": "Unit to be used...",
            "add_complex_parameter_window_symbol": "Parameter symbol:",
            "add_complex_parameter_window_symbol_exp": "Text to be used as parameter symbol in formulas.",
            "add_complex_parameter_window_desc": "Parameter description:",
            "add_complex_parameter_window_desc_exp": "Text to be used for short explinations.",
            "add_complex_parameter_window_formula": "Complex parameter formula:",
            "add_complex_parameter_window_formula_exp": "Formula used to calculate parameter.",
            "add_complex_parameter_window_btn_add": "Save",
            "add_complex_parameter_window_btn_cancel": "Cancel",
            "add_complex_parameter_window_save_message": "Parameter name or unit empty...",
            "add_complex_parameter_window_save_message_caption": "Missing data...",
            "add_complex_parameter_window_saved_message": "Parameter saved...",
            "add_complex_parameter_window_saved_message_caption": "Successuful...",
            "add_complex_parameter_window_ename_message": "Parameter with this name already exists.",
            "add_complex_parameter_window_name_message_caption": "Filename...",
            "add_complex_parameter_window_sc": "Input special character:",
            "add_complex_parameter_window_bp": "Input basic parameter:"
        }
        self.window_gui()

    def window_gui(self):
        font = self.font()
        font.setPointSize(14) # učitati font iz mortija
        self.setFont(font)
        self.setWindowState(Qt.WindowMaximized)
        self.setMinimumSize(1200, 600)
        self.setWindowTitle(self.language['add_complex_parameter_window_title'])
        #self.setWindowIcon(QIcon(css.parameters_complex_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.pb_name_groupbox(), 0, 0, 1, 1)
        self.grid.addWidget(self.pb_category_groupbox(), 0, 1, 1, 1)
        self.grid.addWidget(self.pb_symbol_groupbox(), 1, 0, 1, 1)
        self.grid.addWidget(self.pb_unit_groupbox(), 1, 1, 1, 1)
        self.grid.addWidget(self.pb_formula_groupbox(), 2, 0, 1, 2)
        self.grid.addWidget(self.pb_description_groupbox(), 3, 0, 1, 2)
        self.grid.addWidget(self.basic_parameters_groupbox(), 0, 2, 4, 1)
        self.grid.addWidget(self.special_character_groupbox(), 0, 3, 4, 1)
        self.grid.addWidget(self.button_groupbox(), 4, 0, 1, 4)
        self.setLayout(self.grid)
        QApplication.instance().focusChanged.connect(self.on_focus_changed)
        self.center_gui()
        self.show()
        
    def center_gui(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def on_focus_changed(self, widget):
        self.on_focused_change = widget
        
    def special_character_clicked(self, i):
        sender = self.sender()
        sender_text = sender.text()
        if self.on_focused_change.__class__.__name__ == 'QTextEdit':
            self.on_focused_change.setPlainText(self.on_focused_change.toPlainText() + sender_text)
        elif self.on_focused_change.__class__.__name__ == 'QLineEdit':
            self.on_focused_change.setText(self.on_focused_change.text() + sender_text)
        else:
            pass
        
    def pb_name_groupbox(self):
        self.pbn_groupbox = QGroupBox(self.language['add_complex_parameter_window_name'])
        self.text_parameter_name = QLabel(self.language['add_complex_parameter_window_name_exp'])
        self.parameter_name = QLineEdit()
        self.pbn_groupbox.layout = QVBoxLayout()
        self.pbn_groupbox.layout.addWidget(self.text_parameter_name)
        self.pbn_groupbox.layout.addWidget(self.parameter_name)
        self.pbn_groupbox.layout.addStretch(1)
        self.pbn_groupbox.setLayout(self.pbn_groupbox.layout)
        return self.pbn_groupbox
    
    def pb_category_groupbox(self):
        categoriess_file = 'parameter_types.json' # uvezati iz var
        self.pbc_groupbox = QGroupBox(self.language['add_complex_parameter_window_category'])
        self.text_parameter_category = QLabel(self.language['add_complex_parameter_window_category_exp'])
        categories_file = open(os.path.join(cwd + language_folder + self.language['language_description'] + '/' + categoriess_file))
        self.categories_file_data = json.load(categories_file)
        self.categories_list = []
        for category in self.categories_file_data:
            self.categories_list.append(self.categories_file_data[category])
        self.comboBox = QComboBox()
        self.comboBox.addItems(self.categories_list)
        self.pbc_groupbox.layout = QVBoxLayout()
        self.pbc_groupbox.layout.addWidget(self.text_parameter_category)
        self.pbc_groupbox.layout.addWidget(self.comboBox)
        self.pbc_groupbox.layout.addStretch(1)
        self.pbc_groupbox.setLayout(self.pbc_groupbox.layout)
        return self.pbc_groupbox
    
    def pb_symbol_groupbox(self):
        self.pbs_groupbox = QGroupBox(self.language['add_complex_parameter_window_symbol'])
        self.text_parameter_symbol = QLabel(self.language['add_complex_parameter_window_symbol_exp'])
        self.parameter_symbol = QLineEdit()
        self.pbs_groupbox.layout = QVBoxLayout()
        self.pbs_groupbox.layout.addWidget(self.text_parameter_symbol)
        self.pbs_groupbox.layout.addWidget(self.parameter_symbol)
        self.pbs_groupbox.layout.addStretch(1)
        self.pbs_groupbox.setLayout(self.pbs_groupbox.layout)
        return self.pbs_groupbox
    
    def pb_unit_groupbox(self):
        self.pbu_groupbox = QGroupBox(self.language['add_complex_parameter_window_unit'])
        self.text_parameter_unit = QLabel(self.language['add_complex_parameter_window_unit_exp'])
        self.parameter_unit = QLineEdit()
        self.pbu_groupbox.layout = QVBoxLayout()
        self.pbu_groupbox.layout.addWidget(self.text_parameter_unit)
        self.pbu_groupbox.layout.addWidget(self.parameter_unit)
        self.pbu_groupbox.layout.addStretch(1)
        self.pbu_groupbox.setLayout(self.pbu_groupbox.layout)
        return self.pbu_groupbox

    def pb_description_groupbox(self):
        self.pbd_groupbox = QGroupBox(self.language['add_complex_parameter_window_desc'])
        self.text_parameter_descriprion = QLabel(self.language['add_complex_parameter_window_desc_exp'])
        self.parameter_descriprion = QTextEdit()
        self.pbd_groupbox.layout = QVBoxLayout()
        self.pbd_groupbox.layout.addWidget(self.text_parameter_descriprion)
        self.pbd_groupbox.layout.addWidget(self.parameter_descriprion)
        self.pbd_groupbox.layout.addStretch(1)
        self.pbd_groupbox.setLayout(self.pbd_groupbox.layout)
        return self.pbd_groupbox
    
    def pb_formula_groupbox(self):
        self.pbf_groupbox = QGroupBox(self.language['add_complex_parameter_window_formula'])
        self.text_parameter_formula = QLabel(self.language['add_complex_parameter_window_formula_exp'])
        self.parameter_formula = QTextEdit()
        self.pbf_groupbox.layout = QVBoxLayout()
        self.pbf_groupbox.layout.addWidget(self.text_parameter_formula)
        self.pbf_groupbox.layout.addWidget(self.parameter_formula)
        self.pbf_groupbox.layout.addStretch(1)
        self.pbf_groupbox.setLayout(self.pbf_groupbox.layout)
        return self.pbf_groupbox
    
    def special_character_groupbox(self):
        self.sc_groupbox = QGroupBox(self.language['add_complex_parameter_window_sc'])
        self.sc_layout = QGridLayout()
        self.sc_scroll = QWidget()
        self.button_list, self.rows, self.columns = read_characters('/srclet/characters/') # uvezati iz var
        i = 0
        for row in range(self.rows):
            for column in range(self.columns):
                button = QPushButton(f'{self.button_list[i]}', self)
                button.clicked.connect(self.special_character_clicked)
                self.sc_layout.addWidget(button, row+1, column)
                i += 1
                if i == len(self.button_list): break
        self.sc_scroll.setLayout(self.sc_layout)
        sc = QScrollArea()
        sc.setWidget(self.sc_scroll)
        sc.setWidgetResizable(1)
        self.sc_groupbox.layout = QVBoxLayout()
        self.sc_groupbox.layout.addWidget(sc)
        self.sc_groupbox.setLayout(self.sc_groupbox.layout)
        return self.sc_groupbox
    
    def basic_parameters_groupbox(self):
        self.bp_groupbox = QGroupBox(self.language['add_complex_parameter_window_bp'])
        self.bp_layout = QGridLayout()
        self.bp_scroll = QWidget()
        self.button_list, self.rows, self.columns = read_basic_parameters() # uvezati iz var
        i = 0
        for row in range(self.rows):
            for column in range(self.columns):
                button = QPushButton(f'{self.button_list[i]}', self)
                button.clicked.connect(self.special_character_clicked)
                self.bp_layout.addWidget(button, row+1, column)
                i += 1
                if i == len(self.button_list): break
        self.bp_scroll.setLayout(self.bp_layout)
        bp = QScrollArea()
        bp.setWidget(self.bp_scroll)
        bp.setWidgetResizable(1)
        self.bp_groupbox.layout = QVBoxLayout()
        self.bp_groupbox.layout.addWidget(bp)
        self.bp_groupbox.setLayout(self.bp_groupbox.layout)
        return self.bp_groupbox
            
    def button_groupbox(self):
        self.btn_groupbox = QGroupBox()
        self.buttonSaveParameter = QPushButton(self.language['add_complex_parameter_window_btn_add'])
        self.buttonSaveParameter.clicked.connect(self.add_parameter)
        self.buttonCancel = QPushButton(self.language['add_complex_parameter_window_btn_cancel'])
        self.buttonCancel.clicked.connect(self.close)
        self.btn_groupbox.layout = QHBoxLayout()
        self.btn_groupbox.layout.addWidget(self.buttonSaveParameter)
        self.btn_groupbox.layout.addWidget(self.buttonCancel)
        self.btn_groupbox.setLayout(self.btn_groupbox.layout)
        return self.btn_groupbox
    
    def add_parameter(self):
        self.file_name_to_save = get_filename('cp')
        get_files = next(os.walk(cwd + complex_parameters_folder), (None, None, []))[2]
        self.file_list = []
        for file in get_files:
            self.file_to_read = open(os.path.join(cwd + complex_parameters_folder + file))
            self.file_data = json.load(self.file_to_read)
            if self.parameter_name.text() == self.file_data['name']:
                self.file_list.append(file)
                        
        if self.file_list:
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['add_complex_parameter_window_name_message'])
            self.msg.setWindowTitle(self.language['add_complex_parameter_window_name_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            if not self.parameter_symbol.text() or not self.parameter_unit.text() or not self.parameter_name.text():
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
                    "category": list(self.categories_file_data.keys())[list(self.categories_file_data.values()).index(self.comboBox.currentText())],
                    "unit": self.parameter_unit.text(),
                    "symbol": self.parameter_symbol.text(),
                    "formula": self.parameter_formula.toPlainText(),
                    "description": self.parameter_descriprion.toPlainText(),
                    "type": "a"
                    }
                json_object = json.dumps(parameter_dict, indent = 4)
                with open(cwd + complex_parameters_folder + self.file_name_to_save + ".json", "w") as outfile:
                    outfile.write(json_object)
                self.msg = QMessageBox()
                self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText(self.language['add_complex_parameter_window_saved_message'])
                self.msg.setWindowTitle(self.language['add_complex_parameter_window_saved_message_caption'])
                self.msg.setStandardButtons(QMessageBox.Ok)
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
    mainWindow = AddComplexParameter()
    sys.exit(mainApplication.exec_())