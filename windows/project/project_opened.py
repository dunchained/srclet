import sys, os, json
from pathlib import Path
from css import css
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QDesktopWidget
from PyQt5.QtWidgets import QPushButton, QGridLayout, QListWidget, QGroupBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit

from windows.project.project_opened_calc import CalculateWidget

class ProjectWindow(QMainWindow):
    def __init__(self, project_path, language):
        super().__init__()
        self.language = language
        self.project_path = project_path
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.showMaximized()
        self.setWindowTitle(self.project_path)
        self.setWindowIcon(QIcon(css.srclet_main_window_icon))
        self.centerUserInterface()
        self.fileMenu()
        self.central_widget = CalculateWidget(project_path=self.project_path, language=language)
        self.setCentralWidget(self.central_widget)
        self.show()

    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def fileMenu(self):
        menubar = self.menuBar()
        #menubar.setStyleSheet(css.menu_background_image)
        fileMenu = menubar.addMenu('File')
        exitAct = QAction(QIcon(css.menu_exit_icon), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.exitSrclet)
        fileMenu.addAction(exitAct)

    def exitSrclet(self):
        self.hide()
        
  

#if __name__ == '__main__':
 #   mainApplication = QApplication(sys.argv)
  #  mainWindow = ProjectWindow()
   # sys.exit(mainApplication.exec_())
