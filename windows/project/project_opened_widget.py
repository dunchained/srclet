from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QProgressBar, QFormLayout, QApplication, QCheckBox
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QPushButton, QGroupBox, QTextEdit
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGridLayout, QLabel, QLineEdit, QScrollArea
from variables import css, var
from plambas.project_plambases import other_read_methods_data, other_read_methods_data_on_update, eto_read_methods_data, wb_read_methods_data
from plambas.project_plambases import read_methods_data, available_changable_parameters, read_project_data
import os
import sys
cwd = os.path.curdir


class CalculateWidget(QWidget):
    def __init__(self, project_path, language):
        self.project_path = project_path
        self.language = language
        self.project_title = self.project_path.split('/')[-1]
        super().__init__()
        self.project_data, self.available_parameters_list, self.list_param_symbol = read_project_data(
            project_path=self.project_title)
        self.window_gui()

    def window_gui(self):
        self.grid = QGridLayout()
        self.grid.addWidget(self.project_data_info(), 0, 0, 1, 1)
        self.grid.addWidget(self.available_changable_parameters(), 1, 0, 1, 1)
        self.grid.addWidget(self.other_methods_info(), 0, 1, 2, 1)
        self.grid.addWidget(self.eto_methods_info(), 0, 2, 2, 1)
        self.grid.addWidget(self.wb_methods_info(), 0, 3, 2, 1)
        self.grid.addWidget(self.calculate_options(), 2, 0, 1, 4)
        self.grid.addWidget(self.status_info(), 3, 0, 1, 2)
        self.grid.addWidget(self.buttons_calculate(), 3, 2, 1, 2)
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
        self.list_of_acp, _ = available_changable_parameters(
            project_path=self.project_title)
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
        self.label_weather_station_read = QLabel(
            self.project_data['weather_station'])
        self.flay.addRow(self.label_weather_station,
                         self.label_weather_station_read)
        self.label_weather_station_country = QLabel('WS country: ')
        self.label_weather_station_country_read = QLabel(
            self.project_data['weather_station_country'])
        self.flay.addRow(self.label_weather_station_country,
                         self.label_weather_station_country_read)
        self.label_weather_station_elevation = QLabel('WS elevation: ')
        self.label_weather_station_elevation_read = QLabel(
            self.project_data['weather_station_elevation'])
        self.flay.addRow(self.label_weather_station_elevation,
                         self.label_weather_station_elevation_read)
        self.label_weather_station_latitude = QLabel('WS latitude: ')
        self.label_weather_station_latitude_read = QLabel(
            self.project_data['weather_station_latitude'])
        self.flay.addRow(self.label_weather_station_latitude,
                         self.label_weather_station_latitude_read)
        self.label_weather_station_longitude = QLabel('WS longitude: ')
        self.label_weather_station_longitude_read = QLabel(
            self.project_data['weather_station_longitude'])
        self.flay.addRow(self.label_weather_station_longitude,
                         self.label_weather_station_longitude_read)
        self.label_data_parameters = QLabel('Available paramteres')
        self.label_data_parameters_read = QLabel(
            ', '.join(self.available_parameters_list))
        self.label_data_parameters_read.setWordWrap(True)
        self.flay.addRow(self.label_data_parameters,
                         self.label_data_parameters_read)
        self.project_data_info_groupbox.setLayout(self.flay)
        return self.project_data_info_groupbox

    def other_methods_info(self):
        self.other_methods_groupbox = QGroupBox('Other Methods: ')
        self.other_methods_layout = QVBoxLayout()
        self.other_methods_scroll = QWidget()
        self.all_data_from_project_dict, self.all_pa_data_file_list, self.lista_dostupnih_param = read_project_data(
            project_path=self.project_title)
        _, self.base_data_list = available_changable_parameters(
            project_path=self.project_title)
        for self.method in self.all_pa_data_file_list:
            self.method_groupbox = QGroupBox(self.method)
            self.method_groupbox.setCheckable(False)
            self.method_groupbox.setChecked(True)
            self.method_groupbox.layout = QGridLayout()
            self.method_name = self.name_symbol = QLabel(self.method)
            self.method_groupbox.layout.addWidget(self.method_name)
            self.method_groupbox.setLayout(self.method_groupbox.layout)
            self.other_methods_layout.addWidget(self.method_groupbox)
        self.all_available_others_methods_data, self.method_parameters_dict = other_read_methods_data()
        for self.method, self.parameters in self.method_parameters_dict.items():
            self.parameters = self.parameters.split(', ')
            result = all(
                elem in self.lista_dostupnih_param for elem in self.parameters)
            if result:
                self.method_groupbox1 = QGroupBox(self.method)
                self.method_groupbox1.setCheckable(True)
                self.method_groupbox1.setChecked(False)
                self.method_groupbox1.clicked.connect(
                    self.other_method_checked)
                self.method_groupbox1.layout = QGridLayout()
                self.method_name1 = self.name_symbol1 = QLabel(self.method)
                self.method_groupbox1.layout.addWidget(self.method_name1)
                self.method_groupbox1.setLayout(self.method_groupbox1.layout)
                self.other_methods_layout.addWidget(self.method_groupbox1)
            else:
                pass
        self.other_methods_scroll.setLayout(self.other_methods_layout)
        methods = QScrollArea()
        methods.setWidget(self.other_methods_scroll)
        methods.setWidgetResizable(1)
        self.texte = ', '.join(self.base_data_list)
        self.label_remove = QLabel(self.texte)
        self.label_remove.setWordWrap(True)
        self.other_methods_groupbox.layout = QVBoxLayout()
        self.other_methods_groupbox.layout.addWidget(methods)
        self.other_methods_groupbox.layout.addWidget(self.label_remove)
        self.other_methods_groupbox.setLayout(
            self.other_methods_groupbox.layout)
        return self.other_methods_groupbox

    @QtCore.pyqtSlot()
    def other_method_checked(self):
        if not self.label_remove.text():
            self.cpl = []
        else:
            self.cpl = self.label_remove.text().split(', ')
            self.apl = self.label_remove_.text().split(', ')
            self.kpl = self.label_remove_k.text().split(', ')
        if self.sender().isChecked() == True:
            sender = self.sender().title()
            self.cpl.append(sender)
            self.apl.append(sender)
            self.kpl.append(sender)
            self.label_remove.setText(', '.join(self.cpl))
            self.label_remove_.setText(', '.join(self.apl))
            self.label_remove_k.setText(', '.join(self.kpl))
            if sender in self.label_remove.text():
                _, self.method_parameters_dicte = other_read_methods_data_on_update()
                self.methods_list__ = []
                for self.method_, self.parameters_ in self.method_parameters_dicte.items():
                    self.parameters_ = self.parameters_.split(', ')
                    self.parameters_all = self.cpl + self.lista_dostupnih_param
                    result = all(
                        elem in self.parameters_all for elem in self.parameters_)
                    self.methods_list_ = []
                    for self.object in self.other_methods_scroll.children():
                        if self.object.__class__.__name__ == 'QGroupBox':
                            self.methods_list_.append(self.object.title())
                    if result:
                        if self.method_ not in self.methods_list_:
                            self.methods_list__.append(self.method_)
                for self._method in self.methods_list__:
                    self.method_groupbox3 = QGroupBox(self._method)
                    self.method_groupbox3.setCheckable(True)
                    self.method_groupbox3.setChecked(False)
                    self.method_groupbox3.clicked.connect(
                        self.other_method_checked)
                    self.method_groupbox3.layout = QGridLayout()
                    self.method_name3 = self.name_symbol3 = QLabel(
                        self._method)
                    self.method_groupbox3.layout.addWidget(self.method_name3)
                    self.method_groupbox3.setLayout(
                        self.method_groupbox3.layout)
                    self.other_methods_layout.addWidget(self.method_groupbox3)

                _, self.method_parameters_dictef = eto_read_methods_data()
                self.methods_list___ = []
                for self.method_f, self.parameters_f in self.method_parameters_dictef.items():
                    self.parameters_f = self.parameters_f.split(', ')
                    self.parameters_to_check_f = self.label_remove_.text().split(', ') + \
                        self.lista_dostupnih_param
                    resulta = all(
                        elem in self.parameters_to_check_f for elem in self.parameters_f)
                    if resulta:
                        if sender in self.parameters_f:
                            self.methods_list___.append(self.method_f)
                for self.f_method in self.methods_list___:
                    self.method_groupbox5 = QGroupBox(self.f_method)
                    self.method_groupbox5.setCheckable(True)
                    self.method_groupbox5.setChecked(False)
                    self.method_groupbox5.clicked.connect(
                        self.eto_method_checked)
                    self.method_groupbox5.layout = QGridLayout()
                    self.method_name5 = self.name_symbol5 = QLabel(
                        self.f_method)
                    self.method_groupbox5.layout.addWidget(self.method_name5)
                    self.method_groupbox5.setLayout(
                        self.method_groupbox5.layout)
                    self.eto_methods_layout.addWidget(self.method_groupbox5)

                _, self.method_parameters_dictefa = wb_read_methods_data()
                self.methods_list___a = []
                for self.method_fa, self.parameters_fa in self.method_parameters_dictefa.items():
                    self.parameters_fa = self.parameters_fa.split(', ')
                    self.parameters_to_check_fa = self.label_remove_k.text().split(', ') + \
                        self.lista_dostupnih_param
                    resultaa = all(
                        elem in self.parameters_to_check_fa for elem in self.parameters_fa)
                    if resultaa:
                        if sender in self.parameters_fa:
                            self.methods_list___a.append(self.method_fa)
                for self.fa_method in self.methods_list___a:
                    self.method_groupbox6 = QGroupBox(self.fa_method)
                    self.method_groupbox6.setCheckable(True)
                    self.method_groupbox6.setChecked(False)
                    self.method_groupbox6.clicked.connect(
                        self.wb_method_checked)
                    self.method_groupbox6.layout = QGridLayout()
                    self.method_name6 = self.name_symbol6 = QLabel(
                        self.fa_method)
                    self.method_groupbox6.layout.addWidget(self.method_name6)
                    self.method_groupbox6.setLayout(
                        self.method_groupbox6.layout)
                    self.wb_methods_layout.addWidget(self.method_groupbox6)
        else:
            sender = self.sender().title()
            self.cpl.remove(sender)
            self.apl.remove(sender)
            self.kpl.remove(sender)
            self.label_remove.setText(', '.join(self.cpl))
            self.label_remove_.setText(', '.join(self.apl))
            self.label_remove_k.setText(', '.join(self.kpl))

            if sender not in self.label_remove.text():
                _, self.method_parameters_dictee = other_read_methods_data_on_update()
                self.methods_list__e = []
                for self.method_e, self.parameters_e in self.method_parameters_dictee.items():
                    self.parameters_e = self.parameters_e.split(', ')
                    if sender in self.parameters_e:
                        self.methods_list__e.append(self.method_e)
                for self.objectee in self.other_methods_scroll.children():
                    if self.objectee.__class__.__name__ == 'QGroupBox':
                        if self.objectee.title() in self.methods_list__e:
                            self.other_methods_scroll.children().remove(self.objectee)
                            if self.objectee.title() in self.apl:
                                self.apl.remove(self.objectee.title())
                                self.label_remove_.setText(', '.join(self.apl))
                            if self.objectee.title() in self.cpl:
                                self.cpl.remove(self.objectee.title())
                                self.label_remove.setText(', '.join(self.cpl))
                            if self.objectee.title() in self.kpl:
                                self.kpl.remove(self.objectee.title())
                                self.label_remove_k.setText(
                                    ', '.join(self.kpl))
                            self.objectee.deleteLater()

                _, self.method_parameters_dicteeg = eto_read_methods_data()
                self.methods_list__g = []
                for self.method_g, self.parameters_g in self.method_parameters_dicteeg.items():
                    self.parameters_g = self.parameters_g.split(', ')
                    if sender in self.parameters_g:
                        self.methods_list__g.append(self.method_g)
                for self.objecteeg in self.eto_methods_scroll.children():
                    if self.objecteeg.__class__.__name__ == 'QGroupBox':
                        if self.objecteeg.title() in self.methods_list__g:
                            self.eto_methods_scroll.children().remove(self.objecteeg)
                            if self.objecteeg.title() in self.apl:
                                self.apl.remove(self.objecteeg.title())
                                self.label_remove_.setText(', '.join(self.apl))
                            if self.objecteeg.title() in self.kpl:
                                self.kpl.remove(self.objecteeg.title())
                                self.label_remove_k.setText(
                                    ', '.join(self.kpl))
                            self.objecteeg.deleteLater()

                _, self.method_parameters_dicteega = wb_read_methods_data()
                self.methods_list__ga = []
                for self.method_ga, self.parameters_ga in self.method_parameters_dicteega.items():
                    self.parameters_ga = self.parameters_ga.split(', ')
                    if sender in self.parameters_ga:
                        self.methods_list__ga.append(self.method_ga)
                for self.objecteega in self.wb_methods_scroll.children():
                    if self.objecteega.__class__.__name__ == 'QGroupBox':
                        if self.objecteega.title() in self.methods_list__ga:
                            self.wb_methods_scroll.children().remove(self.objecteega)
                            self.objecteega.deleteLater()

    def eto_methods_info(self):
        self.eto_methods_groupbox = QGroupBox('ETO Methods: ')
        self.eto_methods_layout = QVBoxLayout()
        self.eto_methods_scroll = QWidget()
        self.texte_ = ', '.join(self.base_data_list)
        self.label_remove_ = QLabel(self.texte_)
        self.label_remove_.setWordWrap(True)
        self.all_available_eto_methods_data, self.eto_method_parameters_dict = eto_read_methods_data()
        for self.method_w, self.parameters in self.eto_method_parameters_dict.items():
            self.parameters = self.parameters.split(', ')
            self.parameters_to_check = self.label_remove_.text().split(', ') + \
                self.lista_dostupnih_param
            resulta = all(
                elem in self.parameters_to_check for elem in self.parameters)
            if resulta:
                self.method_groupbox = QGroupBox(self.method_w)
                self.method_groupbox.setCheckable(True)
                self.method_groupbox.setChecked(False)
                self.method_groupbox.clicked.connect(self.eto_method_checked)
                self.method_groupbox.layout = QGridLayout()
                self.method_name = self.name_symbol = QLabel(self.method_w)
                self.method_groupbox.layout.addWidget(self.method_name)
                self.method_groupbox.setLayout(self.method_groupbox.layout)
                self.eto_methods_layout.addWidget(self.method_groupbox)
            else:
                pass
        self.eto_methods_scroll.setLayout(self.eto_methods_layout)
        methods = QScrollArea()
        methods.setWidget(self.eto_methods_scroll)
        methods.setWidgetResizable(1)
        self.eto_methods_groupbox.layout = QVBoxLayout()
        self.eto_methods_groupbox.layout.addWidget(methods)
        self.eto_methods_groupbox.layout.addWidget(self.label_remove_)
        self.eto_methods_groupbox.setLayout(self.eto_methods_groupbox.layout)
        return self.eto_methods_groupbox

    @QtCore.pyqtSlot()
    def eto_method_checked(self):
        if not self.label_remove_.text():
            self.apl = []
        else:
            self.apl = self.label_remove_.text().split(', ')
            self.kpl = self.label_remove_k.text().split(', ')

        if self.sender().isChecked() == True:
            sender = self.sender().title()
            self.apl.append(sender)
            self.kpl.append(sender)
            self.label_remove_.setText(', '.join(self.apl))
            self.label_remove_k.setText(', '.join(self.kpl))
            _, self.method_parameters_dictefau = wb_read_methods_data()
            self.methods_list___au = []
            for self.method_fau, self.parameters_fau in self.method_parameters_dictefau.items():
                self.parameters_fau = self.parameters_fau.split(', ')
                self.parameters_to_check_fau = self.label_remove_k.text().split(', ') + \
                    self.lista_dostupnih_param
                resultaau = all(
                    elem in self.parameters_to_check_fau for elem in self.parameters_fau)
                if resultaau:
                    if sender in self.parameters_fau:
                        self.methods_list___au.append(self.method_fau)
            for self.fau_method in self.methods_list___au:
                self.method_groupbox7 = QGroupBox(self.fau_method)
                self.method_groupbox7.setCheckable(True)
                self.method_groupbox7.setChecked(False)
                self.method_groupbox7.clicked.connect(self.wb_method_checked)
                self.method_groupbox7.layout = QGridLayout()
                self.method_name7 = self.name_symbol7 = QLabel(self.fau_method)
                self.method_groupbox7.layout.addWidget(self.method_name7)
                self.method_groupbox7.setLayout(self.method_groupbox7.layout)
                self.wb_methods_layout.addWidget(self.method_groupbox7)
        else:
            sender = self.sender().title()
            self.apl.remove(sender)
            self.kpl.remove(sender)
            self.label_remove_.setText(', '.join(self.apl))
            self.label_remove_k.setText(', '.join(self.kpl))

            _, self.method_parameters_dicteegab = wb_read_methods_data()
            self.methods_list__gab = []
            for self.method_gab, self.parameters_gab in self.method_parameters_dicteegab.items():
                self.parameters_gab = self.parameters_gab.split(', ')
                if sender in self.parameters_gab:
                    self.methods_list__gab.append(self.method_gab)
            for self.objecteegab in self.wb_methods_scroll.children():
                if self.objecteegab.__class__.__name__ == 'QGroupBox':
                    if self.objecteegab.title() in self.methods_list__gab:
                        self.wb_methods_scroll.children().remove(self.objecteegab)
                        self.objecteegab.deleteLater()

    def wb_methods_info(self):
        self.wb_methods_groupbox = QGroupBox('WB Methods: ')
        self.wb_methods_layout = QVBoxLayout()
        self.wb_methods_scroll = QWidget()
        self.texte_k = ', '.join(self.base_data_list)
        self.label_remove_k = QLabel(self.texte_k)
        self.label_remove_k.setWordWrap(True)
        self.all_available_wb_methods_data, self.wb_method_parameters_dict = wb_read_methods_data()
        for self.method_k, self.parameters_k in self.wb_method_parameters_dict.items():
            self.parameters_k = self.parameters_k.split(', ')
            self.parameters_to_check_k = self.label_remove_k.text().split(', ') + \
                self.lista_dostupnih_param
            resultak = all(
                elem in self.parameters_to_check_k for elem in self.parameters_k)
            if resultak:
                self.method_groupbox8 = QGroupBox(self.method_k)
                self.method_groupbox8.setCheckable(True)
                self.method_groupbox8.setChecked(False)
                self.method_groupbox8.clicked.connect(self.wb_method_checked)
                self.method_groupbox8.layout = QGridLayout()
                self.method_name8 = self.name_symbol8 = QLabel(self.method_k)
                self.method_groupbox8.layout.addWidget(self.method_name8)
                self.method_groupbox8.setLayout(self.method_groupbox8.layout)
                self.wb_methods_layout.addWidget(self.method_groupbox8)
            else:
                pass
        self.wb_methods_scroll.setLayout(self.wb_methods_layout)
        methods = QScrollArea()
        methods.setWidget(self.wb_methods_scroll)
        methods.setWidgetResizable(1)
        self.wb_methods_groupbox.layout = QVBoxLayout()
        self.wb_methods_groupbox.layout.addWidget(methods)
        self.wb_methods_groupbox.layout.addWidget(self.label_remove_k)
        self.wb_methods_groupbox.setLayout(self.wb_methods_groupbox.layout)
        return self.wb_methods_groupbox

    @QtCore.pyqtSlot()
    def wb_method_checked(self):
        if not self.label_remove_k.text():
            self.kpl = []
        else:
            self.kpl = self.label_remove_k.text().split(', ')
        if self.sender().isChecked() == True:
            sender = self.sender().title()
            self.kpl.append(sender)
            self.label_remove_k.setText(', '.join(self.kpl))
        else:
            sender = self.sender().title()
            self.kpl.remove(sender)
            self.label_remove_k.setText(', '.join(self.kpl))

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
        self.calculate_options_groupbox.setLayout(
            self.calculate_options_groupbox.layout)
        return self.calculate_options_groupbox

    def status_info(self):
        groupBox = QGroupBox('status')
        groupBox.setFixedHeight(80)
        self.status_label = QLabel(
            'status  | kalkulacija: 0 | mezertacmuminacija: 0')
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        # self.progress_bar.setVisible(False)
        # self.progress_bar.setSizePolicy()
        hbox = QHBoxLayout()
        hbox.addWidget(self.status_label)
        hbox.addWidget(self.progress_bar)
        groupBox.setLayout(hbox)
        return groupBox


if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = CalculateWidget()
    sys.exit(mainApplication.exec_())
