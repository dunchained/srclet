from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QProxyStyle, QStyle, QToolTip
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QDesktopWidget, QMenu
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QDesktopServices
from mortys.icon_morty import icon_size
from mortys.font_morty import read_menu_font_size
from mortys.language_morty import language
from widgets.image_widget import ImageWidget
from remove_after.methods_other import OtherMethodsWindow
from remove_after.methods_wb import WBMethodsWindow
from windows.settings.settings import SettingsWindow
from windows.manual.manual import ManualWindow
from windows.about.about import AboutWindow
from windows.project.new_project import NewProjectWindow
from variables import css, var
import sys
import os
cwd = os.path.curdir

# from windows.project.open_project import OpenProjectWindow
# from windows.parameters.basic_parameters import BasicParameters
# from windows.parameters.complex_parameters import ComplexParameters
# from remove_after.methods_eto import ETOMethodsWindow


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
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint)
        self.language = language()
        self.window_gui()

    def window_gui(self):
        self.setMinimumSize(var.srclet_window_min_widith,
                            var.srclet_window_min_height)
        self.setWindowIcon(QIcon(css.srclet_icon))
        self.setWindowTitle(self.language['main_window_title'])
        self.fileMenu()
        self.center_gui()
        self.central_widget = ImageWidget()
        self.setCentralWidget(self.central_widget)
        self.show()

    def center_gui(self):
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
        settingsAct = QAction(QIcon(css.settings_icon),
                              self.language['menu_file_settings'], self)
        settingsAct.setShortcut('Ctrl+S')
        settingsAct.setToolTip(self.language['menu_file_settings_tooltip'])
        settingsAct.triggered.connect(self.settings_window)
        fileMenu.addAction(settingsAct)

        fileMenu.addSeparator()

        # File - Exit:
        exitAct = QAction(QIcon(css.exit_icon),
                          self.language['menu_file_exit'], self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setToolTip(self.language['menu_file_exit_tooltip'])
        exitAct.triggered.connect(self.exit_srclet)
        fileMenu.addAction(exitAct)

        # Project:
        fileMenu = menubar.addMenu(self.language['menu_project'])
        font = fileMenu.font()
        font.setPointSize(read_menu_font_size())
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # Project - New project:
        newProjectAct = QAction(
            QIcon((css.new_project_icon)), self.language['menu_project_new_project'], self)
        newProjectAct.setShortcut('Ctrl+N')
        newProjectAct.setToolTip(
            self.language['menu_project_new_project_tooltip'])
        newProjectAct.triggered.connect(self.new_project_window)
        fileMenu.addAction(newProjectAct)

        # Project - Open existing project:
        openProjectAct = QAction(
            QIcon((css.open_project_icon)), self.language['menu_project_open_project'], self)
        openProjectAct.setShortcut('Ctrl+O')
        openProjectAct.setToolTip(
            self.language['menu_project_open_project_tooltip'])
        openProjectAct.triggered.connect(self.open_project_window)
        fileMenu.addAction(openProjectAct)

        # Customize:
        fileMenu = menubar.addMenu(self.language['menu_customize'])
        font = fileMenu.font()
        font.setPointSize(read_menu_font_size())
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # Customize - Parameters:
        parameters_menu = QMenu(
            self.language['menu_customize_parameters'], self)
        parameters_menu.setIcon(QIcon(css.parameters_icon))
        font = parameters_menu.font()
        font.setPointSize(read_menu_font_size())
        parameters_menu.setFont(font)
        parameters_menu.setToolTipsVisible(True)

        parametersAct = QAction(QIcon(css.parameters_basic_icon),
                                self.language['menu_customize_basic_parameters'], self)
        parametersAct.setShortcut('Ctrl+B')
        parametersAct.setToolTip(
            self.language['menu_customize_basic_parameters_tooltip'])
        parametersAct.triggered.connect(self.basic_parameters_window)
        parameters_menu.addAction(parametersAct)

        complexParametersAct = QAction(QIcon(
            css.parameters_complex_icon), self.language['menu_customize_complex_parameters'], self)
        complexParametersAct.setShortcut('Ctrl+R')
        complexParametersAct.setToolTip(
            self.language['menu_customize_complex_parameters_tooltip'])
        complexParametersAct.triggered.connect(self.complex_parameters_window)
        parameters_menu.addAction(complexParametersAct)

        fileMenu.addMenu(parameters_menu)

        # Customize - Methods:
        methods_menu = QMenu(self.language['menu_customize_methods'], self)
        methods_menu.setIcon(QIcon(css.methods_icon))
        font = methods_menu.font()
        font.setPointSize(read_menu_font_size())
        methods_menu.setFont(font)
        methods_menu.setToolTipsVisible(True)

        etoAct = QAction(QIcon(css.methods_eto_icon),
                         self.language['menu_customize_methods_eto'], self)
        etoAct.triggered.connect(self.eto_methods_window)
        etoAct.setShortcut('Ctrl+E')
        etoAct.setToolTip(self.language['menu_customize_methods_eto_tooltip'])
        methods_menu.addAction(etoAct)

        wbAct = QAction(QIcon(css.methods_wb_icon),
                        self.language['menu_customize_methods_wb'], self)
        wbAct.triggered.connect(self.wb_methods_window)
        wbAct.setShortcut('Ctrl+W')
        wbAct.setToolTip(self.language['menu_customize_methods_wb_tooltip'])
        methods_menu.addAction(wbAct)

        otherAct = QAction(QIcon(css.methods_others_icon),
                           self.language['menu_customize_methods_others'], self)
        otherAct.triggered.connect(self.other_methods_window)
        otherAct.setShortcut('Ctrl+T')
        otherAct.setToolTip(
            self.language['menu_customize_methods_others_tooltip'])
        methods_menu.addAction(otherAct)

        fileMenu.addMenu(methods_menu)

        # Help:
        fileMenu = menubar.addMenu(self.language['menu_help'])
        font = fileMenu.font()
        font.setPointSize(read_menu_font_size())
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # Help - About:
        aboutAct = QAction(QIcon(css.about_icon),
                           self.language['menu_help_about'], self)
        aboutAct.setShortcut('Ctrl+A')
        aboutAct.setToolTip(self.language['menu_help_about_tooltip'])
        aboutAct.triggered.connect(self.about_window)
        fileMenu.addAction(aboutAct)

        # Help - Manual:
        helpAct = QAction(QIcon(css.manual_icon),
                          self.language['menu_help_manual'], self)
        helpAct.setShortcut('F1')
        helpAct.setToolTip(self.language['menu_help_manual_tooltip'])
        helpAct.triggered.connect(self.manual_window)
        fileMenu.addAction(helpAct)

    # File:
    def settings_window(self):
        self.window_settings = SettingsWindow(self.language)

    def exit_srclet(self):
        mainApplication.quit()
        # self.close()

        # self.window_basic_parameters.close()

    # Project:
    def new_project_window(self):
        self.window = NewProjectWindow(self.language)

    def open_project_window(self):
        pass
        # self.window = OpenProjectWindow(self.language)

    # Customize:
    def basic_parameters_window(self):
        pass
        # self.window_basic_parameters = BasicParameters()

    def complex_parameters_window(self):
        pass
        # self.window = ComplexParameters()

    def eto_methods_window(self):
        pass
        # self.window = ETOMethodsWindow(self.language)

    def wb_methods_window(self):
        self.window = WBMethodsWindow(self.language)

    def other_methods_window(self):
        self.window = OtherMethodsWindow(self.language)

    # Help:
    def about_window(self):
        self.window = AboutWindow(self.language)

    def manual_window(self):
        # self.window = ManualWindow(self.language)
        QDesktopServices.openUrl(QUrl(
            'https://www.youtube.com/watch?v=ECTLzJow1Wo&list=PLBO2iP5zSYD7CbGOXEnMsUoWSkyxRsXTd'))


if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    myStyle = MyProxyStyle('Plastique')
    # The proxy style should be based on an existing style, like 'Windows',
    # 'Motif', 'Plastique', 'Fusion', ...
    mainApplication.setStyle(myStyle)
    mainWindow = MainWindow()
    sys.exit(mainApplication.exec_())
