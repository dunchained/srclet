# python standard modules
import sys, os, json
from pathlib import Path

# app modules and windows
#from appdata import css
#from windows.parameters.add_parameter import AddParameter

# pyqt5 modules
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QListView, QPushButton, QApplication
from PyQt5.QtWidgets import QSizePolicy, QLineEdit, QAbstractItemView, QListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

class Parameters(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.WindowGUI()

    def WindowGUI(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('Parameters')
        #self.setWindowIcon(QIcon(css.menu_about_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.createLeftGroupBox(), 0, 0, 1, 1)
        self.grid.addWidget(self.createRightGroupBox(), 0, 1, 1, 1)
        self.grid.addWidget(self.createDownGroupBox(), 1, 0, 1, 2)
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def createLeftGroupBox(self):
        LeftGroupBox = QGroupBox('Parameters used for calucation:')
        self.list_widget = QListWidget()
        get_files = next(os.walk(os.path.curdir + "/parameters/"), (None, None, []))[2]
        file_list = []
        for file in get_files:
            file_list.append(Path(file).stem)
                   
        self.list_widget.addItems(file_list)

        self.list_widget.currentItemChanged.connect(self.index_changed)
        
        buttonRefresh = QPushButton('Refresh parameter list')
        buttonRefresh.clicked.connect(self.refresh_parameters_list)
        
               

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(buttonRefresh)
        layout.addStretch(1)
        LeftGroupBox.setLayout(layout)
        
        return LeftGroupBox
    
    def index_changed(self, i): # Not an index, i is a QListItem
        json_path = 'parameters/' + i.text() + '.json'
       
        with open(json_path) as json_file:
            data = json.load(json_file)
            self.parameter_name.setText(data["name"])
            self.parameter_unit.setText(data["unit"])
            
    def refresh_parameters_list(self):
        self.list_widget.repaint()
    
    def createRightGroupBox(self):
        RightGroupBox = QGroupBox('Parameters definition:')
        self.text_parameter_name = QLabel('Parameter name:')
        self.parameter_name = QLineEdit()
        self.text_parameter_unit = QLabel('Parameter unit:')
        self.parameter_unit = QLineEdit()
        buttonSaveProject = QPushButton('Save changes')
        buttonSaveProject.clicked.connect(self.close)
        buttonCancel = QPushButton('Cancel')
        buttonCancel.clicked.connect(self.close)
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_parameter_name)
        layout.addWidget(self.parameter_name)
        layout.addWidget(self.text_parameter_unit)
        layout.addWidget(self.parameter_unit)
        layout.addWidget(buttonSaveProject)
        layout.addWidget(buttonCancel)
        layout.addStretch(1)
        RightGroupBox.setLayout(layout)
        
        return RightGroupBox
    
    def createDownGroupBox(self):
        DownGroupBox = QGroupBox()
        
        buttonClose = QPushButton('Close')
        buttonClose.clicked.connect(self.close)
        
        buttonAddParameter = QPushButton('Add new parameter')
        buttonAddParameter.clicked.connect(self.newParameterWindow)
        
        layout = QHBoxLayout()
        layout.addWidget(buttonAddParameter)
        
        layout.addWidget(buttonClose)
        
        
        layout.setAlignment(Qt.AlignRight)
        layout.addStretch(1)
        DownGroupBox.setLayout(layout)
        
        return DownGroupBox
    
    def newParameterWindow(self):
        self.window = AddParameter()
        
    


#obrisati nakon uvezivanja cijelog
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = Parameters()
    sys.exit(mainApplication.exec_())