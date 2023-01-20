# python standard modules
from concurrent.futures import process
from importlib.resources import path
import sys, os, json
from pathlib import Path
cwd = os.path.curdir

# app modules and windows
#from variables import css, var
#from windows.parameters.add_basic_parameter import AddParameter
from windows.parameters.basic_parameters_add import AddParameter
#from add_parameter import AddParameter
#from mortys.parameters_morty import read_parameter_categories_list
# pyqt5 modules
from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QHBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QListView, QPushButton, QApplication
from PyQt5.QtWidgets import QLineEdit, QListWidget, QTextEdit, QMessageBox, QWidget, QMainWindow, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

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

class ParametersWindow(QWidget):
    def __init__(self):
        super(ParametersWindow, self).__init__()
        self.language = {
                        "language_description": "en",
                         "//": "Parameters Window",
                        "parameters_window_title": "Parameters",
                        "parameters_window_caption": "List of available parameters in this category:",
                        "parameters_window_btn_add_new": "Add new parameter",
                        "parameters_window_btn_delete": "Delete selected parameter",
                        "parameters_window_parameter_caption": "Parameters information:",
                        "parameters_window_parameter_filename": "Filename:",
                        "parameters_window_parameter_name": "Parameter name:",
                        "parameters_window_parameter_symbol": "Parameter symbol:",
                        "parameters_window_parameter_unit": "Parameter unit:",
                        "parameters_window_parameter_desc": "Parameter description:",
                        "parameters_window_parameter_btn_save": "Save changes",
                        "parameters_window_parameter_btn_cancel": "Cancel changes",
                        "parameters_window_btn_close": "Close",
                        "parameters_window_save_changes_message": "Parameter name or unit empty...",
                        "parameters_window_save_changes_message_caption": "Missing data...",
                        "parameters_window_save_message": "Parameter saved...",
                        "parameters_window_save_message_caption": "Successuful..."
                         }
        #self.AddParameter = AddParameter()
        #self.AddParameter.hide()
        #self.AddParameter.clicked.connect(self.refresh_parameters_list)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.window_gui()

    def window_gui(self):
        #self.setFixedSize(800, 600)
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle(self.language['parameters_window_title'])
        #self.setWindowIcon(QIcon(css.menu_about_icon))
        self.grid = QGridLayout()
        self.central_widget = ParametersCategoryTabs(self.language)
        self.grid.addWidget(self.central_widget)
        #self.grid.addWidget(self.centralGroupBox())
        self.setLayout(self.grid)
        self.center_gui()
        self.show()
        
    def center_gui(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
            
    #def refresh_parameters_list(self):
        #get_files = next(os.walk(cwd + parameters_folder), (None, None, []))[2]
        #self.file_list_update = []
        #for file in get_files:
            #if Path(file).stem not in self.file_list:
                #self.file_list_update.append(Path(file).stem)
        #self.list_widget.addItems(self.file_list_update)

    #def delete_parameter(self):
        #list_items = self.list_widget.selectedItems()
        #if not list_items: return
        #for item in list_items:
            #self.list_widget.takeItem(self.list_widget.row(item))
        #os.remove(cwd + parameters_folder + item.text() + '.json')
    

    #def cancel(self):
        #self.json_path = cwd + parameters_folder + self.list_widget.currentItem().text() + '.json'
        #with open(self.json_path) as json_file:
            #data = json.load(json_file)
            
        #self.parameter_name.setText(data['name'])
        #self.parameter_symbol.setText(data['symbol'])
        #self.parameter_unit.setText(data['unit'])
        #self.parameter_descriprion.setText(data['description'])
    
    def newParameterWindow(self):
        self.AddParameter.show()

    def save_changes_parameter(self):
        if not self.parameter_filename and not self.parameter_name.text() and not self.parameter_unit.text():
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['parameters_window_save_changes_message'])
            self.msg.setWindowTitle(self.language['parameters_window_save_changes_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            parameter_dict = {
                "name": self.parameter_name.text(),
                "symbol": self.parameter_symbol.text(),
                "unit": self.parameter_unit.text(),
                "description": self.parameter_descriprion.toPlainText(),
                "type": "a"
                }
            json_object = json.dumps(parameter_dict, indent = 4)
            with open(cwd + parameters_folder + self.parameter_filename.text() + ".json", "w") as outfile:
                outfile.write(json_object)
                
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['parameters_window_save_message'])
            self.msg.setWindowTitle(self.language['parameters_window_save_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.show()

    def close_me(self):
        self.close()

class ParametersCategoryTabs(QDialog):
    def __init__(self, language):
        super().__init__()
        self.language = language
        self.tab_widget()
        self.show()

    def tab_widget(self):
        self.categories_tabs = QTabWidget()
        categoriess_file = 'parameter_types.json' ### import iz var
        categories_file = open(os.path.join(cwd + language_folder + self.language['language_description'] + '/' + categoriess_file))
        self.categories_file_data = json.load(categories_file)
        self.categories_list = []
        for category in self.categories_file_data:
            self.categories_list.append(self.categories_file_data[category])
        for tabName in self.categories_list:
            self.category = list(self.categories_file_data.keys())[list(self.categories_file_data.values()).index(tabName)]
            tabWidget = QWidget()
            listWidget = ParametersWidget(self.category, self.language)
            tabLayout = QGridLayout()
            tabLayout.addWidget(listWidget)
            tabWidget.setLayout(tabLayout)
            self.categories_tabs.addTab(tabWidget, tabName)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.categories_tabs)
        self.setLayout(mainLayout)

class ParametersWidget(QWidget):
    def __init__(self, category, language):
        super().__init__()
        self.category = category
        self.language = language
        self.get_files = next(os.walk(cwd + parameters_folder), (None, None, []))[2]
        self.category_list = []
        for file in self.get_files:
            self.file_to_load = open(os.path.join(cwd + parameters_folder + file))
            self.file_data = json.load(self.file_to_load)
            if self.category == self.file_data['category']:
                self.category_list.append(self.file_data['name'])
        self.grid = QGridLayout()
        self.grid.addWidget(self.create_list_widget(self.category_list), 0, 0, 1, 1)
        self.grid.addWidget(self.create_parameter_widget(), 0, 1, 1, 1)
        self.grid.addWidget(self.close_button(), 1, 0, 1, 2)
        self.setLayout(self.grid)

    def create_list_widget(self, category_list):
        self.category_list = category_list
        groupBox = QGroupBox(self.language['parameters_window_caption'])
        self.list_widget = QListWidget()
        self.list_widget.addItems(self.category_list)
        self.list_widget.currentItemChanged.connect(self.index_changed)

        self.buttonAddParameter = QPushButton(self.language['parameters_window_btn_add_new'])
        self.buttonAddParameter.clicked.connect(self.new_parameter_window)

        self.buttonDelete = QPushButton(self.language['parameters_window_btn_delete'])
        self.buttonDelete.clicked.connect(self.delete_parameter)

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.buttonAddParameter)
        layout.addWidget(self.buttonDelete)
        layout.addStretch(1)
        groupBox.setLayout(layout)
        return groupBox

    def index_changed(self, i):
        self.get_files = next(os.walk(cwd + parameters_folder), (None, None, []))[2]
        #self.file_to_load = ''
        for file in self.get_files:
            self.file_to_read = open(os.path.join(cwd + parameters_folder + file))
            self.file_data = json.load(self.file_to_read)
            if i.text() == self.file_data['name']:
                self.file_to_load = file
        self.json_path = cwd + parameters_folder + self.file_to_load
        with open(self.json_path) as json_file:
            data = json.load(json_file)
            if data['type'] == 'b':
                self.update_labels(state=False, name=data['name'], symbol=data['symbol'], unit=data['unit'], description=data['description'])
            else:
                self.update_labels(state=True, name=data['name'], symbol=data['symbol'], unit=data['unit'], description=data['description'])

    def new_parameter_window(self):
        pass

    def delete_parameter(self):
        pass
    
    ### desna strana
    def create_parameter_widget(self):
        groupBox = QGroupBox(self.language['parameters_window_parameter_caption'])

        self.text_parameter_name = QLabel(self.language['parameters_window_parameter_name'])
        self.parameter_name = QLineEdit()
        
        self.text_parameter_symbol = QLabel(self.language['parameters_window_parameter_symbol'])
        self.parameter_symbol = QLineEdit()
        
        self.text_parameter_unit = QLabel(self.language['parameters_window_parameter_unit'])
        self.parameter_unit = QLineEdit()

        self.text_parameter_descriprion = QLabel(self.language['parameters_window_parameter_desc'])
        self.parameter_descriprion = QTextEdit()

        self.buttonSave = QPushButton(self.language['parameters_window_parameter_btn_save'])
        self.buttonSave.clicked.connect(self.save_changes_parameter)
        
        self.buttonCancel = QPushButton(self.language['parameters_window_parameter_btn_cancel'])
        self.buttonCancel.clicked.connect(self.cancel)
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_parameter_name)
        layout.addWidget(self.parameter_name)
        layout.addWidget(self.text_parameter_symbol)
        layout.addWidget(self.parameter_symbol)
        layout.addWidget(self.text_parameter_unit)
        layout.addWidget(self.parameter_unit)
        layout.addWidget(self.text_parameter_descriprion)
        layout.addWidget(self.parameter_descriprion)
        layout.addWidget(self.buttonSave)
        layout.addWidget(self.buttonCancel)
        layout.addStretch(1)
        groupBox.setLayout(layout)
        
        return groupBox

    def update_labels(self, name, state, symbol, unit, description):
        self.parameter_name.setText(name)
        self.parameter_name.setEnabled(state)
        self.parameter_symbol.setText(symbol)
        self.parameter_symbol.setEnabled(state)
        self.parameter_unit.setText(unit)
        self.parameter_unit.setEnabled(state)
        self.parameter_descriprion.setText(description)
        self.parameter_descriprion.setEnabled(state)
        self.buttonSave.setEnabled(state)
        self.buttonDelete.setEnabled(state)
        self.buttonCancel.setEnabled(state)
        # Dodati pucad ovdje

    def save_changes_parameter(self):
        pass

    def cancel(self):
        pass

    def close_button(self):
        groupBox = QGroupBox()
        
        buttonClose = QPushButton(self.language['parameters_window_btn_close'])
        buttonClose.clicked.connect(self.close_window)
        
        layout = QHBoxLayout()
        layout.addWidget(buttonClose)
        layout.setAlignment(Qt.AlignRight)
        layout.addStretch(1)
        groupBox.setLayout(layout)
        
        return groupBox
    
    def close_window(ParametersWindow):
        quit()
        
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = ParametersWindow()
    sys.exit(mainApplication.exec_())