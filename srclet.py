import sys, json

from appdata import css
from windows.project.new_project import NewProjectWindow
from windows.project.open_project import OpenProjectWindow
from windows.about.about import AboutWindow
from windows.manual.manual import ManualWindow
from windows.settings.settings import SettingsWindow
from windows.settings.language import LanguageWindow
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
        #self.setStyleSheet(css.window_background_image)
        language_settings = open('settings.json')
        language_settings_data = json.load(language_settings)
        selected_language = language_settings_data['language']
        language_settings.close()
        language_file = 'appdata/languages/' + selected_language + '/' + selected_language + '.json'
        selected_language_file = open(language_file)
        self.language = json.load(selected_language_file)
        selected_language_file.close()       
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
        menubar = self.menuBar()
        fileMenu = menubar.addMenu(self.language['menu_project'])
        projectAct = QAction(QIcon((css.menu_project_icon)), self.language['menu_project_new_project'], self)
        projectAct.setShortcut('Ctrl+N')
        projectAct.triggered.connect(self.newProjectWindow)
        fileMenu.addAction(projectAct)
        projectAct = QAction(QIcon((css.menu_project_icon)), self.language['menu_project_open_project'], self)
        projectAct.setShortcut('Ctrl+O')
        projectAct.triggered.connect(self.openProjectWindow)
        fileMenu.addAction(projectAct)

        fileMenu = menubar.addMenu(self.language['menu_customize'])
        parametersAct = QAction(QIcon(css.menu_settings_icon), self.language['menu_customize_create_parameter'], self)
        parametersAct.setShortcut('Crtl + P')
        parametersAct.triggered.connect(self.parametersWindow)
        fileMenu.addAction(parametersAct)
        methodsAct = QAction(QIcon(css.menu_settings_icon), self.language['menu_customize_create_complex_parameter'], self)
        methodsAct.setShortcut('Ctrl + M')
        methodsAct.triggered.connect(self.methodsWindow)
        fileMenu.addAction(methodsAct)
        settingsAct = QAction(QIcon(css.menu_settings_icon), self.language['menu_customize_create_method'], self)
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

        fileMenu = menubar.addMenu('Settings')
        languageAct = QAction(QIcon(css.menu_manual_icon), 'Language', self)
        languageAct.triggered.connect(self.languageWindow)
        fileMenu.addAction(languageAct) 
       

    def exitSrclet(self):
        mainApication.quit()

    def newProjectWindow(self):
        self.window = NewProjectWindow(self.language)

    def openProjectWindow(self):
        self.window = OpenProjectWindow(self.language)

    def settingsWindow(self):
        self.window = SettingsWindow(self.language)

    def languageWindow(self):
        self.window = LanguageWindow(self.language)

    def aboutWindow(self):
        self.window = AboutWindow(self.language)

    def manualWindow(self):
        self.window = ManualWindow(self.language)
        
    def parametersWindow(self):
        self.window = Parameters(self.language)
        
    def methodsWindow(self):
        self.window = Methods(self.language)

if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(mainApplication.exec_())
