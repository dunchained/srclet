# python standard modules
import sys, json, os
from pathlib import Path
cwd = os.path.curdir
# pyqt5 modules
from PyQt5.QtWidgets import QVBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QPushButton
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

class CharacterWidget(QWidget):
    clicked = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.language = {
            "//": "Insert Special Character Window",
            "insert_character_window_title": "Insert special character...",
            "insert_character_window_btn_cancel": "Close",
            "":""
        }
        self.window_gui()

    def window_gui(self):
        self.setWindowTitle(self.language['insert_character_window_title'])
        self.grid = QGridLayout()
        self.grid.addWidget(self.insert_special_character_widget(), 0, 0)
        self.setLayout(self.grid)
        self.show()
        
    def insert_special_character_widget(self):
        self.scrollLayout = QGridLayout()
        self.parameters_scroll = QWidget()
        self.json_path = os.path.join(cwd + '/srclet/characters/special_characters.json')
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
           
#if __name__ == '__main__':
   #mainApplication = QApplication(sys.argv)
   #mainWindow = CharacterWidget()
   #sys.exit(mainApplication.exec_())