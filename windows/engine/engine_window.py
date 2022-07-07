import os, sys, time
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGridLayout, QApplication
from PyQt5.QtWidgets import QDesktopWidget, QPushButton, QGroupBox, QTextEdit, QProgressBar
from PyQt5.QtCore import Qt


class EngineWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.WindowGUI()

    def WindowGUI(self):
        self.setFixedSize(400, 300)
        self.grid = QGridLayout()
        self.grid.addWidget(self.consoleLog(), 1, 1, 1, 1)
        self.grid.addWidget(self.progressLog(), 2, 1, 1, 1)
        self.grid.addWidget(self.optionsButtons(), 3, 1, 1, 1)
        self.setLayout(self.grid)
        self.centerUserInterface()
        self.show()
        
    def centerUserInterface(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def consoleLog(self):
        self.label_console = QTextEdit()
        self.label_console.setWordWrapMode(True)
        self.label_console.setText('srclet v1:2022')
        return self.label_console

    def progressLog(self):
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        return self.progress


    def optionsButtons(self):
        
        groupBox = QGroupBox()
        buttonIncrement = QPushButton('Progress Bar')
        buttonIncrement.clicked.connect(self.progressIncrement)
        buttonCancel = QPushButton('Cancel')
        buttonCancel.clicked.connect(self.close)
        vbox = QVBoxLayout()
        vbox.addWidget(buttonIncrement)
        vbox.addWidget(buttonCancel)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def progressIncrement(self):
        count = self.progress.value()
        count += 1
        self.progress.setValue(count)

if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = EngineWindow()
    sys.exit(mainApplication.exec_())