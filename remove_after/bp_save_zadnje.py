import sys, os, json, shutil
cwd = os.path.curdir
#from variables import css, var
from windows.parameters.basic_parameters_add import AddParameter
#from add_basic_parameter import AddParameter
from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QHBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QListView, QPushButton, QApplication
from PyQt5.QtWidgets import QLineEdit, QListWidget, QTextEdit, QMessageBox, QWidget, QMainWindow, QDialog
from PyQt5.QtCore import Qt, QCoreApplication, QObject, QProcess, pyqtSignal
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem, QRegion

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

class BasicParametersWindow(QMainWindow):
    signale = pyqtSignal(object)
    def __init__(self):
        super(BasicParametersWindow, self).__init__()
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
        self.setUpdatesEnabled(True)
        self.window_gui()

    def window_gui(self):
        #self.setFixedSize(800, 600)
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle(self.language['parameters_window_title'])
        #self.setWindowIcon(QIcon(css.menu_about_icon))
        #self.grid = QGridLayout()
        #self.grid.addWidget(self.tab_widget())
        #self.setLayout(self.grid)
        self.central_widget = QWidget()
        self.central_widget.layout = QVBoxLayout()
        self.central_widget.layout.addWidget(self.tab_widget())
        self.central_widget.setLayout(self.central_widget.layout)
        self.setCentralWidget(self.central_widget)
        self.setMinimumSize(800, 600)
        self.center_gui()
        self.show()
        
    def signal(self):
        self.signale.emit()
        print('makamaka')
        
    def center_gui(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def tab_widget(self):
        self.tab_widget = QTabWidget()
        self.cat_file = 'parameter_types.json' ### import iz var
        self.cat_file = open(os.path.join(cwd + language_folder + self.language['language_description'] + '/' + self.cat_file))
        self.cat_file_data = json.load(self.cat_file)
        self.cat_list = []
        for category in self.cat_file_data:
            self.cat_list.append(self.cat_file_data[category])
        for tabName in self.cat_list:
            self.category = list(self.cat_file_data.keys())[list(self.cat_file_data.values()).index(tabName)]
            self.tab = QWidget()
            self.tab_layout = QGridLayout()
            self.tab_layout.addWidget(TabWidget(self.category, self.language), 0, 0, 1, 1)
            self.tab.setLayout(self.tab_layout)
            self.tab_widget.addTab(self.tab, tabName)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.tab_widget)
        self.setLayout(self.mainLayout)
        return self.tab_widget
    
class TabWidget(QWidget):
    signale = pyqtSignal(object)
    def __init__(self, category, language):
        super(TabWidget, self).__init__()
        
        self.parameter_category = category
        self.language = language
        
        self.get_parameters = next(os.walk(cwd + parameters_folder), (None, None, []))[2]
        self.category_list = []
        for self.parameter_file in self.get_parameters:
            self.parameter_file_to_load = open(os.path.join(cwd + parameters_folder + self.parameter_file))
            self.parameter_file_data = json.load(self.parameter_file_to_load)
            if self.parameter_category == self.parameter_file_data['category']:
                self.category_list.append(self.parameter_file_data['name'])
        
        self.clw_groupbox = QGroupBox('Lista parametara:')
        self.clw_list_widget = QListWidget()
        self.clw_list_widget.addItems(self.category_list)
        self.clw_list_widget.currentItemChanged.connect(self.index_changed)
        self.btn_add_parameter = QPushButton('Add parameter')
        self.btn_add_parameter.clicked.connect(self.add_parameter)
        self.btn_delete_parameter = QPushButton('Delete parameter')
        self.btn_delete_parameter.clicked.connect(self.delete_procedure)
        self.clw_groupbox.layout = QVBoxLayout()
        self.clw_groupbox.layout.addWidget(self.clw_list_widget)
        self.clw_groupbox.layout.addWidget(self.btn_add_parameter)
        self.clw_groupbox.layout.addWidget(self.btn_delete_parameter)
        self.clw_groupbox.setLayout(self.clw_groupbox.layout)
        
        self.cpw_gruopbox = QGroupBox(self.language['parameters_window_parameter_caption'])
        self.text_parameter_name = QLabel(self.language['parameters_window_parameter_name'])
        self.parameter_name = QLineEdit()
        self.text_parameter_symbol = QLabel(self.language['parameters_window_parameter_symbol'])
        self.parameter_symbol = QLineEdit()
        self.text_parameter_unit = QLabel(self.language['parameters_window_parameter_unit'])
        self.parameter_unit = QLineEdit()
        self.text_parameter_descriprion = QLabel(self.language['parameters_window_parameter_desc'])
        self.parameter_descriprion = QTextEdit()
        self.btn_save_parameter_changes = QPushButton(self.language['parameters_window_parameter_btn_save'])
        self.btn_save_parameter_changes.clicked.connect(self.save_parameter_changes)
        self.btn_cancel_parameter_changes = QPushButton(self.language['parameters_window_parameter_btn_cancel'])
        self.btn_cancel_parameter_changes.clicked.connect(self.cancel_parameter_changes)
        self.cpw_gruopbox.layout = QVBoxLayout()
        self.cpw_gruopbox.layout.addWidget(self.text_parameter_name)
        self.cpw_gruopbox.layout.addWidget(self.parameter_name)
        self.cpw_gruopbox.layout.addWidget(self.text_parameter_symbol)
        self.cpw_gruopbox.layout.addWidget(self.parameter_symbol)
        self.cpw_gruopbox.layout.addWidget(self.text_parameter_unit)
        self.cpw_gruopbox.layout.addWidget(self.parameter_unit)
        self.cpw_gruopbox.layout.addWidget(self.text_parameter_descriprion)
        self.cpw_gruopbox.layout.addWidget(self.parameter_descriprion)
        self.cpw_gruopbox.layout.addWidget(self.btn_save_parameter_changes)
        self.cpw_gruopbox.layout.addWidget(self.btn_cancel_parameter_changes)
        self.cpw_gruopbox.setLayout(self.cpw_gruopbox.layout)
        
        self.ccbw_groupbox = QGroupBox()
        self.btn_close_window = QPushButton(self.language['parameters_window_btn_close'])
        self.btn_close_window.clicked.connect(self.close_window)
        self.ccbw_groupbox.layout = QHBoxLayout()
        self.ccbw_groupbox.layout.addWidget(self.btn_close_window)
        self.ccbw_groupbox.setLayout(self.ccbw_groupbox.layout)
        
        
        self.layout = QGridLayout()
        self.layout.addWidget(self.clw_groupbox, 0, 0, 1, 1)
        self.layout.addWidget(self.cpw_gruopbox, 0, 1, 1, 1)
        self.layout.addWidget(self.ccbw_groupbox, 1, 0, 1, 2)
        self.setLayout(self.layout)
        
    def add_parameter(self):
        self.window = AddParameter()
        self.window.clicked.connect(self.refresh_parameters_list_after_addition)
        
    def refresh_parameters_list_after_addition(self):
        self.signale
        print('ekipno')
    
    def delete_procedure(self):
        pass
    
    def delete_parameter(self):
        pass
    
    def create_parameter_widget(self):
        pass
    
    def index_changed(self, i):
        self.get_files = next(os.walk(cwd + parameters_folder), (None, None, []))[2]
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
                
    def update_labels(self, name, state, symbol, unit, description):
        self.parameter_name.setText(name)
        self.parameter_name.setEnabled(state)
        self.parameter_symbol.setText(symbol)
        self.parameter_symbol.setEnabled(state)
        self.parameter_unit.setText(unit)
        self.parameter_unit.setEnabled(state)
        self.parameter_descriprion.setText(description)
        self.parameter_descriprion.setEnabled(state)
        self.btn_save_parameter_changes.setEnabled(state)
        self.btn_delete_parameter.setEnabled(state)
        self.btn_cancel_parameter_changes.setEnabled(state)
        
    def save_parameter_changes(self):
        pass
    
    def cancel_parameter_changes(self):
        pass
    
    def create_close_buttons_widget(self):
        pass
        
    def close_window(self):
        quit()

#     def new_parameter_window(self):
#         self.window = AddParameter()
#         self.window.clicked.connect(self.refresh_parameters_list_after_addition)
        
#     def delete_procedure(self):
#         msgBox = QMessageBox()
#         msgBox.setIcon(QMessageBox.Information)
#         msgBox.setText('sigurno zelis obrisati')
#         msgBox.setWindowTitle('brisanje parametra')
#         msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
#         buttonOK = msgBox.button(QMessageBox.Ok)
#         buttonOK.setText('da')
#         buttonCancel = msgBox.button(QMessageBox.Cancel)
#         buttonCancel.setText('odustani')
#         msgBox.buttonClicked.connect(self.delete_parameter)
#         returnValue = msgBox.exec()

#     def delete_parameter(self, value):
#         if value.text() == 'da':
#             self.get_list_of_files = next(os.walk(cwd + parameters_folder), (None, None, []))[2]
#             for self.file_to_delete in self.get_list_of_files:
#                 self.path_to_file_to_delete = open(os.path.join(cwd + parameters_folder + self.file_to_delete))
#                 self.data_of_file_to_delete = json.load(self.path_to_file_to_delete)
#                 if self.list_widget.currentItem().text() == self.data_of_file_to_delete['name']:
#                     os.remove(os.path.join(cwd + parameters_folder + self.file_to_delete))
#             self.refresh_parameters_list_after_deletion()
            
        
#     def refresh_parameters_list_after_deletion(self):
#         self.item_to_remove = self.list_widget.selectedItems()
#         if not self.item_to_remove: return
#         for item in self.item_to_remove:
#             self.list_widget.takeItem(self.list_widget.row(item))
            
#     def refresh_parameters_list_after_addition(self):
#         print('Prošo ParametersWindow')
#         #self.kenozoik = ParametersWindow(self.language)
#         #self.kenozoik.signale
#         self.signali = Signals()
#         self.signali.do_something()
#         print(self.parent.__str__)
#         print('šalje')
#         #self.close_window()
        
#     

#     def save_changes_parameter(self):
#         pass

#     def cancel(self):
#         pass


    
#     def close_window(ParametersWindow):
#         quit()
        
if __name__ == '__main__':
   mainApplication = QApplication(sys.argv)
   mainWindow = BasicParametersWindow()
   sys.exit(mainApplication.exec_())