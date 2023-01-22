import sys, os, json
from pathlib import Path
cwd = os.path.curdir
#from variables import css, var
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QPushButton
from PyQt5.QtWidgets import QLineEdit, QListWidget, QTextEdit, QMessageBox, QWidget, QApplication, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

from eto_methods_add import AddETOMethod
from methods_morty import read_characters, read_basic_parameters, read_complex_parameters

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

class ETOMethodsWidget(QWidget):
    def __init__(self):
        super(ETOMethodsWidget, self).__init__()
        QApplication.instance().focusChanged.connect(self.on_focus_changed)
        self.language = {
                            "//": "ETO Methods Widget",
                            "eto_methods_widget_caption": "List of available ETO Methods:",
                            "eto_methods_widget_btn_add_new": "Add new ETO method",
                            "eto_methods_widget_btn_delete": "Delete method",
                            "eto_methods_widget_parameter_caption": "Method information:",
                            "eto_methods_widget_parameter_filename": "Filename:",
                            "eto_methods_widget_parameter_name": "Method name:",
                            "eto_methods_widget_parameter_symbol": "Parameter symbol:",
                            "eto_methods_widget_parameter_unit": "Parameter unit:",
                            "eto_methods_widget_parameter_formula": "Calculation foruma:",
                            "eto_methods_widget_parameter_desc": "Parameter description:",
                            "eto_methods_widget_parameter_btn_save": "Save changes",
                            "eto_methods_widget_parameter_btn_cancel": "Cancel changes",
                            "eto_methods_widget_btn_close": "Close",
                            "eto_methods_widget_save_changes_message": "Parameter name, symbol or unit empty...",
                            "eto_methods_widget_save_changes_message_caption": "Missing data...",
                            "eto_methods_widget_save_message": "Complex Parameter saved...",
                            "eto_methods_widget_save_message_caption": "Successuful..."
                         }
        #self.AddParameter = AddComplexParameter(self.language)
        #self.AddParameter.hide()
        #self.AddParameter.clicked.connect(self.refresh_parameters_list)
        self.window_gui()

    def window_gui(self):
        self.grid = QGridLayout()
        self.grid.addWidget(self.create_list_of_methods(), 0, 0, 1, 1)
        self.grid.addWidget(self.create_method_info(), 0, 1, 1, 1)
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
        
    def create_list_of_methods(self):
        self.methods_groupbox = QGroupBox(self.language['eto_methods_widget_caption'])
        self.list_widget = QListWidget()
        self.get_files = next(os.walk(cwd + eto_methods_folder), (None, None, []))[2]
        self.methods_list = []
        for file in self.get_files:
            self.file_to_load = open(os.path.join(cwd + eto_methods_folder + file))
            self.file_data = json.load(self.file_to_load)
            self.methods_list.append(self.file_data['name'])
            
        self.list_widget.addItems(self.methods_list)
        self.list_widget.currentItemChanged.connect(self.index_changed)
        self.btn_add_method = QPushButton('Add new ETO method')
        self.btn_add_method.clicked.connect(self.new_method)
        self.btn_delete_method = QPushButton('Delete method')
        self.btn_delete_method.clicked.connect(self.delete_procedure)
        self.methods_groupbox.layout = QGridLayout()
        self.methods_groupbox.layout.addWidget(self.list_widget, 0, 0, 1, 1)
        self.methods_groupbox.layout.addWidget(self.btn_add_method, 2, 0, 1, 1)
        self.methods_groupbox.layout.addWidget(self.special_character_groupbox(), 1, 0, 1, 1)
        self.methods_groupbox.layout.addWidget(self.btn_delete_method, 3, 0, 1, 1)
        self.methods_groupbox.setLayout(self.methods_groupbox.layout)
        return self.methods_groupbox
    
    def index_changed(self, i):
        self.get_files = next(os.walk(cwd + eto_methods_folder), (None, None, []))[2]
        for file in self.get_files:
            self.file_to_read = open(os.path.join(cwd + eto_methods_folder + file))
            self.file_data = json.load(self.file_to_read)
            if i.text() == self.file_data['name']:
                self.file_to_load = file
                self.json_path = cwd + eto_methods_folder + self.file_to_load
                with open(self.json_path) as json_file:
                    data = json.load(json_file)
                    if data['type'] == 'b':
                        self.update_labels(
                            state=False, 
                            name=data['name'],
                            short_name=data['short_name'],
                            symbol=data['symbol'],
                            description=data['description'],
                            conditions=data['method_conditions'],
                            formula=data['method_formula'],
                            bparam=data['basic_parameters'],
                            cparam=data['complex_parameters'])
                    else:
                        self.update_labels(
                            state=True, 
                            name=data['name'],
                            short_name=data['short_name'],
                            symbol=data['symbol'],
                            description=data['description'],
                            conditions=data['method_conditions'],
                            formula=data['method_formula'],
                            bparam=data['basic_parameters'],
                            cparam=data['complex_parameters'])

    def update_labels(self, state, name, short_name, symbol, description, conditions, formula, bparam, cparam):
        self.method_name.setText(name)
        self.method_name.setEnabled(state)
        self.method_short_name.setText(short_name)
        self.method_short_name.setEnabled(state)
        self.method_symbol.setText(symbol)
        self.method_symbol.setEnabled(state)
        self.method_description.setText(description)
        self.method_description.setEnabled(state)
        self.method_conditions.setText(conditions)
        self.method_conditions.setEnabled(state)
        self.method_formula.setText(formula)
        self.method_formula.setEnabled(state)
        self.bp_groupbox.setEnabled(state)
        self.selected_bp_list.setText(bparam)
        self.bp_list_to_update = bparam.split(', ')
        for self.bp_check in range(self.bp_layout.count()):
            self.bp_check_widget = self.bp_layout.itemAt(self.bp_check).widget()
            self.bp_check_widget.setChecked(False)
            if self.bp_check_widget.text() in self.bp_list_to_update: self.bp_check_widget.setChecked(True)
        self.cp_groupbox.setEnabled(state)
        self.selected_cp_list.setText(cparam)
        self.cp_list_to_update = cparam.split(', ')
        for self.cp_check in range(self.cp_layout.count()):
            self.cp_check_widget = self.cp_layout.itemAt(self.cp_check).widget()
            self.cp_check_widget.setChecked(False)
            if self.cp_check_widget.text() in self.cp_list_to_update: self.cp_check_widget.setChecked(True)
        self.btn_save_method_changes.setEnabled(state)
        self.btn_cancel_method_changes.setEnabled(state)
        self.btn_delete_method.setEnabled(state)
            
    def new_method(self):
        self.window = AddETOMethod()
        
    def delete_procedure(self):
        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.setText('Are you sure you want to delete method?')
        self.msgBox.setWindowTitle('Delete?')
        self.msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.buttonOK = self.msgBox.button(QMessageBox.Ok)
        self.buttonOK.setText('yes')
        self.buttonCancel = self.msgBox.button(QMessageBox.Cancel)
        self.buttonCancel.setText('cancel')
        self.msgBox.buttonClicked.connect(self.delete_method)
        returnValue = self.msgBox.exec()

    def delete_method(self, value):
        if value.text() == 'yes':
            self.get_list_of_files = next(os.walk(cwd + eto_methods_folder), (None, None, []))[2]
            for self.file_to_delete in self.get_list_of_files:
                self.path_to_file_to_delete = open(os.path.join(cwd + eto_methods_folder + self.file_to_delete))
                self.data_of_file_to_delete = json.load(self.path_to_file_to_delete)
                if self.list_widget.currentItem().text() == self.data_of_file_to_delete['name']:
                    os.remove(os.path.join(cwd + eto_methods_folder + self.file_to_delete))
            self.refresh_methods_list_after_deletion()
            
    def refresh_methods_list_after_deletion(self):
        self.item_to_remove = self.list_widget.selectedItems()
        if not self.item_to_remove: return
        for item in self.item_to_remove:
            self.list_widget.takeItem(self.list_widget.row(item))
    
    def special_character_groupbox(self):
        self.sc_groupbox = QGroupBox('Input special character:')
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
        self.bp_groupbox = QGroupBox()
        self.bp_layout = QGridLayout()
        self.bp_scroll = QWidget()
        self.bp_check_list, self.rows, self.columns = read_basic_parameters() # uvezati iz var
        i = 0
        for row in range(self.rows):
            for column in range(self.columns):
                self.bp_check = QCheckBox(f'{self.bp_check_list[i]}', self)
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
            
    def complex_parameters_groupbox(self):
        self.cp_groupbox = QGroupBox()
        self.cp_layout = QGridLayout()
        self.cp_scroll = QWidget()
        self.cp_check_list, self.rows, self.columns = read_complex_parameters() # uvezati iz var
        i = 0
        for row in range(self.rows):
            for column in range(self.columns):
                self.cp_check = QCheckBox(f'{self.cp_check_list[i]}', self)
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
    
    def create_method_info(self):
        self.method_info_groupbox = QGroupBox('Method information:')
        
        self.text_method_name = QLabel('Method name:')
        self.method_name = QLineEdit()
        self.text_method_short_name = QLabel('Method short name:')
        self.method_short_name = QLineEdit()
        self.text_method_symbol = QLabel('Method symbol:')
        self.method_symbol = QLineEdit()
        self.text_method_description = QLabel('Method description:')
        self.method_description = QTextEdit()
        self.text_method_conditions = QLabel('Method conditions:')
        self.method_conditions = QTextEdit()
        self.text_method_formula = QLabel('Method calculation formula:')
        self.method_formula = QTextEdit()
        self.text_basic_parameters = QLabel('Basic parameters:')
        self.text_complex_parameters = QLabel('Complex parameters:')
        self.text_bp_selected = QLabel('Selected basic parameters:')
        self.selected_bp_list = QLabel()
        self.text_cp_selected = QLabel('Selected complex parameters:')
        self.selected_cp_list = QLabel()
        self.btn_save_method_changes = QPushButton('Save changes')
        self.btn_save_method_changes.clicked.connect(self.save_changes_method)
        self.btn_cancel_method_changes = QPushButton('Cancel changes')
        self.btn_cancel_method_changes.clicked.connect(self.cancel_changes_method)
        
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
        self.method_info_groupbox.layout.addWidget(self.btn_save_method_changes, 12, 0, 1, 2)
        self.method_info_groupbox.layout.addWidget(self.btn_cancel_method_changes, 13, 0, 1, 2)
        
        self.method_info_groupbox.setLayout(self.method_info_groupbox.layout)
        return self.method_info_groupbox
    
    def save_changes_method(self):
        self.get_files = next(os.walk(cwd + eto_methods_folder), (None, None, []))[2]
        for file in self.get_files:
            self.file_to_read = open(os.path.join(cwd + eto_methods_folder + file))
            self.file_data = json.load(self.file_to_read)
            if self.method_name.text() == self.file_data['name']:
                self.file_to_load = file
        if not self.method_name.text() or not self.method_short_name.text() or not self.method_symbol.text() or not self.method_formula.toPlainText() or not self.selected_bp_list.text():
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText('Missing data, nabrojati šta mora imati...')
            self.msg.setWindowTitle('Missing data...')
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
            with open(cwd + eto_methods_folder + self.file_to_load, "w") as outfile:
                outfile.write(json_object)
                
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText('Method data saved...')
            self.msg.setWindowTitle('Success...')
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.show()
        
    def cancel_changes_method(self):
        self.json_path = cwd + eto_methods_folder + self.file_to_load
        with open(self.json_path) as json_file:
            data = json.load(json_file)
        
        self.method_name.setText(data['name'])
        self.method_short_name.setText(data['short_name'])
        self.method_symbol.setText(data['symbol'])
        self.method_description.setText(data['description'])
        self.method_conditions.setText(data['method_conditions'])
        self.method_formula.setText(data['method_formula'])
        self.selected_bp_list.setText(data['basic_parameters'])
        self.bp_list_to_update = data['basic_parameters'].split(', ')
        for self.bp_check in range(self.bp_layout.count()):
            self.bp_check_widget = self.bp_layout.itemAt(self.bp_check).widget()
            self.bp_check_widget.setChecked(False)
            if self.bp_check_widget.text() in self.bp_list_to_update: self.bp_check_widget.setChecked(True)
        self.selected_cp_list.setText(data['complex_parameters'])
        self.cp_list_to_update = data['complex_parameters'].split(', ')
        for self.cp_check in range(self.cp_layout.count()):
            self.cp_check_widget = self.cp_layout.itemAt(self.cp_check).widget()
            self.cp_check_widget.setChecked(False)
            if self.cp_check_widget.text() in self.cp_list_to_update: self.cp_check_widget.setChecked(True)
            
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = ETOMethodsWidget()
    sys.exit(mainApplication.exec_())