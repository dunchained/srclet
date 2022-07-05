# python standard modules
import imp
from re import I
from sqlite3 import paramstyle
import sys, json, os

# app modules and windows
#from appdata import css

# pyqt5 modules
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QPushButton, QLineEdit
from PyQt5.QtWidgets import QMessageBox, QApplication, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class AddParameter(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.WindowGUI()

    def WindowGUI(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('Add new parameter')
        #self.setWindowIcon(QIcon(css.menu_about_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.addParameterGroupBox())
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def addParameterGroupBox(self):
        RightGroupBox = QGroupBox('Parameters definition:')
        self.text_parameter_filename = QLabel('Filename:')
        self.text_parameter_filename1 = QLabel('Text to be used as file name:')
        self.parameter_filename = QLineEdit()
        
        self.text_parameter_name = QLabel('Parameter name:')
        self.text_parameter_name1 = QLabel('Text to be used as parameter name in computations.')
        self.parameter_name = QLineEdit()
        
        self.text_parameter_unit = QLabel('Parameter unit:')
        self.parameter_unit = QLineEdit()
        
        self.text_parameter_descriprion = QLabel('Parameter description:')
        self.text_parameter_descriprion1 = QLabel('To be used as hoover explinations.')
        self.parameter_descriprion = QTextEdit()
        
        buttonSaveProject = QPushButton('Add parameter')
        buttonSaveProject.clicked.connect(self.add_parameter)
        buttonCancel = QPushButton('Cancel')
        buttonCancel.clicked.connect(self.close)
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_parameter_filename)
        layout.addWidget(self.text_parameter_filename1)
        layout.addWidget(self.parameter_filename)
        
        layout.addWidget(self.text_parameter_name)
        layout.addWidget(self.text_parameter_name1)
        layout.addWidget(self.parameter_name)
        
        layout.addWidget(self.text_parameter_unit)
        layout.addWidget(self.parameter_unit)
        
        layout.addWidget(self.text_parameter_descriprion)
        layout.addWidget(self.text_parameter_descriprion1)
        layout.addWidget(self.parameter_descriprion)
        
        layout.addWidget(buttonSaveProject)
        layout.addWidget(buttonCancel)
        layout.addStretch(1)
        RightGroupBox.setLayout(layout)
        
        return RightGroupBox
    
    def add_parameter(self):
        
        if not self.parameter_filename.text() and not self.parameter_unit.text() and not self.parameter_name.text():
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
            self.msg.buttonClicked.connect(self.message_box_success)
            self.msg.show()
            
    def message_box_success(self):
        self.close()

            
    
   
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = AddParameter()
    sys.exit(mainApplication.exec_())