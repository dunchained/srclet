# python standard modules
import sys, json, os
from pathlib import Path
cwd = os.path.curdir

# app modules and windows
#from css import css, var
eto_methods_folder = '/methods/eto/'
parameters_folder = '/parameters/basic/'
complex_parameters_folder = '/parameters/complex/'


# pyqt5 modules
from PyQt5.QtWidgets import QVBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QPushButton
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

class AddETOMethod(QWidget):
    clicked = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = {
            "//": "Insert Special Character Window",
            "insert_character_window_title": "Insert special character...",
            "insert_character_window_btn_cancel": "Close",
            "":""
        }
        self.WindowGUI()

    def WindowGUI(self):
        self.setFixedSize(600, 400)
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle(self.language['insert_character_window_title'])
        #self.setWindowIcon(QIcon(css.menu_about_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.addMethodGroupBoxLeft(), 0, 0)
        self.grid.addWidget(self.addMethodGroupBoxDown(), 1, 0, 1, 2)
        #self.grid.addWidget(a0, row, column, rowSpan, columnSpan)
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def addMethodGroupBoxLeft(self):
        self.scrollLayout = QGridLayout()
        self.parameters_scroll = QWidget()
        self.json_path = os.path.join(cwd + '/appdata/characters/special_characters.json')
        with open(self.json_path) as json_file:
            characters = json.load(json_file)
        
        self.columns = 5
        if len(characters.items()) % 5 == 0:
            self.rows = len(characters.items()) // 5
        else:
            self.rows = len(characters.items()) // 5 + 1
        
        self.button_list = []
        for key, value in characters.items():
            self.button_list.append(value)
        
        i = 0
        for row in range(self.rows):
            for column in range(self.columns):
                button = QPushButton(f'{self.button_list[i]}', self)
                #button.clicked.connect(partial(self.oncliced, self.button_list[i]))
                self.scrollLayout.addWidget(button, row+1, column)
                i += 1
                if i == len(self.button_list): break
        self.parameters_scroll.setLayout(self.scrollLayout)
        
        scroll = QScrollArea()
        scroll.setWidget(self.parameters_scroll)
        scroll.setWidgetResizable(1)

        
        return scroll
    
    def onStateChangeBasicParameters(self):
        change = self.sender().title()
        #change = change.title()
        if change not in self.basic_parameters_list:
            self.basic_parameters_list.append(change)
        else:
            if change in self.basic_parameters_list:
                self.basic_parameters_list.remove(change)
        
        print(self.basic_parameters_list)
    
    def addMethodGroupBoxDown(self):
        groupBox = QGroupBox()
        buttonCancel = QPushButton(self.language['insert_character_window_btn_cancel'])
        buttonCancel.clicked.connect(self.close)
        
        layout = QVBoxLayout()
        
        layout.addWidget(buttonCancel)
        layout.addStretch(1)
        
        groupBox.setLayout(layout)
        
        return groupBox
           
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = AddETOMethod()
    sys.exit(mainApplication.exec_())