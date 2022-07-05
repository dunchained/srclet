# python standard modules
import os, sys, json
from pathlib import Path


# app modules and windows
#from appdata import css

# pyqt5 modules
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu, QPushButton, QTableWidget, QApplication, QSizePolicy
from PyQt5.QtWidgets import QGroupBox, QTableWidgetItem, QGridLayout

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
                print(item_text)
                lista2.append(item_text)
            lista.append(lista2)
        pd.DataFrame(data=None, index=[0], columns=None, dtype=None, copy=False)

        pprf = pd.DataFrame(lista)
        rt = pprf.transpose()
        rt.to_excel(self.project_path + "/data.xlsx")
    
    def closeSelf(self):
        self.close()

    def createDataType(self):

        get_files = next(os.walk(os.path.curdir + "/parameters/"), (None, None, []))[2]
        self.file_list = []
        for file in get_files:
            #self.file_list.append(Path(file).stem)
            #print('/parameters/' + Path(file).stem + '.json')
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
            for parameter in self.file_list:

                self.temp = self.menu.addAction(parameter)
                self.temp.triggered.connect(self.buttonClicked)
            self.buttons[i].setMenu(self.menu)
            self.menu.columnIndex = i

    def buttonClicked(self, ):
        sender = self.sender()
        sender_text = sender.text()
        self.buttons[sender.parent().columnIndex].setText(sender_text)
        return sender

    def createOptions(self):

        self.groupBoxCheckables = QGroupBox('Options:')
        self.groupBoxButtons = QGroupBox('Options:')
        self.groupBox = QGroupBox('Options:')
        self.boxButtons = QGridLayout()
        self.boxCheckables = QGridLayout()
        self.boxGroupBox = QGridLayout()

        self.buttonSave = QPushButton('Save Project Data')
        self.buttonSave.clicked.connect(self.saveData)
        self.buttonClose = QPushButton('Cancel')
        self.buttonClose.clicked.connect(self.closeSelf)

        self.boxButtons.addWidget(self.buttonSave, 0, 0)
        self.boxButtons.addWidget(self.buttonClose, 1, 0)
        self.groupBoxButtons.setLayout(self.boxButtons)

        self.boxCheckables.addWidget(self.buttonSave, 0, 0)
        self.boxCheckables.addWidget(self.buttonClose, 1, 0)
        self.groupBoxCheckables.setLayout(self.boxCheckables)

        self.boxGroupBox.addWidget(self.groupBoxCheckables, 0, 0)
        self.boxGroupBox.addWidget(self.groupBoxButtons, 1, 0)
        self.groupBox.setLayout(self.boxGroupBox)


        return self.groupBox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CheckDataTypeWidget()
    sys.exit(app.exec_())