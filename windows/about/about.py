import sys
# app modules and windows
#from variables import css
#
# pyqt5 modules
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QDialog, QTabWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class AboutWindow(QWidget):
    def __init__(self):
        self.language = {
            "about_window_title": "Abouta SRCLET",
            "version": "Version",
            "development": "Development",
            "copyright": "Copyright",
            "disclamair": "Disclamair",
            "version_ver": "Version 1.0",
            "version_date": "October 2022",
            "version_dev": "Developed by:",
            "version_dev_by": "Sabrija Čadro and Mirza Uzunović",
            "version_contact": "Contact:",
            "version_contact_mail": "meet.jeanmonnet@gmail.com",
            "version_web": "Web:",
            "version_web_location": "https://meet.motherlandia.org/srclet/"
        }
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        #self.language = language
        self.window_gui()

    def window_gui(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle(self.language['about_window_title'])
        #self.setWindowIcon(QIcon(css.menu_about_icon))
        self.center_gui()
        self.tabovi = MyTabWidget(self, language=self.language)
        self.tabovi.resize(800, 600)
        self.show()
        
    def center_gui(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
class MyTabWidget(QWidget):
    def __init__(self, parent, language):
        super(QWidget, self).__init__(parent)
        self.language = language
        self.layout = QVBoxLayout(self)
  
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab_version = QWidget()
        self.tab_development = QWidget()
        self.tab_copyright = QWidget()
        self.tab_disclamair = QWidget()
          
        # Add tabs
        self.tabs.addTab(self.tab_version, self.language['version'])
        self.tabs.addTab(self.tab_development, self.language['development'])
        self.tabs.addTab(self.tab_copyright, self.language['copyright'])
        self.tabs.addTab(self.tab_disclamair, self.language['disclamair'])
  
        # Create tab version
        self.tab_version.layout = QGridLayout()
        #self.tab_version.layout = QVBoxLayout(self)
        
        self.version_ver = QLabel(self.language['version_ver'])
        self.tab_version.layout.addWidget(self.version_ver)
        
        self.version_date = QLabel(self.language['version_date'])
        self.tab_version.layout.addWidget(self.version_date)
        
        self.version_dev = QLabel(self.language['version_dev'])
        self.tab_version.layout.addWidget(self.version_dev)
        
        self.version_dev_by = QLabel(self.language['version_dev_by'])
        self.tab_version.layout.addWidget(self.version_dev_by)
        
        self.tab_version.setLayout(self.tab_version.layout)
        
        # Create tab development
        self.tab_development.layout = QVBoxLayout(self)
        self.l = QLabel()
        self.l.setText("Version")
        self.tab_development.layout.addWidget(self.l)
        self.tab_development.setLayout(self.tab_development.layout)
        
        # Create tab copyright
        self.tab_copyright.layout = QVBoxLayout(self)
        self.l = QLabel()
        self.l.setText("Version")
        self.tab_copyright.layout.addWidget(self.l)
        self.tab_copyright.setLayout(self.tab_copyright.layout)
        
        # Create tab disclamair
        self.tab_disclamair.layout = QVBoxLayout(self)
        self.l = QLabel()
        self.l.setText("Version")
        self.tab_disclamair.layout.addWidget(self.l)
        self.tab_disclamair.setLayout(self.tab_disclamair.layout)
  
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        

        
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = AboutWindow()
    sys.exit(mainApplication.exec_())