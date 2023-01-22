import sys, os, json
from pathlib import Path
cwd = os.path.curdir
#from variables import css, var
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QPushButton
from PyQt5.QtWidgets import QLineEdit, QListWidget, QTextEdit, QMessageBox, QWidget, QApplication, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

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
                            short_name=data['short_name']
                            )
                    else:
                        self.update_labels(
                            state=True, 
                            name=data['name'],
                            short_name=data['short_name'])

    def update_labels(self, state, name, short_name):
        self.method_name.setText(name)
        self.method_name.setEnabled(state)
        self.method_short_name.setText(short_name)
        self.method_short_name.setEnabled(state)
    
    def new_method(self):
        print('new method')
        
    def delete_procedure(self):
        print('delete procedure')
        self.delete_method()
        
    def delete_method(self):
        print('delete method')
    
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
        self.button_list, self.rows, self.columns = read_basic_parameters() # uvezati iz var
        i = 0
        for row in range(self.rows):
            for column in range(self.columns):
                button = QCheckBox(f'{self.button_list[i]}', self)
                button.clicked.connect(self.basic_parameter_checked)
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
        self.button_list, self.rows, self.columns = read_complex_parameters() # uvezati iz var
        i = 0
        for row in range(self.rows):
            for column in range(self.columns):
                button = QCheckBox(f'{self.button_list[i]}', self)
                button.clicked.connect(self.complex_parameter_checked)
                self.cp_layout.addWidget(button, row+1, column)
                i += 1
                if i == len(self.button_list): break
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
    
    
    # def refresh_parameters_list(self):
    #     get_files = next(os.walk(cwd + complex_parameters_folder), (None, None, []))[2]
    #     self.file_list_update = []
    #     for file in get_files:
    #         if Path(file).stem not in self.file_list:
    #             self.file_list_update.append(Path(file).stem)
    #     self.list_widget.addItems(self.file_list_update)

    # def delete_parameter(self):
    #     list_items = self.list_widget.selectedItems()
    #     if not list_items: return
    #     for item in list_items:
    #         self.list_widget.takeItem(self.list_widget.row(item))
    #     os.remove(cwd + complex_parameters_folder + item.text() + '.json')
    
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
        print('save changes method')
        
    def cancel_changes_method(self):
        print('cancel changes method')
    
    
    
    # def cancel(self):
    #     self.json_path = cwd + complex_parameters_folder + self.list_widget.currentItem().text() + '.json'
    #     with open(self.json_path) as json_file:
    #         data = json.load(json_file)
            
    #     self.parameter_name.setText(data['name'])
    #     self.parameter_symbol.setText(data['symbol'])
    #     self.parameter_unit.setText(data['unit'])
    #     self.parameter_formula.setText(data['formula'])
    #     self.parameter_descriprion.setText(data['description'])
    
    # def newParameterWindow(self):
    #     self.AddParameter.show()

    # def save_changes_parameter(self):
    #     if not self.parameter_filename or not self.parameter_name.text() or not self.parameter_unit.text() or not self.parameter_symbol.text():
    #         self.msg = QMessageBox()
    #         self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
    #         self.msg.setIcon(QMessageBox.Information)
    #         self.msg.setText(self.language['eto_methods_widget_save_changes_message'])
    #         self.msg.setWindowTitle(self.language['eto_methods_widget_save_changes_message_caption'])
    #         self.msg.setStandardButtons(QMessageBox.Ok)
    #         self.msg.buttonClicked.connect(self.msg.close)
    #         self.msg.show()
    #     else:
    #         parameter_dict = {
    #             "name": self.parameter_name.text(),
    #             "symbol": self.parameter_symbol.text(),
    #             "unit": self.parameter_unit.text(),
    #             "formula": self.parameter_formula.toPlainText(),
    #             "description": self.parameter_descriprion.toPlainText(),
    #             "type": "a"
    #             }
    #         json_object = json.dumps(parameter_dict, indent = 4)
    #         with open(cwd + complex_parameters_folder + self.parameter_filename.text() + ".json", "w") as outfile:
    #             outfile.write(json_object)
                
    #         self.msg = QMessageBox()
    #         self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
    #         self.msg.setIcon(QMessageBox.Information)
    #         self.msg.setText(self.language['eto_methods_widget_save_message'])
    #         self.msg.setWindowTitle(self.language['eto_methods_widget_save_message_caption'])
    #         self.msg.setStandardButtons(QMessageBox.Ok)
    #         self.msg.show()
            
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = ETOMethodsWidget()
    sys.exit(mainApplication.exec_())