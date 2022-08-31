import sys, json, os
cwd = os.path.curdir

from variables import css, var
from windows.project.new_project import NewProjectWindow
from windows.project.open_project import OpenProjectWindow
from windows.about.about import AboutWindow
from windows.manual.manual import ManualWindow
from windows.settings.settings import SettingsWindow
from windows.parameters.parameters import ParametersWindow
from windows.parameters.complex_paramateres import ComplexParametersWindow
from windows.methods.methods_eto import ETOMethodsWindow
from windows.methods.methods_wb import WBMethodsWindow
from windows.methods.methods_other import OtherMethodsWindow
from widgets.image_widget import ImageWidget
from mortys.language_morty import language
from mortys.font_morty import read_menu_font_size
from mortys.icon_morty import icon_size

from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QDesktopWidget, QMenu
from PyQt5.QtWidgets import QProxyStyle, QStyle, QToolTip

class MyProxyStyle(QProxyStyle):
    pass
    def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):

        if QStyle_PixelMetric == QStyle.PM_SmallIconSize:
            return icon_size()
        else:
            return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowState(QtCore.Qt.WindowMaximized)
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint)
        self.language = language()
        self.WindowGUI()

    def WindowGUI(self):

        self.setMinimumSize(1024, 768)
        self.setWindowIcon(QIcon(css.srclet_icon))
        self.setWindowTitle(self.language['main_window_title'])
        self.fileMenu()
        self.centerUserInterface()
        self.central_widget = ImageWidget()
        self.setCentralWidget(self.central_widget)
        self.show()

    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def fileMenu(self):
        menubar = self.menuBar()
        font = menubar.font()
        font.setPointSize(read_menu_font_size())
        menubar.setFont(font)
        
        # File:        
        fileMenu = menubar.addMenu(self.language['menu_file'])
        font = fileMenu.font()
        font.setPointSize(read_menu_font_size())
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # File - Settings:
        settingsAct = QAction(QIcon(css.settings_icon), self.language['menu_file_settings'], self)
        settingsAct.setShortcut('Ctrl+S')
        settingsAct.setToolTip(self.language['menu_file_settings_tooltip'])
        settingsAct.triggered.connect(self.settingsWindow)
        fileMenu.addAction(settingsAct) 
        
        fileMenu.addSeparator()

        # File - Exit:
        exitAct = QAction(QIcon(css.exit_icon), self.language['menu_file_exit'], self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setToolTip(self.language['menu_file_exit_tooltip'])
        exitAct.triggered.connect(self.exitSrclet)
        fileMenu.addAction(exitAct)
        
        # Project:
        fileMenu = menubar.addMenu(self.language['menu_project'])
        font = fileMenu.font()
        font.setPointSize(read_menu_font_size())
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # Project - New project:
        newProjectAct = QAction(QIcon((css.new_project_icon)), self.language['menu_project_new_project'], self)
        newProjectAct.setShortcut('Ctrl+N')
        newProjectAct.setToolTip(self.language['menu_project_new_project_tooltip'])
        newProjectAct.triggered.connect(self.newProjectWindow)
        fileMenu.addAction(newProjectAct)
        
        # Project - Open existing project:
        openProjectAct = QAction(QIcon((css.open_project_icon)), self.language['menu_project_open_project'], self)
        openProjectAct.setShortcut('Ctrl+O')
        openProjectAct.setToolTip(self.language['menu_project_open_project_tooltip'])
        openProjectAct.triggered.connect(self.openProjectWindow)
        fileMenu.addAction(openProjectAct)
        
        # Customize:
        fileMenu = menubar.addMenu(self.language['menu_customize'])
        font = fileMenu.font()
        font.setPointSize(read_menu_font_size())
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # Customize - Parameters:
        parameters_menu = QMenu(self.language['menu_customize_parameters'], self)
        parameters_menu.setIcon(QIcon(css.parameters_icon))
        font = parameters_menu.font()
        font.setPointSize(read_menu_font_size())
        parameters_menu.setFont(font)
        parameters_menu.setToolTipsVisible(True)
        
        parametersAct = QAction(QIcon(css.parameters_basic_icon), self.language['menu_customize_basic_parameters'], self)
        parametersAct.setShortcut('Ctrl+B')
        parametersAct.setToolTip(self.language['menu_customize_basic_parameters_tooltip'])
        parametersAct.triggered.connect(self.parametersWindow)
        parameters_menu.addAction(parametersAct)
        
        complexParametersAct = QAction(QIcon(css.parameters_complex_icon), self.language['menu_customize_complex_parameters'], self)
        complexParametersAct.setShortcut('Ctrl+R')
        complexParametersAct.setToolTip(self.language['menu_customize_complex_parameters_tooltip'])
        complexParametersAct.triggered.connect(self.complexParametersWindow)
        parameters_menu.addAction(complexParametersAct)

        fileMenu.addMenu(parameters_menu)
        
        # Customize - Methods:
        methods_menu = QMenu(self.language['menu_customize_methods'], self)
        methods_menu.setIcon(QIcon(css.methods_icon))
        font = methods_menu.font()
        font.setPointSize(read_menu_font_size())
        methods_menu.setFont(font)
        methods_menu.setToolTipsVisible(True)
                
        etoAct = QAction(QIcon(css.methods_eto_icon), self.language['menu_customize_methods_eto'], self)
        etoAct.triggered.connect(self.etoMethodsWindow)
        etoAct.setShortcut('Ctrl+E')
        etoAct.setToolTip(self.language['menu_customize_methods_eto_tooltip'])
        methods_menu.addAction(etoAct)

        wbAct = QAction(QIcon(css.methods_wb_icon), self.language['menu_customize_methods_wb'], self)
        wbAct.triggered.connect(self.wbMethodsWindow)
        wbAct.setShortcut('Ctrl+W')
        wbAct.setToolTip(self.language['menu_customize_methods_wb_tooltip'])
        methods_menu.addAction(wbAct)

        otherAct = QAction(QIcon(css.methods_others_icon), self.language['menu_customize_methods_others'], self)
        otherAct.triggered.connect(self.otherMethodsWindow)
        otherAct.setShortcut('Ctrl+T')
        otherAct.setToolTip(self.language['menu_customize_methods_others_tooltip'])
        methods_menu.addAction(otherAct)
        
        fileMenu.addMenu(methods_menu)
        
        # Help: 
        fileMenu = menubar.addMenu(self.language['menu_help'])
        font = fileMenu.font()
        font.setPointSize(read_menu_font_size())
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # Help - About:
        aboutAct = QAction(QIcon(css.about_icon), self.language['menu_help_about'], self)
        aboutAct.setShortcut('Ctrl+A')
        aboutAct.setToolTip(self.language['menu_help_about_tooltip'])
        aboutAct.triggered.connect(self.aboutWindow)
        fileMenu.addAction(aboutAct)
        
        # Help - Manual:
        helpAct = QAction(QIcon(css.manual_icon), self.language['menu_help_manual'], self)
        helpAct.setShortcut('F1')
        helpAct.setToolTip(self.language['menu_help_manual_tooltip'])
        helpAct.triggered.connect(self.manualWindow)
        fileMenu.addAction(helpAct)

    # File:
    def settingsWindow(self):
        self.window = SettingsWindow(self.language)   

    def exitSrclet(self):
        self.close()
        
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
        
    def etoMethodsWindow(self):
        self.window = ETOMethodsWindow(self.language)

    def wbMethodsWindow(self):
        self.window = WBMethodsWindow(self.language)

    def otherMethodsWindow(self):
        self.window = OtherMethodsWindow(self.language)

    # Help:
    def aboutWindow(self):
        self.window = AboutWindow(self.language)

    def manualWindow(self):
        self.window = ManualWindow(self.language)  

if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    myStyle = MyProxyStyle('Plastique') # The proxy style should be based on an existing style, like 'Windows', 'Motif', 'Plastique', 'Fusion', ...
    mainApplication.setStyle(myStyle)
    mainWindow = MainWindow()
    sys.exit(mainApplication.exec_())
