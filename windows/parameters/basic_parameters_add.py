import sys, json, os, random
from pathlib import Path
cwd = os.path.curdir
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

from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QPushButton, QLineEdit
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QTextEdit, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class AddBasicParameter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = {

            "language_description": "en",


            "//": "Add Parameter Window",
            "add_basic_parameter_window_title": "Add new basic parameter",
            "add_basic_parameter_window_caption": "Parameter information:",
            "add_basic_parameter_window_filename": "Filename:",
            "add_basic_parameter_window_filename_exp": "Text to be used as parameter filename.",
            "add_basic_parameter_window_category": "Parameter category:",
            "add_basic_parameter_window_category_exp": "Paremeter category...",
            "add_basic_parameter_window_name": "Parameter name:",
            "add_basic_parameter_window_name_exp": "Text to be used as parameter short description.",
            "add_basic_parameter_window_unit": "Parameter unit:",
            "add_basic_parameter_window_unit_exp": "Unit to be used...",
            "add_basic_parameter_window_symbol": "Parameter symbol:",
            "add_basic_parameter_window_symbol_exp": "Text to be used as parameter symbol in forulas.",
            "add_basic_parameter_window_desc": "Parameter description:",
            "add_basic_parameter_window_desc_exp": "Text to be used for short explinations.",
            "add_basic_parameter_window_btn_add": "Save",
            "add_basic_parameter_window_btn_cancel": "Cancel",
            "add_basic_parameter_window_save_message": "Parameter name or unit empty...",
            "add_basic_parameter_window_save_message_caption": "Missing data...",
            "add_basic_parameter_window_saved_message": "Parameter saved...",
            "add_basic_parameter_window_saved_message_caption": "Successuful...",
            "add_basic_parameter_window_filename_message": "Parameter with this filename already exists.",
            "add_basic_parameter_window_filename_message_caption": "Filename...",
            "add_basic_parameter_window_insert_special": "Insert special character",
            "add_basic_parameter_window_sc": "Input special character:"
        }
        self.window_gui()

    def window_gui(self):
        self.setFixedSize(1200, 600)
        #self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle(self.language['add_basic_parameter_window_title'])
        #self.setWindowIcon(QIcon(css.menu_about_icon))
        self.grid = QGridLayout()
        #self.grid.addWidget(self.centralGroupBox())
        self.grid.addWidget(self.pb_name_groupbox(), 0, 0, 1, 1)
        self.grid.addWidget(self.pb_category_groupbox(), 0, 1, 1, 1)
        self.grid.addWidget(self.pb_symbol_groupbox(), 1, 0, 1, 1)
        self.grid.addWidget(self.pb_unit_groupbox(), 1, 1, 1, 1)
        self.grid.addWidget(self.pb_description_groupbox(), 2, 0, 1, 2)
        self.grid.addWidget(self.special_character_groupbox(), 0, 2, 3, 1)
        self.grid.addWidget(self.button_groupbox(), 3, 0, 1, 3)
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
        self.pbn_groupbox = QGroupBox(self.language['add_basic_parameter_window_name'])
        self.text_parameter_name = QLabel(self.language['add_basic_parameter_window_name_exp'])
        self.parameter_name = QLineEdit()
        self.pbn_groupbox.layout = QVBoxLayout()
        self.pbn_groupbox.layout.addWidget(self.text_parameter_name)
        self.pbn_groupbox.layout.addWidget(self.parameter_name)
        self.pbn_groupbox.layout.addStretch(1)
        self.pbn_groupbox.setLayout(self.pbn_groupbox.layout)
        return self.pbn_groupbox
    
    def pb_category_groupbox(self):
        categoriess_file = 'parameter_types.json'
        self.pbc_groupbox = QGroupBox(self.language['add_basic_parameter_window_category'])
        self.text_parameter_category = QLabel(self.language['add_basic_parameter_window_category_exp'])
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
        self.pbs_groupbox = QGroupBox(self.language['add_basic_parameter_window_symbol'])
        self.text_parameter_symbol = QLabel(self.language['add_basic_parameter_window_symbol_exp'])
        self.parameter_symbol = QLineEdit()
        self.pbs_groupbox.layout = QVBoxLayout()
        self.pbs_groupbox.layout.addWidget(self.text_parameter_symbol)
        self.pbs_groupbox.layout.addWidget(self.parameter_symbol)
        self.pbs_groupbox.layout.addStretch(1)
        self.pbs_groupbox.setLayout(self.pbs_groupbox.layout)
        return self.pbs_groupbox
    
    def pb_unit_groupbox(self):
        self.pbu_groupbox = QGroupBox(self.language['add_basic_parameter_window_unit'])
        self.text_parameter_unit = QLabel(self.language['add_basic_parameter_window_unit_exp'])
        self.parameter_unit = QLineEdit()
        self.pbu_groupbox.layout = QVBoxLayout()
        self.pbu_groupbox.layout.addWidget(self.text_parameter_unit)
        self.pbu_groupbox.layout.addWidget(self.parameter_unit)
        self.pbu_groupbox.layout.addStretch(1)
        self.pbu_groupbox.setLayout(self.pbu_groupbox.layout)
        return self.pbu_groupbox

    def pb_description_groupbox(self):
        self.pbd_groupbox = QGroupBox(self.language['add_basic_parameter_window_desc'])
        self.text_parameter_descriprion = QLabel(self.language['add_basic_parameter_window_desc_exp'])
        self.parameter_descriprion = QTextEdit()
        self.pbd_groupbox.layout = QVBoxLayout()
        self.pbd_groupbox.layout.addWidget(self.text_parameter_descriprion)
        self.pbd_groupbox.layout.addWidget(self.parameter_descriprion)
        self.pbd_groupbox.layout.addStretch(1)
        self.pbd_groupbox.setLayout(self.pbd_groupbox.layout)
        return self.pbd_groupbox
    
    def special_character_groupbox(self):
        self.sc_groupbox = QGroupBox(self.language['add_basic_parameter_window_sc'])
        self.sc_layout = QGridLayout()
        self.sc_scroll = QWidget()
        self.lista_fajlova = next(os.walk(cwd + '/srclet/characters/'), (None, None, []))[2]
        self.button_list = []
        for self.file_names in self.lista_fajlova:
            self.json_path = os.path.join(cwd + '/srclet/characters/' + self.file_names)
            with open(self.json_path) as json_file:
                characters = json.load(json_file)
            for key, value in characters.items():
                self.button_list.append(value)
        self.columns = 5
        if len(self.button_list) % 5 == 0:
            self.rows = len(self.button_list) // 5
        else:
            self.rows = len(self.button_list) // 5 + 1
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
        sc.setFixedWidth(500)
        sc.setWidget(self.sc_scroll)
        sc.setWidgetResizable(1)
        self.sc_groupbox.layout = QVBoxLayout()
        self.sc_groupbox.layout.addWidget(sc)
        self.sc_groupbox.setLayout(self.sc_groupbox.layout)
        return self.sc_groupbox
        
    def button_groupbox(self):
        self.btn_groupbox = QGroupBox()
        self.buttonSaveParameter = QPushButton(self.language['add_basic_parameter_window_btn_add'])
        self.buttonSaveParameter.clicked.connect(self.add_parameter)
        self.buttonCancel = QPushButton(self.language['add_basic_parameter_window_btn_cancel'])
        self.buttonCancel.clicked.connect(self.close)
        self.btn_groupbox.layout = QHBoxLayout()
        self.btn_groupbox.layout.addWidget(self.buttonSaveParameter)
        self.btn_groupbox.layout.addWidget(self.buttonCancel)
        self.btn_groupbox.setLayout(self.btn_groupbox.layout)
        return self.btn_groupbox
    
    ### Kod uvezivanja izvući u mortije
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


        filename = 'bp_' + p + d + t + c + p2 + s + p3 + d2
        
        return filename
      
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
            self.msg.setText(self.language['add_basic_parameter_window_filename_message'])
            self.msg.setWindowTitle(self.language['add_basic_parameter_window_filename_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            if not self.parameter_symbol.text() or not self.parameter_unit.text() or not self.parameter_name.text():
                self.msg = QMessageBox()
                self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText(self.language['add_basic_parameter_window_save_message'])
                self.msg.setWindowTitle(self.language['add_basic_parameter_window_save_message_caption'])
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
                self.msg.setText(self.language['add_basic_parameter_window_saved_message'])
                self.msg.setWindowTitle(self.language['add_basic_parameter_window_saved_message_caption'])
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.buttonClicked.connect(self.clicked)
                #self.clicked.emit(self.parameter_name.text(), self.comboBox.currentText())
                #self.msg.buttonClicked.connect(partial(self.clicked, parameter=self.parameter_name))
                self.msg.buttonClicked.connect(self.message_box_success)
                self.msg.show()
            
    def message_box_success(self):
        #self.clicked.emit(self.parameter_name.text(), self.comboBox.currentText())
        self.parameter_name.clear()
        self.parameter_symbol.clear()
        self.parameter_unit.clear()
        self.parameter_descriprion.clear()
        self.close()

if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = AddBasicParameter()
    sys.exit(mainApplication.exec_())