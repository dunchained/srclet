import os, json
from appdata import css

from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QGridLayout, QLabel, QFileDialog
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QPushButton, QGroupBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class DataWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.WindowGUI()
        
    def WindowGUI(self):
        self.grid = QGridLayout()
        self.grid.addWidget(self.loadAndCheckData(), 0, 0, 1, 1)
        self.grid.addWidget(self.loadAndCheckData(), 0, 1, 1, 1)
        self.grid.addWidget(self.loadAndCheckData(), 0, 2, 1, 1)
        self.grid.addWidget(self.loadAndCheckData(), 1, 0, 1, 3)
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())    

    def loadAndCheckData(self):
        groupBox = QGroupBox('project data file...')
        buttonBrowse = QPushButton('Browse')
        buttonBrowse.clicked.connect(self.buttonBrowse)
        vbox = QVBoxLayout()
        vbox.addWidget(buttonBrowse)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox
  
    def buttonBrowse(self):
        pass