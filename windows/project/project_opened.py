from PyQt5.QtWidgets import QAction, QMainWindow, QDesktopWidget, QApplication
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from mortys.font_morty import read_menu_font_size
from variables import css, var
from windows.project.project_opened_widget import CalculateWidget
import sys
import os
cwd = os.path.curdir


class ProjectWindow(QMainWindow):
    def __init__(self, project_path, language):
        # def __init__(self):
        super().__init__()
        self.language = language
        self.project_path = project_path
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(var.project_opened_window_widith,
                          var.project_opened_window_height)
        # self.showMaximized()
        # self.project_title = self.project_path.split('/')[-1]
        # self.setWindowTitle(self.language['project_opened_title'] + self.project_title)
        # self.setWindowTitle(self.language['project_opened_title'] + self.project_path)
        # self.setWindowIcon(QIcon(css.srclet_icon))
        self.center_gui()
        self.file_menu()
        self.central_widget = CalculateWidget(
            project_path=self.project_path, language=language)
        self.setCentralWidget(self.central_widget)
        self.show()

    def center_gui(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def file_menu(self):
        menubar = self.menuBar()
        font = menubar.font()
        font.setPointSize(read_menu_font_size())
        menubar.setFont(font)

        fileMenu = menubar.addMenu('file')
        font = fileMenu.font()
        font.setPointSize(read_menu_font_size())
        fileMenu.setFont(font)
        # exitAct = QAction(QIcon(css.exit_icon), self.language['project_opened_menu_exit'], self)
        exitAct = QAction('exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.exit_project)
        fileMenu.addAction(exitAct)

    def exit_project(self):
        self.hide()


if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = ProjectWindow()
    sys.exit(mainApplication.exec_())
