import sys, os, json
from pathlib import Path
from appdata import css
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QDesktopWidget
from PyQt5.QtWidgets import QPushButton, QGridLayout, QListWidget, QGroupBox
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLineEdit

class ProjectWindow(QMainWindow):
    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint)
        self.setStyleSheet(css.window_background_image)
        self.WindowGUI()

    def WindowGUI(self):
        self.setFixedSize(800, 600)
        self.setWindowIcon(QIcon(css.srclet_main_window_icon))
        self.setWindowTitle('Project: ' + self.project_path)
        self.fileMenu()
        self.centerUserInterface()
        self.show()
        self.grid = QGridLayout()
        self.grid.addWidget(self.createLeftGroupBox(), 0, 0, 1, 1)
        self.grid.addWidget(self.createLeftGroupBox(), 0, 1, 1, 1)
        self.grid.addWidget(self.createLeftGroupBox(), 1, 0, -1, 2)
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()

    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def fileMenu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet(css.menu_background_image)
        fileMenu = menubar.addMenu('File')
        exitAct = QAction(QIcon(css.menu_exit_icon), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.exitSrclet)
        fileMenu.addAction(exitAct)

    def exitSrclet(self):
        self.hide()

    def createLeftGroupBox(self):
        groupBox = QGroupBox()
        
        self.text_save_project = QLabel('Enter new project name:')
        self.project_name = QLineEdit()
        
        buttonSaveProject = QPushButton('Create project')
        buttonSaveProject.clicked.connect(self.close)
        
        buttonCancel = QPushButton('Cancel')
        buttonCancel.clicked.connect(self.close)
       
        vbox = QVBoxLayout()
        vbox.addWidget(self.text_save_project)
        vbox.addWidget(self.project_name)
        vbox.addWidget(buttonSaveProject)
        vbox.addWidget(buttonCancel)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        
        return groupBox

if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = ProjectWindow()
    sys.exit(mainApplication.exec_())
