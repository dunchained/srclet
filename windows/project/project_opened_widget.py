import os, json
from variables import css, var

from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QGridLayout, QLabel, QFileDialog
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QPushButton, QGroupBox, QTextEdit
from PyQt5.QtWidgets import QHBoxLayout, QProgressBar
from PyQt5.QtCore import Qt

#from plambas.the_constructor import SrcletEngine
#
class CalculateWidget(QWidget):
    
    def __init__(self, project_path, language):
        self.project_path = project_path
        self.language = language
        super().__init__()
        #SrcletEngine.calculator(self, calculation_data=self.project_path)
        self.window_gui()
        
    def window_gui(self):
        self.grid = QGridLayout()
        self.grid.addWidget(self.project_data_info(), 0, 0, 1, 1)
        self.grid.addWidget(self.export_save_calculate(), 1, 0, 1, 1)
        self.grid.addWidget(self.status_info(), 2, 0, 1, 1)
        self.grid.addWidget(self.methods_info(), 0, 1, 3, 1)

        self.setLayout(self.grid)
        self.center_gui()
        self.show()
        
    def center_gui(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())    

    def project_data_info(self):
        groupBox = QGroupBox(self.language['project_opened_widget_project_info'])
        label = QLabel(self.project_path)
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def methods_info(self):
        groupBox = QGroupBox(self.language['project_opened_widget_methods_info'])
        groupBox.setFixedWidth(400)
        label = QLabel(self.project_path  + 'methods')
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        groupBox.setEnabled(False)
        return groupBox

    def export_save_calculate(self):
        groupBox = QGroupBox(self.language['project_opened_widget_export_save_calc'])
        label = QLabel(self.project_path  + 'export')
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def status_info(self):
        groupBox = QGroupBox(self.language['project_opened_widget_status_info'])
        groupBox.setFixedHeight(80)
        self.status_label = QLabel('status  | kalkulacija: 0 | mezertacmuminacija: 0')
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        #self.progress_bar.setVisible(False)
        #self.progress_bar.setSizePolicy()
        hbox = QHBoxLayout()
        hbox.addWidget(self.status_label)
        hbox.addWidget(self.progress_bar)
        hbox.addStretch(1)
        groupBox.setLayout(hbox)
        return groupBox