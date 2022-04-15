# python standard modules
import os

# app modules and windows
from appdata import css

# pyqt5 modules
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QGridLayout, QLabel, QFileDialog, QPushButton, QGroupBox
from PyQt5.QtWidgets import QMessageBox, QComboBox, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QLineF, Qt

class OpenProjectWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.WindowGUI()

    def WindowGUI(self):
        self.setFixedSize(400, 300)
        self.setWindowTitle('Open Existing Project')
        self.setWindowIcon(QIcon(css.menu_about_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.listOfProjects())
        self.grid.addWidget(self.doSomethingWithProject())
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def listOfProjects(self):
        groupBox = QGroupBox('List of existing Projects...')
        self.combo_box = QComboBox()
        self.combo_box.addItems(next(os.walk(os.path.curdir + '/projects/'))[1])
        vbox = QVBoxLayout()
        vbox.addWidget(self.combo_box)
        groupBox.setLayout(vbox)
        return groupBox

    def doSomethingWithProject(self):
        groupBox = QGroupBox('Save project...')
        buttonOpenProject = QPushButton('Open selected project')
        buttonOpenProject.clicked.connect(self.openProject)
        buttonDeleteProject = QPushButton('Delete selected project')
        buttonDeleteProject.clicked.connect(self.deleteProject)
        buttonCancel = QPushButton('Cancel')
        buttonCancel.clicked.connect(self.close)
        vbox = QVBoxLayout()
        vbox.addWidget(buttonOpenProject)
        vbox.addWidget(buttonDeleteProject)
        vbox.addWidget(buttonCancel)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox
    
    def openProject(self):
        pass
        print(self.combo_box.currentText())

    def deleteProject(self):
        pass