import sys, json, os
cwd = os.path.curdir

from css import css
from windows.project.new_project import NewProjectWindow
from windows.project.open_project import OpenProjectWindow
from windows.about.about import AboutWindow
from windows.manual.manual import ManualWindow
from windows.settings.settings import SettingsWindow
from windows.parameters.parameters import ParametersWindow
from windows.parameters.complex_paramateres import ComplexParametersWindow
from windows.methods.methods import Methods

from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QDesktopWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowState(QtCore.Qt.WindowMaximized)
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint)
        #self.setStyleSheet(css.window_background_image)
        language_settings = open(cwd + '/appdata/languages/language.json')
        language_settings_data = json.load(language_settings)
        selected_language = language_settings_data['language']
        language_settings.close()
        language_file = cwd + '/appdata/languages/' + selected_language + '/' + selected_language + '.json'
        selected_language_file = open(language_file)
        self.language = json.load(selected_language_file)
        selected_language_file.close()       
        self.WindowGUI()

    def WindowGUI(self):

        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon(css.srclet_main_window_icon))
        self.setWindowTitle(self.language['main_window_title'])
        self.fileMenu()
        self.centerUserInterface()
        self.show()

    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def fileMenu(self):
        menubar = self.menuBar()
        
        # File:        
        fileMenu = menubar.addMenu(self.language['menu_file'])
        
        # File - Settings:
        settingsAct = QAction(QIcon(css.menu_manual_icon), self.language['menu_file_settings'], self)
        settingsAct.setShortcut('Ctrl+S')
        settingsAct.triggered.connect(self.settingsWindow)
        fileMenu.addAction(settingsAct) 
        
        fileMenu.addSeparator()
        
        # File - Exit:
        exitAct = QAction(QIcon(css.menu_manual_icon), self.language['menu_file_exit'], self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.exitSrclet)
        fileMenu.addAction(exitAct)
        
        # Project:
        fileMenu = menubar.addMenu(self.language['menu_project'])
        
        # Project - New project:
        newProjectAct = QAction(QIcon((css.menu_project_icon)), self.language['menu_project_new_project'], self)
        newProjectAct.setShortcut('Ctrl+N')
        newProjectAct.triggered.connect(self.newProjectWindow)
        fileMenu.addAction(newProjectAct)
        
        # Project - Open existing project:
        openProjectAct = QAction(QIcon((css.menu_project_icon)), self.language['menu_project_open_project'], self)
        openProjectAct.setShortcut('Ctrl+O')
        openProjectAct.triggered.connect(self.openProjectWindow)
        fileMenu.addAction(openProjectAct)
        
        # Customize:
        fileMenu = menubar.addMenu(self.language['menu_customize'])
        
        # Customize - Parameters:
        parametersAct = QAction(QIcon(css.menu_settings_icon), self.language['menu_customize_parameters'], self)
        parametersAct.setShortcut('Ctrl+P')
        parametersAct.triggered.connect(self.parametersWindow)
        fileMenu.addAction(parametersAct)
        
        # Customize - Complex paramateres:
        complexParametersAct = QAction(QIcon(css.menu_settings_icon), self.language['menu_customize_complex_parameters'], self)
        complexParametersAct.setShortcut('Ctrl+R')
        complexParametersAct.triggered.connect(self.complexParametersWindow)
        fileMenu.addAction(complexParametersAct)
        
        # Customize - Methods:
        methodsAct = QAction(QIcon(css.menu_settings_icon), self.language['menu_customize_methods'], self)
        methodsAct.setShortcut('Ctrl+M')
        methodsAct.triggered.connect(self.methodsWindow)
        fileMenu.addAction(methodsAct)

        # Help: 
        fileMenu = menubar.addMenu(self.language['menu_help'])
        
        # Help - About:
        aboutAct = QAction(QIcon(css.menu_about_icon), self.language['menu_help_about'], self)
        aboutAct.setShortcut('Ctrl+A')
        aboutAct.triggered.connect(self.aboutWindow)
        fileMenu.addAction(aboutAct)
        
        # Help - Manual:
        helpAct = QAction(QIcon(css.menu_manual_icon), self.language['menu_help_manual'], self)
        helpAct.setShortcut('F1')
        helpAct.triggered.connect(self.manualWindow)
        fileMenu.addAction(helpAct)

    # File:
    def settingsWindow(self):
        self.window = SettingsWindow(self.language)   

    def exitSrclet(self):
        mainApication.quit()
        
    # Project:
    def newProjectWindow(self):
        self.window = NewProjectWindow(self.language)

    def openProjectWindow(self):
        self.window = OpenProjectWindow(self.language)
        
    # Customize:
    def parametersWindow(self):
        self.window = ParametersWindow(self.language)
        
    def complexParametersWindow(self):
        self.window = ComplexParametersWindow(self.language)
        
    def methodsWindow(self):
        self.window = Methods(self.language)
        
    # Help:
    def aboutWindow(self):
        self.window = AboutWindow(self.language)

    def manualWindow(self):
        self.window = ManualWindow(self.language)  

if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(mainApplication.exec_())
