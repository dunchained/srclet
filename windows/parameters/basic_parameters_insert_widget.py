import sys, json, os
cwd = os.path.curdir

from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QPushButton, QFormLayout, QDateEdit
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QTextEdit, QComboBox, QHBoxLayout, QLineEdit, QTabWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
#rom mortys.parameters_morty import read_characters, get_filename
from parameters_morty import read_characters, get_filename
#from variables import var, css
import var, css
from language import language
#from windows.parameters.language import language

class InputBasicParameterNameWidget(QTabWidget):
    def __init__(self, columns):
        super().__init__()
        self.columns = columns
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = language
        self.window_gui()

    def window_gui(self):
        self.setWindowState(Qt.WindowMaximized)
        main_layout = QGridLayout()
        self.setLayout(main_layout)
        self.categories_list = self.read_parameter_categories()
        self.tabs = QTabWidget()
        for category in self.categories_list:
            self.tab = QWidget()
            self.tab.layout = QGridLayout()
            self.sc_groupbox = QGroupBox()
            self.sc_layout = QGridLayout()
            self.sc_scroll = QWidget()
            category_name_to_send = category['category']
            self.characters_list, self.rows, self.columns = self.read_categories_files(category=category_name_to_send, columns=self.columns)
            i = 0
            for row in range(self.rows):
                for column in range(self.columns):
                    self.button = QPushButton(self.characters_list[i])
                    self.setStyleSheet('''QToolTip {min-width: 300px;}''')
                    self.get_basic = self.get_files = next(os.walk(cwd + var.basic_parameters_folder), (None, None, []))[2]
                    self.get_complex = self.get_files = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
                    for file in self.get_basic:
                        self.file_to_read = open(os.path.join(cwd + var.basic_parameters_folder + file))
                        self.file_data = json.load(self.file_to_read)
                        if self.characters_list[i] == self.file_data['symbol']:
                            self.file_to_load = file
                            self.json_path = cwd + var.basic_parameters_folder + self.file_to_load
                            with open(self.json_path) as json_file:
                                tooltip_data = json.load(json_file)
                            self.text = '<b>' + 'Parameter name: ' + '</b>' + tooltip_data['name'] + '<br>' + \
                                        '<b>' + 'Parameter category: ' + '</b>' + tooltip_data['category'] + '<br>' + \
                                        '<b>' + 'Parameter unit: ' + '</b>' + tooltip_data['unit'] + '<br>' + \
                                        '<b>' + 'Parameter symbol: ' + '</b>' + tooltip_data['symbol'] + '<br>' + \
                                        '<b>' + 'Parameter description: ' + '</b>' + tooltip_data['description']
                            self.button.setToolTip(self.text)
                        else:
                            for file in self.get_complex:
                                self.file_to_read = open(os.path.join(cwd + var.complex_parameters_folder + file))
                                self.file_data = json.load(self.file_to_read)
                                if self.characters_list[i] == self.file_data['symbol']:
                                    self.file_to_load = file
                                    self.json_path = cwd + var.complex_parameters_folder + self.file_to_load
                                    with open(self.json_path) as json_file:
                                        tooltip_data = json.load(json_file)
                                    self.text = '<b>' + 'Parameter name: ' + '</b>' + tooltip_data['name'] + '<br>' + \
                                                '<b>' + 'Parameter category: ' + '</b>' + tooltip_data['category'] + '<br>' + \
                                                '<b>' + 'Parameter unit: ' + '</b>' + tooltip_data['unit'] + '<br>' + \
                                                '<b>' + 'Parameter symbol: ' + '</b>' + tooltip_data['symbol'] + '<br>' + \
                                                '<b>' + 'Parameter formula: ' + '</b>' + tooltip_data['formula'] + '<br>' + \
                                                '<b>' + 'Parameter basic parameters: ' + '</b>' + tooltip_data['basic_parameters'] + '<br>' + \
                                                '<b>' + 'Parameter complex parameters: ' + '</b>' + tooltip_data['complex_parameters'] + '<br>' + \
                                                '<b>' + 'Parameter description: ' + '</b>' + tooltip_data['description']
                                    self.button.setToolTip(self.text)
                                    
                            
                    
                    
                    self.button.clicked.connect(self.special_character_clicked)
                    self.sc_layout.addWidget(self.button, row+1, column)
                    i += 1
                    if i == len(self.characters_list): break
            self.sc_scroll.setLayout(self.sc_layout)
            sc = QScrollArea()
            sc.setWidget(self.sc_scroll)
            sc.setWidgetResizable(1)
            self.sc_groupbox.layout = QVBoxLayout()
            self.sc_groupbox.layout.addWidget(sc)
            self.sc_groupbox.setLayout(self.sc_groupbox.layout)
            self.tab.layout.addWidget(self.sc_groupbox)
            self.tab.setLayout(self.tab.layout)
            self.tabs.addTab(self.tab, category['name'])
        main_layout.addWidget(self.tabs)
        QApplication.instance().focusChanged.connect(self.on_focus_changed)
        self.show()
        
    def read_parameter_categories(self):
        self.cat = open(os.path.join(cwd + var.language_folder + self.language['language_description'] + '/' + var.p_cat_file))
        self.cat_file_data = json.load(self.cat)
        self.cat_list = []
        for category in self.cat_file_data:
            dict_to_send = {
                "category": category,
                "name": self.cat_file_data[category]
            }
            self.cat_list.append(dict_to_send)
        return self.cat_list
    
    def read_categories_files(self, category, columns):
        self.get_files = next(os.walk(cwd + var.basic_parameters_folder), (None, None, []))[2]
        self.category_list = []
        print(category)
        for file_name in self.get_files:
            json_path = os.path.join(cwd +var.basic_parameters_folder + file_name)
            with open(json_path) as json_file:
                parameters = json.load(json_file)
                print()
                if parameters['category'] == category:
                    self.category_list.append(parameters['symbol'])
        
        self.lista_kompleksnih = self.read_complex_parameters_changable(category=category)
        self.category_list = self.category_list + self.lista_kompleksnih
                
        if len(self.category_list) % columns == 0:
            rows = len(self.category_list) // columns
        else:
            rows = len(self.category_list) // columns + 1
        return self.category_list, rows, columns   
    
    def read_complex_parameters_changable(self, category):
        lista_fajlova = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
        lista_kompleksnih = []
        for file_names in lista_fajlova:
            json_path = os.path.join(cwd + var.complex_parameters_folder + file_names)
            with open(json_path) as json_file:
                c_parameters = json.load(json_file)
                if c_parameters['type'] == 'a':
                    if c_parameters['changable'] == 'yes':
                        if c_parameters['category'] == category:
                            lista_kompleksnih.append(c_parameters['symbol'])
        return lista_kompleksnih
       

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

if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = InputBasicParameterNameWidget()
    sys.exit(mainApplication.exec_())