import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication
#from other_methods_widget import OtherMethodsCategoryTabs
from language import language
import css
from font_morty import read_menu_font_size


class BasicParameters(QMainWindow):
    #def __init__(self, language):
    def __init__(self):
        super().__init__()
        self.language = language
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.window_gui()

    def window_gui(self):
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon(css.parameters_basic_icon))
        self.setWindowTitle(self.language['other_methods_window_title'])
        self.fileMenu()
        #self.central_widget = OtherMethodsCategoryTabs(language=self.language)
        #self.setCentralWidget(self.central_widget)
        self.show()

    def fileMenu(self):
        menubar = self.menuBar()
        font = menubar.font()
        font.setPointSize(read_menu_font_size())
        menubar.setFont(font)

        fileMenu = menubar.addMenu(
            self.language['other_methods_window_file_menu'])
        font = fileMenu.font()
        font.setPointSize(14)
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        refreshAct = QAction(QIcon(
            css.refresh_icon), self.language['basic_parameters_window_file_menu_refresh'], self)
        refreshAct.triggered.connect(self.refresh_widget)
        fileMenu.addAction(refreshAct)

        fileMenu.addSeparator()

        exitAct = QAction(QIcon(
            css.exit_icon), self.language['other_methods_window_file_menu_exit'], self)
        exitAct.triggered.connect(self.exit_window)
        fileMenu.addAction(exitAct)

    def refresh_widget(self):
        self.takeCentralWidget()
        self.new_widget = ParametersCategoryTabs(self.language)
        self.setCentralWidget(self.new_widget)

    def exit_window(self):
        self.hide()


if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = BasicParameters()
    sys.exit(mainApplication.exec_())
