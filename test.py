from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TabWidget(object):
    def setupUi(self, TabWidget):
        TabWidget.setObjectName("TabWidget")
        TabWidget.resize(400, 300)
        
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
		
        self.Ouvrir_Onglet_1 = QtWidgets.QPushButton(self.tab_1)
        self.Ouvrir_Onglet_1.setGeometry(QtCore.QRect(10, 20, 91, 23))
        self.Ouvrir_Onglet_1.setObjectName("Ouvrir_Onglet_1")
		
        self.Ouvrir_Onglet_2 = QtWidgets.QPushButton(self.tab_1)
        self.Ouvrir_Onglet_2.setGeometry(QtCore.QRect(10, 50, 91, 23))
        self.Ouvrir_Onglet_2.setObjectName("Ouvrir_Onglet_2")
		
        self.Ouvrir_Onglet_3 = QtWidgets.QPushButton(self.tab_1)
        self.Ouvrir_Onglet_3.setGeometry(QtCore.QRect(10, 80, 91, 23))
        self.Ouvrir_Onglet_3.setObjectName("Ouvrir_Onglet_3")
		
        TabWidget.addTab(self.tab_1, "")
		
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        TabWidget.addTab(self.tab_2, "")
		
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        TabWidget.addTab(self.tab_3, "")
		
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        TabWidget.addTab(self.tab_4, "")

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)
		
    def Fonction_Ouvrir_Onglet_1(self):
        self.window = QtWidgets()
        self.ui = Ui_TabWidget()
        self.ui.setupUi(self.window.tab_2)
        self.window.tab_2.show()
		
        self.Ouvrir_Onglet_1.clicked.connect(self.Fonction_Ouvrir_Onglet_1)
		
    def Fonction_Ouvrir_Onglet_2(self):
        self.Ui_TabWidget.setCurrentIndex(2)

        self.Ouvrir_Onglet_2.clicked.connect(self.Fonction_Ouvrir_Onglet_2)
		
        self.Ouvrir_Onglet_3.clicked.connect(self.TabWidget.setCurrentIndex(3))


    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "TabWidget"))
        self.Ouvrir_Onglet_1.setText(_translate("TabWidget", "Ouvrir_Onglet_1"))
        self.Ouvrir_Onglet_2.setText(_translate("TabWidget", "Ouvrir_Onglet_2"))
        self.Ouvrir_Onglet_3.setText(_translate("TabWidget", "Ouvrir_Onglet_3"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_1), _translate("TabWidget", "Menu_principal"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_2), _translate("TabWidget", "Onglet 1"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_3), _translate("TabWidget", "Onglet 2"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_4), _translate("TabWidget", "Onlget 3"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TabWidget = QtWidgets.QTabWidget()
    ui = Ui_TabWidget()
    ui.setupUi(TabWidget)
    TabWidget.show()
    sys.exit(app.exec_())