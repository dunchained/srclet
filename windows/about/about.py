import sys, os
# app modules and windows
#from variables import css
# pyqt5 modules
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QDialog, QTabWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QGridLayout, QHBoxLayout, QGroupBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

class AboutWindow(QWidget):
    def __init__(self):
        self.language = {
            "about_window_title": "Abouta SRCLET",
            "version": "Version",
            "development": "Development",
            "copyright": "Copyright",
            "disclamair": "Disclamair",
            "version_ver": "Version:",
            "version_version": "1.0",
            "version_date_text": "Released:",
            "version_date_date": "October 2022",
            "version_dev_text": "Developed by:",
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
        self.tabs = QTabWidget()
        self.tab_version = QWidget()
        self.tab_development = QWidget()
        self.tab_copyright = QWidget()
        self.tab_disclamair = QWidget()
        self.tabs.addTab(self.tab_version, self.language['version'])
        self.tabs.addTab(self.tab_development, self.language['development'])
        self.tabs.addTab(self.tab_copyright, self.language['copyright'])
        self.tabs.addTab(self.tab_disclamair, self.language['disclamair'])
  
        # Create tab version
        self.tab_version.layout = QGridLayout()
        
        self.left_groupbox = QGroupBox()
        self.left_groupbox.layout = QVBoxLayout()
        self.label_photo = QLabel()
        self.pixmap = QPixmap('srclet/images/icons/srclet_drop.png')
        self.pixmap = self.pixmap.scaled(300, 300, Qt.KeepAspectRatio)
        self.label_photo.setPixmap(self.pixmap)
        self.left_groupbox.layout.addWidget(self.label_photo, alignment=Qt.AlignCenter)
        self.left_groupbox.setLayout(self.left_groupbox.layout)
        self.left_groupbox.setFlat(True)
        
        self.right_groupbox = QGroupBox()
        self.font =self.right_groupbox.font()
        self.font.setPointSize(14)
        self.right_groupbox.setFont(self.font)
        self.right_groupbox.layout = QGridLayout()
        self.flay = QFormLayout()
        
        self.label_photo = QLabel()
        self.pixmap = QPixmap('srclet/images/icons/srclet_cap.png')
        self.pixmap = self.pixmap.scaled(350, 300, Qt.KeepAspectRatio)
        self.label_photo.setPixmap(self.pixmap)
        self.flay.addRow(self.label_photo)
        
        self.label_version = QLabel(self.language['version_ver'])
        self.label_version_ver = QLabel(self.language['version_version'])
        self.flay.addRow(self.label_version, self.label_version_ver)
        
        self.label_date = QLabel(self.language['version_date_text'])
        self.label_date_date = QLabel(self.language['version_date_date'])
        self.flay.addRow(self.label_date, self.label_date_date)
        
        self.right_groupbox.setLayout(self.flay)
        self.right_groupbox.setFlat(True)
        

        self.tab_version.layout.addWidget(self.left_groupbox, 0, 0)
        self.tab_version.layout.addWidget(self.right_groupbox, 0, 1)
        self.tab_version.setLayout(self.tab_version.layout)
        
        # Create tab development
        self.tab_development.layout = QGridLayout()
        
        self.lijevi_groupbox = QGroupBox()
        self.lijevi_groupbox.layout = QVBoxLayout()
        self.label_slika = QLabel()
        self.pixmap = QPixmap('srclet/images/icons/srclet_drop.png')
        self.pixmap = self.pixmap.scaled(500, 400, Qt.KeepAspectRatio)
        self.label_slika.setPixmap(self.pixmap)
        self.lijevi_groupbox.layout.addWidget(self.label_slika, alignment=Qt.AlignCenter)
        self.lijevi_groupbox.setLayout(self.lijevi_groupbox.layout)
        self.lijevi_groupbox.setFlat(True)
        
        self.desni_groupbox = QGroupBox()
        self.desni_groupbox.layout = QVBoxLayout()
        self.label_slika1 = QLabel()
        self.pixmap1 = QPixmap('srclet/images/icons/srclet_drop.png')
        self.label_slika1.setPixmap(self.pixmap1)
        self.desni_groupbox.layout.addWidget(self.label_slika1, alignment=Qt.AlignCenter)
        self.desni_groupbox.setLayout(self.desni_groupbox.layout)
        
        self.tab_development.layout.addWidget(self.lijevi_groupbox, 0, 0)
        self.tab_development.layout.addWidget(self.desni_groupbox, 0, 1) 
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