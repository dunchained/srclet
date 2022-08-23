import os, json
from css import css

from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QGridLayout, QLabel, QFileDialog
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QPushButton, QGroupBox, QTextEdit
from PyQt5.QtWidgets import QHBoxLayout, QProgressBar
from PyQt5.QtCore import Qt

#from plambas.the_constructor import SrcletEngine

class CalculateWidget(QWidget):
    
    def __init__(self, project_path, language):
        self.project_path = project_path
        self.language = language
        super().__init__()
        #SrcletEngine.calculator(self, calculation_data=self.project_path)
        self.WindowGUI()
        
    def WindowGUI(self):
        self.grid = QGridLayout()
        self.grid.addWidget(self.projectInfo(), 0, 0, 1, 1)
        self.grid.addWidget(self.dataInfo(), 0, 1, 1, 1)
        self.grid.addWidget(self.methodsInfo(), 0, 2, 1, 1)
        self.grid.addWidget(self.dataVizualizationOptions(), 1, 0, 1, 1)
        self.grid.addWidget(self.exportSaveCalculate(), 1, 1, 1, 2)
        self.grid.addWidget(self.statusniCincilator(), 2 , 0 , 1, 3)

        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())    

    def projectInfo(self):
        groupBox = QGroupBox(self.language['project_opened_widget_project_info'])
        label = QLabel(self.project_path + 'project')
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def dataInfo(self):
        groupBox = QGroupBox(self.language['project_opened_widget_data_info'])
        label = QLabel(self.project_path + 'data')
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def methodsInfo(self):
        groupBox = QGroupBox(self.language['project_opened_widget_methods_info'])
        label = QLabel(self.project_path  + 'methods')
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        groupBox.setEnabled(False)
        return groupBox

    def dataVizualizationOptions(self):
        groupBox = QGroupBox(self.language['project_opened_widget_vizualization_options'])
        label = QLabel(self.project_path  + 'vizual')
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def exportSaveCalculate(self):
        groupBox = QGroupBox(self.language['project_opened_widget_export_save_calc'])
        label = QLabel(self.project_path  + 'export')
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def statusniCincilator(self):
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