# python standard modules
import sys, os, json
from pathlib import Path
cwd = os.path.curdir

# app modules and windows
from css import css, var
from windows.parameters.add_complex_parameter import AddComplexParameter

# pyqt5 modules
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QPushButton
from PyQt5.QtWidgets import QLineEdit, QListWidget, QTextEdit, QMessageBox, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

class ComplexParametersWindow(QWidget):
    def __init__(self, language):
        super(ComplexParametersWindow, self).__init__()
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.language = language
        self.AddParameter = AddComplexParameter(self.language)
        self.AddParameter.hide()
        self.AddParameter.clicked.connect(self.refresh_parameters_list)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.WindowGUI()

    def WindowGUI(self):
        #self.setFixedSize(800, 600)
        self.setWindowTitle(self.language['complex_parameters_window_title'])
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
        LeftGroupBox = QGroupBox(self.language['complex_parameters_window_caption'])
        self.list_widget = QListWidget()
        get_files = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
        self.file_list = []
        for file in get_files:
            self.file_list.append(Path(file).stem)
        self.list_widget.addItems(self.file_list)
        self.list_widget.currentItemChanged.connect(self.index_changed)
        self.buttonAddParameter = QPushButton(self.language['complex_parameters_window_btn_add_new'])
        self.buttonAddParameter.clicked.connect(self.newParameterWindow)
        self.buttonDelete = QPushButton(self.language['complex_parameters_window_btn_delete'])
        self.buttonDelete.clicked.connect(self.delete_parameter)
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.buttonAddParameter)
        layout.addWidget(self.buttonDelete)
        layout.addStretch(1)
        LeftGroupBox.setLayout(layout)
        return LeftGroupBox
    
    def index_changed(self, i):
        self.json_path = cwd + var.complex_parameters_folder + i.text() + '.json'
        with open(self.json_path) as json_file:
            data = json.load(json_file)
            if data['type'] == 'b':
                self.parameter_filename.setText(i.text())
                self.parameter_name.setEnabled(False)                
                self.parameter_name.setText(data['name'])
                self.parameter_symbol.setEnabled(False)
                self.parameter_symbol.setText(data['symbol'])
                self.parameter_unit.setEnabled(False)
                self.parameter_unit.setText(data['unit'])
                self.parameter_formula.setEnabled(False)
                self.parameter_formula.setText(data['formula'])
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
                self.parameter_formula.setText(data['formula'])
                self.parameter_formula.setEnabled(True)
                self.parameter_descriprion.setText(data['description'])
                self.parameter_descriprion.setEnabled(True)
                self.buttonSaveProject.setEnabled(True)
                self.buttonCancel.setEnabled(True)
                self.buttonDelete.setEnabled(True)
            
    def refresh_parameters_list(self):
        get_files = next(os.walk(cwd + var.complex_parameters_folder), (None, None, []))[2]
        self.file_list_update = []
        for file in get_files:
            if Path(file).stem not in self.file_list:
                self.file_list_update.append(Path(file).stem)
        self.list_widget.addItems(self.file_list_update)

    def delete_parameter(self):
        list_items = self.list_widget.selectedItems()
        if not list_items: return
        for item in list_items:
            self.list_widget.takeItem(self.list_widget.row(item))
        os.remove(cwd + var.complex_parameters_folder + item.text() + '.json')
    
    def createRightGroupBox(self):
        RightGroupBox = QGroupBox(self.language['complex_parameters_window_parameter_caption'])
        self.text_parameter_filename = QLabel(self.language['complex_parameters_window_parameter_filename'])
        self.parameter_filename = QLineEdit()
        self.parameter_filename.setEnabled(False)
        self.text_parameter_name = QLabel(self.language['complex_parameters_window_parameter_name'])
        self.parameter_name = QLineEdit()
        
        self.text_parameter_symbol = QLabel(self.language['complex_parameters_window_parameter_symbol'])
        self.parameter_symbol = QLineEdit()
        
        self.text_parameter_unit = QLabel(self.language['complex_parameters_window_parameter_unit'])
        self.parameter_unit = QLineEdit()

        self.text_parameter_formula = QLabel(self.language['complex_parameters_window_parameter_formula'])
        self.parameter_formula = QTextEdit()

        self.text_parameter_descriprion = QLabel(self.language['complex_parameters_window_parameter_desc'])
        self.parameter_descriprion = QTextEdit()

        self.buttonSaveProject = QPushButton(self.language['complex_parameters_window_parameter_btn_save'])
        self.buttonSaveProject.clicked.connect(self.save_changes_parameter)
        self.buttonCancel = QPushButton(self.language['complex_parameters_window_parameter_btn_cancel'])
        self.buttonCancel.clicked.connect(self.cancel)
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_parameter_filename)
        layout.addWidget(self.parameter_filename)
        layout.addWidget(self.text_parameter_name)
        layout.addWidget(self.parameter_name)
        layout.addWidget(self.text_parameter_symbol)
        layout.addWidget(self.parameter_symbol)
        layout.addWidget(self.text_parameter_unit)
        layout.addWidget(self.parameter_unit)
        layout.addWidget(self.text_parameter_formula)
        layout.addWidget(self.parameter_formula)
        layout.addWidget(self.text_parameter_descriprion)
        layout.addWidget(self.parameter_descriprion)
        layout.addWidget(self.buttonSaveProject)
        layout.addWidget(self.buttonCancel)
        layout.addStretch(1)
        RightGroupBox.setLayout(layout)
        
        return RightGroupBox

    def cancel(self):
        self.json_path = cwd + var.complex_parameters_folder + self.list_widget.currentItem().text() + '.json'
        with open(self.json_path) as json_file:
            data = json.load(json_file)
            
        self.parameter_name.setText(data['name'])
        self.parameter_symbol.setText(data['symbol'])
        self.parameter_unit.setText(data['unit'])
        self.parameter_formula.setText(data['formula'])
        self.parameter_descriprion.setText(data['description'])

    def createDownGroupBox(self):
        DownGroupBox = QGroupBox()
        
        buttonClose = QPushButton(self.language['complex_parameters_window_btn_close'])
        buttonClose.clicked.connect(self.close)
        
        layout = QHBoxLayout()
        layout.addWidget(buttonClose)
        layout.setAlignment(Qt.AlignRight)
        layout.addStretch(1)
        DownGroupBox.setLayout(layout)
        
        return DownGroupBox
    
    def newParameterWindow(self):
        self.AddParameter.show()

    def save_changes_parameter(self):
        if not self.parameter_filename or not self.parameter_name.text() or not self.parameter_unit.text() or not self.parameter_symbol.text():
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['complex_parameters_window_save_changes_message'])
            self.msg.setWindowTitle(self.language['complex_parameters_window_save_changes_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            parameter_dict = {
                "name": self.parameter_name.text(),
                "symbol": self.parameter_symbol.text(),
                "unit": self.parameter_unit.text(),
                "formula": self.parameter_formula.toPlainText(),
                "description": self.parameter_descriprion.toPlainText(),
                "type": "a"
                }
            json_object = json.dumps(parameter_dict, indent = 4)
            with open(cwd + var.complex_parameters_folder + self.parameter_filename.text() + ".json", "w") as outfile:
                outfile.write(json_object)
                
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['complex_parameters_window_save_message'])
            self.msg.setWindowTitle(self.language['complex_parameters_window_save_message_caption'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.show()