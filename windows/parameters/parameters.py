# python standard modules
from concurrent.futures import process
from importlib.resources import path
import sys, os, json
from pathlib import Path

# app modules and windows
from appdata import css
from windows.parameters.add_parameter import AddParameter

# pyqt5 modules
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QListView, QPushButton, QApplication
from PyQt5.QtWidgets import QLineEdit, QListWidget, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

class Parameters(QDialog):
    def __init__(self, language):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = language
        self.WindowGUI()

    def WindowGUI(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('Parameters')
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
        LeftGroupBox = QGroupBox('Parameters used for calucation:')
        self.list_widget = QListWidget()
        get_files = next(os.walk(os.path.curdir + "/parameters/"), (None, None, []))[2]
        self.file_list = []
        for file in get_files:
            self.file_list.append(Path(file).stem)
        self.list_widget.addItems(self.file_list)
        self.list_widget.currentItemChanged.connect(self.index_changed)
        buttonRefresh = QPushButton('Refresh parameter list')
        buttonRefresh.clicked.connect(self.refresh_parameters_list)
        buttonAddParameter = QPushButton('Add new parameter')
        buttonAddParameter.clicked.connect(self.newParameterWindow)
        buttonDelete = QPushButton('Delete selected parameter')
        buttonDelete.clicked.connect(self.delete_parameter)

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(buttonRefresh)
        layout.addWidget(buttonAddParameter)
        layout.addWidget(buttonDelete)
        layout.addStretch(1)
        LeftGroupBox.setLayout(layout)
        
        return LeftGroupBox
    
    def index_changed(self, i):
        self.json_path = 'parameters/' + i.text() + '.json'
       
        with open(self.json_path) as json_file:
            data = json.load(json_file)
            self.parameter_filename.setText(i.text())
            self.parameter_name.setText(data["name"])
            self.parameter_unit.setText(data["unit"])
            self.parameter_descriprion.setText(data["description"])

    def delete_parameter(self):
        list_items = self.list_widget.selectedItems()
        if not list_items: return
        for item in list_items:
            self.list_widget.takeItem(self.list_widget.row(item))
        os.remove('parameters/' + item.text() + '.json')
            
    def refresh_parameters_list(self):
        get_files = next(os.walk(os.path.curdir + "/parameters/"), (None, None, []))[2]
        self.file_list_update = []
        for file in get_files:
            if Path(file).stem in self.file_list:
                pass
            else:
                self.file_list_update.append(Path(file).stem)
        
        self.list_widget.addItems(self.file_list_update)
    
    def createRightGroupBox(self):
        RightGroupBox = QGroupBox('Parameters definition:')
        self.text_parameter_filename = QLabel('Filename:')
        self.parameter_filename = QLineEdit()
        self.parameter_filename.setEnabled(False)
        self.text_parameter_name = QLabel('Parameter name:')
        self.parameter_name = QLineEdit()
        self.text_parameter_unit = QLabel('Parameter unit:')
        self.parameter_unit = QLineEdit()

        self.text_parameter_descriprion = QLabel('Parameter description:')
        self.parameter_descriprion = QTextEdit()

        buttonSaveProject = QPushButton('Save changes')
        buttonSaveProject.clicked.connect(self.save_changes_parameter)
        buttonCancel = QPushButton('Cancel')
        buttonCancel.clicked.connect(self.close)
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_parameter_filename)
        layout.addWidget(self.parameter_filename)
        layout.addWidget(self.text_parameter_name)
        layout.addWidget(self.parameter_name)
        layout.addWidget(self.text_parameter_unit)
        layout.addWidget(self.parameter_unit)
        layout.addWidget(self.text_parameter_descriprion)
        layout.addWidget(self.parameter_descriprion)
        layout.addWidget(buttonSaveProject)
        layout.addWidget(buttonCancel)
        layout.addStretch(1)
        RightGroupBox.setLayout(layout)
        
        return RightGroupBox
    
    def createDownGroupBox(self):
        DownGroupBox = QGroupBox()
        
        buttonClose = QPushButton('Close')
        buttonClose.clicked.connect(self.close)
        
        layout = QHBoxLayout()
        layout.addWidget(buttonClose)
        layout.setAlignment(Qt.AlignRight)
        layout.addStretch(1)
        DownGroupBox.setLayout(layout)
        
        return DownGroupBox
    
    def newParameterWindow(self):
        self.window = AddParameter()

    def save_changes_parameter(self):
        if not self.parameter_filename and not self.parameter_name.text() and not self.parameter_unit.text():
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText('Parameter name or unit empty...')
            self.msg.setWindowTitle('Missing data...')
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            # ovdje treba još jedan uslov da provjeri da li ima već projekat sa istim imenom
            # poruka da li želite otvoriti kreirani projekat
            parameter_dict = {
                "name": self.parameter_name.text(),
                "unit": self.parameter_unit.text(),
                "description": self.parameter_descriprion.toPlainText()
                }
            json_object = json.dumps(parameter_dict, indent = 4)
            with open(os.path.curdir + "/parameters/" + self.parameter_filename.text() + ".json", "w") as outfile:
                outfile.write(json_object)
                
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText('Parameter saved...')
            self.msg.setWindowTitle('Successuful...')
            self.msg.setStandardButtons(QMessageBox.Ok)
            #self.msg.buttonClicked.connect(self.close)
            self.msg.show()
 
#obrisati nakon uvezivanja cijelog
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = Parameters()
    sys.exit(mainApplication.exec_())