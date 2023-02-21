import sys, os, json
cwd = os.path.curdir
from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel, QPushButton, QApplication
from PyQt5.QtWidgets import QLineEdit, QListWidget, QTextEdit, QMessageBox, QWidget, QScrollArea, QToolTip
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt
#from variables import var
import var
#from mortys.parameters_morty import read_characters, read_basic_parameters
from parameters_morty import read_characters, read_basic_parameters, read_complex_parameters
#from windows.parameters.complex_parameters_add import AddComplexParameter
from complex_parameters_add import AddComplexParameter
from language import language
from character_widget import InputCharacterWidget
from basic_parameters_insert_widget import InputBasicParameterNameWidget

class ParametersCategoryTabs(QWidget):
    def __init__(self):
        super().__init__()
        self.setUpdatesEnabled(True)
        self.language = language
        self.categories_tabs = QTabWidget()
        self.categories_file = open(os.path.join(cwd + var.language_folder + self.language['language_description'] + '/' + var.p_cat_file))
        self.categories_file_data = json.load(self.categories_file)
        self.categories_list = []
        for category in self.categories_file_data:
            self.categories_list.append(self.categories_file_data[category])
        for tabName in self.categories_list:
            self.category = list(self.categories_file_data.keys())[list(self.categories_file_data.values()).index(tabName)]
            self.tabWidget = QWidget()
            self.listWidget = ParametersWidget(self.category, self.language)
            self.tabLayout = QGridLayout()
            self.tabLayout.addWidget(self.listWidget)
            self.tabWidget.setLayout(self.tabLayout)
            self.categories_tabs.addTab(self.tabWidget, tabName)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.categories_tabs)
        self.setLayout(self.mainLayout)
        self.show()
 
class ParametersWidget(QWidget):
    def __init__(self, category, language):
        super().__init__()
        QApplication.instance().focusChanged.connect(self.on_focus_changed)
        self.category = category
        self.language = language
        self.get_files = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
        self.category_list = []
        for file in self.get_files:
            self.file_to_load = open(os.path.join(cwd + var.complex_parameters_folder + file))
            self.file_data = json.load(self.file_to_load)
            if self.category == self.file_data['category']:
                self.category_list.append(self.file_data['name'])
        self.grid = QGridLayout()
        self.grid.addWidget(self.create_list_widget(self.category_list), 0, 0, 2, 1)
        self.grid.addWidget(self.create_parameter_widget(), 0, 1, 2, 1)
        self.grid.addWidget(InputBasicParameterNameWidget(columns=3), 0, 2, 1, 1)
        self.grid.addWidget(InputBasicParameterNameWidget(columns=3), 1, 2, 1, 1)

        
        #self.grid.addWidget(self.special_character_groupbox(), 1, 0, 1, 1)
        #self.grid.addWidget(InputCharacterWidget(columns=5), 1, 0, 1, 1)
        #self.grid.addWidget(self.basic_parameters_groupbox(), 1, 1, 1, 1)
        #self.grid.addWidget(InputBasicParameterNameWidget(columns=5), 1, 1, 1, 1)
        self.setLayout(self.grid)
        
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
        
    def special_character_groupbox(self):
        self.sc_groupbox = QGroupBox(self.language['complex_parameters_widget_sc'])
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
        self.bp_groupbox = QGroupBox(self.language['complex_parameters_widget_bp'])
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
    
    def complex_parameters_groupbox_check(self):
        self.cpc_groupbox = QGroupBox('complex parameters:')
        self.cpc_layout = QGridLayout()
        self.cpc_scroll = QWidget()
        self.cpc_check_list, self.rows, self.columns = read_complex_parameters()
        i = 0
        for row in range(self.rows):
            for column in range(self.columns):
                self.cpc_check = QCheckBox(f'{self.cpc_check_list[i]}', self)
                
                self.setStyleSheet('''QToolTip {min-width: 300px;}''')
                self.get_files = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
                for file in self.get_files:
                    self.file_to_read = open(os.path.join(cwd + var.complex_parameters_folder + file))
                    self.file_data = json.load(self.file_to_read)
                    if self.cpc_check_list[i] == self.file_data['symbol']:
                        self.file_to_load = file
                self.json_path = cwd + var.complex_parameters_folder + self.file_to_load
                with open(self.json_path) as json_file:
                    tooltip_data = json.load(json_file)
                # dodati šta fali za parameter od polja
                self.text = '<b>' + self.language['add_basic_parameter_window_name'] + '</b>' + tooltip_data['name'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_symbol'] + '</b>' + self.cpc_check_list[i] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_category'] + '</b>' + tooltip_data['category'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_unit'] + '</b>' + tooltip_data['unit'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_desc'] + '</b>' + tooltip_data['description']
                self.cpc_check.setToolTip(self.text)
                
                self.cpc_check.clicked.connect(self.complex_parameter_checked)
                self.cpc_layout.addWidget(self.cpc_check, row+1, column)
                i += 1
                if i == len(self.cpc_check_list): break
        self.cpc_scroll.setLayout(self.cpc_layout)
        cpc = QScrollArea()
        cpc.setWidget(self.cpc_scroll)
        cpc.setWidgetResizable(1)
        self.cpc_groupbox.layout = QVBoxLayout()
        self.cpc_groupbox.layout.addWidget(cpc)
        self.cpc_groupbox.setLayout(self.cpc_groupbox.layout)
        return self.cpc_groupbox
    
    def complex_parameter_checked(self):
        if not self.selected_cp_list.text():
            self.bpl = []
        else:
            self.bpl = self.selected_cp_list.text().split(', ')
        if self.sender().checkState() == 2:
            self.bpl.append(self.sender().text())
            self.selected_cp_list.setText(', '.join(self.bpl))
        else:
            self.bpl.remove(self.sender().text())
            self.selected_cp_list.setText(', '.join(self.bpl))
    
    def frame_complex_groupbox(self):
        self.frame_groupbox = QGroupBox('complex parameters:')
        self.text_cp_selected = QLabel('selected')
        self.text_complex_parameters = QLabel('add_eto_method_info_bp')
        self.selected_cp_list = QLabel()
        self.frame_groupbox.layout = QGridLayout()
        self.frame_groupbox.layout.addWidget(self.text_complex_parameters, 0, 0)
        self.frame_groupbox.layout.addWidget(self.complex_parameters_groupbox_check(), 1, 0)
        self.frame_groupbox.layout.addWidget(self.text_cp_selected, 2, 0)
        self.frame_groupbox.layout.addWidget(self.selected_cp_list, 3, 0)
        self.frame_groupbox.setLayout(self.frame_groupbox.layout)
        return self.frame_groupbox
    
    def basic_parameters_groupbox_check(self):
        self.bpc_groupbox = QGroupBox()
        self.bpc_layout = QGridLayout()
        self.bpc_scroll = QWidget()
        self.bpc_check_list, self.rows, self.columns = read_basic_parameters()
        i = 0
        for row in range(self.rows):
            for column in range(self.columns):
                self.bpc_check = QCheckBox(f'{self.bpc_check_list[i]}', self)
                
                self.setStyleSheet('''QToolTip {min-width: 300px;}''')
                self.get_files = next(os.walk(cwd + var.basic_parameters_folder), (None, None, []))[2]
                for file in self.get_files:
                    self.file_to_read = open(os.path.join(cwd + var.basic_parameters_folder + file))
                    self.file_data = json.load(self.file_to_read)
                    if self.bpc_check_list[i] == self.file_data['symbol']:
                        self.file_to_load = file
                self.json_path = cwd + var.basic_parameters_folder + self.file_to_load
                with open(self.json_path) as json_file:
                    tooltip_data = json.load(json_file)
                # dodati šta fali za parameter od polja
                self.text = '<b>' + self.language['add_basic_parameter_window_name'] + '</b>' + tooltip_data['name'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_symbol'] + '</b>' + self.bpc_check_list[i] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_category'] + '</b>' + tooltip_data['category'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_unit'] + '</b>' + tooltip_data['unit'] + '<br>' + \
                            '<b>' + self.language['add_basic_parameter_window_desc'] + '</b>' + tooltip_data['description']
                self.bpc_check.setToolTip(self.text)
                
                self.bpc_check.clicked.connect(self.basic_parameter_checked)
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
            
    def create_list_widget(self, category_list):
        self.category_list = category_list
        self.groupBox = QGroupBox(self.language['complex_parameters_widget_caption'])
        self.list_widget = QListWidget()
        self.list_widget.addItems(self.category_list)
        self.list_widget.currentItemChanged.connect(self.index_changed)
        self.buttonAddcomplexParameter = QPushButton(self.language['complex_parameters_widget_btn_add_new'])
        self.buttonAddcomplexParameter.clicked.connect(self.new_parameter_window)
        self.buttonDelete = QPushButton(self.language['complex_parameters_widget_btn_delete'])
        self.buttonDelete.clicked.connect(self.delete_procedure)
        self.buttonDelete.setEnabled(False)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(InputCharacterWidget(columns=5))
        self.layout.addWidget(self.buttonAddcomplexParameter)
        self.layout.addWidget(self.buttonDelete)
        self.groupBox.setLayout(self.layout)
        return self.groupBox

    def index_changed(self, i):
        self.get_files = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
        for file in self.get_files:
            self.file_to_read = open(os.path.join(cwd + var.complex_parameters_folder + file))
            self.file_data = json.load(self.file_to_read)
            if i.text() == self.file_data['name']:
                self.file_to_load = file
                self.kategorija = self.file_data['category']
        self.json_path = cwd + var.complex_parameters_folder + self.file_to_load
        with open(self.json_path) as json_file:
            data = json.load(json_file)
            if data['type'] == 'b':
                self.update_labels(
                    state=False, 
                    name=data['name'], 
                    symbol=data['symbol'], 
                    unit=data['unit'],
                    bp = data['basic_parameters'],
                    cp = data['complex_parameters'], 
                    description=data['description'], 
                    formula=data['formula'],
                    change='b')
                
            else:
                self.update_labels(
                    state=True, 
                    name=data['name'], 
                    symbol=data['symbol'], 
                    unit=data['unit'],
                    bp = data['basic_parameters'],
                    cp = data['complex_parameters'],
                    description=data['description'], 
                    formula=data['formula'],
                    change=data['changable'])

    def new_parameter_window(self):
        self.window = AddComplexParameter()
        
    def delete_procedure(self):
        self.msgBox = QMessageBox()
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.setText(self.language['complex_parameters_widget_delete_msg_title'])
        self.msgBox.setWindowTitle(self.language['complex_parameters_widget_delete_msg_message'])
        self.msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.buttonOK = self.msgBox.button(QMessageBox.Ok)
        self.buttonOK.setText(self.language['complex_parameters_widget_delete_msg_yes'])
        self.buttonCancel = self.msgBox.button(QMessageBox.Cancel)
        self.buttonCancel.setText(self.language['complex_parameters_widget_delete_msg_cancel'])
        self.msgBox.buttonClicked.connect(self.delete_parameter)
        returnValue = self.msgBox.exec()

    def delete_parameter(self, value):
        if value.text() == self.language['complex_parameters_widget_delete_msg_yes']:
            self.get_list_of_files = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
            for self.file_to_delete in self.get_list_of_files:
                self.path_to_file_to_delete = open(os.path.join(cwd + var.complex_parameters_folder + self.file_to_delete))
                self.data_of_file_to_delete = json.load(self.path_to_file_to_delete)
                if self.list_widget.currentItem().text() == self.data_of_file_to_delete['name']:
                    os.remove(os.path.join(cwd + var.complex_parameters_folder + self.file_to_delete))
            self.refresh_parameters_list_after_deletion()
            
    def refresh_parameters_list_after_deletion(self):
        self.item_to_remove = self.list_widget.selectedItems()
        if not self.item_to_remove: return
        for item in self.item_to_remove:
            self.list_widget.takeItem(self.list_widget.row(item))
        
    def create_parameter_widget(self):
        self.groupBox = QGroupBox(self.language['complex_parameters_widget_parameter_caption'])
        self.text_parameter_name = QLabel(self.language['complex_parameters_widget_parameter_name'])
        self.parameter_name = QLineEdit()
        self.text_parameter_symbol = QLabel(self.language['complex_parameters_widget_parameter_symbol'])
        self.parameter_symbol = QLineEdit()
        self.text_parameter_unit = QLabel(self.language['complex_parameters_widget_parameter_unit'])
        self.parameter_unit = QLineEdit()
        self.text_parameter_formula = QLabel(self.language['complex_parameters_widget_parameter_formula'])
        self.parameter_formula = QTextEdit()
        self.text_parameter_descriprion = QLabel(self.language['complex_parameters_widget_parameter_desc'])
        self.parameter_descriprion = QTextEdit()
        self.buttonSave = QPushButton(self.language['complex_parameters_widget_parameter_btn_save'])
        self.buttonSave.clicked.connect(self.save_changes_parameter)
        self.buttonCancel = QPushButton(self.language['complex_parameters_widget_parameter_btn_cancel'])
        self.buttonCancel.clicked.connect(self.cancel)
        self.buttonCancel.setEnabled(False)
        self.layout = QGridLayout()
        self.layout.addWidget(self.text_parameter_name, 0, 0, 1, 1)
        self.layout.addWidget(self.parameter_name, 1, 0, 1, 1)
        self.layout.addWidget(self.text_parameter_symbol, 0, 1, 1, 1)
        self.layout.addWidget(self.parameter_symbol, 1, 1, 1, 1)
        self.layout.addWidget(self.text_parameter_unit, 2, 0, 1, 1)
        self.layout.addWidget(self.parameter_unit, 3, 0, 1, 1)
        self.layout.addWidget(self.pb_changable_groupbox(), 2, 1, 2, 1)
        self.layout.addWidget(self.text_parameter_descriprion, 4, 0, 1, 1)
        self.layout.addWidget(self.parameter_descriprion, 5, 0, 1, 1)
        self.layout.addWidget(self.text_parameter_formula, 4, 1, 1, 1)
        self.layout.addWidget(self.parameter_formula, 5, 1, 1, 1)
        self.layout.addWidget(self.frame_groupbox(), 6, 0, 1, 1)
        self.layout.addWidget(self.frame_complex_groupbox(), 6, 1, 1, 1)
        self.layout.addWidget(self.buttonSave, 7, 0, 1, 2)
        self.layout.addWidget(self.buttonCancel, 8, 0, 1, 2)
        self.groupBox.setLayout(self.layout)
        return self.groupBox
    
    def pb_changable_groupbox(self):
        self.chd_gruopbox = QGroupBox(self.language['add_complex_parameter_window_change_caption'])
        self.changable_check = QCheckBox(self.language['add_complex_parameter_window_change'])
        self.chd_gruopbox.layout = QVBoxLayout()
        self.chd_gruopbox.layout.addWidget(self.changable_check)
        self.chd_gruopbox.setLayout(self.chd_gruopbox.layout)
        return self.chd_gruopbox

    def update_labels(self, name, bp, cp, state, symbol, unit, description, formula, change):
        self.parameter_name.setText(name)
        self.parameter_name.setEnabled(state)
        self.parameter_symbol.setText(symbol)
        self.parameter_symbol.setEnabled(state)
        self.parameter_unit.setText(unit)
        self.parameter_unit.setEnabled(state)
        self.parameter_formula.setText(formula)
        self.parameter_formula.setEnabled(state)
        self.parameter_descriprion.setText(description)
        self.parameter_descriprion.setEnabled(state)
        self.buttonSave.setEnabled(state)
        self.buttonDelete.setEnabled(state)
        self.buttonCancel.setEnabled(state)
        #self.bp_groupbox.setEnabled(state)
        self.selected_bp_list.setText(bp)
        self.bpc_list_to_update = bp.split(', ')
        for self.bpc_check in range(self.bpc_layout.count()):
            self.bpc_check_widget = self.bpc_layout.itemAt(self.bpc_check).widget()
            self.bpc_check_widget.setChecked(False)
            if self.bpc_check_widget.text() in self.bpc_list_to_update: self.bpc_check_widget.setChecked(True)
            
        self.selected_cp_list.setText(cp)
        self.cpc_list_to_update = cp.split(', ')
        for self.cpc_check in range(self.cpc_layout.count()):
            self.cpc_check_widget = self.cpc_layout.itemAt(self.cpc_check).widget()
            self.cpc_check_widget.setChecked(False)
            if self.cpc_check_widget.text() in self.cpc_list_to_update: self.cpc_check_widget.setChecked(True)
            
        if change == 'b':
            self.changable_check.setEnabled(False)
        elif change == 'yes':
            self.get_files = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
            self.files =[]
            for file in self.get_files:
                if self.file_data['changable'] == 'yes' and name==self.file_data['name']:
                    self.file_to_read = open(os.path.join(cwd + var.complex_parameters_folder + file))
                self.changable_check.setEnabled(True)
                self.changable_check.setChecked(True)
        else:
            self.changable_check.setEnabled(True)
            self.changable_check.setChecked(False)

    def save_changes_parameter(self):
        self.get_files = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
        if self.changable_check.checkState() == 2:
            self.change_write = 'yes'
        else:
            self.change_write = 'no'
            
        for file in self.get_files:
            self.file_to_read = open(os.path.join(cwd + var.complex_parameters_folder + file))
            self.file_data = json.load(self.file_to_read)
            if self.parameter_name.text() == self.file_data['name']:
                self.file_to_load = file
        if not self.file_to_load or not self.parameter_name.text() or not self.parameter_symbol.text():
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['complex_parameters_widget_save_changes_message'])
            self.msg.setWindowTitle(self.language['complex_parameters_widget_save_changes_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            parameter_dict = {
                "name": self.parameter_name.text(),
                "symbol": self.parameter_symbol.text(),
                "category": self.kategorija,
                "basic_parameters": self.selected_bp_list.text(),
                "complex_parameters": self.selected_cp_list.text(),
                "unit": self.parameter_unit.text(),
                "changable": self.change_write,
                "description": self.parameter_descriprion.toPlainText(),
                "formula": self.parameter_formula.toPlainText(),
                "type": "a"
                }
            json_object = json.dumps(parameter_dict, indent = 4)
            with open(cwd + var.complex_parameters_folder + self.file_to_load, "w") as outfile:
                outfile.write(json_object)
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['complex_parameters_widget_save_message'])
            self.msg.setWindowTitle(self.language['complex_parameters_widget_save_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.show()

    def cancel(self):
        self.get_files = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
        for file in self.get_files:
            self.file_to_read = open(os.path.join(cwd + var.complex_parameters_folder + file))
            self.file_data = json.load(self.file_to_read)
            if self.parameter_name.text() == self.file_data['name']:
                self.file_to_load = file
        self.json_path = cwd + var.complex_parameters_folder + self.file_to_load
        with open(self.json_path) as json_file:
            data = json.load(json_file)
        self.parameter_name.setText(data['name'])
        self.parameter_symbol.setText(data['symbol'])
        self.parameter_unit.setText(data['unit'])
        self.parameter_descriprion.setText(data['description'])
        self.parameter_formula.setText(data['formula'])
        self.selected_bp_list.setText(data['basic_parameters'])
        self.bp_list_to_update = data['basic_parameters'].split(', ')
        for self.bpc_check in range(self.bpc_layout.count()):
            self.bpc_check_widget = self.bpc_layout.itemAt(self.bpc_check).widget()
            self.bpc_check_widget.setChecked(False)
            if self.bpc_check_widget.text() in self.bp_list_to_update: self.bpc_check_widget.setChecked(True)
        
        self.selected_cp_list.setText(data['complex_parameters'])
        self.cp_list_to_update = data['complex_parameters'].split(', ')
        for self.cpc_check in range(self.cpc_layout.count()):
            self.cpc_check_widget = self.cpc_layout.itemAt(self.cpc_check).widget()
            self.cpc_check_widget.setChecked(False)
            if self.cpc_check_widget.text() in self.cp_list_to_update: self.cpc_check_widget.setChecked(True)
        
if __name__ == '__main__':
   mainApplication = QApplication(sys.argv)
   mainWindow = ParametersCategoryTabs()
   sys.exit(mainApplication.exec_())