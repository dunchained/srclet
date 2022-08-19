import sys

from appdata import css
from windows.project.new_project import NewProjectWindow
from windows.project.open_project import OpenProjectWindow
from windows.about.about import AboutWindow
from windows.manual.manual import ManualWindow
from windows.settings.settings import SettingsWindow
from windows.parameters.parameters import Parameters
from windows.methods.methods import Methods

from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QDesktopWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint)
        self.setStyleSheet(css.window_background_image)
        self.WindowGUI()

    def WindowGUI(self):

        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon(css.srclet_main_window_icon))
        self.setWindowTitle(css.srclet_main_window_title)
        self.fileMenu()
        self.centerUserInterface()
        self.show()

    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def fileMenu(self):
        self.ime_projekta = 'Projekat'
        menubar = self.menuBar()
        fileMenu = menubar.addMenu(self.ime_projekta)
        projectAct = QAction(QIcon((css.menu_project_icon)), 'New Project', self)
        projectAct.setShortcut('Ctrl+N')
        projectAct.triggered.connect(self.newProjectWindow)
        fileMenu.addAction(projectAct)
        projectAct = QAction(QIcon((css.menu_project_icon)), 'Open Existing Project', self)
        projectAct.setShortcut('Ctrl+O')
        projectAct.triggered.connect(self.openProjectWindow)
        fileMenu.addAction(projectAct)

        fileMenu = menubar.addMenu('Customize')
        parametersAct = QAction(QIcon(css.menu_settings_icon), 'Create parameter', self)
        parametersAct.setShortcut('Crtl + P')
        parametersAct.triggered.connect(self.parametersWindow)
        fileMenu.addAction(parametersAct)
        methodsAct = QAction(QIcon(css.menu_settings_icon), 'Create complex parameter', self)
        methodsAct.setShortcut('Ctrl + M')
        methodsAct.triggered.connect(self.methodsWindow)
        fileMenu.addAction(methodsAct)
        settingsAct = QAction(QIcon(css.menu_settings_icon), 'Create method', self)
        settingsAct.setShortcut('Ctrl+S')
        settingsAct.triggered.connect(self.settingsWindow)
        fileMenu.addAction(settingsAct)

        fileMenu = menubar.addMenu('Help')
        aboutAct = QAction(QIcon(css.menu_about_icon), 'About', self)
        aboutAct.setShortcut('Ctrl+A')
        aboutAct.triggered.connect(self.aboutWindow)
        fileMenu.addAction(aboutAct)
        helpAct = QAction(QIcon(css.menu_manual_icon), 'Manual', self)
        helpAct.setShortcut('F1')
        helpAct.triggered.connect(self.manualWindow)
        fileMenu.addAction(helpAct)
       

    def exitSrclet(self):
        mainApication.quit()

    def newProjectWindow(self):
        self.window = NewProjectWindow()

    def openProjectWindow(self):
        self.window = OpenProjectWindow()

    def settingsWindow(self):
        self.window = SettingsWindow()

    def aboutWindow(self):
        self.window = AboutWindow()

    def manualWindow(self):
        self.window = ManualWindow()
        
    def parametersWindow(self):
        self.window = Parameters()
        
    def methodsWindow(self):
        self.window = Methods()

if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(mainApplication.exec_())
