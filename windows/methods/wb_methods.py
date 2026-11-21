from mortys.language_morty import bind_key
import sys
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication
from variables import css
from windows.methods.wb_methods_widget import WBMethodsWidget

class WBMethods(QMainWindow):
    def __init__(self, language):
        super().__init__()
        self.language = language
        self.setWindowState(QtCore.Qt.WindowState.WindowMaximized)
        self.window_gui()

    def window_gui(self):
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon(css.methods_eto_icon))
        bind_key(self, "windowTitle", 'wb_methods_window_title')
        self.fileMenu()
        self.central_widget = WBMethodsWidget(self.language)
        self.setCentralWidget(self.central_widget)
        self.show()

    def fileMenu(self):
        menubar = self.menuBar()
        font = menubar.font()
        font.setPointSize(14)
        menubar.setFont(font)
        
        fileMenu = bind_key(menubar.addMenu(""), "title", 'eto_methods_window_file_menu')
        font = fileMenu.font()
        font.setPointSize(14)
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        refreshAct = bind_key(QAction(QIcon(css.refresh_icon), "", self), "text", 'eto_methods_window_file_menu_refresh')
        refreshAct.triggered.connect(self.refresh_widget)
        fileMenu.addAction(refreshAct)
        
        fileMenu.addSeparator()
        
        exitAct = bind_key(QAction(QIcon(css.exit_icon),"", self), "text", 'eto_methods_window_file_menu_exit')
        exitAct.triggered.connect(self.exit_window)
        fileMenu.addAction(exitAct)
        
    def refresh_widget(self):
        self.takeCentralWidget()
        self.new_widget = WBMethodsWidget(self.language)
        self.setCentralWidget(self.new_widget)
        
    def exit_window(self):
        self.hide()
   
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = WBMethods()
    sys.exit(mainApplication.exec())
