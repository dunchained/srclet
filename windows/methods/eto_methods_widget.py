import sys, os, json
cwd = os.path.curdir
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QGridLayout, QGroupBox, QLabel, QPushButton
from PyQt5.QtWidgets import QLineEdit, QListWidget, QTextEdit, QMessageBox, QWidget, QApplication, QCheckBox
from PyQt5.QtCore import Qt
from variables import var
from windows.methods.eto_methods_add import AddET0Method
from mortys.methods_morty import read_om, read_bp, read_cp

from widgets.ch_widget import InputCharacterWidget
from widgets.bp_widget import BasicParameterWidget
from widgets.cp_widget import ChangableParameterWidget
from widgets.om_widget import OtherMethodsWidget

class ETOMethodsWidget(QWidget):
    def __init__(self, language):
        super().__init__()
        QApplication.instance().focusChanged.connect(self.on_focus_changed)
        self.language = language
        self.window_gui()

    def window_gui(self):
        self.grid = QGridLayout()
        self.grid.addWidget(self.create_list_of_methods(), 0, 0, 2, 1)
        self.grid.addWidget(self.create_method_info(), 0, 1, 2, 1)
        self.grid.addWidget(BasicParameterWidget(language=language, title=self.language['add_other_method_inserts_bp'], columns=2), 0, 2, 1, 1)
        self.grid.addWidget(ChangableParameterWidget(language=language, title=self.language['add_other_method_inserts_cp'], columns=2), 0, 3, 1, 1)
        self.grid.addWidget(OtherMethodsWidget(language=language, title=self.language['add_other_method_inserts_om'], columns=2), 1, 2, 1, 1)
        self.grid.addWidget(InputCharacterWidget(language=language, title=self.language['add_other_method_inserts_sc'], columns=2), 1, 3, 1, 1)
        self.setLayout(self.grid)
        self.show()
        
    def on_focus_changed(self, widget):
        self.on_focused_change = widget
        
     # brisati kod ovezivanja   
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
        self.methods_groupbox = QGroupBox(self.language['eto_methods_widget_list'])
        self.list_widget = QListWidget()
        self.get_files = next(os.walk(cwd + var.eto_methods_folder), (None, None, []))[2]
        self.methods_list = []
        for file in self.get_files:
            self.file_to_load = open(os.path.join(cwd + var.eto_methods_folder + file))
            self.file_data = json.load(self.file_to_load)
            self.methods_list.append(self.file_data['name'])
        self.list_widget.addItems(self.methods_list)
        self.list_widget.currentItemChanged.connect(self.index_changed)
        self.btn_add_method = QPushButton(self.language['eto_methods_widget_btn_add_method'])
        self.btn_add_method_inherit = QPushButton(self.language['other_methods_widget_btn_add_new_inherit'])
        self.btn_add_method_inherit.setEnabled(False)
        self.btn_add_method_inherit.clicked.connect(self.new_method_inherit)
        self.btn_add_method.clicked.connect(self.new_method)
        self.btn_delete_method = QPushButton(self.language['eto_methods_widget_btn_delete_method'])
        self.btn_delete_method.clicked.connect(self.delete_procedure)
        self.btn_delete_method.setEnabled(False)
        self.methods_groupbox.layout = QGridLayout()
        self.methods_groupbox.layout.addWidget(self.list_widget)
        self.methods_groupbox.layout.addWidget(self.btn_add_method)
        self.methods_groupbox.layout.addWidget(self.btn_add_method_inherit)
        self.methods_groupbox.layout.addWidget(self.btn_delete_method)
        self.methods_groupbox.setLayout(self.methods_groupbox.layout)
        return self.methods_groupbox
    
    def index_changed(self, i):
        self.get_files = next(os.walk(cwd + var.eto_methods_folder), (None, None, []))[2]
        for file in self.get_files:
            self.file_to_read = open(os.path.join(cwd + var.eto_methods_folder + file))
            self.file_data = json.load(self.file_to_read)
            if i.text() == self.file_data['name']:
                self.file_to_load = file
                self.json_path = cwd + var.eto_methods_folder + self.file_to_load
                with open(self.json_path) as json_file:
                    data = json.load(json_file)
                    if data['type'] == 'b':
                        self.update_labels(
                            state=False, 
                            name=data['name'],
                            short_name=data['unit'],
                            symbol=data['symbol'],
                            description=data['description'],
                            conditions=data['method_conditions'],
                            formula=data['method_formula'],
                            bparam=data['basic_parameters'],
                            cparam=data['changable_parameters'],
                            om=data['other_methods'])
                        self.method_dict = {
                                    "name": data['name'] + self.language['other_methods_new_addition'],
                                    "symbol": data['symbol'],
                                    "unit": data['unit'],
                                    "description": data['description'] + self.language['other_methods_new_addition'],
                                    "method_conditions": data['method_conditions'],
                                    "method_formula": data['method_formula'],
                                    "basic_parameters": data['basic_parameters'],
                                    "changable_parameters": data['changable_parameters'],
                                    "other_methods": data['other_methods'],
                                    "type": "a"
                                }
                        self.btn_add_method_inherit.setEnabled(True)
                    else:
                        self.update_labels(
                            state=True, 
                            name=data['name'],
                            short_name=data['unit'],
                            symbol=data['symbol'],
                            description=data['description'],
                            conditions=data['method_conditions'],
                            formula=data['method_formula'],
                            bparam=data['basic_parameters'],
                            cparam=data['changable_parameters'],
                            om=data['other_methods'])
                        self.method_dict = {
                                    "name": data['name'] + self.language['other_methods_new_addition'],
                                    "symbol": data['symbol'],
                                    "unit": data['unit'],
                                    "description": data['description'] + self.language['other_methods_new_addition'],
                                    "method_conditions": data['method_conditions'],
                                    "method_formula": data['method_formula'],
                                    "basic_parameters": data['basic_parameters'],
                                    "changable_parameters": data['changable_parameters'],
                                    "other_methods": data['other_methods'],
                                    "type": "a"
                                }
                        self.btn_add_method_inherit.setEnabled(True)

    def update_labels(self, state, name, short_name, symbol, description, conditions, formula, bparam, cparam, om):
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

        self.selected_om_list.setText(om)
        self.om_list_to_update = om.split(', ')
        for self.om_check in range(self.om_layout.count()):
            self.om_check_widget = self.om_layout.itemAt(self.om_check).widget()
            self.om_check_widget.setChecked(False)
            if self.om_check_widget.text() in self.om_list_to_update: self.om_check_widget.setChecked(True)
        
        self.btn_save_method_changes.setEnabled(state)
        self.btn_cancel_method_changes.setEnabled(state)
        self.btn_delete_method.setEnabled(state)
            
    def new_method(self):
        self.window = AddET0Method(language=self.language, data_to_input=None)

    def new_method_inherit(self):
        self.window = AddET0Method(language=self.language, data_to_input=self.method_dict)
        
    def delete_procedure(self):
        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.setText(self.language['eto_methods_widget_msg_delete'])
        self.msgBox.setWindowTitle(self.language['eto_methods_widget_msg_delete_title'])
        self.msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.buttonOK = self.msgBox.button(QMessageBox.Ok)
        self.buttonOK.setText(self.language['eto_methods_widget_msg_delete_yes'])
        self.buttonCancel = self.msgBox.button(QMessageBox.Cancel)
        self.buttonCancel.setText(self.language['eto_methods_widget_msg_delete_cancel'])
        self.msgBox.buttonClicked.connect(self.delete_method)
        returnValue = self.msgBox.exec()

    def delete_method(self, value):
        if value.text() == self.language['eto_methods_widget_msg_delete_yes']:
            self.get_list_of_files = next(os.walk(cwd + var.eto_methods_folder), (None, None, []))[2]
            for self.file_to_delete in self.get_list_of_files:
                self.path_to_file_to_delete = open(os.path.join(cwd + var.eto_methods_folder + self.file_to_delete))
                self.data_of_file_to_delete = json.load(self.path_to_file_to_delete)
                if self.list_widget.currentItem().text() == self.data_of_file_to_delete['name']:
                    os.remove(os.path.join(cwd + var.eto_methods_folder + self.file_to_delete))
            self.refresh_methods_list_after_deletion()
            
    def refresh_methods_list_after_deletion(self):
        self.item_to_remove = self.list_widget.selectedItems()
        if not self.item_to_remove: return
        for item in self.item_to_remove:
            self.list_widget.takeItem(self.list_widget.row(item))
 
    
    def create_method_info(self):
        self.method_info_groupbox = QGroupBox(self.language['eto_methods_widget_list'])
        
        self.text_method_name = QLabel(self.language['add_wb_method_info_name'])
        self.method_name = QLineEdit()
        
        self.text_method_short_name = QLabel(self.language['add_wb_method_info_unit'])
        self.method_short_name = QLineEdit()
        
        self.text_method_symbol = QLabel(self.language['add_wb_method_info_symbol'])
        self.method_symbol = QLineEdit()
        
        self.text_method_description = QLabel(self.language['add_wb_method_info_description'])
        self.method_description = QTextEdit()
        
        self.text_method_conditions = QLabel(self.language['add_wb_method_info_conditions'])
        self.method_conditions = QTextEdit()
        
        self.text_method_formula = QLabel(self.language['add_wb_method_info_formula'])
        self.method_formula = QTextEdit()
        
        self.text_basic_parameters = QLabel(self.language['add_wb_method_info_bp'])
        self.text_complex_parameters = QLabel(self.language['add_wb_method_info_cp'])
        self.text_om = QLabel(self.language['add_wb_method_info_om'])
        
        self.text_bp_selected = QLabel(self.language['add_wb_method_info_bp_s'])
        self.selected_bp_list = QLabel()
        
        self.text_cp_selected = QLabel(self.language['add_wb_method_info_cp_s'])
        self.selected_cp_list = QLabel()

        self.text_om_selected = QLabel(self.language['add_wb_method_info_om_s'])
        self.selected_om_list = QLabel()
        
        self.btn_save_method_changes = QPushButton(self.language['eto_methods_widget_btn_save_changes'])
        self.btn_save_method_changes.clicked.connect(self.save_changes_method)

        self.btn_cancel_method_changes = QPushButton(self.language['eto_methods_widget_btn_cancel_changes'])
        self.btn_cancel_method_changes.clicked.connect(self.cancel_changes_method)

        self.method_info_groupbox.layout = QGridLayout()

        self.method_info_groupbox.layout.addWidget(self.text_method_name, 0, 0, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.method_name, 1, 0, 1, 1)

        self.method_info_groupbox.layout.addWidget(self.text_method_short_name, 0, 1, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.method_short_name, 1, 1, 1, 1)

        self.method_info_groupbox.layout.addWidget(self.text_method_symbol, 0, 2, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.method_symbol, 1, 2, 1, 1)

        self.method_info_groupbox.layout.addWidget(self.text_method_description, 2, 0, 1, 2)
        self.method_info_groupbox.layout.addWidget(self.method_description, 3, 0, 1, 2)

        self.method_info_groupbox.layout.addWidget(self.text_method_conditions, 2, 2, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.method_conditions, 3, 2, 1, 1)

        self.method_info_groupbox.layout.addWidget(self.text_method_formula, 4, 0, 1, 3)
        self.method_info_groupbox.layout.addWidget(self.method_formula, 5, 0, 1, 3)

        self.method_info_groupbox.layout.addWidget(self.text_basic_parameters, 6, 0, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.basic_parameters_groupbox(), 7, 0, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.text_bp_selected, 8, 0, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.selected_bp_list, 9, 0, 1, 1)

        self.method_info_groupbox.layout.addWidget(self.text_complex_parameters, 6, 1, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.changable_parameters_groupbox(), 7, 1, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.text_cp_selected, 8, 1, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.selected_cp_list, 9, 1, 1, 1)

        self.method_info_groupbox.layout.addWidget(self.text_om, 6, 2, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.om_groupbox(), 7, 2, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.text_om_selected, 8, 2, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.selected_om_list, 9, 2, 1, 1)

        self.method_info_groupbox.layout.addWidget(self.btn_save_method_changes, 10, 0, 1, 3)
        self.method_info_groupbox.layout.addWidget(self.btn_cancel_method_changes, 11, 0, 1, 3)

        self.method_info_groupbox.setLayout(self.method_info_groupbox.layout)
        return self.method_info_groupbox
    
    def save_changes_method(self):
        self.get_files = next(os.walk(cwd + var.eto_methods_folder), (None, None, []))[2]
        for file in self.get_files:
            self.file_to_read = open(os.path.join(cwd + var.eto_methods_folder + file))
            self.file_data = json.load(self.file_to_read)
            if self.method_name.text() == self.file_data['name']:
                self.file_to_load = file
        if not self.method_name.text() or not self.method_short_name.text() or not self.method_symbol.text() or not self.method_formula.toPlainText() or not self.selected_bp_list.text():
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['add_wb_method_msg_missing'])
            self.msg.setWindowTitle(self.language['add_wb_method_msg_missing_title'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            parameter_dict = {
                    "name": self.method_name.text(),
                    "unit": self.method_short_name.text(),
                    "symbol": self.method_symbol.text(),
                    "description": self.method_description.toPlainText(),
                    "method_conditions": self.method_conditions.toPlainText(),
                    "method_formula": self.method_formula.toPlainText(),
                    "basic_parameters": self.selected_bp_list.text(),
                    "changable_parameters": self.selected_cp_list.text(),
                    "other_methods": self.selected_om_list.text(),
                    "type": "a"
                    }
            json_object = json.dumps(parameter_dict, indent = 4)
            with open(cwd + var.eto_methods_folder + self.file_to_load, "w") as outfile:
                outfile.write(json_object)
                
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['add_wb_method_msg_saved'])
            self.msg.setWindowTitle(self.language['add_wb_method_msg_saved_title'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.show()
        
    def cancel_changes_method(self):
        self.json_path = cwd + var.eto_methods_folder + self.file_to_load
        with open(self.json_path) as json_file:
            data = json.load(json_file)
        self.method_name.setText(data['name'])
        self.method_short_name.setText(data['unit'])
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
        
        self.selected_cp_list.setText(data['changable_parameters'])
        self.cp_list_to_update = data['changable_parameters'].split(', ')
        for self.cp_check in range(self.cp_layout.count()):
            self.cp_check_widget = self.cp_layout.itemAt(self.cp_check).widget()
            self.cp_check_widget.setChecked(False)
            if self.cp_check_widget.text() in self.cp_list_to_update: self.cp_check_widget.setChecked(True)

        self.selected_om_list.setText(data['other_methods'])
        self.om_list_to_update = data['other_methods'].split(', ')
        for self.om_check in range(self.om_layout.count()):
            self.om_check_widget = self.om_layout.itemAt(self.om_check).widget()
            self.om_check_widget.setChecked(False)
            if self.om_check_widget.text() in self.om_list_to_update: self.om_check_widget.setChecked(True)


    def basic_parameters_groupbox(self):
        self.bp_groupbox = QGroupBox()
        self.bp_layout = QGridLayout()
        self.bp_scroll = QWidget()
        self.bp_check_list, self.rows, self.columns = read_bp()
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
            
    def changable_parameters_groupbox(self):
        self.cp_groupbox = QGroupBox()
        self.cp_layout = QGridLayout()
        self.cp_scroll = QWidget()
        self.cp_check_list, self.rows, self.columns = read_cp()
        i = 0
        for row in range(self.rows):
            for column in range(self.columns):
                self.cp_check = QCheckBox(f'{self.cp_check_list[i]}', self)
                
                self.setStyleSheet('''QToolTip {min-width: 300px;}''')
                self.get_files = next(os.walk(cwd + var.changable_parameters_folder), (None, None, []))[2]
                for file in self.get_files:
                    self.file_to_read = open(os.path.join(cwd + var.changable_parameters_folder + file))
                    self.file_data = json.load(self.file_to_read)
                    if self.cp_check_list[i] == self.file_data['symbol']:
                        self.file_to_load = file
                self.json_path = cwd + var.changable_parameters_folder + self.file_to_load
                with open(self.json_path) as json_file:
                    tooltip_data = json.load(json_file)
                self.text = '<b>' + self.language['add_basic_parameter_window_name'] + '</b>' + tooltip_data['name'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_symbol'] + '</b>' + self.cp_check_list[i] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_category'] + '</b>' + tooltip_data['category'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_unit'] + '</b>' + tooltip_data['unit'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_desc'] + '</b>' + tooltip_data['description'] + \
                            '<b>' + self.language['input_cp_parameter_val'] + '</b>' + tooltip_data['value']
                self.cp_check.setToolTip(self.text)
                self.cp_check.clicked.connect(self.changable_parameter_checked)
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
    
    def changable_parameter_checked(self):
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

    def om_groupbox(self):
        self.om_groupboxx = QGroupBox()
        self.om_layout = QGridLayout()
        self.om_scroll = QWidget()
        self.om_check_list, self.rows, self.columns = read_om()
        i = 0
        for row in range(self.rows):
            for column in range(self.columns):
                self.om_check = QCheckBox(f'{self.om_check_list[i]}', self)
                self.setStyleSheet('''QToolTip {min-width: 300px;}''')
                self.get_files = next(os.walk(cwd + var.other_methods_folder), (None, None, []))[2]
                for file in self.get_files:
                    self.file_to_read = open(os.path.join(cwd + var.other_methods_folder + file))
                    self.file_data = json.load(self.file_to_read)
                    if self.om_check_list[i] == self.file_data['symbol']:
                        self.file_to_load = file
                self.json_path = cwd + var.other_methods_folder + self.file_to_load
                with open(self.json_path) as json_file:
                    tooltip_data = json.load(json_file)

                self.text = '<b>' + self.language['add_basic_parameter_window_name'] + '</b>' + tooltip_data['name'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_symbol'] + '</b>' + self.om_check_list[i] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_category'] + '</b>' + tooltip_data['category'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_unit'] + '</b>' + tooltip_data['unit'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_desc'] + '</b>' + tooltip_data['description'] 
                self.om_check.setToolTip(self.text)
                self.om_check.clicked.connect(self.om_checked)
                self.om_layout.addWidget(self.om_check, row+1, column)
                i += 1
                if i == len(self.om_check_list): break
        self.om_scroll.setLayout(self.om_layout)
        om = QScrollArea()
        om.setWidget(self.om_scroll)
        om.setWidgetResizable(1)
        self.om_groupboxx.layout = QVBoxLayout()
        self.om_groupboxx.layout.addWidget(om)
        self.om_groupboxx.setLayout(self.om_groupboxx.layout)
        return self.om_groupboxx
    
    def om_checked(self):
        if not self.selected_om_list.text():
            self.ompl = []
        else:
            self.ompl = self.selected_om_list.text().split(', ')
        if self.sender().checkState() == 2:
            self.ompl.append(self.sender().text())
            self.selected_om_list.setText(', '.join(self.ompl))
        else:
            self.ompl.remove(self.sender().text())
            self.selected_om_list.setText(', '.join(self.ompl))
            
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = ETOMethodsWidget()
    sys.exit(mainApplication.exec_())