# python standard modules
import sys

# app modules and windows
#from css import css

# pyqt5 modules
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QDesktopWidget, QGridLayout
from PyQt5.QtWidgets import QCheckBox, QGroupBox, QLabel, QListView, QPushButton, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class Methods(QDialog):
    def __init__(self, language):
        super().__init__()
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = language
        self.WindowGUI()

    def WindowGUI(self):
        
        self.setWindowTitle('Methods')
        #self.setWindowIcon(QIcon(css.menu_about_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.createTopLeftGroupBox(), 0, 0, 1, 1)
        self.grid.addWidget(self.createTopRightGroupBox(), 0, 1, 1, 1)
        self.grid.addWidget(self.createDownLeftGroupBox(), 1, 0, 1, 1)
        self.grid.addWidget(self.createDownRightGroupBox(), 1, 1, 1, 1)
        self.grid.addWidget(self.createDownGroupBox(), 2, 0, 1, 2)
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def createTopLeftGroupBox(self):
        LeftGroupBox = QGroupBox('Data and station information:')
        
        
        return LeftGroupBox
    
    def createDownLeftGroupBox(self):
        LeftGroupBox = QGroupBox('Calculation options:')
       
        
        return LeftGroupBox
    
    def createTopRightGroupBox(self):
        RightGroupBox = QGroupBox('Calculate:')
 
        ###
        et_Groupbox = QGroupBox('Evapotranspiration methods:')
        grid_layout = QGridLayout()
        et_Groupbox.setLayout(grid_layout)
        parameters = ['Method1', 'Method2', 'Method3', 'Method4']
        self.rows = 1
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
        ###
        swb_Groupbox = QGroupBox('SWB methods:')
        grid_layout = QGridLayout()
        swb_Groupbox.setLayout(grid_layout)
        parameters = ['Method1', 'Method2', 'Method3', 'Method4']
        self.rows = 1
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
        ###
        hm_Groupbox = QGroupBox('Hydromodule methods:')
        grid_layout = QGridLayout()
        hm_Groupbox.setLayout(grid_layout)
        parameters = ['Method1', 'Method2', 'Method3', 'Method4']
        self.rows = 1
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
        ###
        s_Groupbox = QGroupBox('Stat methods:')
        grid_layout = QGridLayout()
        s_Groupbox.setLayout(grid_layout)
        parameters = ['Method1', 'Method2', 'Method3', 'Method4']
        self.rows = 1
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
        
        layout = QVBoxLayout()
        layout.addWidget(et_Groupbox)
        layout.addWidget(swb_Groupbox)
        layout.addWidget(hm_Groupbox)
        layout.addWidget(s_Groupbox)
       
        layout.addStretch(1)
        RightGroupBox.setLayout(layout)
        
        return RightGroupBox
    
    def createDownRightGroupBox(self):
        RightGroupBox = QGroupBox('Results options:')
        
                
        return RightGroupBox
    
    def createDownGroupBox(self):
        DownGroupBox = QGroupBox()
        
        buttonClose = QPushButton('Close')
        buttonClose.clicked.connect(self.close)
        buttonRefresh = QPushButton('Calculate')
        buttonRefresh.clicked.connect(self.close)
        buttonAddParameter = QPushButton('Calculate & Save')
        buttonAddParameter.clicked.connect(self.close)
        
        layout = QHBoxLayout()
        layout.addWidget(buttonAddParameter)
        layout.addWidget(buttonRefresh)
        layout.addWidget(buttonClose)
        
        
        layout.setAlignment(Qt.AlignRight)
        layout.addStretch(1)
        DownGroupBox.setLayout(layout)
        
        return DownGroupBox

#obrisati nakon uvezivanja cijelog
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = Methods()
    sys.exit(mainApplication.exec_())