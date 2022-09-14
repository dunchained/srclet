# python standard modules
import sys, os, json
from pathlib import Path
cwd = os.path.curdir
#
# app modules and windows
#from css import css, var
#from windows.methods.add_method import AddMethod
#from add_method_eto import AddETOMethod
eto_methods_folder = '/methods/eto/'
parameters_folder = '/parameters/basic/'
complex_parameters_folder = '/parameters/complex/'

# pyqt5 modules
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QListView, QPushButton, QApplication
from PyQt5.QtWidgets import QLineEdit, QListWidget, QTextEdit, QMessageBox, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

class ETOMethodsWindow(QWidget):
    def __init__(self):
        super(ETOMethodsWindow, self).__init__()
        self.language = {
            "//": "ETO Methods Window",
            "eto_methods_window_title": "ETO Methods",
            "eto_methods_window_caption": "List of available ETO methods:",
            "eto_methods_window_btn_add_new": "Add new ETO method",
            "eto_methods_window_btn_delete": "Delete selected method",
            "eto_methods_window_method_caption": "Method information:",
            "eto_methods_window_method_filename": "Filename:",
            "eto_methods_window_method_name": "Method name:",
            "eto_methods_window_method_symbol": "Method symbol:",
            "eto_methods_window_method_unit": "Method unit:",
            "eto_methods_window_method_desc": "Method description:",
            "eto_methods_window_method_btn_save": "Save changes",
            "eto_methods_window_method_btn_cancel": "Cancel changes",
            "eto_methods_window_btn_close": "Close",
            "eto_methods_window_save_changes_message": "Method name or unit empty...",
            "eto_methods_window_save_changes_message_caption": "Missing data...",
            "eto_methods_window_save_message": "Method saved...",
            "eto_methods_window_save_message_caption": "Successuful...",
            
            "//": "Add ETO methods Window",
            "add_eto_methods_window_title": "Add new ETO method",
            "add_eto_methods_window_caption": "Method information:",
            "add_eto_methods_window_filename": "Filename:",
            "add_eto_methods_window_filename_exp": "Text to be used as method filename.",
            "add_eto_methods_window_name": "Method name:",
            "add_eto_methods_window_name_exp": "Text to be used as method short description.",
            "add_eto_methods_window_conditions": "Method conditions:",
            "add_eto_methods_window_conditions_exp": "Conditions to be used...",
            "add_eto_methods_window_formula": "Method formula:",
            "add_eto_methods_window_formula_exp": "Formula used to calculate method...",
            "add_eto_methods_window_desc": "Method description:",
            "add_eto_methods_window_desc_exp": "Text to be used for short explinations.",
            "add_eto_methods_window_btn_add": "Save",
            "add_eto_methods_window_btn_cancel": "Cancel",
            "add_eto_methods_window_save_message": "Method name or unit empty...",
            "add_eto_methods_window_save_message_caption": "Missing data...",
            "add_eto_methods_window_saved_message": "Method saved...",
            "add_eto_methods_window_saved_message_caption": "Successuful...",
            "add_eto_methods_window_filename_message": "Method with this filename already exists.",
            "add_eto_methods_window_filename_message_caption": "Filename...",
            "":""
        }
        
        self.AddETOMethod = AddETOMethod(self.language)
        self.AddETOMethod.hide()
        self.AddETOMethod.clicked.connect(self.refresh_methods_list)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.WindowGUI()

    def WindowGUI(self):
        #self.setFixedSize(800, 600)
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle(self.language['eto_methods_window_title'])
        #self.setWindowIcon(QIcon(css.menu_about_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.createLeftGroupBox(), 0, 0, 1, 1)
        self.grid.addWidget(self.createRightGroupBox(), 0, 1, 1, 1)
        self.grid.addWidget(self.createDownGroupBox(), 1, 0, 1, 2)
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def createLeftGroupBox(self):
        LeftGroupBox = QGroupBox(self.language['eto_methods_window_caption'])
        self.list_widget = QListWidget()
        get_files = next(os.walk(cwd + eto_methods_folder), (None, None, []))[2]
        self.file_list = []
        for file in get_files:
            self.file_list.append(Path(file).stem)
        self.list_widget.addItems(self.file_list)
        self.list_widget.currentItemChanged.connect(self.index_changed)
        self.buttonAddMethod = QPushButton(self.language['eto_methods_window_btn_add_new'])
        self.buttonAddMethod.clicked.connect(self.newMethodWindow)
        self.buttonDelete = QPushButton(self.language['eto_methods_window_btn_delete'])
        self.buttonDelete.clicked.connect(self.delete_method)
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.buttonAddMethod)
        layout.addWidget(self.buttonDelete)
        layout.addStretch(1)
        LeftGroupBox.setLayout(layout)
        return LeftGroupBox
    
    def index_changed(self, i):
        self.json_path = cwd + eto_methods_folder + i.text() + '.json'
        with open(self.json_path) as json_file:
            data = json.load(json_file)
            if data['type'] == 'b':
                self.method_filename.setText(i.text())
                self.method_name.setEnabled(False)                
                self.method_name.setText(data['name'])
                self.method_symbol.setEnabled(False)
                self.method_symbol.setText(data['symbol'])
                self.method_unit.setEnabled(False)
                self.method_unit.setText(data['unit'])
                self.method_descriprion.setEnabled(False)
                self.method_descriprion.setText(data['description'])
                self.buttonSaveProject.setEnabled(False)
                self.buttonCancel.setEnabled(False)
                self.buttonDelete.setEnabled(False)
            else:
                self.method_filename.setText(i.text())
                self.method_name.setText(data['name'])
                self.method_name.setEnabled(True) 
                self.method_symbol.setText(data['symbol'])
                self.method_symbol.setEnabled(True)
                self.method_unit.setText(data['unit'])
                self.method_unit.setEnabled(True)
                self.method_descriprion.setText(data['description'])
                self.method_descriprion.setEnabled(True)
                self.buttonSaveProject.setEnabled(True)
                self.buttonCancel.setEnabled(True)
                self.buttonDelete.setEnabled(True)
            
    def refresh_methods_list(self):
        get_files = next(os.walk(cwd + eto_methods_folder), (None, None, []))[2]
        self.file_list_update = []
        for file in get_files:
            if Path(file).stem not in self.file_list:
                self.file_list_update.append(Path(file).stem)
        self.list_widget.addItems(self.file_list_update)

    def delete_method(self):
        list_items = self.list_widget.selectedItems()
        if not list_items: return
        for item in list_items:
            self.list_widget.takeItem(self.list_widget.row(item))
        os.remove(cwd + eto_methods_folder + item.text() + '.json')
    
    def createRightGroupBox(self):
        RightGroupBox = QGroupBox(self.language['eto_methods_window_method_caption'])
        self.text_method_filename = QLabel(self.language['eto_methods_window_method_filename'])
        self.method_filename = QLineEdit()
        self.method_filename.setEnabled(False)
        self.text_method_name = QLabel(self.language['eto_methods_window_method_name'])
        self.method_name = QLineEdit()
        
        self.text_method_symbol = QLabel(self.language['eto_methods_window_method_symbol'])
        self.method_symbol = QLineEdit()
        
        self.text_method_unit = QLabel(self.language['eto_methods_window_method_unit'])
        self.method_unit = QLineEdit()

        self.text_method_descriprion = QLabel(self.language['eto_methods_window_method_desc'])
        self.method_descriprion = QTextEdit()

        self.buttonSaveProject = QPushButton(self.language['eto_methods_window_method_btn_save'])
        self.buttonSaveProject.clicked.connect(self.save_changes_method)
        self.buttonCancel = QPushButton(self.language['eto_methods_window_method_btn_cancel'])
        self.buttonCancel.clicked.connect(self.cancel)
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_method_filename)
        layout.addWidget(self.method_filename)
        layout.addWidget(self.text_method_name)
        layout.addWidget(self.method_name)
        layout.addWidget(self.text_method_symbol)
        layout.addWidget(self.method_symbol)
        layout.addWidget(self.text_method_unit)
        layout.addWidget(self.method_unit)
        layout.addWidget(self.text_method_descriprion)
        layout.addWidget(self.method_descriprion)
        layout.addWidget(self.buttonSaveProject)
        layout.addWidget(self.buttonCancel)
        layout.addStretch(1)
        RightGroupBox.setLayout(layout)
        
        return RightGroupBox

    def cancel(self):
        self.json_path = cwd + eto_methods_folder + self.list_widget.currentItem().text() + '.json'
        with open(self.json_path) as json_file:
            data = json.load(json_file)
            
        self.method_name.setText(data['name'])
        self.method_symbol.setText(data['symbol'])
        self.method_unit.setText(data['unit'])
        self.method_descriprion.setText(data['description'])

    def createDownGroupBox(self):
        DownGroupBox = QGroupBox()
        
        buttonClose = QPushButton(self.language['eto_methods_window_btn_close'])
        buttonClose.clicked.connect(self.close)
        
        layout = QHBoxLayout()
        layout.addWidget(buttonClose)
        layout.setAlignment(Qt.AlignRight)
        layout.addStretch(1)
        DownGroupBox.setLayout(layout)
        
        return DownGroupBox
    
    def newMethodWindow(self):
        self.AddETOMethod.show()

    def save_changes_method(self):
        if not self.method_filename and not self.method_name.text() and not self.method_unit.text():
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['eto_methods_window_save_changes_message'])
            self.msg.setWindowTitle(self.language['eto_methods_window_save_changes_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            method_dict = {
                "name": self.method_name.text(),
                "symbol": self.method_symbol.text(),
                "unit": self.method_unit.text(),
                "description": self.method_descriprion.toPlainText(),
                "type": "a"
                }
            json_object = json.dumps(method_dict, indent = 4)
            with open(cwd + eto_methods_folder + self.method_filename.text() + ".json", "w") as outfile:
                outfile.write(json_object)
                
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['eto_methods_window_save_message'])
            self.msg.setWindowTitle(self.language['eto_methods_window_save_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.show()
            
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = ETOMethodsWindow()
    sys.exit(mainApplication.exec_())