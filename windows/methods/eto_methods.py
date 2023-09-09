import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication
from variables import css
from windows.methods.eto_methods_widget import ETOMethodsWidget

class ETOMethods(QMainWindow):
    def __init__(self, language):
        super().__init__()
        self.language = language
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.window_gui()

    def window_gui(self):
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon(css.methods_eto_icon))
        self.setWindowTitle(self.language['eto_methods_window_title'])
        self.fileMenu()
        self.central_widget = ETOMethodsWidget(self.language)
        self.setCentralWidget(self.central_widget)
        self.show()

    def fileMenu(self):
        menubar = self.menuBar()
        font = menubar.font()
        font.setPointSize(14)
        menubar.setFont(font)
        
        fileMenu = menubar.addMenu(self.language['eto_methods_window_file_menu'])
        font = fileMenu.font()
        font.setPointSize(14)
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        refreshAct = QAction(QIcon(css.refresh_icon), self.language['eto_methods_window_file_menu_refresh'], self)
        refreshAct.triggered.connect(self.refresh_widget)
        fileMenu.addAction(refreshAct)
        
        fileMenu.addSeparator()
        
        exitAct = QAction(QIcon(css.exit_icon),self.language['eto_methods_window_file_menu_exit'], self)
        exitAct.triggered.connect(self.exit_window)
        fileMenu.addAction(exitAct)
        
    def refresh_widget(self):
        self.takeCentralWidget()
        self.new_widget = ETOMethodsWidget(self.language)
        self.setCentralWidget(self.new_widget)
        
    def exit_window(self):
        self.hide()
   
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = ETOMethods()
    sys.exit(mainApplication.exec_())
