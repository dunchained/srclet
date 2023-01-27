import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication
#from windows.parameters.basic_parameters_widget import ParametersCategoryTabs
from basic_parameters_widget import ParametersCategoryTabs
#from variables import css
import css
#from mortys.font_morty import read_menu_font_size
from language import language
#from windows.parameters.language import language

class BasicParameters(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language = language
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.window_gui()

    def window_gui(self):
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon(css.parameters_basic_icon))
        self.setWindowTitle(self.language['basic_parameters_window_title'])
        self.fileMenu()
        self.central_widget = ParametersCategoryTabs()
        self.setCentralWidget(self.central_widget)
        self.show()

    def fileMenu(self):
        menubar = self.menuBar()
        font = menubar.font()
        font.setPointSize(14)
        menubar.setFont(font)
        
        fileMenu = menubar.addMenu(self.language['basic_parameters_window_file_menu'])
        font = fileMenu.font()
        font.setPointSize(14)
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        refreshAct = QAction(QIcon(css.refresh_icon), self.language['basic_parameters_window_file_menu_refresh'], self)
        refreshAct.triggered.connect(self.refresh_widget)
        fileMenu.addAction(refreshAct)
        
        fileMenu.addSeparator()
        
        exitAct = QAction(QIcon(css.exit_icon),self.language['basic_parameters_window_file_menu_exit'], self)
        exitAct.triggered.connect(self.exit_window)
        fileMenu.addAction(exitAct)
        
    def refresh_widget(self):
        self.takeCentralWidget()
        self.new_widget = ParametersCategoryTabs()
        self.setCentralWidget(self.new_widget)
        
    def exit_window(self):
        self.hide()

if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = BasicParameters()
    sys.exit(mainApplication.exec_())
