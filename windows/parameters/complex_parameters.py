import sys, os
cwd = os.path.curdir

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from variables import css
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication
from windows.parameters.complex_parameters_widget import ParametersCategoryTabs
#from mortys.font_morty import read_menu_font_size
#from complex_parameters_widget import ParametersCategoryTabs

class ComplexParameters(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language = {
            "//": "Complex Parameters Window",
            "complex_parameters_window_title": "Complex Parameters",
            "complex_parameters_window_file_menu": "File",
            "complex_parameters_window_file_menu_refresh": "Refresh parameters list",
            "complex_parameters_window_file_menu_exit": "Close"
        }
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.window_gui()

    def window_gui(self):
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon(css.parameters_complex_icon))
        self.setWindowTitle(self.language['complex_parameters_window_title'])
        self.fileMenu()
        self.central_widget = ParametersCategoryTabs()
        self.setCentralWidget(self.central_widget)
        self.show()

    def fileMenu(self):
        menubar = self.menuBar()
        font = menubar.font()
        font.setPointSize(14)
        menubar.setFont(font)
        
        fileMenu = menubar.addMenu(self.language['complex_parameters_window_file_menu'])
        font = fileMenu.font()
        font.setPointSize(14)
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        refreshAct = QAction(QIcon(css.exit_icon), self.language['complex_parameters_window_file_menu_refresh'], self)
        #refreshAct = QAction(self.language['complex_parameters_window_file_menu_refresh'], self)
        refreshAct.triggered.connect(self.refresh_widget)
        fileMenu.addAction(refreshAct)
        
        fileMenu.addSeparator()
        
        exitAct = QAction(QIcon(css.exit_icon),self.language['complex_parameters_window_file_menu_exit'], self)
        #exitAct = QAction(self.language['complex_parameters_window_file_menu_exit'], self)
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
    mainWindow = ComplexParameters()
    sys.exit(mainApplication.exec_())
