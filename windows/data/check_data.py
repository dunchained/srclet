from mortys.language_morty import bind_key
import pandas
import numpy
import os
import sys
import json
from PyQt6.QtWidgets import QMessageBox, QVBoxLayout, QFormLayout, QHBoxLayout
from PyQt6.QtWidgets import QGroupBox, QTableWidgetItem, QGridLayout, QLineEdit, QLabel
from PyQt6.QtWidgets import QMenu, QPushButton, QTableWidget, QApplication, QSizePolicy, QDateEdit
from PyQt6.QtCore import Qt, QDateTime, QDate, pyqtSignal
from pathlib import Path
from variables import var
cwd = os.path.curdir


class TableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)
        self.horizontalHeader().hide()

    def scroll_contents_by(self, dx, dy):
        super(TableWidget, self).scroll_contents_by(dx, dy)


class CheckDataTypeWidget(TableWidget):
    clicked = pyqtSignal()

    def __init__(self, file_path, project_path, language):
        super(CheckDataTypeWidget, self).__init__()
        self.language = language
        self.file_path = file_path
        self.project_path = project_path
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.buttons = []
        self.data = numpy.loadtxt(file_path, skiprows=1)

        self.create_table()
        self.create_options()
        self.create_data_type()

        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = QGridLayout(self)
        layout.addWidget(self.table, 0, 0)
        layout.addWidget(self.groupBoxDataOptions, 1, 0)
        self.setLayout(layout)
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
        categories_file = open(os.path.join(
            cwd + var.language_folder + self.language['language_description'] + '/' + var.categories_file))
        self.categories_file_data = json.load(categories_file)
        self.categories_list = []
        for category in self.categories_file_data:
            self.categories_list.append(self.categories_file_data[category])

        self.get_files_parameters = next(
            os.walk(os.path.curdir + var.basic_parameters_folder), (None, None, []))[2]
        self.file_list_parameters = []
        for file in self.get_files_parameters:
            with open(var.basic_parameters_folder_ + Path(file).stem + '.json') as jsonFile:
                data = json.load(jsonFile)
                jsonData = data['name']
                self.file_list_parameters.append(jsonData)

        self.get_files_eto_methods = next(
            os.walk(os.path.curdir + var.eto_methods_folder), (None, None, []))[2]
        self.file_list_eto_methods = []
        for file in self.get_files_eto_methods:
            self.file_list_eto_methods.append(Path(file).stem + '.json')

        self.get_files_wb_methods = next(
            os.walk(os.path.curdir + var.wb_methods_folder), (None, None, []))[2]
        self.file_list_wb_methods = []
        for file in self.get_files_wb_methods:
            self.file_list_wb_methods.append(Path(file).stem + '.json')

        self.get_files_other_methods = next(
            os.walk(os.path.curdir + var.other_methods_folder), (None, None, []))[2]
        self.file_list_other_methods = []
        for file in self.get_files_other_methods:
            self.file_list_other_methods.append(Path(file).stem + '.json')

        self.buttons
        for i in range(0, self.table.columnCount()):
            button = bind_key(QPushButton(), "text", 'check_data_select')
            button.columnIndex = i
            self.buttons.append(button)
            self.table.setCellWidget(
                0, i, self.buttons[self.buttons.__len__() - 1])
            self.menu_kat = QMenu()
            for kategorija in self.categories_list:
                self.menu_param = self.menu_kat.addMenu(kategorija)
                self.category_list = []
                self.kategorija_code = list(self.categories_file_data.keys())[
                    list(self.categories_file_data.values()).index(kategorija)]
                for file in self.get_files_parameters:
                    self.file_to_load = open(os.path.join(
                        cwd + var.basic_parameters_folder + file))
                    self.file_data = json.load(self.file_to_load)
                    if self.kategorija_code == self.file_data['category']:
                        self.category_list.append(
                            'BP | ' + self.file_data['name'] + '  |  ' + self.file_data['unit'])
                for parameter in self.category_list:
                    self.menu_action = self.menu_param.addAction(parameter)
                    self.menu_action.triggered.connect(self.set_column_value)
            self.buttons[i].setMenu(self.menu_kat)
            self.menu_kat.columnIndex = i
            self.menu_kat.addSeparator()

            self.eto_method_menu = bind_key(self.menu_kat.addMenu(""), "title", 'check_data_select_eto_method')
            for file in self.file_list_eto_methods:
                self.file_to_load = open(os.path.join(
                    cwd + var.eto_methods_folder + file))
                self.file_data = json.load(self.file_to_load)
                self.menu_action = self.eto_method_menu.addAction(
                    'ET0 | ' + self.file_data['name'] + '  |  ' + self.file_data['unit'])
                self.menu_action.triggered.connect(self.set_column_value)

            self.wb_method_menu = bind_key(self.menu_kat.addMenu(""), "title", 'check_data_select_wb_method')
            for file in self.file_list_wb_methods:
                self.file_to_load = open(os.path.join(
                    cwd + var.wb_methods_folder + file))
                self.file_data = json.load(self.file_to_load)
                self.menu_action = self.wb_method_menu.addAction(
                    'WB | ' + self.file_data['name'] + '  |  ' + self.file_data['unit'])
                self.menu_action.triggered.connect(self.set_column_value)

            self.other_method_menu = bind_key(self.menu_kat.addMenu(""), "title", 'check_data_select_other_method')
            for file in self.file_list_other_methods:
                self.file_to_load = open(os.path.join(
                    cwd + var.other_methods_folder + file))
                self.file_data = json.load(self.file_to_load)
                self.menu_action = self.other_method_menu.addAction(
                    'OTHER | ' + self.file_data['name'] + '  |  ' + self.file_data['unit'])
                self.menu_action.triggered.connect(self.set_column_value)

            self.menu_kat.addSeparator()
            self.dont_use_action = self.menu_kat.addAction(
                self.language['check_data_select_donotuse'])
            self.dont_use_action.triggered.connect(self.do_not_use)

    def do_not_use(self):
        sender = self.sender()
        sender_text = sender.text()
        self.buttons[sender.parent().columnIndex].setText(sender_text)
        return sender

    def set_column_value(self, ):
        sender = self.sender()
        sender_text = sender.text()
        sender_text_preped = sender_text.split(' | ')
        text1 = sender_text_preped[1].strip()
        text2 = self.language['month'].strip()

        if sender_text_preped[1].strip() == self.language['month'].strip() or sender_text_preped[1].strip() == self.language['year'].strip():
            self.nrows = self.table.rowCount()
            for row in range(0, self.nrows):
                cell = self.table.item(
                    row, sender.parent().parent().columnIndex).text()
                x = cell.split('.')
                self.table.item(row, sender.parent(
                ).parent().columnIndex).setText(x[0])

        self.buttons[sender.parent().parent().columnIndex].setText(
            sender_text_preped[1])
        return sender

    def create_options(self):
        # Glavni box:
        self.groupBoxDataOptions = bind_key(QGroupBox(), "title", 'check_data_data_options')
        self.groupBoxDataOptionsLayout = QGridLayout()

        # Options box:
        self.groupBoxOptions = QGroupBox()
        self.groupBoxOptionsLayout = QVBoxLayout()
        self.flay = QFormLayout()

        self.label_weather_station = bind_key(QLabel(), "text", 'check_data_station_name')
        self.line_weather_station = QLineEdit()
        self.flay.addRow(self.label_weather_station, self.line_weather_station)

        self.label_weather_station_country = bind_key(QLabel(), "text", 'check_data_country')
        self.line_weather_station_country = QLineEdit()
        self.flay.addRow(self.label_weather_station_country,
                         self.line_weather_station_country)

        self.label_weather_station_elevation = bind_key(QLabel(), "text", 'check_data_elevation')
        self.label_weather_station_elevation1 = bind_key(QLabel(), "text", 'check_data_elevation1')
        self.line_weather_station_elevation = QLineEdit()
        self.hlay_elevation = QHBoxLayout()
        self.hlay_elevation.addWidget(self.label_weather_station_elevation)
        self.hlay_elevation.addWidget(self.line_weather_station_elevation)
        self.hlay_elevation.addWidget(self.label_weather_station_elevation1)
        self.flay.addRow(self.hlay_elevation)

        self.label_weather_station_latitude = bind_key(QLabel(), "text", 'check_data_latitude')
        self.label_weather_station_latitude1 = bind_key(QLabel(), "text", 'check_data_latitude1')
        self.line_weather_station_latitude = QLineEdit()
        self.hlay_latitude = QHBoxLayout()
        self.hlay_latitude.addWidget(self.label_weather_station_latitude)
        self.hlay_latitude.addWidget(self.line_weather_station_latitude)
        self.hlay_latitude.addWidget(self.label_weather_station_latitude1)
        self.flay.addRow(self.hlay_latitude)

        self.label_weather_station_longitude = bind_key(QLabel(), "text", 'check_data_longitude')
        self.label_weather_station_longitude1 = bind_key(QLabel(), "text", 'check_data_longitude1')
        self.line_weather_station_longitude = QLineEdit()
        self.hlay_longitude = QHBoxLayout()
        self.hlay_longitude.addWidget(self.label_weather_station_longitude)
        self.hlay_longitude.addWidget(self.line_weather_station_longitude)
        self.hlay_longitude.addWidget(self.label_weather_station_longitude1)
        self.flay.addRow(self.hlay_longitude)

        self.label_skip_rows = bind_key(QLabel(), "text", 'check_data_number_of_rows')
        self.line_skip_rows = QLineEdit('1')
        self.flay.addRow(self.label_skip_rows, self.line_skip_rows)

        self.groupBoxOptions.setLayout(self.flay)

        # Check box:
        self.groupBoxCheck = QGroupBox()
        self.groupBoxCheckLayout = QGridLayout()
        self.flay_check = QFormLayout()

        self.label_date_begining = bind_key(QLabel(), "text", 'check_data_begining_date')
        self.date_date_begining = QDateEdit(calendarPopup=True)
        self.date_date_begining.setDateTime(QDateTime.currentDateTime())
        self.flay_check.addRow(self.label_date_begining,
                               self.date_date_begining)

        self.label_date_end = bind_key(QLabel(), "text", 'check_data_end_date')
        self.date_date_end = QDateEdit(calendarPopup=True)
        self.date_date_end.setDateTime(QDateTime.currentDateTime())
        self.flay_check.addRow(self.label_date_end, self.date_date_end)

        self.label_number_of_rows = bind_key(QLabel(), "text", 'check_data_num_rows')
        self.label_number_of_rows_num = QLabel('/')
        self.flay_check.addRow(self.label_number_of_rows,
                               self.label_number_of_rows_num)

        self.label_number_of_selected_columns = bind_key(QLabel(), "text", 'check_data_num_cols')
        self.label_number_of_selected_columns_num = QLabel('/')
        self.flay_check.addRow(
            self.label_number_of_selected_columns, self.label_number_of_selected_columns_num)

        self.button_data_check = bind_key(QPushButton(), "text", 'check_data_btn_check_data')
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
        self.buttonSave = bind_key(QPushButton(), "text", 'check_data_btn_save_data')
        self.buttonSave.setEnabled(False)
        self.buttonSave.clicked.connect(self.save_data)
        self.buttonClose = bind_key(QPushButton(), "text", 'check_data_btn_cancel')
        self.buttonClose.clicked.connect(self.close_self)

        self.groupBoxDataOptionsLayout.addWidget(
            self.groupBoxOptions, 0, 0, 1, 1)
        self.groupBoxDataOptionsLayout.addWidget(
            self.groupBoxCheck, 0, 1, 1, 1)
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
        self.list_of_selected_columns = []

        for column in range(table_data.shape[1]):
            if table_data[column].values[0] == self.language['year']:
                self.begining_year = int(table_data[column].values[1])
                self.end_year = int(table_data[column].values[-1])
            if table_data[column].values[0] == self.language['month']:
                self.begining_month = int(table_data[column].values[1])
                self.end_month = int(table_data[column].values[-1])
            if table_data[column].values[0] != self.language['check_data_select'] and table_data[column].values[0] != self.language['check_data_select_donotuse']:
                self.list_of_selected_columns.append(column)
        self.date_date_begining.setDate(
            QDate(self.begining_year, self.begining_month, 1))
        self.date_date_end.setDate(QDate(self.end_year, self.end_month, 1))
        self.label_number_of_rows_num.setText(
            str(table_data.shape[0] - int(self.line_skip_rows.text())))
        self.label_number_of_selected_columns_num.setText(
            str(len(self.list_of_selected_columns)))
        broj_redova = int(self.label_number_of_rows_num.text())
        if broj_redova % 12 == 0:
            bind_key(self.label_check_done, "text", 'check_data_msg_1')
            self.label_check_done1.setText(self.language['check_data_msg_2'] + self.label_number_of_rows_num.text(
            ) + 'x' + self.label_number_of_selected_columns_num.text())
            bind_key(self.label_check_done2, "text", 'check_data_msg_3')
            self.buttonSave.setEnabled(True)
        else:
            bind_key(self.label_check_done, "text", 'check_data_msg_4')
            self.label_check_done1.setText(self.language['check_data_msg_2'] + self.label_number_of_rows_num.text(
            ) + 'x' + self.label_number_of_selected_columns_num.text())
            bind_key(self.label_check_done2, "text", 'check_data_msg_5')
            self.buttonSave.setEnabled(False)

    def read_table(self):
        self.number_of_rows = self.table.rowCount()
        self.number_of_columns = self.table.columnCount()
        self.lista = []

        for column in range(self.number_of_columns):
            self.dugmad = self.buttons[column].text()
            if self.dugmad != self.language['check_data_select'] and self.dugmad != self.language['check_data_select_donotuse']:
                self.lista2 = []
                self.lista2.append(self.dugmad)
                for row in range(self.number_of_rows):
                    item = self.table.item(row, column)
                    item_text = item.text()
                    self.lista2.append(item_text)
                self.lista.append(self.lista2)
        # pandas.DataFrame(data=None, index=[0], columns=None, dtype=None, copy=False)
        self.data_frame = pandas.DataFrame(self.lista)
        return self.data_frame.transpose()

    def save_data(self):
        rt = self.read_table()
        rt.to_excel(self.project_path + "/data.xlsx",
                    sheet_name='data_input', index=False)
        if not self.line_weather_station.text() or not self.line_weather_station_country.text() or not self.line_weather_station_elevation.text() or not self.line_weather_station_latitude.text() or not self.line_weather_station_longitude.text():
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Icon.Information)
            bind_key(self.msg, "text", 'check_data_message')
            bind_key(self.msg, "windowTitle", 'check_data_caption')
            self.msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            parameter_dict = {
                "weather_station": self.line_weather_station.text(),
                "weather_station_country": self.line_weather_station_country.text(),
                "weather_station_elevation": self.line_weather_station_elevation.text(),
                "weather_station_latitude": self.line_weather_station_latitude.text(),
                "weather_station_longitude": self.line_weather_station_longitude.text(),
                "skip_rows": self.line_skip_rows.text()
            }
            json_object = json.dumps(parameter_dict, indent=4)
            self.ambalage = self.project_path + "/data.json"
            with open(self.ambalage, "w") as outfile:
                outfile.write(json_object)

            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Icon.Information)
            bind_key(self.msg, "text", 'check_data_message1')
            bind_key(self.msg, "windowTitle", 'check_data_caption1')
            self.msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.msg.buttonClicked.connect(self.clicked)
            self.msg.buttonClicked.connect(self.close_self)
            self.msg.show()

    def close_self(self):
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CheckDataTypeWidget()
    sys.exit(app.exec())
