import os, json, sys
cwd = os.path.curdir

#from plambas.project_plambases import read_methods_data, read_project_data
#from bregasta.reading import read_data_file
from project_plambases import read_methods_data, available_changable_parameters, read_project_data
from project_plambases import other_read_methods_data
#from variables import css, var
import var

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGridLayout, QLabel, QLineEdit, QScrollArea
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QPushButton, QGroupBox, QTextEdit
from PyQt5.QtWidgets import QHBoxLayout, QProgressBar, QFormLayout, QApplication, QCheckBox
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
        
        self.window_gui()
        
    def window_gui(self):
        self.grid = QGridLayout()
        
        self.grid.addWidget(self.project_data_info(), 0, 0, 1, 1)
        self.grid.addWidget(self.available_changable_parameters(), 1, 0, 1, 1)
        self.grid.addWidget(self.other_methods_info(), 0, 1, 2, 1)
        #self.grid.addWidget(self.eto_methods_info(), 0, 2, 2, 1)
        #self.grid.addWidget(self.wb_methods_info(), 0, 3, 2, 1)
        self.grid.addWidget(self.calculate_options(), 2, 0, 1, 4)
        self.grid.addWidget(self.status_info(), 3, 0, 1, 2)
        self.grid.addWidget(self.buttons_calculate(), 3, 2, 1, 2)
       
        
        # self.grid.addWidget(self.project_data_info(), 0, 0, 1, 1)
        # self.grid.addWidget(self.available_changable_parameters(), 0, 1, 1, 1)
        # self.grid.addWidget(self.methods_info(), 0, 2, 2, 1)
        # self.grid.addWidget(self.calculate_options(), 1, 0, 1, 2)
        # self.grid.addWidget(self.buttons_calculate(), 2, 2, 1, 1)
        # self.grid.addWidget(self.status_info(), 2, 0, 1, 2)

        self.setLayout(self.grid)
        self.center_gui()
        self.show()
        
    def center_gui(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def buttons_calculate(self):
        groupBox = QGroupBox('buttons')
        label = QPushButton('huehue')
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        groupBox.setLayout(vbox)
        return groupBox
        
    def available_changable_parameters(self):
        self.acp_groupbox = QGroupBox('Available changable parameters:')
        self.acp_groupbox.setCheckable(True)
        self.acp_groupbox.setChecked(False)
        self.acp_layout = QVBoxLayout()
        self.acp_scroll = QWidget()
        
        self.list_of_acp, _ = available_changable_parameters(project_path=self.project_title)

        for self.acp in self.list_of_acp:
            self.acp1_groupbox = QGroupBox(self.acp['name'] + ':')
            self.flay = QFormLayout()
            self.name_symbol = QLabel(self.acp['symbol'] + ' = ')
            self.name_value = QLineEdit(self.acp['value'])
            self.flay.addRow(self.name_symbol, self.name_value)
            self.acp1_groupbox.setLayout(self.flay)

            self.acp_layout.addWidget(self.acp1_groupbox)
            
        self.acp_scroll.setLayout(self.acp_layout)
        acp = QScrollArea()
        acp.setWidget(self.acp_scroll)
        acp.setWidgetResizable(1)

        self.acp_groupbox.layout = QVBoxLayout()
        self.acp_groupbox.layout.addWidget(acp)
        self.acp_groupbox.setLayout(self.acp_groupbox.layout)
        return self.acp_groupbox

    def project_data_info(self):
        self.project_data_info_groupbox = QGroupBox('projekat i data info')
        self.project_data_info_groupbox.layout = QVBoxLayout()
        
        self.flay = QFormLayout()
        
        self.label_weather_station = QLabel('Weather station: ')
        self.label_weather_station_read = QLabel(self.project_data['weather_station'])
        self.flay.addRow(self.label_weather_station, self.label_weather_station_read)
        
        self.label_weather_station_country = QLabel('WS country: ')
        self.label_weather_station_country_read = QLabel(self.project_data['weather_station_country'])
        self.flay.addRow(self.label_weather_station_country, self.label_weather_station_country_read)
        
        self.label_weather_station_elevation = QLabel('WS elevation: ')
        self.label_weather_station_elevation_read = QLabel(self.project_data['weather_station_elevation'])
        self.flay.addRow(self.label_weather_station_elevation, self.label_weather_station_elevation_read)
        
        self.label_weather_station_latitude = QLabel('WS latitude: ')
        self.label_weather_station_latitude_read = QLabel(self.project_data['weather_station_latitude'])
        self.flay.addRow(self.label_weather_station_latitude, self.label_weather_station_latitude_read)
        
        self.label_weather_station_longitude = QLabel('WS longitude: ')
        self.label_weather_station_longitude_read = QLabel(self.project_data['weather_station_longitude'])
        self.flay.addRow(self.label_weather_station_longitude, self.label_weather_station_longitude_read)
        
        self.label_data_parameters = QLabel('Available paramteres')
        self.label_data_parameters_read = QLabel(', '.join(self.available_parameters_list))
        self.label_data_parameters_read.setWordWrap(True)
        self.flay.addRow(self.label_data_parameters, self.label_data_parameters_read)
        
        self.project_data_info_groupbox.setLayout(self.flay)
        return self.project_data_info_groupbox
    
    def eto_methods_info(self):
        self.other_methods_groupbox = QGroupBox('Other Methods: ')
        self.other_methods_layout = QVBoxLayout()
        self.other_methods_scroll = QWidget()
        
        # učitati parametre iz fajla plambas_read_available_parameters_fromdata_file()
        # učitaš ih kao listu list_of_available_parameters
        # na tu listu dodaš sve other metode koji se mogu rač
        
        self.methods_data = other_read_methods_data()
        
        for self.method in self.methods_data:
            self.method_groupbox = QGroupBox(self.method)
            self.method_groupbox.setCheckable(True)
            self.method_groupbox.setChecked(False)
            self.method_groupbox.layout = QGridLayout()
            self.method_name = self.name_symbol = QLabel(self.method)
            self.method_groupbox.layout.addWidget(self.method_name)
            self.method_groupbox.setLayout(self.method_groupbox.layout)

            self.other_methods_layout.addWidget(self.method_groupbox)
            
        self.other_methods_scroll.setLayout(self.other_methods_layout)
        methods = QScrollArea()
        methods.setWidget(self.other_methods_scroll)
        methods.setWidgetResizable(1)

        self.other_methods_groupbox.layout = QVBoxLayout()
        self.other_methods_groupbox.layout.addWidget(methods)
        self.other_methods_groupbox.setLayout(self.other_methods_groupbox.layout)
        return self.other_methods_groupbox
    
       
    def other_methods_info(self):
        self.other_methods_groupbox = QGroupBox('Other Methods: ')
        self.other_methods_layout = QVBoxLayout()
        self.other_methods_scroll = QWidget()
        
       
        self.all_data_from_project_dict, self.all_pa_data_file_list = read_project_data(project_path=self.project_title)
        
        _, self.base_data_list = available_changable_parameters(project_path=self.project_title)
        # for item in self.base_data_list:
        #     if item not in self.all_pa_data_file_list:
        #         self.base_data_list.append(item)    
            
        for self.method in self.all_pa_data_file_list:
            self.method_groupbox = QGroupBox(self.method)
            self.method_groupbox.setCheckable(False)
            self.method_groupbox.setChecked(True)
            self.method_groupbox.layout = QGridLayout()
            self.method_name = self.name_symbol = QLabel(self.method)
            self.method_groupbox.layout.addWidget(self.method_name)
            self.method_groupbox.setLayout(self.method_groupbox.layout)

            self.other_methods_layout.addWidget(self.method_groupbox)
        
        
        self.all_available_others_methods_data, _ = other_read_methods_data()
        for self.method, self.parameters in _.items():
            self.parameters = self.parameters.split(', ')
            if 
            
            print(self.parameters)
            self.method_groupbox1 = QGroupBox(self.method)
            self.method_groupbox1.setCheckable(True)
            self.method_groupbox1.setChecked(False)
            self.method_groupbox1.layout = QGridLayout()
            self.method_name1 = self.name_symbol1 = QLabel(self.method)
            self.method_groupbox1.layout.addWidget(self.method_name1)
            self.method_groupbox1.setLayout(self.method_groupbox1.layout)
            
            self.other_methods_layout.addWidget(self.method_groupbox1)
    
        self.other_methods_scroll.setLayout(self.other_methods_layout)
        methods = QScrollArea()
        methods.setWidget(self.other_methods_scroll)
        methods.setWidgetResizable(1)
        
        self.text = ', '.join(self.base_data_list)
        self.label_remove = QLabel(self.text)
        self.label_remove.setWordWrap(True)
        
        self.other_methods_groupbox.layout = QVBoxLayout()
        self.other_methods_groupbox.layout.addWidget(methods)
        self.other_methods_groupbox.layout.addWidget(self.label_remove)
        self.other_methods_groupbox.setLayout(self.other_methods_groupbox.layout)
        return self.other_methods_groupbox

    def wb_methods_info(self):
        self.methods_groupbox = QGroupBox('WB Methods: ')
        self.methods_layout = QVBoxLayout()
        self.methods_scroll = QWidget()
        
        self.methods_data = read_methods_data()
        
        for self.method in self.methods_data:
            self.method_groupbox = QGroupBox(self.method)
            self.method_groupbox.setCheckable(True)
            self.method_groupbox.setChecked(False)
            self.method_groupbox.layout = QGridLayout()
            self.method_name = self.name_symbol = QLabel(self.method)
            self.method_groupbox.layout.addWidget(self.method_name)
            self.method_groupbox.setLayout(self.method_groupbox.layout)

            self.methods_layout.addWidget(self.method_groupbox)
            
        self.methods_scroll.setLayout(self.methods_layout)
        methods = QScrollArea()
        methods.setWidget(self.methods_scroll)
        methods.setWidgetResizable(1)

        self.methods_groupbox.layout = QVBoxLayout()
        self.methods_groupbox.layout.addWidget(methods)
        self.methods_groupbox.setLayout(self.methods_groupbox.layout)
        return self.methods_groupbox

    def calculate_options(self):
        self.calculate_options_groupbox = QGroupBox('options')
        self.calculate_options_groupbox.layout = QGridLayout()
        
        self.groupbox_1 = QGroupBox('Opcije 1')
        self.groupbox_1.layout = QVBoxLayout()
        self.qcheck_1 = QCheckBox('Pritisni me 1')
        self.groupbox_1.layout.addWidget(self.qcheck_1)
        self.groupbox_1.setLayout(self.groupbox_1.layout)
        
        self.groupbox_2 = QGroupBox('Opcije 2')
        self.groupbox_2.layout = QVBoxLayout()
        self.qcheck_2 = QCheckBox('Pritisni me 2')
        self.groupbox_2.layout.addWidget(self.qcheck_2)
        self.groupbox_2.setLayout(self.groupbox_2.layout)
        
        self.groupbox_3 = QGroupBox('Opcije 3')
        self.groupbox_3.layout = QVBoxLayout()
        self.qcheck_3 = QCheckBox('Pritisni me 3')
        self.groupbox_3.layout.addWidget(self.qcheck_3)
        self.groupbox_3.setLayout(self.groupbox_3.layout)
              
        self.calculate_options_groupbox.layout.addWidget(self.groupbox_1, 0, 0)
        self.calculate_options_groupbox.layout.addWidget(self.groupbox_2, 0, 1)
        self.calculate_options_groupbox.layout.addWidget(self.groupbox_3, 0, 2)
        self.calculate_options_groupbox.setLayout(self.calculate_options_groupbox.layout)
        return self.calculate_options_groupbox

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
        groupBox.setLayout(hbox)
        return groupBox
    
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = CalculateWidget()
    sys.exit(mainApplication.exec_())