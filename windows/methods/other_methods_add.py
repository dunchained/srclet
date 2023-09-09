import sys, os, json
cwd = os.path.curdir
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QHBoxLayout, QGridLayout, QGroupBox, QLabel, QPushButton
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QMessageBox, QWidget, QApplication, QCheckBox, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import css, var
from methods_morty import read_basic_parameters, get_filename, read_changable_parameters, read_om
from language import language

from bp_widget import BasicParameterWidget
from ch_widget import InputCharacterWidget
from cp_widget import ChangableParameterWidget
from om_widget import OtherMethodsWidget

class AddOtherMethod(QWidget):
    #def __init__(self, language, data_to_input):
    def __init__(self, data_to_input=None):
        super().__init__()
        self.language = language
        self.data_to_input = data_to_input
        QApplication.instance().focusChanged.connect(self.on_focus_changed)
        self.window_gui()

    def window_gui(self):
        font = self.font()
        font.setPointSize(14) # učitati font iz mortija
        self.setFont(font)
        self.setWindowState(Qt.WindowMaximized)
        self.setMinimumSize(1200, 600)
        self.setWindowTitle(self.language['add_other_method_window_title'])
        self.setWindowIcon(QIcon(css.methods_others_icon))
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
        self.methods_groupbox = QGroupBox(self.language['add_other_method_inserts'])
        self.methods_groupbox.layout = QGridLayout()
        self.methods_groupbox.layout.addWidget(BasicParameterWidget(language=self.language, title=self.language['add_other_method_inserts_bp'], columns=3), 0, 0, 1, 1)
        self.methods_groupbox.layout.addWidget(ChangableParameterWidget(language=self.language, title=self.language['add_other_method_inserts_cp'], columns=3), 0, 1, 1, 1)
        self.methods_groupbox.layout.addWidget(OtherMethodsWidget(language=self.language, title=self.language['add_other_method_inserts_om'], columns=3), 1, 0, 1, 1)
        self.methods_groupbox.layout.addWidget(InputCharacterWidget(language=self.language, title=self.language['add_other_method_inserts_sc'], columns=3), 1, 1, 1, 1)
        self.methods_groupbox.setLayout(self.methods_groupbox.layout)
        return self.methods_groupbox
            

    def left_groupbox(self):
        self.method_info_groupbox = QGroupBox(self.language['add_other_method_info_caption'])
        
        self.text_method_name = QLabel(self.language['add_other_method_info_name'])
        self.text_method_unit = QLabel(self.language['add_other_method_info_unit'])
        self.text_method_symbol = QLabel(self.language['add_other_method_info_symbol'])
        self.text_method_category = QLabel(self.language['add_other_method_info_category'])
        self.text_method_description = QLabel(self.language['add_other_method_info_description'])
        self.text_method_conditions = QLabel(self.language['add_other_method_info_conditions'])
        self.text_method_formula = QLabel(self.language['add_other_method_info_formula'])
        self.text_basic_parameters = QLabel(self.language['add_other_method_info_bp'])
        self.text_changable_parameters = QLabel(self.language['add_other_method_info_cp'])
        self.text_om_parameters = QLabel(self.language['add_other_method_info_om'])
        self.text_bp_selected = QLabel(self.language['add_other_method_info_bp_s'])
        self.text_cp_selected = QLabel(self.language['add_other_method_info_cp_s'])
        self.text_om_selected = QLabel(self.language['add_other_method_info_om_s'])

        if self.data_to_input == None:
            self.method_name = QLineEdit()
            self.method_unit = QLineEdit()
            self.method_symbol = QLineEdit()
            categories_file = open(os.path.join(cwd + var.language_folder + self.language['language_description'] + '/' + var.om_cat_file))
            self.categories_file_data = json.load(categories_file)
            self.categories_list = []
            for category in self.categories_file_data:
                self.categories_list.append(self.categories_file_data[category])
            self.category_combo = QComboBox()
            self.category_combo.addItems(self.categories_list)
            self.method_description = QTextEdit()
            self.method_conditions = QTextEdit()
            self.method_formula = QTextEdit()
            self.selected_bp_list = QLabel()
            self.selected_cp_list = QLabel()
            self.selected_om_list = QLabel()

        else:
            self.method_name = QLineEdit(self.data_to_input['name'])
            self.method_unit = QLineEdit(self.data_to_input['unit'])
            self.method_symbol = QLineEdit(self.data_to_input['symbol'])
            categories_file = open(os.path.join(cwd + var.language_folder + self.language['language_description'] + '/' + var.om_cat_file))
            self.categories_file_data = json.load(categories_file)
            self.categories_list = []
            for category in self.categories_file_data:
                self.categories_list.append(self.categories_file_data[category])
            self.category_combo = QComboBox()
            self.category_combo.addItems(self.categories_list)
            for category, category_val in self.categories_file_data.items():
                if self.data_to_input['category'] == category:
                    self.category_combo.setCurrentText(category_val)
            self.method_description = QTextEdit(self.data_to_input['description'])
            self.method_conditions = QTextEdit(self.data_to_input['method_conditions'])
            self.method_formula = QTextEdit(self.data_to_input['method_formula'])
            self.selected_bp_list = QLabel(self.data_to_input['basic_parameters'])
            self.selected_cp_list = QLabel(self.data_to_input['changable_parameters'])
            self.selected_om_list = QLabel(self.data_to_input['other_methods'])
     
        self.method_info_groupbox.layout = QGridLayout()

        self.method_info_groupbox.layout.addWidget(self.text_method_name, 0, 0, 1, 2)
        self.method_info_groupbox.layout.addWidget(self.method_name, 1, 0, 1, 2)

        self.method_info_groupbox.layout.addWidget(self.text_method_unit, 0, 2, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.method_unit, 1, 2, 1, 1)

        self.method_info_groupbox.layout.addWidget(self.text_method_symbol, 2, 0, 1, 2)
        self.method_info_groupbox.layout.addWidget(self.method_symbol, 3, 0, 1, 2)

        self.method_info_groupbox.layout.addWidget(self.text_method_category, 2, 2, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.category_combo, 3, 2, 1, 1)

        self.method_info_groupbox.layout.addWidget(self.text_method_description, 4, 0, 1, 2)
        self.method_info_groupbox.layout.addWidget(self.method_description, 5, 0, 1, 2)

        self.method_info_groupbox.layout.addWidget(self.text_method_conditions, 4, 2, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.method_conditions, 5, 2, 1, 1)

        self.method_info_groupbox.layout.addWidget(self.text_method_formula, 6, 0, 1, 3)
        self.method_info_groupbox.layout.addWidget(self.method_formula, 7, 0, 1, 3)

        self.method_info_groupbox.layout.addWidget(self.text_basic_parameters, 8, 0, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.basic_parameters_groupbox(), 9, 0, 1, 1)

        self.method_info_groupbox.layout.addWidget(self.text_changable_parameters, 8, 1, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.changable_parameters_groupbox(), 9, 1, 1, 1)

        self.method_info_groupbox.layout.addWidget(self.text_om_parameters, 8, 2, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.om_groupbox(), 9, 2, 1, 1)

        self.method_info_groupbox.layout.addWidget(self.text_bp_selected, 10, 0, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.selected_bp_list, 11, 0, 1, 1)

        self.method_info_groupbox.layout.addWidget(self.text_cp_selected, 10, 1, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.selected_cp_list, 11, 1, 1, 1)

        self.method_info_groupbox.layout.addWidget(self.text_om_selected, 10, 2, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.selected_om_list, 11, 2, 1, 1)

        self.method_info_groupbox.setLayout(self.method_info_groupbox.layout)
        return self.method_info_groupbox  
    
    def down_groupbox(self):
        self.btn_groupbox = QGroupBox()
        self.btn_save = QPushButton(self.language['add_other_method_btn_save'])
        self.btn_save.clicked.connect(self.add_method)
        self.btn_cancel = QPushButton(self.language['add_other_method_btn_close'])
        self.btn_cancel.clicked.connect(self.close)
        self.btn_groupbox.layout = QHBoxLayout()
        self.btn_groupbox.layout.addWidget(self.btn_save)
        self.btn_groupbox.layout.addWidget(self.btn_cancel)
        self.btn_groupbox.setLayout(self.btn_groupbox.layout)
        return self.btn_groupbox
    
    def add_method(self):
        self.file_name_to_save = get_filename('other')
        get_files = next(os.walk(cwd + var.other_methods_folder), (None, None, []))[2]
        self.file_list = []
        for file in get_files:
            self.file_to_read = open(os.path.join(cwd + var.other_methods_folder + file))
            self.file_data = json.load(self.file_to_read)
            if self.method_name.text() == self.file_data['name']:
                self.file_list.append(file)
                        
        if self.file_list:
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['add_other_method_msg_exists'])
            self.msg.setWindowTitle(self.language['add_other_method_msg_exists_title'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            if not self.method_name.text() or not self.method_unit.text() or not self.method_symbol.text() or not self.method_formula.toPlainText() or not self.selected_bp_list.text():
                self.msg = QMessageBox()
                self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText(self.language['add_other_method_msg_missing'])
                self.msg.setWindowTitle(self.language['add_other_method_msg_missing_title'])
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.buttonClicked.connect(self.msg.close)
                self.msg.show()
            else:
                parameter_dict = {
                    "name": self.method_name.text(),
                    "unit": self.method_unit.text(),
                    "symbol": self.method_symbol.text(),
                    "description": self.method_description.toPlainText(),
                    "method_conditions": self.method_conditions.toPlainText(),
                    "method_formula": self.method_formula.toPlainText(),
                    "basic_parameters": self.selected_bp_list.text(),
                    "changable_parameters": self.selected_cp_list.text(),
                    "other_methods": self.selected_om_list.text(),
                    "category": list(self.categories_file_data.keys())[list(self.categories_file_data.values()).index(self.category_combo.currentText())],
                    "type": "a"
                    }
                
                json_object = json.dumps(parameter_dict, indent = 4)
                with open(cwd + var.other_methods_folder + self.file_name_to_save + ".json", "w") as outfile:
                    outfile.write(json_object)
                self.msg = QMessageBox()
                self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText(self.language['add_other_method_msg_saved'])
                self.msg.setWindowTitle(self.language['add_other_method_msg_saved_title'])
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.buttonClicked.connect(self.message_box_success)
                self.msg.show()

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
                self.text = '<b>' + self.language['tooltips_bp_name'] + '</b>' + tooltip_data['name'] + '<br>' + \
                            '<b>' + self.language['tooltips_bp_symbol'] + '</b>' + self.bp_check_list[i] + '<br>' + \
                            '<b>' + self.language['tooltips_bp_unit'] + '</b>' + tooltip_data['unit'] + '<br>' + \
                            '<b>' + self.language['tooltips_bp_category'] + '</b>' + tooltip_data['category'] + '<br>' + \
                            '<b>' + self.language['tooltips_bp_desc'] + '</b>' + tooltip_data['description']
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
        if self.data_to_input == None:
            pass
        else:
            self.bp_list_to_update = self.selected_bp_list.text().split(', ')
            for self.bp_check in range(self.bp_layout.count()):
                self.bp_check_widget = self.bp_layout.itemAt(self.bp_check).widget()
                self.bp_check_widget.setChecked(False)
                if self.bp_check_widget.text() in self.bp_list_to_update: self.bp_check_widget.setChecked(True)
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
        self.cp_check_list, self.rows, self.columns = read_changable_parameters()
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
                self.text = '<b>' + self.language['tooltips_bp_name'] + '</b>' + tooltip_data['name'] + '<br>' + \
                            '<b>' + self.language['tooltips_cp_value'] + '</b>' + tooltip_data['value'] + '<br>' + \
                            '<b>' + self.language['tooltips_bp_symbol'] + '</b>' + self.cp_check_list[i] + '<br>' + \
                            '<b>' + self.language['tooltips_bp_unit'] + '</b>' + tooltip_data['unit'] + '<br>' + \
                            '<b>' + self.language['tooltips_bp_category'] + '</b>' + tooltip_data['category'] + '<br>' + \
                            '<b>' + self.language['tooltips_bp_desc'] + '</b>' + tooltip_data['description']
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
        if self.data_to_input == None:
            pass 
        else:
            self.cp_list_to_update = self.selected_cp_list.text().split(', ')
            for self.cp_check in range(self.cp_layout.count()):
                self.cp_check_widget = self.cp_layout.itemAt(self.cp_check).widget()
                self.cp_check_widget.setChecked(False)
                if self.cp_check_widget.text() in self.cp_list_to_update: self.cp_check_widget.setChecked(True)
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
                self.text = '<b>' + self.language['tooltips_om_name'] + '</b>' + tooltip_data['name'] + '<br>' + \
                            '<b>' + self.language['tooltips_om_symbol'] + '</b>' + self.om_check_list[i] + '<br>' + \
                            '<b>' + self.language['tooltips_om_unit'] + '</b>' + tooltip_data['unit'] + '<br>' + \
                            '<b>' + self.language['tooltips_om_mc'] + '</b>' + tooltip_data['method_conditions'] + '<br>' + \
                            '<b>' + self.language['tooltips_om_mf'] + '</b>' + tooltip_data['method_formula'] + '<br>' + \
                            '<b>' + self.language['tooltips_om_bps'] + '</b>' + tooltip_data['basic_parameters'] + '<br>' + \
                            '<b>' + self.language['tooltips_om_cps'] + '</b>' + tooltip_data['changable_parameters'] + '<br>' + \
                            '<b>' + self.language['tooltips_om_oms'] + '</b>' + tooltip_data['other_methods'] + '<br>' + \
                            '<b>' + self.language['tooltips_om_category'] + '</b>' + tooltip_data['category'] + '<br>' + \
                            '<b>' + self.language['tooltips_om_desc'] + '</b>' + tooltip_data['description'] 
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
        if self.data_to_input == None:
            pass
        else:
            self.om_list_to_update = self.selected_om_list.text().split(', ')
            for self.om_check in range(self.om_layout.count()):
                self.om_check_widget = self.om_layout.itemAt(self.om_check).widget()
                self.om_check_widget.setChecked(False)
                if self.om_check_widget.text() in self.om_list_to_update: self.om_check_widget.setChecked(True)
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
                
    def message_box_success(self):
        self.close()
            
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = AddOtherMethod()
    sys.exit(mainApplication.exec_())