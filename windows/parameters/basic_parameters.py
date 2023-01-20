import sys, os, json, shutil
cwd = os.path.curdir
#from variables import css, var
from windows.parameters.add_basic_parameter import AddParameter
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

class Signals(QObject):
    asignal = pyqtSignal()

    def __init__(self):
        super(Signals, self).__init__()
        self.do_something()

    def do_something(self):
        self.asignal.emit()

class ParametersWindow(QWidget):
    signale = pyqtSignal()
    def __init__(self, language):
        super(ParametersWindow, self).__init__()
        self.language = language
        self.AddParameter = AddParameter()
        self.AddParameter.hide()
        #self.AddParameter.clicked.connect(self.refresh_parameters_list)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.window_gui()
        print(self.parent.__class__.__name__)

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
    
class ParametersCategoryTabs(QWidget):
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
            self.tabWidget = QWidget()
            self.listWidget = ParametersWidget(self.category, self.language)
            self.tabLayout = QGridLayout()
            self.tabLayout.addWidget(self.listWidget)
            self.tabWidget.setLayout(self.tabLayout)
            self.categories_tabs.addTab(self.tabWidget, tabName)
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
        self.buttonDelete.clicked.connect(self.delete_procedure)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.buttonAddParameter)
        self.layout.addWidget(self.buttonDelete)
        self.layout.addStretch(1)
        groupBox.setLayout(self.layout)
        return groupBox

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

    def new_parameter_window(self):
        self.window = AddParameter()
        self.window.clicked.connect(self.refresh_parameters_list_after_addition)
        
    def delete_procedure(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('sigurno zelis obrisati')
        msgBox.setWindowTitle('brisanje parametra')
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        buttonOK = msgBox.button(QMessageBox.Ok)
        buttonOK.setText('da')
        buttonCancel = msgBox.button(QMessageBox.Cancel)
        buttonCancel.setText('odustani')
        msgBox.buttonClicked.connect(self.delete_parameter)
        returnValue = msgBox.exec()

    def delete_parameter(self, value):
        if value.text() == 'da':
            self.get_list_of_files = next(os.walk(cwd + parameters_folder), (None, None, []))[2]
            for self.file_to_delete in self.get_list_of_files:
                self.path_to_file_to_delete = open(os.path.join(cwd + parameters_folder + self.file_to_delete))
                self.data_of_file_to_delete = json.load(self.path_to_file_to_delete)
                if self.list_widget.currentItem().text() == self.data_of_file_to_delete['name']:
                    os.remove(os.path.join(cwd + parameters_folder + self.file_to_delete))
            self.refresh_parameters_list_after_deletion()
            
        
    def refresh_parameters_list_after_deletion(self):
        self.item_to_remove = self.list_widget.selectedItems()
        if not self.item_to_remove: return
        for item in self.item_to_remove:
            self.list_widget.takeItem(self.list_widget.row(item))
            
    def refresh_parameters_list_after_addition(self):
        print('Prošo ParametersWindow')
        #self.kenozoik = ParametersWindow(self.language)
        #self.kenozoik.signale
        self.signali = Signals()
        self.signali.do_something()
        print(self.parent.__str__)
        print('šalje')
        #self.close_window()
        
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
        
#if __name__ == '__main__':
   #mainApplication = QApplication(sys.argv)
   #mainWindow = ParametersWindow()
   #sys.exit(mainApplication.exec_())