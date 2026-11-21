from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
from mortys.font_morty import read_menu_font_size
from variables import css, var
from PyQt6.QtWidgets import QTabWidget
from windows.project.calculations import MonthlyCalculations
from windows.project.method_selection import MethodSelection
from mortys.language_morty import bind, events, tr
import sys
import os

cwd = os.path.curdir


class ProjectWindow(QMainWindow):
    def __init__(self, project_path, language):
        # def __init__(self):
        super().__init__()
        self.language = language
        self.project_path = project_path
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        # self.setFixedSize(var.project_opened_window_widith, var.project_opened_window_height)
        self.showMaximized()
        self.project_title = self.project_path.split("/")[-1]
        self.setWindowTitle(self.language["project_opened_title"] + self.project_title)
        self.setWindowTitle(self.language["project_opened_title"] + self.project_path)
        self.setWindowIcon(QIcon(css.srclet_icon))
        self.center_gui()
        self.file_menu()
        self.tabs = QTabWidget()
        self.calculations = MonthlyCalculations(self.project_path, results_only=True)
        self.central_widget = MethodSelection(self.calculations, self)
        self.tabs.addTab(self.central_widget, tr("Method selection"))
        self.tabs.addTab(self.calculations, tr("Saved results"))
        self.tabs.currentChanged.connect(self.tab_changed)
        events.catalogChanged.connect(self.catalog_changed)
        self.setCentralWidget(self.tabs)
        events.changed.connect(self.retranslate)
        self.retranslate()
        self.show()

    def tab_changed(self, index):
        if index == 0 and not self.central_widget.plan:
            self.central_widget.sync_sources(self.calculations.input_path)

    def catalog_changed(self):
        self.calculations.refresh_catalog()
        self.central_widget.plan.clear()
        self.central_widget.refresh()

    def retranslate(self):
        self.setWindowTitle(f"SRCLET · {self.project_title}")
        self.tabs.setTabText(0, tr("Method selection"))
        self.tabs.setTabText(1, tr("Saved results"))

    def center_gui(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def file_menu(self):
        menubar = self.menuBar()
        font = menubar.font()
        font.setPointSize(read_menu_font_size())
        menubar.setFont(font)

        fileMenu = bind(menubar.addMenu("File"), "title", "File")
        font = fileMenu.font()
        font.setPointSize(read_menu_font_size())
        fileMenu.setFont(font)
        # exitAct = QAction(QIcon(css.exit_icon), self.language['project_opened_menu_exit'], self)
        exitAct = bind(QAction(self), "text", "Close")
        exitAct.setShortcut("Ctrl+Q")
        exitAct.triggered.connect(self.exit_project)
        fileMenu.addAction(exitAct)

    def exit_project(self):
        self.hide()


if __name__ == "__main__":
    mainApplication = QApplication(sys.argv)
    mainWindow = ProjectWindow()
    sys.exit(mainApplication.exec())
