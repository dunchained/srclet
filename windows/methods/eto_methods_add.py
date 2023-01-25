import sys, os, json
cwd = os.path.curdir
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QHBoxLayout, QGridLayout, QGroupBox, QLabel, QPushButton
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QMessageBox, QWidget, QApplication, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
#from variables import css, var
import css, var
#from mortys.methods_morty import read_characters, read_basic_parameters, read_complex_parameters, get_filename
from methods_morty import read_characters, read_basic_parameters, read_complex_parameters, get_filename
from language import language

class AddETOMethod(QWidget):
    def __init__(self):
        super(AddETOMethod, self).__init__()
        self.language = language
        QApplication.instance().focusChanged.connect(self.on_focus_changed)
        self.window_gui()

    def window_gui(self):
        font = self.font()
        font.setPointSize(14) # učitati font iz mortija
        self.setFont(font)
        self.setWindowState(Qt.WindowMaximized)
        self.setMinimumSize(1200, 600)
        self.setWindowTitle(self.language['add_eto_method_window_title'])
        self.setWindowIcon(QIcon(css.parameters_basic_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.left_groupbox(), 0, 0, 1, 1)
        self.grid.addWidget(self.right_groupbox(), 0, 1, 1, 1)
        self.grid.addWidget(self.down_groupbox(), 1, 0, 1, 2)
        self.setLayout(self.grid)
        self.show()
        
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
        
    def right_groupbox(self):
        self.methods_groupbox = QGroupBox(self.language['add_eto_method_inserts'])
        self.methods_groupbox.layout = QGridLayout()
        self.methods_groupbox.layout.addWidget(self.special_character_groupbox(), 0, 0, 1, 2)
        self.methods_groupbox.layout.addWidget(self.basic_parameters_groupbox_insert(), 1, 0, 1, 1)
        self.methods_groupbox.layout.addWidget(self.complex_parameters_groupbox_insert(), 1, 1, 1, 1)
        self.methods_groupbox.setLayout(self.methods_groupbox.layout)
        return self.methods_groupbox
            
    def special_character_groupbox(self):
        self.sc_groupbox = QGroupBox(self.language['add_eto_method_inserts_sc'])
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
            
    def basic_parameters_groupbox_insert(self):
        self.bpi_groupbox = QGroupBox(self.language['add_eto_method_inserts_bp'])
        self.bpi_layout = QGridLayout()
        self.bpi_scroll = QWidget()
        self.bpi_check_list, self.rows, self.columns = read_basic_parameters()
        i = 0
        for row in range(self.rows):
            for column in range(self.columns):
                self.bpi_check = QPushButton(f'{self.bpi_check_list[i]}', self)
                
                self.setStyleSheet('''QToolTip {min-width: 300px;}''')
                self.get_files = next(os.walk(cwd + var.basic_parameters_folder), (None, None, []))[2]
                for file in self.get_files:
                    self.file_to_read = open(os.path.join(cwd + var.basic_parameters_folder + file))
                    self.file_data = json.load(self.file_to_read)
                    if self.bpi_check_list[i] == self.file_data['symbol']:
                        self.file_to_load = file
                self.json_path = cwd + var.basic_parameters_folder + self.file_to_load
                with open(self.json_path) as json_file:
                    tooltip_data = json.load(json_file)
                # dodati šta fali za parameter od polja
                self.text = '<b>' + self.language['add_basic_parameter_window_name'] + '</b>' + tooltip_data['name'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_symbol'] + '</b>' + self.bpi_check_list[i] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_category'] + '</b>' + tooltip_data['category'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_unit'] + '</b>' + tooltip_data['unit'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_desc'] + '</b>' + tooltip_data['description']
                self.bpi_check.setToolTip(self.text)
                
                self.bpi_check.clicked.connect(self.special_character_clicked)
                self.bpi_layout.addWidget(self.bpi_check, row+1, column)
                i += 1
                if i == len(self.bpi_check_list): break
        self.bpi_scroll.setLayout(self.bpi_layout)
        bpi = QScrollArea()
        bpi.setWidget(self.bpi_scroll)
        bpi.setWidgetResizable(1)
        self.bpi_groupbox.layout = QVBoxLayout()
        self.bpi_groupbox.layout.addWidget(bpi)
        self.bpi_groupbox.setLayout(self.bpi_groupbox.layout)
        return self.bpi_groupbox
    
    def complex_parameters_groupbox_insert(self):
        self.bpc_groupbox = QGroupBox(self.language['add_eto_method_inserts_cp'])
        self.bpc_layout = QGridLayout()
        self.bpc_scroll = QWidget()
        self.bpc_check_list, self.rows, self.columns = read_complex_parameters()
        i = 0
        for row in range(self.rows):
            for column in range(self.columns):
                self.bpc_check = QPushButton(f'{self.bpc_check_list[i]}', self)
                
                self.setStyleSheet('''QToolTip {min-width: 300px;}''')
                self.get_files = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
                for file in self.get_files:
                    self.file_to_read = open(os.path.join(cwd + var.complex_parameters_folder + file))
                    self.file_data = json.load(self.file_to_read)
                    if self.bpc_check_list[i] == self.file_data['symbol']:
                        self.file_to_load = file
                self.json_path = cwd + var.complex_parameters_folder + self.file_to_load
                with open(self.json_path) as json_file:
                    tooltip_data = json.load(json_file)
                # dodati šta fali za parameter od polja
                self.text = '<b>' + self.language['add_basic_parameter_window_name'] + '</b>' + tooltip_data['name'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_symbol'] + '</b>' + self.bpc_check_list[i] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_category'] + '</b>' + tooltip_data['category'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_unit'] + '</b>' + tooltip_data['unit'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_desc'] + '</b>' + tooltip_data['description']
                self.bpc_check.setToolTip(self.text)
                
                self.bpc_check.clicked.connect(self.special_character_clicked)
                self.bpc_layout.addWidget(self.bpc_check, row+1, column)
                i += 1
                if i == len(self.bpc_check_list): break
        self.bpc_scroll.setLayout(self.bpc_layout)
        bpc = QScrollArea()
        bpc.setWidget(self.bpc_scroll)
        bpc.setWidgetResizable(1)
        self.bpc_groupbox.layout = QVBoxLayout()
        self.bpc_groupbox.layout.addWidget(bpc)
        self.bpc_groupbox.setLayout(self.bpc_groupbox.layout)
        return self.bpc_groupbox
            
    def complex_parameters_groupbox(self):
        self.cp_groupbox = QGroupBox()
        self.cp_layout = QGridLayout()
        self.cp_scroll = QWidget()
        self.cp_check_list, self.rows, self.columns = read_complex_parameters()
        i = 0
        for row in range(self.rows):
            for column in range(self.columns):
                self.cp_check = QCheckBox(f'{self.cp_check_list[i]}', self)
                
                self.setStyleSheet('''QToolTip {min-width: 300px;}''')
                self.get_files = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
                for file in self.get_files:
                    self.file_to_read = open(os.path.join(cwd + var.complex_parameters_folder + file))
                    self.file_data = json.load(self.file_to_read)
                    if self.cp_check_list[i] == self.file_data['symbol']:
                        self.file_to_load = file
                self.json_path = cwd + var.complex_parameters_folder + self.file_to_load
                with open(self.json_path) as json_file:
                    tooltip_data = json.load(json_file)
                # dodati šta fali za parameter od polja
                self.text = '<b>' + self.language['add_basic_parameter_window_name'] + '</b>' + tooltip_data['name'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_symbol'] + '</b>' + self.cp_check_list[i] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_category'] + '</b>' + tooltip_data['category'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_unit'] + '</b>' + tooltip_data['unit'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_desc'] + '</b>' + tooltip_data['description']
                self.cp_check.setToolTip(self.text)
                
                self.cp_check.clicked.connect(self.complex_parameter_checked)
                self.cp_layout.addWidget(self.cp_check, row+1, column)
                i += 1
                if i == len(self.cp_check_list): break
        self.cp_scroll.setLayout(self.cp_layout)
        cp = QScrollArea()
        cp.setWidget(self.cp_scroll)
        cp.setWidgetResizable(1)
        self.cp_groupbox.layout = QVBoxLayout()
        self.cp_groupbox.layout.addWidget(cp)
        self.cp_groupbox.setLayout(self.cp_groupbox.layout)
        return self.cp_groupbox
    
    def complex_parameter_checked(self):
        if not self.selected_cp_list.text():
            self.cpl = []
        else:
            self.cpl = self.selected_cp_list.text().split(', ')
        if self.sender().checkState() == 2:
            self.cpl.append(self.sender().text())
            self.selected_cp_list.setText(', '.join(self.cpl))
        else:
            self.cpl.remove(self.sender().text())
            self.selected_cp_list.setText(', '.join(self.cpl))
    
    
    def left_groupbox(self):
        self.method_info_groupbox = QGroupBox(self.language['add_eto_method_info_caption'])
        self.text_method_name = QLabel(self.language['add_eto_method_info_name'])
        self.method_name = QLineEdit()
        self.text_method_short_name = QLabel(self.language['add_eto_method_info_short_name'])
        self.method_short_name = QLineEdit()
        self.text_method_symbol = QLabel(self.language['add_eto_method_info_symbol'])
        self.method_symbol = QLineEdit()
        self.text_method_description = QLabel(self.language['add_eto_method_info_description'])
        self.method_description = QTextEdit()
        self.text_method_conditions = QLabel(self.language['add_eto_method_info_conditions'])
        self.method_conditions = QTextEdit()
        self.text_method_formula = QLabel(self.language['add_eto_method_info_formula'])
        self.method_formula = QTextEdit()
        self.text_basic_parameters = QLabel(self.language['add_eto_method_info_bp'])
        self.text_complex_parameters = QLabel(self.language['add_eto_method_info_cp'])
        self.text_bp_selected = QLabel(self.language['add_eto_method_info_bp_s'])
        self.selected_bp_list = QLabel()
        self.text_cp_selected = QLabel(self.language['add_eto_method_info_cp_s'])
        self.selected_cp_list = QLabel()
        self.method_info_groupbox.layout = QGridLayout()
        self.method_info_groupbox.layout.addWidget(self.text_method_name, 0, 0, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.method_name, 1, 0, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.text_method_short_name, 0, 1, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.method_short_name, 1, 1, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.text_method_symbol, 2, 0, 1, 2)
        self.method_info_groupbox.layout.addWidget(self.method_symbol, 3, 0, 1, 2)
        self.method_info_groupbox.layout.addWidget(self.text_method_description, 4, 0, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.method_description, 5, 0, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.text_method_conditions, 4, 1, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.method_conditions, 5, 1, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.text_method_formula, 6, 0, 1, 2)
        self.method_info_groupbox.layout.addWidget(self.method_formula, 7, 0, 1, 2)
        self.method_info_groupbox.layout.addWidget(self.text_basic_parameters, 8, 0, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.basic_parameters_groupbox(), 9, 0, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.text_complex_parameters, 8, 1, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.complex_parameters_groupbox(), 9, 1, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.text_bp_selected, 10, 0, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.selected_bp_list, 11, 0, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.text_cp_selected, 10, 1, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.selected_cp_list, 11, 1, 1, 1)
        self.method_info_groupbox.setLayout(self.method_info_groupbox.layout)
        return self.method_info_groupbox  
    
    def down_groupbox(self):
        self.btn_groupbox = QGroupBox()
        self.btn_save = QPushButton(self.language['add_eto_method_btn_save'])
        self.btn_save.clicked.connect(self.add_method)
        self.btn_cancel = QPushButton(self.language['add_eto_method_btn_close'])
        self.btn_cancel.clicked.connect(self.close)
        self.btn_groupbox.layout = QHBoxLayout()
        self.btn_groupbox.layout.addWidget(self.btn_save)
        self.btn_groupbox.layout.addWidget(self.btn_cancel)
        self.btn_groupbox.setLayout(self.btn_groupbox.layout)
        return self.btn_groupbox
    
    def add_method(self):
        self.file_name_to_save = get_filename('eto')
        get_files = next(os.walk(cwd + var.eto_methods_folder), (None, None, []))[2]
        self.file_list = []
        for file in get_files:
            self.file_to_read = open(os.path.join(cwd + var.eto_methods_folder + file))
            self.file_data = json.load(self.file_to_read)
            if self.method_name.text() == self.file_data['name']:
                self.file_list.append(file)
                        
        if self.file_list:
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['add_eto_method_msg_exists'])
            self.msg.setWindowTitle(self.language['add_eto_method_msg_exists_title'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            if not self.method_name.text() or not self.method_short_name.text() or not self.method_symbol.text() or not self.method_formula.toPlainText() or not self.selected_bp_list.text():
                self.msg = QMessageBox()
                self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText(self.language['add_eto_method_msg_missing'])
                self.msg.setWindowTitle(self.language['add_eto_method_msg_missing_title'])
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.buttonClicked.connect(self.msg.close)
                self.msg.show()
            else:
                parameter_dict = {
                    "name": self.method_name.text(),
                    "short_name": self.method_short_name.text(),
                    "symbol": self.method_symbol.text(),
                    "description": self.method_description.toPlainText(),
                    "method_conditions": self.method_conditions.toPlainText(),
                    "method_formula": self.method_formula.toPlainText(),
                    "basic_parameters": self.selected_bp_list.text(),
                    "complex_parameters": self.selected_cp_list.text(),
                    "type": "a"
                    }
                json_object = json.dumps(parameter_dict, indent = 4)
                with open(cwd + var.eto_methods_folder + self.file_name_to_save + ".json", "w") as outfile:
                    outfile.write(json_object)
                self.msg = QMessageBox()
                self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText(self.language['add_eto_method_msg_saved'])
                self.msg.setWindowTitle(self.language['add_eto_method_msg_saved_title'])
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.buttonClicked.connect(self.message_box_success)
                self.msg.show()
            
    def message_box_success(self):
        self.close()
            
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = AddETOMethod()
    sys.exit(mainApplication.exec_())