import sys, json, os
cwd = os.path.curdir
from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QGridLayout, QGroupBox, QPushButton
from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget, QLabel
from PyQt6.QtCore import Qt
from variables import var

class BasicParameterWidget(QTabWidget):
    def __init__(self, language, title, columns=3):
        super().__init__()
        self.columns = columns
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowCloseButtonHint)
        self.language = language
        self.input_title = title
        self.window_gui()

    def window_gui(self):
        self.setWindowState(Qt.WindowState.WindowMaximized)
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
                    for file in self.get_basic:
                        with open(os.path.join(cwd + var.basic_parameters_folder + file), encoding="utf-8") as handle:
                            self.file_data = json.load(handle)
                        if self.characters_list[i] == self.file_data['symbol']:
                            self.file_to_load = file
                            self.json_path = cwd + var.basic_parameters_folder + self.file_to_load
                            with open(self.json_path) as json_file:
                                tooltip_data = json.load(json_file)
                            self.text = '<b>' + self.language['input_bp_parameter_name'] + '</b>' + tooltip_data['name'] + '<br>' + \
                                        '<b>' + self.language['input_bp_parameter_cat'] + '</b>' + tooltip_data['category'] + '<br>' + \
                                        '<b>' + self.language['input_bp_parameter_unit'] + '</b>' + tooltip_data['unit'] + '<br>' + \
                                        '<b>' + self.language['input_bp_parameter_sym'] + '</b>' + tooltip_data['symbol'] + '<br>' + \
                                        '<b>' + self.language['input_bp_parameter_desc'] + '</b>' + tooltip_data['description']
                            self.button.setToolTip(self.text)
                    self.button.clicked.connect(self.special_character_clicked)
                    self.sc_layout.addWidget(self.button, row+1, column)
                    i += 1
                    if i == len(self.characters_list): break
            self.sc_scroll.setLayout(self.sc_layout)
            sc = QScrollArea()
            sc.setWidget(self.sc_scroll)
            sc.setWidgetResizable(True)
            self.sc_groupbox.layout = QVBoxLayout()
            self.sc_groupbox.layout.addWidget(sc)
            self.sc_groupbox.setLayout(self.sc_groupbox.layout)
            self.tab.layout.addWidget(self.sc_groupbox)
            self.tab.setLayout(self.tab.layout)
            self.tabs.addTab(self.tab, category['name'])
        self.label_caption = QLabel(self.input_title)
        main_layout.addWidget(self.label_caption)
        main_layout.addWidget(self.tabs)
        QApplication.instance().focusChanged.connect(self.on_focus_changed)
        #self.show()
        
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
        for file_name in self.get_files:
            json_path = os.path.join(cwd +var.basic_parameters_folder + file_name)
            with open(json_path) as json_file:
                parameters = json.load(json_file)
                if parameters['category'] == category:
                    self.category_list.append(parameters['symbol'])
        
        if len(self.category_list) % columns == 0:
            rows = len(self.category_list) // columns
        else:
            rows = len(self.category_list) // columns + 1
        return self.category_list, rows, columns   

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
    mainWindow = BasicParameterWidget()
    sys.exit(mainApplication.exec())