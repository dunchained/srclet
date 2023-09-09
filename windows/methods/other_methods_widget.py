import os, sys, json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QListWidget, QTextEdit, QMessageBox, QWidget, QCheckBox, QScrollArea
from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel, QPushButton, QApplication
cwd = os.path.curdir
from widgets.ch_widget import InputCharacterWidget
from widgets.bp_widget import BasicParameterWidget
from widgets.cp_widget import ChangableParameterWidget
from widgets.om_widget import OtherMethodsWidget
from windows.methods.other_methods_add import AddOtherMethod
from mortys.methods_morty import read_bp, read_cp, read_om
from variables import var

class OtherMethodCategoryTabs(QWidget):
    def __init__(self, language):
        super().__init__()
        self.setUpdatesEnabled(True)
        self.language = language
        self.tab_widget()
        self.show()

    def tab_widget(self):
        self.categories_tabs = QTabWidget()
        self.categories_file = open(os.path.join(cwd + var.language_folder + self.language['language_description'] + '/' + var.om_cat_file))
        self.categories_file_data = json.load(self.categories_file)
        self.categories_list = []
        for category in self.categories_file_data:
            self.categories_list.append(self.categories_file_data[category])
        for tabName in self.categories_list:
            self.category = list(self.categories_file_data.keys())[
                list(self.categories_file_data.values()).index(tabName)]
            self.tabWidget = QWidget()
            self.listWidget = OtherMethodWidget(self.category, self.language)
            self.tabLayout = QGridLayout()
            self.tabLayout.addWidget(self.listWidget)
            self.tabWidget.setLayout(self.tabLayout)
            self.categories_tabs.addTab(self.tabWidget, tabName)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.categories_tabs)
        self.setLayout(self.mainLayout)

class OtherMethodWidget(QWidget):
    def __init__(self, category, language):
        super().__init__()
        self.category = category
        self.language = language
        self.get_files = next(
            os.walk(cwd + var.other_methods_folder), (None, None, []))[2]
        self.category_list = []
        for file in self.get_files:
            self.file_to_load = open(os.path.join(cwd + var.other_methods_folder + file))
            self.file_data = json.load(self.file_to_load)
            if self.category == self.file_data['category']:
                self.category_list.append(self.file_data['name'])
        self.grid = QGridLayout()
        self.grid.addWidget(self.create_list_widget(self.category_list), 0, 0, 3, 1)
        self.grid.addWidget(self.create_parameter_widget(), 0, 1, 3, 1)
        self.grid.addWidget(BasicParameterWidget(language=language, title=self.language['add_other_method_inserts_bp'], columns=2), 0, 2, 1, 1)
        self.grid.addWidget(ChangableParameterWidget(language=language, title=self.language['add_other_method_inserts_cp'], columns=2), 0, 3, 1, 1)
        self.grid.addWidget(OtherMethodsWidget(language=language, title=self.language['add_other_method_inserts_om'], columns=2), 2, 2, 1, 1)
        self.grid.addWidget(InputCharacterWidget(language=language, title=self.language['add_other_method_inserts_sc'], columns=2), 2, 3, 1, 1)

        self.setLayout(self.grid)

    def create_list_widget(self, category_list):
        self.category_list = category_list
        self.groupBox = QGroupBox(self.language['other_methods_widget_caption'])
        self.list_widget = QListWidget()
        self.list_widget.addItems(self.category_list)
        self.list_widget.currentItemChanged.connect(self.index_changed)

        self.buttonAddBasicParameter = QPushButton(self.language['other_methods_widget_btn_add_new'])
        self.buttonAddBasicParameter.clicked.connect(self.new_om_window)

        self.buttonAddBasicParameterInherit = QPushButton(self.language['other_methods_widget_btn_add_new_inherit'])
        self.buttonAddBasicParameterInherit.setEnabled(False)
        self.buttonAddBasicParameterInherit.clicked.connect(self.new_om_window_inherit)

        self.buttonDelete = QPushButton(self.language['other_methods_widget_btn_delete'])
        self.buttonDelete.clicked.connect(self.delete_procedure)
        self.buttonDelete.setEnabled(False)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.buttonAddBasicParameter)
        self.layout.addWidget(self.buttonAddBasicParameterInherit)
        self.layout.addWidget(self.buttonDelete)
        self.groupBox.setLayout(self.layout)
        return self.groupBox

    def index_changed(self, i):
        self.get_files = next(os.walk(cwd + var.other_methods_folder), (None, None, []))[2]
        for file in self.get_files:
            self.file_to_read = open(os.path.join(cwd + var.other_methods_folder + file))
            self.file_data = json.load(self.file_to_read)
            if i.text() == self.file_data['name']:
                self.file_to_load = file
                self.kategorija = self.file_data['category']
        self.json_path = cwd + var.other_methods_folder + self.file_to_load
        with open(self.json_path) as json_file:
            data = json.load(json_file)
            if data['type'] == 'b':
                self.update_labels(state=False,
                                   name=data['name'],
                                   symbol=data['symbol'],
                                   unit=data['unit'],
                                   description=data['description'],
                                   conditions=data['method_conditions'],
                                   formula=data['method_formula'],
                                   bps=data['basic_parameters'],
                                   cps=data['changable_parameters'],
                                   oms=data['other_methods'])
                self.method_dict = {
                                    "name": data['name'] + self.language['other_methods_new_addition'],
                                    "symbol": data['symbol'],
                                    "category": data['category'],
                                    "unit": data['unit'],
                                    "description": data['description'] + self.language['other_methods_new_addition'],
                                    "method_conditions": data['method_conditions'],
                                    "method_formula": data['method_formula'],
                                    "basic_parameters": data['basic_parameters'],
                                    "changable_parameters": data['changable_parameters'],
                                    "other_methods": data['other_methods'],
                                    "type": "a"
                                }
                self.buttonAddBasicParameterInherit.setEnabled(True)

            else:
                self.update_labels(state=True,
                                   name=data['name'],
                                   symbol=data['symbol'],
                                   unit=data['unit'],
                                   description=data['description'],
                                   conditions=data['method_conditions'],
                                   formula=data['method_formula'],
                                   bps=data['basic_parameters'],
                                   cps=data['changable_parameters'],
                                   oms=data['other_methods'])
                self.method_dict = {
                                    "name": data['name'] + self.language['other_methods_new_addition'],
                                    "symbol": data['symbol'],
                                    "category": data['category'],
                                    "unit": data['unit'],
                                    "description": data['description'] + self.language['other_methods_new_addition'],
                                    "method_conditions": data['method_conditions'],
                                    "method_formula": data['method_formula'],
                                    "basic_parameters": data['basic_parameters'],
                                    "changable_parameters": data['changable_parameters'],
                                    "other_methods": data['other_methods'],
                                    "type": "a"
                                }
                self.buttonAddBasicParameterInherit.setEnabled(True)

    def new_om_window(self):
        self.window = AddOtherMethod(
            language=self.language, data_to_input=None)

    def new_om_window_inherit(self):
        self.window = AddOtherMethod(
            language=self.language, data_to_input=self.method_dict)

    def delete_procedure(self):
        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Information) 
        self.msgBox.setText(self.language['other_methods_widget_delete_msg_title'])
        self.msgBox.setWindowTitle(self.language['other_methods_widget_delete_msg_message'])
        self.msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.buttonOK = self.msgBox.button(QMessageBox.Ok)
        self.buttonOK.setText(self.language['other_methods_widget_delete_msg_yes'])
        self.buttonCancel = self.msgBox.button(QMessageBox.Cancel)
        self.buttonCancel.setText(self.language['other_methods_widget_delete_msg_cancel'])
        self.msgBox.buttonClicked.connect(self.delete_parameter)
        returnValue = self.msgBox.exec()

    def delete_parameter(self, value):
        if value.text() == self.language['other_methods_widget_delete_msg_yes']:
            self.get_list_of_files = next(os.walk(cwd + var.basic_parameters_folder), (None, None, []))[2]
            for self.file_to_delete in self.get_list_of_files:
                self.path_to_file_to_delete = open(os.path.join(cwd + var.basic_parameters_folder + self.file_to_delete))
                self.data_of_file_to_delete = json.load(self.path_to_file_to_delete)
                if self.list_widget.currentItem().text() == self.data_of_file_to_delete['name']:
                    os.remove(os.path.join(cwd + var.basic_parameters_folder + self.file_to_delete))
            self.refresh_parameters_list_after_deletion()

    def refresh_parameters_list_after_deletion(self):
        self.item_to_remove = self.list_widget.selectedItems()
        if not self.item_to_remove:
            return
        for item in self.item_to_remove:
            self.list_widget.takeItem(self.list_widget.row(item))

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

    def create_parameter_widget(self):
        self.method_info_groupbox = QGroupBox(self.language['add_other_method_info_caption'])
        
        self.text_method_name = QLabel(self.language['add_other_method_info_name'])
        self.method_name = QLineEdit()
        
        self.text_method_unit = QLabel(self.language['add_other_method_info_unit'])
        self.method_unit = QLineEdit()

        self.text_method_symbol = QLabel(self.language['add_other_method_info_symbol'])
        self.method_symbol = QLineEdit()

        self.text_method_description = QLabel(self.language['add_other_method_info_description'])
        self.method_description = QTextEdit()

        self.text_method_conditions = QLabel(self.language['add_other_method_info_conditions'])
        self.method_conditions = QTextEdit()

        self.text_method_formula = QLabel(self.language['add_other_method_info_formula'])
        self.method_formula = QTextEdit()

        self.text_basic_parameters = QLabel(self.language['add_other_method_info_bp'])

        self.text_changable_parameters = QLabel(self.language['add_other_method_info_cp'])
        
        self.text_om_parameters = QLabel(self.language['add_other_method_info_om'])

        self.text_bp_selected = QLabel(self.language['add_other_method_info_bp_s'])
        self.selected_bp_list = QLabel()

        self.text_cp_selected = QLabel(self.language['add_other_method_info_cp_s'])
        self.selected_cp_list = QLabel()

        self.text_om_selected = QLabel(self.language['add_other_method_info_om_s'])
        self.selected_om_list = QLabel()
        
        self.buttonSave = QPushButton(self.language['other_methods_widget_parameter_btn_save_changes'])
        self.buttonSave.clicked.connect(self.save_changes_parameter)
        
        self.buttonCancel = QPushButton(self.language['other_methods_widget_parameter_btn_cancel_changes'])
        self.buttonCancel.clicked.connect(self.cancel)
        self.buttonCancel.setEnabled(False)
        
        self.layout = QGridLayout()
        self.layout.addWidget(self.text_method_name, 0, 0, 1, 1)
        self.layout.addWidget(self.method_name, 1, 0, 1, 1)

        self.layout.addWidget(self.text_method_unit, 0, 1, 1, 1)
        self.layout.addWidget(self.method_unit, 1, 1, 1, 1)

        self.layout.addWidget(self.text_method_symbol, 0, 2, 1, 1)
        self.layout.addWidget(self.method_symbol, 1, 2, 1, 1)

        self.layout.addWidget(self.text_method_description, 2, 0, 1, 2)
        self.layout.addWidget(self.method_description, 3, 0, 1, 2)

        self.layout.addWidget(self.text_method_conditions, 2, 2, 1, 1)
        self.layout.addWidget(self.method_conditions, 3, 2, 1, 1)

        self.layout.addWidget(self.text_method_formula, 4, 0, 1, 3)
        self.layout.addWidget(self.method_formula, 5, 0, 1, 3)

        self.layout.addWidget(self.text_basic_parameters, 6, 0, 1, 1)
        self.layout.addWidget(self.basic_parameters_groupbox(), 7, 0, 1, 1)

        self.layout.addWidget(self.text_changable_parameters, 6, 1, 1, 1)
        self.layout.addWidget(self.changable_parameters_groupbox(), 7, 1, 1, 1)

        self.layout.addWidget(self.text_om_parameters, 6, 2, 1, 1)
        self.layout.addWidget(self.om_groupbox(), 7, 2, 1, 1)

        self.layout.addWidget(self.text_bp_selected, 8, 0, 1, 1)
        self.layout.addWidget(self.selected_bp_list, 9, 0, 1, 1)

        self.layout.addWidget(self.text_cp_selected, 8, 1, 1, 1)
        self.layout.addWidget(self.selected_cp_list, 9, 1, 1, 1)

        self.layout.addWidget(self.text_om_selected, 8, 2, 1, 1)
        self.layout.addWidget(self.selected_om_list, 9, 2, 1, 1)
   
        self.layout.addWidget(self.buttonSave, 10, 0, 1, 3)
        self.layout.addWidget(self.buttonCancel, 11, 0, 1, 3)

        self.method_info_groupbox.setLayout(self.layout)
        return self.method_info_groupbox

    def update_labels(self, state, name, symbol, unit, description, conditions, formula, bps, cps, oms):
        self.method_name.setText(name)
        self.method_name.setEnabled(state)
        self.method_symbol.setText(symbol)
        self.method_symbol.setEnabled(state)
        self.method_unit.setText(unit)
        self.method_unit.setEnabled(state)
        self.method_description.setText(description)
        self.method_description.setEnabled(state)
        self.method_conditions.setPlainText(conditions)
        self.method_conditions.setEnabled(state)
        self.method_formula.setPlainText(formula)
        self.method_formula.setEnabled(state)
        self.selected_bp_list.setText(bps)
        self.bp_groupbox.setEnabled(state)
        self.bp_list_to_update = bps.split(', ')
        for self.bp_check in range(self.bp_layout.count()):
            self.bp_check_widget = self.bp_layout.itemAt(self.bp_check).widget()
            self.bp_check_widget.setChecked(False)
            if self.bp_check_widget.text() in self.bp_list_to_update: self.bp_check_widget.setChecked(True)
        self.selected_cp_list.setText(cps)
        self.cp_groupbox.setEnabled(state)
        self.cp_list_to_update = cps.split(', ')
        for self.cp_check in range(self.cp_layout.count()):
            self.cp_check_widget = self.cp_layout.itemAt(self.cp_check).widget()
            self.cp_check_widget.setChecked(False)
            if self.cp_check_widget.text() in self.cp_list_to_update: self.cp_check_widget.setChecked(True)
        self.selected_om_list.setText(oms)
        self.om_groupboxx.setEnabled(state)
        self.om_list_to_update = oms.split(', ')
        for self.om_check in range(self.om_layout.count()):
            self.om_check_widget = self.om_layout.itemAt(self.om_check).widget()
            self.om_check_widget.setChecked(False)
            if self.om_check_widget.text() in self.om_list_to_update: self.om_check_widget.setChecked(True)
        self.buttonSave.setEnabled(state)
        self.buttonDelete.setEnabled(state)
        self.buttonCancel.setEnabled(state)

    def save_changes_parameter(self):
        self.get_files = next(os.walk(cwd + var.other_methods_folder), (None, None, []))[2]
        for file in self.get_files:
            self.file_to_read = open(os.path.join(
                cwd + var.other_methods_folder + file))
            self.file_data = json.load(self.file_to_read)
            if self.method_name.text() == self.file_data['name']:
                self.file_to_load = file
                # self.kategorija = self.file_data['category']
        if not self.file_to_load or not self.method_name.text() or not self.method_symbol.text():
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['add_basic_parameter_window_save_message'])
            self.msg.setWindowTitle(self.language['add_basic_parameter_window_save_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            method_dicta = {
                "name": self.method_name.text(),
                "unit": self.method_unit.text(),
                "symbol": self.method_symbol.text(),
                "description": self.method_description.toPlainText(),
                "method_conditions": self.method_conditions.toPlainText(),
                "method_formula": self.method_formula.toPlainText(),
                "basic_parameters": self.selected_bp_list.text(),
                "changable_parameters": self.selected_cp_list.text(),
                "other_methods": self.selected_om_list.text(),
                "category": self.kategorija,
                "type": "a"
            }
            json_object = json.dumps(method_dicta, indent=4)
            with open(cwd + var.other_methods_folder + self.file_to_load, "w") as outfile:
                outfile.write(json_object)
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['add_basic_parameter_window_saved_message'])
            self.msg.setWindowTitle(self.language['add_basic_parameter_window_saved_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.show()

    def cancel(self):
        self.get_files = next(os.walk(cwd + var.other_methods_folder), (None, None, []))[2]
        for file in self.get_files:
            self.file_to_read = open(os.path.join(cwd + var.other_methods_folder + file))
            self.file_data = json.load(self.file_to_read)
            if self.method_name.text() == self.file_data['name']:
                self.file_to_load = file
        self.json_path = cwd + var.other_methods_folder + self.file_to_load
        with open(self.json_path) as json_file:
            data = json.load(json_file)
        self.method_name.setText(data['name'])
        self.method_symbol.setText(data['symbol'])
        self.method_unit.setText(data['unit'])
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


if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = OtherMethodCategoryTabs()
    sys.exit(mainApplication.exec_())
