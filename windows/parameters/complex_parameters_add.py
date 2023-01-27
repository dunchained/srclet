import sys, json, os
cwd = os.path.curdir
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QPushButton, QLineEdit
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QTextEdit, QComboBox, QHBoxLayout, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
#from variables import css, var
import var, css
#from mortys.parameters_morty import read_characters, get_filename, read_basic_parameters
from parameters_morty import read_characters, get_filename, read_basic_parameters
from language import language

class AddComplexParameter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = language
        self.window_gui()

    def window_gui(self):
        font = self.font()
        font.setPointSize(14) # učitati font iz mortija
        self.setFont(font)
        self.setWindowState(Qt.WindowMaximized)
        self.setMinimumSize(1200, 600)
        self.setWindowTitle(self.language['add_complex_parameter_window_title'])
        self.setWindowIcon(QIcon(css.parameters_complex_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.pb_name_groupbox(), 0, 0, 1, 1)
        self.grid.addWidget(self.pb_category_groupbox(), 0, 1, 1, 1)
        self.grid.addWidget(self.pb_symbol_groupbox(), 1, 0, 1, 1)
        self.grid.addWidget(self.pb_unit_groupbox(), 1, 1, 1, 1)
        self.grid.addWidget(self.pb_formula_groupbox(), 2, 0, 1, 2)
        self.grid.addWidget(self.pb_description_groupbox(), 3, 0, 1, 2)
        self.grid.addWidget(self.pb_changable_groupbox(), 4, 0, 1, 2)
        self.grid.addWidget(self.basic_parameters_groupbox(), 0, 2, 2, 1)
        self.grid.addWidget(self.frame_groupbox(), 2, 2, 3, 1)
        self.grid.addWidget(self.special_character_groupbox(), 0, 3, 5, 1)
        self.grid.addWidget(self.button_groupbox(), 5, 0, 1, 4)
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
        self.pbc_groupbox = QGroupBox(self.language['add_complex_parameter_window_category'])
        self.text_parameter_category = QLabel(self.language['add_complex_parameter_window_category_exp'])
        categories_file = open(os.path.join(cwd + var.language_folder + self.language['language_description'] + '/' + var.p_cat_file))
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
    
    def pb_changable_groupbox(self):
        self.chd_gruopbox = QGroupBox(self.language['add_complex_parameter_window_change_caption'])
        self.changable_check = QCheckBox(self.language['add_complex_parameter_window_change'])
        self.chd_gruopbox.layout = QVBoxLayout()
        self.chd_gruopbox.layout.addWidget(self.changable_check)
        self.chd_gruopbox.setLayout(self.chd_gruopbox.layout)
        return self.chd_gruopbox
    
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
        self.button_list, self.rows, self.columns = read_characters(var.charactes_loc)
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
        self.button_list, self.rows, self.columns = read_basic_parameters()
        i = 0
        for row in range(self.rows):
            for column in range(self.columns):
                button = QPushButton(f'{self.button_list[i]}', self)
                
                self.setStyleSheet('''QToolTip {min-width: 300px;}''')
                self.get_files = next(os.walk(cwd + var.basic_parameters_folder), (None, None, []))[2]
                for file in self.get_files:
                    self.file_to_read = open(os.path.join(cwd + var.basic_parameters_folder + file))
                    self.file_data = json.load(self.file_to_read)
                    if self.button_list[i] == self.file_data['symbol']:
                        self.file_to_load = file
                self.json_path = cwd + var.basic_parameters_folder + self.file_to_load
                with open(self.json_path) as json_file:
                    tooltip_data = json.load(json_file)
                self.text = '<b>' + self.language['add_basic_parameter_window_name'] + '</b>' + tooltip_data['name'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_symbol'] + '</b>' + self.button_list[i] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_category'] + '</b>' + tooltip_data['category'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_unit'] + '</b>' + tooltip_data['unit'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_desc'] + '</b>' + tooltip_data['description']
                button.setToolTip(self.text)
                
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
    
    def frame_groupbox(self):
        self.frame_groupbox = QGroupBox('Basic parameters:')
        self.text_bp_selected = QLabel('selected')
        self.text_basic_parameters = QLabel('add_eto_method_info_bp')
        self.selected_bp_list = QLabel()
        self.frame_groupbox.layout = QGridLayout()
        self.frame_groupbox.layout.addWidget(self.text_basic_parameters, 0, 0)
        self.frame_groupbox.layout.addWidget(self.basic_parameters_groupbox_check(), 1, 0)
        self.frame_groupbox.layout.addWidget(self.text_bp_selected, 2, 0)
        self.frame_groupbox.layout.addWidget(self.selected_bp_list, 3, 0)
        self.frame_groupbox.setLayout(self.frame_groupbox.layout)
        return self.frame_groupbox
    
    def basic_parameters_groupbox_check(self):
        self.bp_groupbox = QGroupBox()
        self.bp_layout = QGridLayout()
        self.bp_scroll = QWidget()
        self.bp_check_list, self.rows, self.columns = read_basic_parameters()
        i = 0
        for row in range(self.rows):
            for column in range(self.columns):
                self.bp_check = QCheckBox(f'{self.bp_check_list[i]}', self)
                
                self.setStyleSheet('''QToolTip {min-width: 300px;}''')
                self.get_files = next(os.walk(cwd + var.basic_parameters_folder), (None, None, []))[2]
                for file in self.get_files:
                    self.file_to_read = open(os.path.join(cwd + var.basic_parameters_folder + file))
                    self.file_data = json.load(self.file_to_read)
                    if self.bp_check_list[i] == self.file_data['symbol']:
                        self.file_to_load = file
                self.json_path = cwd + var.basic_parameters_folder + self.file_to_load
                with open(self.json_path) as json_file:
                    tooltip_data = json.load(json_file)
                # dodati šta fali za parameter od polja
                self.text = '<b>' + self.language['add_basic_parameter_window_name'] + '</b>' + tooltip_data['name'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_symbol'] + '</b>' + self.bp_check_list[i] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_category'] + '</b>' + tooltip_data['category'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_unit'] + '</b>' + tooltip_data['unit'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_desc'] + '</b>' + tooltip_data['description']
                self.bp_check.setToolTip(self.text)
                
                self.bp_check.clicked.connect(self.basic_parameter_checked)
                self.bp_layout.addWidget(self.bp_check, row+1, column)
                i += 1
                if i == len(self.bp_check_list): break
        self.bp_scroll.setLayout(self.bp_layout)
        bp = QScrollArea()
        bp.setWidget(self.bp_scroll)
        bp.setWidgetResizable(1)
        self.bp_groupbox.layout = QVBoxLayout()
        self.bp_groupbox.layout.addWidget(bp)
        self.bp_groupbox.setLayout(self.bp_groupbox.layout)
        return self.bp_groupbox
    
    def basic_parameter_checked(self):
        if not self.selected_bp_list.text():
            self.bpl = []
        else:
            self.bpl = self.selected_bp_list.text().split(', ')
        if self.sender().checkState() == 2:
            self.bpl.append(self.sender().text())
            self.selected_bp_list.setText(', '.join(self.bpl))
        else:
            self.bpl.remove(self.sender().text())
            self.selected_bp_list.setText(', '.join(self.bpl))
            
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
        if self.changable_check.checkState() == 2:
            self.change_to_save = 'yes'
        else:
            self.change_to_save = 'no'
        get_files = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
        self.file_list = []
        for file in get_files:
            self.file_to_read = open(os.path.join(cwd + var.complex_parameters_folder + file))
            self.file_data = json.load(self.file_to_read)
            if self.parameter_name.text() == self.file_data['name'] or self.parameter_symbol.text() == self.file_data['symbol']:
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
                    "changable": self.change_to_save,
                    "basic_parameters": self.selected_bp_list.text(),
                    "type": "a"
                    }
                json_object = json.dumps(parameter_dict, indent = 4)
                with open(cwd + var.complex_parameters_folder + self.file_name_to_save + ".json", "w") as outfile:
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
        self.close()

if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = AddComplexParameter()
    sys.exit(mainApplication.exec_())