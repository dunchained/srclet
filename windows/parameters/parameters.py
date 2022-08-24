# python standard modules
from concurrent.futures import process
from importlib.resources import path
import sys, os, json
from pathlib import Path

# app modules and windows
#from css import css
import add_parameter
#from windows.parameters.add_parameter import AddParameter

# pyqt5 modules
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QListView, QPushButton, QApplication
from PyQt5.QtWidgets import QLineEdit, QListWidget, QTextEdit, QMessageBox, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

class ParametersWindow(QWidget):
    def __init__(self):
        super(ParametersWindow, self).__init__()
        self.AddParameter = add_parameter.AddParameter()
        self.AddParameter.hide()
        self.AddParameter.clicked.connect(self.refresh_parameters_list)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = {
            "parameters_window_title": "Parameters",
            "parameters_window_caption": "List of available parameters:",
            "parameters_window_btn_refresh": "Refresh parameters list",
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
        self.WindowGUI()

    def WindowGUI(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle(self.language['parameters_window_title'])
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
        LeftGroupBox = QGroupBox(self.language['parameters_window_caption'])
        self.list_widget = QListWidget()
        get_files = next(os.walk(os.path.curdir + "/parameters/basic/"), (None, None, []))[2]
        self.file_list = []
        for file in get_files:
            self.file_list.append(Path(file).stem)
        
        self.list_widget.addItems(self.file_list)
        
        self.list_widget.currentItemChanged.connect(self.index_changed)
        self.buttonRefresh = QPushButton(self.language['parameters_window_btn_refresh'])
        self.buttonRefresh.clicked.connect(self.refresh_parameters_list)
        
        self.buttonAddParameter = QPushButton(self.language['parameters_window_btn_add_new'])
        self.buttonAddParameter.clicked.connect(self.newParameterWindow)
        
        self.buttonDelete = QPushButton(self.language['parameters_window_btn_delete'])
        self.buttonDelete.clicked.connect(self.delete_parameter)

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        #layout.addWidget(buttonRefresh)
        layout.addWidget(self.buttonAddParameter)
        layout.addWidget(self.buttonDelete)
        layout.addStretch(1)
        LeftGroupBox.setLayout(layout)
        
        return LeftGroupBox
    
    def index_changed(self, i):
        self.json_path = 'parameters/basic/' + i.text() + '.json'
       
        with open(self.json_path) as json_file:
            data = json.load(json_file)
            print(data)
            if data['type'] == 'b':
                self.parameter_filename.setText(i.text())
                self.parameter_name.setEnabled(False)                
                self.parameter_name.setText(data['name'])
                self.parameter_symbol.setEnabled(False)
                self.parameter_symbol.setText(data['symbol'])
                self.parameter_unit.setEnabled(False)
                self.parameter_unit.setText(data['unit'])
                self.parameter_descriprion.setEnabled(False)
                self.parameter_descriprion.setText(data['description'])
                self.buttonSaveProject.setEnabled(False)
                self.buttonCancel.setEnabled(False)
                self.buttonDelete.setEnabled(False)
            
                
            else:
                self.parameter_filename.setText(i.text())
                self.parameter_name.setText(data['name'])
                self.parameter_name.setEnabled(True) 
                self.parameter_symbol.setText(data['symbol'])
                self.parameter_symbol.setEnabled(True)
                self.parameter_unit.setText(data['unit'])
                self.parameter_unit.setEnabled(True)
                self.parameter_descriprion.setText(data['description'])
                self.parameter_descriprion.setEnabled(True)
                self.buttonSaveProject.setEnabled(True)
                self.buttonCancel.setEnabled(True)
                self.buttonDelete.setEnabled(True)
                
            
    def refresh_parameters_list(self):
        get_files = next(os.walk(os.path.curdir + "/parameters/basic/"), (None, None, []))[2]
        self.file_list_update = []
        for file in get_files:
            if Path(file).stem not in self.file_list:
                self.file_list_update.append(Path(file).stem)
                #self.list_widget.clear()
        self.list_widget.addItems(self.file_list_update)

    def delete_parameter(self):
        list_items = self.list_widget.selectedItems()
        if not list_items: return
        for item in list_items:
            self.list_widget.takeItem(self.list_widget.row(item))
        os.remove('parameters/basic/' + item.text() + '.json')
    
    def createRightGroupBox(self):
        RightGroupBox = QGroupBox(self.language['parameters_window_parameter_caption'])
        self.text_parameter_filename = QLabel(self.language['parameters_window_parameter_filename'])
        self.parameter_filename = QLineEdit()
        self.parameter_filename.setEnabled(False)
        self.text_parameter_name = QLabel(self.language['parameters_window_parameter_name'])
        self.parameter_name = QLineEdit()
        
        self.text_parameter_symbol = QLabel(self.language['parameters_window_parameter_symbol'])
        self.parameter_symbol = QLineEdit()
        
        self.text_parameter_unit = QLabel(self.language['parameters_window_parameter_unit'])
        self.parameter_unit = QLineEdit()

        self.text_parameter_descriprion = QLabel(self.language['parameters_window_parameter_desc'])
        self.parameter_descriprion = QTextEdit()

        self.buttonSaveProject = QPushButton(self.language['parameters_window_parameter_btn_save'])
        self.buttonSaveProject.clicked.connect(self.save_changes_parameter)
        self.buttonCancel = QPushButton(self.language['parameters_window_parameter_btn_cancel'])
        self.buttonCancel.clicked.connect(self.close)
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_parameter_filename)
        layout.addWidget(self.parameter_filename)
        layout.addWidget(self.text_parameter_name)
        layout.addWidget(self.parameter_name)
        layout.addWidget(self.text_parameter_symbol)
        layout.addWidget(self.parameter_symbol)
        layout.addWidget(self.text_parameter_unit)
        layout.addWidget(self.parameter_unit)
        layout.addWidget(self.text_parameter_descriprion)
        layout.addWidget(self.parameter_descriprion)
        layout.addWidget(self.buttonSaveProject)
        layout.addWidget(self.buttonCancel)
        layout.addStretch(1)
        RightGroupBox.setLayout(layout)
        
        return RightGroupBox
    
    def createDownGroupBox(self):
        DownGroupBox = QGroupBox()
        
        buttonClose = QPushButton(self.language['parameters_window_btn_close'])
        buttonClose.clicked.connect(self.close)
        
        layout = QHBoxLayout()
        layout.addWidget(buttonClose)
        layout.setAlignment(Qt.AlignRight)
        layout.addStretch(1)
        DownGroupBox.setLayout(layout)
        
        return DownGroupBox
    
    def newParameterWindow(self):
        #self.window = AddParameter()
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
            # ovdje treba još jedan uslov da provjeri da li ima već projekat sa istim imenom
            # poruka da li želite otvoriti kreirani projekat
            parameter_dict = {
                "name": self.parameter_name.text(),
                "symbol": self.parameter_symbol.text(),
                "unit": self.parameter_unit.text(),
                "description": self.parameter_descriprion.toPlainText(),
                "type": "a"
                }
            json_object = json.dumps(parameter_dict, indent = 4)
            with open(os.path.curdir + "/parameters/basic/" + self.parameter_filename.text() + ".json", "w") as outfile:
                outfile.write(json_object)
                
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['parameters_window_save_message'])
            self.msg.setWindowTitle(self.language['parameters_window_save_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            #self.msg.buttonClicked.connect(self.close)
            self.msg.show()

if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = ParametersWindow()
    sys.exit(mainApplication.exec_())