# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
import sys

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("Scroll")
window.resize(300,700)

mainbox = QtWidgets.QVBoxLayout() # Сюда поместим GroupBox

vbox = QtWidgets.QVBoxLayout() # Для кнопочек
scroll = QtWidgets.QScrollArea() # Скролиться должен GroupBox
group = QtWidgets.QGroupBox("Check Me") # Этот GroupBox

scroll.setWidget(group) # Для этого я передаю его в ScrollArea


for i in range(50): # Накидываем кнопочки
    vbox.addWidget(QtWidgets.QPushButton("button {}".format(i)))

group.setLayout(vbox) # Закидываем область с кнопками в группу 
mainbox.addWidget(group) # Закидываем группу в главный слой 
window.setLayout(mainbox) # Закрепляем главный слой

window.show()
sys.exit(app.exec_())