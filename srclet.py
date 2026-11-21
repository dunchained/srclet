from mortys.language_morty import bind_key
from windows.project.open_project import OpenProjectWindow
from PyQt6.QtWidgets import QProxyStyle, QStyle
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QMenu
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
from mortys.icon_morty import icon_size
from mortys.font_morty import apply_settings, read_menu_font_size
from windows.methods.catalog import MethodCatalog
from windows.parameters.catalog import ParameterCatalog
from mortys.language_morty import language,qt_language
from widgets.image_widget import ImageWidget
from windows.settings.settings import SettingsWindow
from windows.manual.manual import ManualWindow
from windows.about.about import AboutWindow
from windows.project.monthly_import import ProjectImport
from windows.project.project_opened import ProjectWindow
from variables import css, var
import sys
import os
cwd = os.path.curdir
class MyProxyStyle(QProxyStyle):
    pass

    def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):
        if QStyle_PixelMetric == QStyle.PixelMetric.PM_SmallIconSize:
            return icon_size()
        else:
            return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowState(QtCore.Qt.WindowState.WindowMaximized)
        # self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint | QtCore.Qt.WindowType.CustomizeWindowHint)
        qt_language()
        apply_settings()
        self.language = language()
        self.window_gui()

    def window_gui(self):
        self.setMinimumSize(var.srclet_window_min_widith,
                            var.srclet_window_min_height)
        self.setWindowIcon(QIcon(css.srclet_icon))
        bind_key(self, "windowTitle", 'main_window_title')
        self.fileMenu()
        self.center_gui()
        self.central_widget = ImageWidget()
        self.setCentralWidget(self.central_widget)
        self.show()

    def center_gui(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def fileMenu(self):
        menubar = self.menuBar()
        font = menubar.font()
        font.setPointSize(read_menu_font_size())
        menubar.setFont(font)

        # File:
        fileMenu = bind_key(menubar.addMenu(""), "title", 'menu_file')
        font = fileMenu.font()
        font.setPointSize(read_menu_font_size())
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # File - Settings:
        settingsAct = bind_key(QAction(QIcon(css.settings_icon),
                              "", self), "text", 'menu_file_settings')
        settingsAct.setShortcut('Ctrl+S')
        bind_key(settingsAct, "toolTip", 'menu_file_settings_tooltip')
        settingsAct.triggered.connect(self.settings_window)
        fileMenu.addAction(settingsAct)

        fileMenu.addSeparator()

        # File - Exit:
        exitAct = bind_key(QAction(QIcon(css.exit_icon),
                          "", self), "text", 'menu_file_exit')
        exitAct.setShortcut('Ctrl+Q')
        bind_key(exitAct, "toolTip", 'menu_file_exit_tooltip')
        exitAct.triggered.connect(self.exit_srclet)
        fileMenu.addAction(exitAct)

        # Project:
        fileMenu = bind_key(menubar.addMenu(""), "title", 'menu_project')
        font = fileMenu.font()
        font.setPointSize(read_menu_font_size())
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # Project - New project:
        newProjectAct = bind_key(QAction(
            QIcon((css.new_project_icon)), "", self), "text", 'menu_project_new_project')
        newProjectAct.setShortcut('Ctrl+N')
        bind_key(newProjectAct, "toolTip", 'menu_project_new_project_tooltip')
        newProjectAct.triggered.connect(self.new_project_window)
        fileMenu.addAction(newProjectAct)

        # Project - Open existing project:
        openProjectAct = bind_key(QAction(
            QIcon((css.open_project_icon)), "", self), "text", 'menu_project_open_project')
        openProjectAct.setShortcut('Ctrl+O')
        bind_key(openProjectAct, "toolTip", 'menu_project_open_project_tooltip')
        openProjectAct.triggered.connect(self.open_project_window)
        fileMenu.addAction(openProjectAct)

        # Customize:
        fileMenu = bind_key(menubar.addMenu(""), "title", 'menu_customize')
        font = fileMenu.font()
        font.setPointSize(read_menu_font_size())
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # Customize - Parameters:
        parameters_menu = bind_key(QMenu(
            "", self), "title", 'menu_customize_parameters')
        parameters_menu.setIcon(QIcon(css.parameters_icon))
        font = parameters_menu.font()
        font.setPointSize(read_menu_font_size())
        parameters_menu.setFont(font)
        parameters_menu.setToolTipsVisible(True)

        parametersAct = bind_key(QAction(QIcon(css.parameters_basic_icon),
                                "", self), "text", 'menu_customize_basic_parameters')
        parametersAct.setShortcut('Ctrl+B')
        bind_key(parametersAct, "toolTip", 'menu_customize_basic_parameters_tooltip')
        parametersAct.triggered.connect(self.basic_parameters_window)
        parameters_menu.addAction(parametersAct)

        complexParametersAct = bind_key(QAction(QIcon(
            css.parameters_complex_icon), "", self), "text", 'menu_customize_changable_parameters')
        complexParametersAct.setShortcut('Ctrl+R')
        bind_key(complexParametersAct, "toolTip", 'menu_customize_changable_parameters_tooltip')
        complexParametersAct.triggered.connect(self.changable_parameters_window)
        parameters_menu.addAction(complexParametersAct)

        fileMenu.addMenu(parameters_menu)

        # Customize - Methods:
        methods_menu = bind_key(QMenu("", self), "title", 'menu_customize_methods')
        methods_menu.setIcon(QIcon(css.methods_icon))
        font = methods_menu.font()
        font.setPointSize(read_menu_font_size())
        methods_menu.setFont(font)
        methods_menu.setToolTipsVisible(True)

        etoAct = bind_key(QAction(QIcon(css.methods_eto_icon),
                         "", self), "text", 'menu_customize_methods_eto')
        etoAct.triggered.connect(self.eto_methods_window)
        etoAct.setShortcut('Ctrl+E')
        bind_key(etoAct, "toolTip", 'menu_customize_methods_eto_tooltip')
        methods_menu.addAction(etoAct)

        wbAct = bind_key(QAction(QIcon(css.methods_wb_icon),
                        "", self), "text", 'menu_customize_methods_wb')
        wbAct.triggered.connect(self.wb_methods_window)
        wbAct.setShortcut('Ctrl+W')
        bind_key(wbAct, "toolTip", 'menu_customize_methods_wb_tooltip')
        methods_menu.addAction(wbAct)

        otherAct = bind_key(QAction(QIcon(css.methods_others_icon),
                           "", self), "text", 'menu_customize_methods_others')
        otherAct.triggered.connect(self.other_methods_window)
        otherAct.setShortcut('Ctrl+T')
        bind_key(otherAct, "toolTip", 'menu_customize_methods_others_tooltip')
        methods_menu.addAction(otherAct)

        fileMenu.addMenu(methods_menu)

        # Help:
        fileMenu = bind_key(menubar.addMenu(""), "title", 'menu_help')
        font = fileMenu.font()
        font.setPointSize(read_menu_font_size())
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # Help - About:
        aboutAct = bind_key(QAction(QIcon(css.about_icon),
                           "", self), "text", 'menu_help_about')
        aboutAct.setShortcut('Ctrl+A')
        bind_key(aboutAct, "toolTip", 'menu_help_about_tooltip')
        aboutAct.triggered.connect(self.about_window)
        fileMenu.addAction(aboutAct)

        # Help - Manual:
        helpAct = bind_key(QAction(QIcon(css.manual_icon),
                          "", self), "text", 'menu_help_manual')
        helpAct.setShortcut('F1')
        bind_key(helpAct, "toolTip", 'menu_help_manual_tooltip')
        helpAct.triggered.connect(self.manual_window)
        fileMenu.addAction(helpAct)

    # File:
    def settings_window(self):
        self.window_settings = SettingsWindow(self.language)

    def exit_srclet(self):
        QApplication.quit()
        # self.close()

        # self.window_basic_parameters.close()

    # Project:
    def new_project_window(self):
        self.window = ProjectImport(self)
        self.window.projectCreated.connect(self.show_project)
        self.window.show()

    def show_project(self, path):
        self.project_window = ProjectWindow(path, self.language)

    def open_project_window(self):
        self.window = OpenProjectWindow(self.language)

    # Customize:
    def basic_parameters_window(self):
        self.window_basic_parameters = ParameterCatalog("basic",self)
        self.window_basic_parameters.show()

    def changable_parameters_window(self):
        self.window = ParameterCatalog("changable",self)
        self.window.show()

    def eto_methods_window(self):
        self.window = MethodCatalog('eto',self)
        self.window.show()

    def wb_methods_window(self):
        self.window = MethodCatalog('wb',self)
        self.window.show()

    def other_methods_window(self):
        self.window = MethodCatalog('',self)
        self.window.show()

    # Help:
    def about_window(self):
        self.window = AboutWindow(self.language)

    def manual_window(self):
        self.window = ManualWindow(self.language)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    mainApplication = QApplication(sys.argv)
    myStyle = MyProxyStyle('Fusion')
    # The proxy style should be based on an existing style, like 'Windows',
    # 'Motif', 'Plastique', 'Fusion', ...
    mainApplication.setStyle(myStyle)
    mainWindow = MainWindow()
    sys.exit(mainApplication.exec())
