import os, json
from sre_constants import AT_END
from appdata import css

from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QGridLayout, QLabel, QFileDialog
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QPushButton, QGroupBox, QTextEdit
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import Qt


class DataWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.WindowGUI()
        
    def WindowGUI(self):
        self.grid = QGridLayout()
        self.grid.addWidget(self.loadAndCheckData(), 0, 0, 1, 1)
        self.grid.addWidget(self.loadAndCheckMethods(), 0, 1, 1, 1)
        self.grid.addWidget(self.loadAndCheckMonitor(), 0, 2, 1, 1)
        self.grid.addWidget(self.exportAndSave(), 1, 0, 1, 3)
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())    

    def loadAndCheckData(self):
        groupBox = QGroupBox('Load and show data info...')
        buttonBrowse = QPushButton('Neki')
        buttonBrowse.clicked.connect(self.buttonBrowse)
        vbox = QVBoxLayout()
        vbox.addWidget(buttonBrowse)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def loadAndCheckMethods(self):
        groupBox = QGroupBox('Check methods to calculate...')
        buttonBrowse = QPushButton('Tekst')
        buttonBrowse.clicked.connect(self.buttonBrowse)
        vbox = QVBoxLayout()
        vbox.addWidget(buttonBrowse)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def loadAndCheckMonitor(self):
        groupBox = QGroupBox('Log...')
        self.label_console = QTextEdit()
        #label2.setGeometry(200, 250, 100, 50)
        #label2.setStyleSheet("border : 2px solid black;")
        #self.label_console = self.label_console.textCursor()
        #self.label_console.insertText('Haba-haba.')
        self.label_console.setWordWrapMode(True)
        self.label_console.setText('srclet v1:2022')
        #self.label_console.setFocus(QTextCursor.atEnd)
        vbox = QVBoxLayout()
        vbox.addWidget(self.label_console)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def exportAndSave(self):
        groupBox = QGroupBox('Export and Save...')
        buttonBrowse = QPushButton('Saki')
        buttonBrowse.clicked.connect(self.buttonBrowse1)
        vbox = QVBoxLayout()
        vbox.addWidget(buttonBrowse)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox
  
    def buttonBrowse(self):
        #self.label_console.setText(self.label_console.toPlainText() + '\n line 2')
        self.label_console.insertPlainText('linija 2 \n')
        
    def buttonBrowse1(self):
        #self.label_console.setText(self.label_console.toPlainText() + '\n line 2')
        self.label_console.insertPlainText('linija 23 \n')