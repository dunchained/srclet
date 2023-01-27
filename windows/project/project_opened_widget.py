import os, json, sys
cwd = os.path.curdir

#from plambas.project_plambases import read_methods_data, read_project_data
from project_plambases import read_project_data, read_methods_data
#from variables import css, var
import var

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGridLayout, QLabel, QFileDialog
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QPushButton, QGroupBox, QTextEdit
from PyQt5.QtWidgets import QHBoxLayout, QProgressBar, QFormLayout, QApplication
from PyQt5.QtCore import Qt

#from plambas.the_constructor import SrcletEngine
#
class CalculateWidget(QWidget):
    #def __init__(self, project_path, language):
    def __init__(self):
        self.project_path = cwd + var.project_path
        #self.language = language
        self.project_title = self.project_path.split('/')[-1]
        super().__init__()
        #SrcletEngine.calculator(self, calculation_data=self.project_path)
        self.project_data, self.available_parameters_list = read_project_data(project_path=self.project_title)
        print(self.project_data, self.available_parameters_list)
        self.methods_data = read_methods_data(project_path=self.project_title)
        
        
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
        self.project_data_info_groupbox = QGroupBox('projekat i data info')
        self.project_data_info_groupbox.layout = QVBoxLayout()
        self.flay = QFormLayout()
        self.label_weather_station = QLabel('weather_station:')
        self.label_weather_station_read = QLabel('value')
        self.flay.addRow(self.label_weather_station, self.label_weather_station_read)
        self.label_weather_station_elevation = QLabel('weather_station_elevation')
        self.label_weather_station_elevation_read = QLabel('value')
        self.flay.addRow(self.label_weather_station_elevation, self.label_weather_station_elevation_read)
        self.label_weather_station_latitude = QLabel('weather_station_latitude:')
        self.label_weather_station_latitude_read = QLabel('value')
        self.flay.addRow(self.label_weather_station_latitude, self.label_weather_station_latitude_read)
        self.project_data_info_groupbox.setLayout(self.flay)
        return self.project_data_info_groupbox

    def methods_info(self):
        #self.methods_list_all, self.methods_list_eto = read_methods_data()
        pass
        
        groupBox = QGroupBox('metode:')
        label = QLabel(self.project_path  + 'methods')
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        groupBox.setEnabled(False)
        return groupBox

    def export_save_calculate(self):
        groupBox = QGroupBox('save')
        label = QLabel(self.project_path  + 'export')
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def status_info(self):
        groupBox = QGroupBox('status')
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
    
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = CalculateWidget()
    sys.exit(mainApplication.exec_())