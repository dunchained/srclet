import sys, os, json
cwd = os.path.curdir
from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel, QPushButton, QApplication
from PyQt5.QtWidgets import QLineEdit, QListWidget, QTextEdit, QMessageBox, QWidget, QScrollArea
from PyQt5.QtCore import Qt
#from variables import var
import var
#from mortys.parameters_morty import read_characters, read_basic_parameters
from parameters_morty import read_characters, read_basic_parameters
#from windows.parameters.complex_parameters_add import AddComplexParameter
from complex_parameters_add import AddComplexParameter
from language import language

class ParametersCategoryTabs(QWidget):
    def __init__(self):
        super().__init__()
        self.setUpdatesEnabled(True)
        self.language = language
        self.tab_widget()
        self.show()
 
    def tab_widget(self):
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
        self.grid.addWidget(self.create_list_widget(self.category_list), 0, 0, 1, 1)
        self.grid.addWidget(self.create_parameter_widget(), 0, 1, 1, 1)
        self.grid.addWidget(self.special_character_groupbox(), 1, 0, 1, 1)
        self.grid.addWidget(self.basic_parameters_groupbox(), 1, 1, 1, 1)
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
                    description=data['description'], 
                    formula=data['formula'])
            else:
                self.update_labels(
                    state=True, 
                    name=data['name'], 
                    symbol=data['symbol'], 
                    unit=data['unit'], 
                    description=data['description'], 
                    formula=data['formula'])

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
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_parameter_name)
        self.layout.addWidget(self.parameter_name)
        self.layout.addWidget(self.text_parameter_symbol)
        self.layout.addWidget(self.parameter_symbol)
        self.layout.addWidget(self.text_parameter_unit)
        self.layout.addWidget(self.parameter_unit)
        self.layout.addWidget(self.text_parameter_formula)
        self.layout.addWidget(self.parameter_formula)
        self.layout.addWidget(self.text_parameter_descriprion)
        self.layout.addWidget(self.parameter_descriprion)
        self.layout.addWidget(self.buttonSave)
        self.layout.addWidget(self.buttonCancel)
        self.groupBox.setLayout(self.layout)
        return self.groupBox

    def update_labels(self, name, state, symbol, unit, description, formula):
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

    def save_changes_parameter(self):
        self.get_files = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
        for file in self.get_files:
            self.file_to_read = open(os.path.join(cwd + var.complex_parameters_folder + file))
            self.file_data = json.load(self.file_to_read)
            if self.parameter_name.text() == self.file_data['name']:
                self.file_to_load = file
        if not self.file_to_load or not self.parameter_name.text() or not self.parameter_unit.text() or not self.parameter_symbol.text():
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
                "unit": self.parameter_unit.text(),
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
        
if __name__ == '__main__':
   mainApplication = QApplication(sys.argv)
   mainWindow = ParametersCategoryTabs()
   sys.exit(mainApplication.exec_())