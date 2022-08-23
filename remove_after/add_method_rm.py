# python standard modules
import sys

# app modules and windows
#from css import css

# pyqt5 modules
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QListView, QPushButton, QApplication
from PyQt5.QtWidgets import QSizePolicy, QLineEdit, QAbstractItemView, QCheckBox, QPlainTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

class AddMethod(QDialog):
    def __init__(self, language):
        super().__init__()
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = language
        self.WindowGUI()

    def WindowGUI(self):
        
        self.setWindowTitle('Add method')
        #self.setWindowIcon(QIcon(css.menu_about_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.createRightGroupBox(), 0, 1, 1, 1)
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def createRightGroupBox(self):
        RightGroupBox = QGroupBox('Method definition:')
        
        self.text_method_name = QLabel('Method name:')
        self.method_name = QLineEdit()
        self.text_method_short = QLabel('Short method name:')
        self.method_short = QLineEdit()
        buttonSaveProject = QPushButton('Add method')
        buttonSaveProject.clicked.connect(self.close)
        buttonCancel = QPushButton('Cancel')
        buttonCancel.clicked.connect(self.close)
        ###
        parameters_Groupbox = QGroupBox('Available paramaters:')
        grid_layout = QGridLayout()
        parameters_Groupbox.setLayout(grid_layout)
        parameters = ['Temp', 'Hum', 'Tmin', 'Tmax', 'n', 'Ta', 'kg', 'cm', 'ta', 'Don\'t use']
        self.rows = 3
        self.columns = 4
        
        len_list = len(parameters)

        i = 0
        for row in range(self.rows): 
           for column in range(self.columns): 
                button = QCheckBox(f'{parameters[i]}', self)
                grid_layout.addWidget(button, row+1, column)
                i += 1
                if i == len_list: break
        ###
        conditions_Groupbox = QGroupBox('Calculation conditions (; separeated):')
        grid_layout = QGridLayout()
        condition_text_area = QPlainTextEdit()
        grid_layout.addWidget(condition_text_area)
        conditions_Groupbox.setLayout(grid_layout)
        ###
        formula_Groupbox = QGroupBox('Calculation formula:')
        grid_layout = QGridLayout()
        formula_text_area = QPlainTextEdit()
        grid_layout.addWidget(formula_text_area)
        formula_Groupbox.setLayout(grid_layout)
        ###
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_method_name)
        layout.addWidget(self.method_name)
        layout.addWidget(self.text_method_short)
        layout.addWidget(self.method_short)
        layout.addWidget(parameters_Groupbox)
        layout.addWidget(conditions_Groupbox)        
        layout.addWidget(formula_Groupbox)
        layout.addWidget(buttonSaveProject)
        layout.addWidget(buttonCancel)
        layout.addStretch(1)
        RightGroupBox.setLayout(layout)
        
        return RightGroupBox
    