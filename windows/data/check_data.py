import os, sys, json
from pathlib import Path
cwd = os.path.curdir
from variables import css, var
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDateTime, QDate, pyqtSignal
from PyQt5.QtWidgets import QMenu, QPushButton, QTableWidget, QApplication, QSizePolicy, QDateEdit
from PyQt5.QtWidgets import QGroupBox, QTableWidgetItem, QGridLayout, QLineEdit, QLabel
from PyQt5.QtWidgets import QMessageBox, QMenuBar, QAbstractScrollArea, QVBoxLayout, QFormLayout, QHBoxLayout
import numpy, pandas

class TableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)
        #self.verticalHeader().hide()
        self.horizontalHeader().hide()
        #self.rowAt(2)

    def scroll_contents_by(self, dx, dy):
        super(TableWidget, self).scroll_contents_by(dx, dy)

class CheckDataTypeWidget(TableWidget):
    #def __init__(self, file_path='data.txt', project_path='/projects/hu'):
    clicked = pyqtSignal()
    def __init__(self, file_path, project_path, language):
        super(CheckDataTypeWidget, self).__init__()
        
        self.language = language        
        self.file_path = file_path
        self.project_path = project_path
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.buttons = []
        self.data = numpy.loadtxt(file_path, skiprows=1)
        
        self.create_table()
        self.create_options()
        self.create_data_type()
        
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QGridLayout(self)
        layout.addWidget(self.table, 0, 0)
        layout.addWidget(self.groupBoxDataOptions, 1, 0)
        self.setLayout(layout)
        #self.setWindowIcon(QIcon(css.srclet_main_window_icon))
        self.setWindowTitle(self.language['check_data_title'] + file_path)
        self.showMaximized()

    def create_table(self):
        self.table = TableWidget(*self.data.shape)
        for i, row_values in enumerate(self.data):
            for j, value in enumerate(row_values):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))
        for col in range(0, self.table.columnCount()):
            self.table.setColumnWidth(col, 200)
        
    def create_data_type(self):
        categories_file = open(os.path.join(cwd + var.language_folder + 'en' + '/' + var.categories_file))
        self.categories_file_data = json.load(categories_file)
        self.categories_list = []
        for category in self.categories_file_data:
            self.categories_list.append(self.categories_file_data[category])

        self.get_files = next(os.walk(os.path.curdir + '/' + var.basic_parameters_folder), (None, None, []))[2]
        self.file_list = []
        for file in self.get_files:
            with open(cwd + var.basic_parameters_folder + Path(file).stem + '.json') as jsonFile:
                data = json.load(jsonFile)
                jsonData = data['name']
                self.file_list.append(jsonData)
            
        self.buttons
        for i in range(0, self.table.columnCount()):
            button = QPushButton(self.language['check_data_select'])
            button.columnIndex = i
            self.buttons.append(button)
            self.table.setCellWidget(0, i, self.buttons[self.buttons.__len__() - 1])
            self.menu_kat = QMenu()
            for kategorija in self.categories_list:
                self.menu_param = self.menu_kat.addMenu(kategorija)
                self.category_list = []
                self.kategorija_code = list(self.categories_file_data.keys())[list(self.categories_file_data.values()).index(kategorija)]
                for file in self.get_files:
                    self.file_to_load = open(os.path.join(cwd + '/' + var.basic_parameters_folder + file))
                    self.file_data = json.load(self.file_to_load)
                    if self.kategorija_code == self.file_data['category']:
                        self.category_list.append(self.file_data['name'])
                for parameter in self.category_list:
                    self.menu_action = self.menu_param.addAction(parameter)
                    self.menu_action.triggered.connect(self.set_column_value)
            self.buttons[i].setMenu(self.menu_kat)
            self.menu_kat.columnIndex = i
            self.menu_kat.addSeparator()
            self.year_action = self.menu_kat.addAction(self.language['check_data_select_year'])
            self.year_action.triggered.connect(self.remove_zeroes)
            self.month_action = self.menu_kat.addAction(self.language['check_data_select_month'])
            self.month_action.triggered.connect(self.remove_zeroes)
            self.menu_kat.addSeparator()
            self.dont_use_action = self.menu_kat.addAction(self.language['check_data_select_donotuse'])
            self.dont_use_action.triggered.connect(self.do_not_use)
            
    def do_not_use(self):
        sender = self.sender()
        sender_text = sender.text()
        self.buttons[sender.parent().columnIndex].setText(sender_text)
        return sender
            
    def remove_zeroes(self):
        sender = self.sender()
        sender_text = sender.text()
        self.buttons[sender.parent().columnIndex].setText(sender_text)
        self.nrows = self.table.rowCount()
        for row in range(0, self.nrows):
            cell = self.table.item(row, sender.parent().columnIndex).text()
            x = cell.split('.')
            self.table.item(row, sender.parent().columnIndex).setText(x[0])
        return sender

    def set_column_value(self, ):
        sender = self.sender()
        sender_text = sender.text()
        self.buttons[sender.parent().parent().columnIndex].setText(sender_text)
        return sender

       
    def create_options(self):
        # Glavni box:
        self.groupBoxDataOptions = QGroupBox('Data options:')
        self.groupBoxDataOptionsLayout = QGridLayout()

        # Options box:
        self.groupBoxOptions = QGroupBox()
        self.groupBoxOptionsLayout = QVBoxLayout()
        self.flay = QFormLayout()

        self.label_weather_station = QLabel('Weather station name: ')
        self.line_weather_station = QLineEdit()
        self.flay.addRow(self.label_weather_station, self.line_weather_station)
        
        self.label_weather_station_country = QLabel('Country:')
        self.line_weather_station_country = QLineEdit()
        self.flay.addRow(self.label_weather_station_country, self.line_weather_station_country)
        
        self.label_weather_station_elevation = QLabel('Weather station elevation (z): ')
        self.label_weather_station_elevation1 = QLabel('meters.')
        self.line_weather_station_elevation = QLineEdit()
        self.hlay_elevation = QHBoxLayout()
        self.hlay_elevation.addWidget(self.label_weather_station_elevation)
        self.hlay_elevation.addWidget(self.line_weather_station_elevation)
        self.hlay_elevation.addWidget(self.label_weather_station_elevation1)
        self.flay.addRow(self.hlay_elevation)
        
        self.label_weather_station_latitude = QLabel('Weather station latitude (fi): ')
        self.label_weather_station_latitude1 = QLabel('decimal degrees.')
        self.line_weather_station_latitude = QLineEdit()
        self.hlay_latitude = QHBoxLayout()
        self.hlay_latitude.addWidget(self.label_weather_station_latitude)
        self.hlay_latitude.addWidget(self.line_weather_station_latitude)
        self.hlay_latitude.addWidget(self.label_weather_station_latitude1)
        self.flay.addRow(self.hlay_latitude)
        
        self.label_weather_station_longitude = QLabel('Weather station longitude (fi): ')
        self.label_weather_station_longitude1 = QLabel('decimal degrees.')
        self.line_weather_station_longitude = QLineEdit()
        self.hlay_longitude = QHBoxLayout()
        self.hlay_longitude.addWidget(self.label_weather_station_longitude)
        self.hlay_longitude.addWidget(self.line_weather_station_longitude)
        self.hlay_longitude.addWidget(self.label_weather_station_longitude1)
        self.flay.addRow(self.hlay_longitude)
        
        self.label_anamometer_height = QLabel('The anamometer height (zu): ')
        self.label_anamometer_height1 = QLabel('meters.')
        self.line_anamometer_height = QLineEdit('10')
        self.hlay_anamometer = QHBoxLayout()
        self.hlay_anamometer.addWidget(self.label_anamometer_height)
        self.hlay_anamometer.addWidget(self.line_anamometer_height)
        self.hlay_anamometer.addWidget(self.label_anamometer_height1)
        self.flay.addRow(self.hlay_anamometer)
        
        self.label_wind_speed = QLabel('Value of wind speed if missing (u2): ')
        self.label_wind_speed1 = QLabel('m/s.')
        self.line_wind_speed = QLineEdit('2')
        self.hlay_wind_speed = QHBoxLayout()
        self.hlay_wind_speed.addWidget(self.label_wind_speed)
        self.hlay_wind_speed.addWidget(self.line_wind_speed)
        self.hlay_wind_speed.addWidget(self.label_wind_speed1)
        self.flay.addRow(self.hlay_wind_speed)
        
        self.label_krs_factor = QLabel('Value of krs factor:')
        self.line_krs_factor = QLineEdit('0.162')
        self.flay.addRow(self.label_krs_factor, self.line_krs_factor)
        
        self.label_skip_rows = QLabel('Skip number of rows:')
        self.line_skip_rows = QLineEdit('1')
        self.flay.addRow(self.label_skip_rows, self.line_skip_rows)
        
        self.label_missing_data = QLabel('Code for missing data:')
        self.line_missing_data = QLineEdit('-999')
        self.flay.addRow(self.label_missing_data, self.line_missing_data)
        
        self.groupBoxOptions.setLayout(self.flay)
 
        # Check box:
        self.groupBoxCheck = QGroupBox()
        self.groupBoxCheckLayout = QGridLayout()
        self.flay_check = QFormLayout()
        
        self.label_date_begining = QLabel('Data begining date: ')
        self.date_date_begining = QDateEdit(calendarPopup=True)
        self.date_date_begining.setDateTime(QDateTime.currentDateTime())
        self.flay_check.addRow(self.label_date_begining, self.date_date_begining)
        
        self.label_date_end = QLabel('Data end date: ')
        self.date_date_end = QDateEdit(calendarPopup=True)
        self.date_date_end.setDateTime(QDateTime.currentDateTime())
        self.flay_check.addRow(self.label_date_end, self.date_date_end)
        
        self.label_number_of_rows = QLabel('Number of rows: ')
        self.label_number_of_rows_num = QLabel('/')
        self.flay_check.addRow(self.label_number_of_rows, self.label_number_of_rows_num)
        
        self.label_number_of_selected_columns = QLabel('Number of selected columns: ')
        self.label_number_of_selected_columns_num = QLabel('/')
        self.flay_check.addRow(self.label_number_of_selected_columns, self.label_number_of_selected_columns_num)
        
        self.button_data_check = QPushButton('Check data')
        self.button_data_check.clicked.connect(self.check_data)
        self.flay_check.addRow(self.button_data_check)
        
        self.label_check_done = QLabel()
        self.label_check_done1 = QLabel()
        self.label_check_done2 = QLabel()
        self.flay_check.addRow(self.label_check_done)
        self.flay_check.addRow(self.label_check_done1)
        self.flay_check.addRow(self.label_check_done2)

        
        self.groupBoxCheck.setLayout(self.flay_check)       
        
        # Postavka svega na DataOptionsGroupBox:
        self.buttonSave = QPushButton('Save data')
        self.buttonSave.setEnabled(False)
        self.buttonSave.clicked.connect(self.save_data)
        self.buttonClose = QPushButton('Cancel')
        self.buttonClose.clicked.connect(self.close_self)

        self.groupBoxDataOptionsLayout.addWidget(self.groupBoxOptions, 0, 0, 1, 1)
        self.groupBoxDataOptionsLayout.addWidget(self.groupBoxCheck, 0, 1, 1, 1)
        self.groupBoxDataOptionsLayout.addWidget(self.buttonSave, 1, 0, 1, 2)
        self.groupBoxDataOptionsLayout.addWidget(self.buttonClose, 2, 0, 1, 2)
        
        self.groupBoxDataOptions.setLayout(self.groupBoxDataOptionsLayout)

        return self.groupBoxDataOptions
    
    def check_data(self):
        table_data = self.read_table()
        self.begining_year = 2022
        self.end_year = 2022
        self.begining_month = 1
        self.end_month = 12
        self.list_of_selected_columns =[]
        
        for column in range(table_data.shape[1]):
            if table_data[column].values[0] == self.language['check_data_select_year']:
                self.begining_year = int(table_data[column].values[1])
                self.end_year = int(table_data[column].values[-1])
            if table_data[column].values[0] == self.language['check_data_select_month']:
                self.begining_month = int(table_data[column].values[1])
                self.end_month = int(table_data[column].values[-1])
            if table_data[column].values[0] != self.language['check_data_select'] and table_data[column].values[0] != self.language['check_data_select_donotuse']:
                self.list_of_selected_columns.append(column)
        self.date_date_begining.setDate(QDate(self.begining_year, self.begining_month, 1))
        self.date_date_end.setDate(QDate(self.end_year, self.end_month, 1))
        self.label_number_of_rows_num.setText(str(table_data.shape[0] - int(self.line_skip_rows.text())))
        self.label_number_of_selected_columns_num.setText(str(len(self.list_of_selected_columns)))
        broj_redova = int(self.label_number_of_rows_num.text())
        if broj_redova % 12 == 0:
            self.label_check_done.setText('Number of rows and months ratio: OK')
            self.label_check_done1.setText('Data shape: ' + self.label_number_of_rows_num.text() + 'x' + self.label_number_of_selected_columns_num.text())
            self.label_check_done2.setText('Good to go...')
            self.buttonSave.setEnabled(True)
        else:
            self.label_check_done.setText('Number of rows and months ratio: NOT OK')
            self.label_check_done1.setText('Data shape: ' + self.label_number_of_rows_num.text() + 'x' + self.label_number_of_selected_columns_num.text())
            self.label_check_done2.setText('Skiping the rows can help...')
            self.buttonSave.setEnabled(False)
    
    def read_table(self):
        self.number_of_rows = self.table.rowCount()
        self.number_of_columns = self.table.columnCount()
        self.lista = []
        
        for column in range(self.number_of_columns):
            self.dugmad = self.buttons[column].text()
            self.lista2 = []
            self.lista2.append(self.dugmad)
            for row in range(self.number_of_rows):
                item = self.table.item(row, column)
                item_text = item.text()
                self.lista2.append(item_text)
            self.lista.append(self.lista2)
        #pandas.DataFrame(data=None, index=[0], columns=None, dtype=None, copy=False)
        data_frame = pandas.DataFrame(self.lista)
        return data_frame.transpose()
        
            
    def save_data(self):
        rt = self.read_table()
        #rt.columns = rt.columns.values.tolist()
        # for (colname,colval) in rt.iteritems():
        #     if colval[0] == self.language['check_data_select']:
        #         rt = rt.drop(rt.columns[colname], axis=1)
        # print(rt)
        rt.to_excel(self.project_path + '/data.xlsx', sheet_name='data_input', index=False)

        if not self.line_weather_station.text() or not self.line_weather_station_country.text() or not self.line_weather_station_elevation.text() or not self.line_weather_station_latitude.text() or not self.line_weather_station_longitude.text():
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['check_data_message'])
            self.msg.setWindowTitle(self.language['check_data_caption'])
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
                "missing_data": self.line_missing_data.text(),
                "project_description": "project_description"
                }
            json_object = json.dumps(parameter_dict, indent = 4)
            self.ambalage = self.project_path + "/data.json"
            with open(self.ambalage, "w") as outfile:
                outfile.write(json_object)
                
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText(self.language['check_data_message1'])
            self.msg.setWindowTitle(self.language['check_data_caption1'])
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.clicked)
            self.msg.buttonClicked.connect(self.close_self)
            
            self.msg.show()
    
    def close_self(self):
        self.hide()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CheckDataTypeWidget()
    sys.exit(app.exec_())