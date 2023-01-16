import sys, os, json
from pathlib import Path
from variables import css
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QDesktopWidget
from PyQt5.QtWidgets import QPushButton, QGridLayout, QListWidget, QGroupBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
#
from windows.project.project_opened_widget import CalculateWidget

class ProjectWindow(QMainWindow):
    def __init__(self, project_path, language):
        super().__init__()
        self.language = language
        self.project_path = project_path
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(800, 600)
        #self.showMaximized()
        self.project_title = self.project_path.split('/')[-1]
        self.setWindowTitle(self.language['project_opened_title'] + self.project_title)
        #self.setWindowIcon(QIcon(css.open_project_icon))
        self.center_gui()
        self.file_menu()
        self.central_widget = CalculateWidget(project_path=self.project_path, language=language)
        self.setCentralWidget(self.central_widget)
        self.show()

    def center_gui(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def file_menu(self):
        menubar = self.menuBar()
        #menubar.setStyleSheet(css.menu_background_image)
        fileMenu = menubar.addMenu(self.language['project_opened_menu_file'])
        exitAct = QAction(QIcon(css.menu_exit_icon), self.language['project_opened_menu_exit'], self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.exit_project)
        fileMenu.addAction(exitAct)

    def exit_project(self):
        self.hide()