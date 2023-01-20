from PyQt5.QtCore import pyqtSignal, QObject

class Communicate(QObject):
    print('smiju nam se djeca')
    refresh_signal = pyqtSignal()
