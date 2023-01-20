import sys, json, os
cwd = os.path.curdir

from PyQt5 import QtCore
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication
from proba import ParametersCategoryTabs

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowState(QtCore.Qt.WindowMaximized)
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint)
        self.window_gui()

    def window_gui(self):
        self.setMinimumSize(800, 600)
        self.setWindowTitle('main_window_title')
        self.fileMenu()
        self.central_widget = ParametersCategoryTabs()
        self.setCentralWidget(self.central_widget)
        self.show()

    def fileMenu(self):
        menubar = self.menuBar()
        font = menubar.font()
        font.setPointSize(14)
        menubar.setFont(font)
        
        # File:        
        fileMenu = menubar.addMenu('File')
        font = fileMenu.font()
        font.setPointSize(14)
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # File - Settings:
        settingsAct = QAction('menu_file_settings', self)
        settingsAct.setShortcut('Ctrl+S')
        settingsAct.triggered.connect(self.settings_window)
        fileMenu.addAction(settingsAct)
        
    # File:
    def settings_window(self):
        self.takeCentralWidget()
        self.novi = ParametersCategoryTabs()
        self.setCentralWidget(self.novi)

   
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(mainApplication.exec_())
