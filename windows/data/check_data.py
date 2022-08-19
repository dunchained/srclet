# python standard modules
import os, sys, json
from pathlib import Path


# app modules and windows
#from appdata import css

# pyqt5 modules
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu, QPushButton, QTableWidget, QApplication, QSizePolicy
from PyQt5.QtWidgets import QGroupBox, QTableWidgetItem, QGridLayout, QLineEdit, QLabel
from PyQt5.QtWidgets import QMessageBox
# data manipulation modules
import numpy
import pandas as pd 



class TableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.rowAt(2)

    def scrollContentsBy(self, dx, dy):
        super(TableWidget, self).scrollContentsBy(dx, dy)

class CheckDataTypeWidget(TableWidget):
    def __init__(self, file_path='data.txt', project_path='/projects/Saigon97'):
    #def __init__(self, file_path, project_path):
        super(CheckDataTypeWidget, self).__init__()
        self.project_path = project_path
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.buttons = []
        self.data = numpy.loadtxt(file_path, skiprows=1)
        self.createTable()
        self.createOptions()
        self.createDataType()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QGridLayout(self)
        layout.addWidget(self.table, 0, 0)
        layout.addWidget(self.groupBox, 1, 0)
        self.setLayout(layout)
        #self.setWindowIcon(QIcon(css.srclet_main_window_icon))
        self.setWindowTitle('Check for data...')
        self.showMaximized()

    def createTable(self):
        self.table = TableWidget(*self.data.shape)
        for i, row_values in enumerate(self.data):
            for j, value in enumerate(row_values):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    def saveData(self):
        
        nrows = self.table.rowCount()
        ncols = self.table.columnCount()
        lista = []

        for column in range(0, ncols):
            print(self.buttons[column].text())
            pucad = self.buttons[column].text()
            lista2 = []
            lista2.append(pucad)
            for row in range(0, nrows):
                item = self.table.item(row, column)
                item_text = item.text()
                lista2.append(item_text)
            lista.append(lista2)
        pd.DataFrame(data=None, index=[0], columns=None, dtype=None, copy=False)

        pprf = pd.DataFrame(lista)
        rt = pprf.transpose()
        print(self.project_path + '/data.xlsx')
        rt.to_excel(self.project_path + "/data.xlsx")

        if not self.line_weather_station.text() and not self.line_weather_station_country.text() and not self.line_weather_station_elevation.text() and not self.line_weather_station_latitude.text() and not self.line_weather_station_longitude.text():
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText('Fill missing data')
            self.msg.setWindowTitle('Missing data...')
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            parameter_dict = {
                "weather_station": self.line_weather_station.text(),
                "weather_station_country": self.line_weather_station_country.text(),
                "weather_station_elevation": self.line_weather_station_elevation.text(),
                "weather_station_latitude": self.line_weather_station_latitude.text(),
                "weather_station_longitude": self.line_weather_station_longitude.text(),
                "anamometer_height": self.line_anamometer_height.text(),
                "wind_speed": self.line_wind_speed.text(),
                "krs_factor": self.line_krs_factor.text(),
                "skip_rows": self.line_skip_rows.text(),
                "missing_data": self.line_missing_data.text()
                }
            json_object = json.dumps(parameter_dict, indent = 4)
            self.ambalage = self.project_path + "/data.json"
            with open(self.ambalage, "w") as outfile:
                outfile.write(json_object)
                
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText('Data saved...')
            self.msg.setWindowTitle('Successuful...')
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.closeSelf)
            self.msg.show()
    
    def closeSelf(self):
        self.close()

    def createDataType(self):

        get_files = next(os.walk(os.path.curdir + "/parameters/"), (None, None, []))[2]
        self.file_list = []
        for file in get_files:
          
            with open('parameters/' + Path(file).stem + '.json') as jsonFile:
                data = json.load(jsonFile)
                jsonData = data['name']
                self.file_list.append(jsonData)
            
        self.buttons
        for i in range(0, self.table.columnCount()):
            button = QPushButton('Data type')
            button.columnIndex = i
            self.buttons.append(button)
            self.table.setCellWidget(0, i, self.buttons[self.buttons.__len__() - 1])
            self.menu = QMenu(self)
            #self.menu.addMenu('Parametri')
            for parameter in sorted(self.file_list):
                self.menu_action = self.menu.addAction(parameter)
                self.menu_action.triggered.connect(self.buttonClicked)
            self.buttons[i].setMenu(self.menu)
            self.menu.columnIndex = i

    def buttonClicked(self, ):
        
        sender = self.sender()
        sender_text = sender.text()
        self.buttons[sender.parent().columnIndex].setText(sender_text)
        return sender

    def createOptions(self):

        self.groupBox = QGroupBox('Data options:')
        self.groupBoxLayout = QGridLayout()

        self.groupBoxOptions = QGroupBox()
        self.groupBoxOptionsLayout = QGridLayout()

        self.label_weather_station = QLabel('Weather station name:')
        self.line_weather_station = QLineEdit()
        self.label_weather_station_country = QLabel('Country:')
        self.line_weather_station_country = QLineEdit()
        self.label_weather_station_elevation = QLabel('Weather station elevation (z) in meters:')
        self.line_weather_station_elevation = QLineEdit()
        self.label_weather_station_latitude = QLabel('Weather station latitude (fi) in decimal degrees:')
        self.line_weather_station_latitude = QLineEdit()
        self.label_weather_station_longitude = QLabel('Weather station longitude (fi) in decimal degrees:')
        self.line_weather_station_longitude = QLineEdit()


        self.label_anamometer_height = QLabel('The anamometer height (zu) in meters:')
        self.line_anamometer_height = QLineEdit('10')
        self.label_wind_speed = QLabel('Value of wind speed if missing (u2) in m/s:')
        self.line_wind_speed = QLineEdit('2')
        self.label_krs_factor = QLabel('Value of krs factor:')
        self.line_krs_factor = QLineEdit('0.162')

        self.label_skip_rows = QLabel('Skip number of rows:')
        self.line_skip_rows = QLineEdit('1')
        self.label_missing_data = QLabel('Code for missing data:')
        self.line_missing_data = QLineEdit('-999')




        self.groupBoxOptionsLayout.addWidget(self.label_weather_station, 0, 0)
        self.groupBoxOptionsLayout.addWidget(self.line_weather_station, 0, 1)
        self.groupBoxOptionsLayout.addWidget(self.label_weather_station_country, 1, 0)
        self.groupBoxOptionsLayout.addWidget(self.line_weather_station_country, 1, 1)
        self.groupBoxOptionsLayout.addWidget(self.label_weather_station_elevation, 2, 0)
        self.groupBoxOptionsLayout.addWidget(self.line_weather_station_elevation, 2, 1)
        self.groupBoxOptionsLayout.addWidget(self.label_weather_station_latitude, 3, 0)
        self.groupBoxOptionsLayout.addWidget(self.line_weather_station_longitude, 3, 1)
        self.groupBoxOptionsLayout.addWidget(self.label_weather_station_longitude, 4, 0)
        self.groupBoxOptionsLayout.addWidget(self.line_weather_station_latitude, 4, 1)
        self.groupBoxOptionsLayout.addWidget(self.label_anamometer_height, 5, 0)
        self.groupBoxOptionsLayout.addWidget(self.line_anamometer_height, 5, 1)
        self.groupBoxOptionsLayout.addWidget(self.label_wind_speed, 6, 0)
        self.groupBoxOptionsLayout.addWidget(self.line_wind_speed, 6, 1)
        self.groupBoxOptionsLayout.addWidget(self.label_krs_factor, 7, 0)
        self.groupBoxOptionsLayout.addWidget(self.line_krs_factor, 7, 1)
        self.groupBoxOptionsLayout.addWidget(self.label_skip_rows, 8, 0)
        self.groupBoxOptionsLayout.addWidget(self.line_skip_rows, 8, 1)
        self.groupBoxOptionsLayout.addWidget(self.label_missing_data, 9, 0)
        self.groupBoxOptionsLayout.addWidget(self.line_missing_data, 9, 1)


        self.groupBoxOptions.setLayout(self.groupBoxOptionsLayout)
 
       
        self.buttonSave = QPushButton('Save Project Data')
        self.buttonSave.clicked.connect(self.saveData)
        self.buttonClose = QPushButton('Cancel')
        self.buttonClose.clicked.connect(self.closeSelf)

        self.groupBoxLayout.addWidget(self.groupBoxOptions, 0, 0)
        self.groupBoxLayout.addWidget(self.buttonSave, 1, 0)
        self.groupBoxLayout.addWidget(self.buttonClose, 2, 0)
        
        self.groupBox.setLayout(self.groupBoxLayout)

        return self.groupBox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CheckDataTypeWidget()
    sys.exit(app.exec_())