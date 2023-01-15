import sys, os
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
            "version_dev_by": "Sabrija Čadro, Mirza Uzunović",
            "version_contact": "Contact:",
            "version_contact_mail": "meet.jeanmonnet@gmail.com",
            "version_web": "Web:",
            "version_web_location": "https://meet.motherlandia.org/srclet/",
            "development_text1": "Text text1",
            "development_text2": "Text text2",
            "development_text3": "Text text3",
            "copyright_text1": "All rights reserved.",
            "copyright_text2": "Reproduction and dissemination of material related to this computer software for educational, research or other non-commercial purposes are authorized without any prior written permission from the copyright holders provided the source is fully acknowledged.",
            "copyright_text3": "The authors hope that this software tool, with God's help, will be useful to all people.",
            "copyright_text4": "Reproduction of material in this information product for resale or other commercial purposes is prohibited without written permission of the copyright holders.",
            "copyright_text5": "Applications for such permission should be addressed to the softwere developer Mirza Uzunović by e-mail meet.jeanmonnet@gmail.com",
            "copyright_text6": "Authors [2022]",
            "disclamair_text1": "Authors decline all responsibility for errors or deficiencies in the database or in the files and documents that come with the SRCLET softwere.",
            "disclamair_text2": "Authors also declines any responsibility for updating the data and assumes no responsibility for errors and omissions in the data provided. Users are, however, kindly asked to report any errors or deficiencies at: meet.jeanmonnet@gmail.com.",
            "disclamair_text3": "The European Commission support for the production of this prodact does not constitute an endorsement of the contents which reflects the views only of the authors, and the Commission cannot be held responsible for any use which may be made of the information contained therein."
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
                
        self.groupbox = QGroupBox()
        self.font = self.groupbox.font()
        self.font.setPointSize(14)
        self.groupbox.setFont(self.font)
        self.groupbox.layout = QGridLayout()
        self.flay = QFormLayout()
        
        self.label_photo = QLabel()
        self.pixmap = QPixmap('srclet/images/icons/srclet_caption.png')
        self.pixmap = self.pixmap.scaled(700, 400, Qt.KeepAspectRatio)
        self.label_photo.setPixmap(self.pixmap)
        self.flay.addRow(self.label_photo)
        
        self.label_version = QLabel(self.language['version_ver'])
        self.label_version_ver = QLabel(self.language['version_version'])
        self.flay.addRow(self.label_version, self.label_version_ver)
        
        self.label_date = QLabel(self.language['version_date_text'])
        self.label_date_date = QLabel(self.language['version_date_date'])
        self.flay.addRow(self.label_date, self.label_date_date)
        
        self.label_developed = QLabel(self.language['version_dev_text'])
        self.label_dev_by = QLabel(self.language['version_dev_by'])
        self.flay.addRow(self.label_developed, self.label_dev_by)
        
        self.label_contact = QLabel(self.language['version_contact'])
        self.label_contact_contact = QLabel(self.language['version_contact_mail'])
        self.flay.addRow(self.label_contact, self.label_contact_contact)
        
        self.label_web = QLabel(self.language['version_web'])
        self.label_web_location = QLabel(self.language['version_web_location'])
        self.flay.addRow(self.label_web, self.label_web_location)
        
        self.groupbox.setLayout(self.flay)
        self.groupbox.setFlat(True)
        
        self.tab_version.layout.addWidget(self.groupbox)
        self.tab_version.setLayout(self.tab_version.layout)
        
        
        
        
        # Create tab development
        self.tab_development.layout = QGridLayout()
                
        self.groupbox2 = QGroupBox()
        self.font = self.groupbox2.font()
        self.font.setPointSize(14)
        self.groupbox2.setFont(self.font)
        self.groupbox2.layout = QGridLayout()
        
        self.label_photo = QLabel()
        self.pixmap = QPixmap('srclet/images/icons/eu_logo.jpg')
        self.pixmap = self.pixmap.scaled(400, 100, Qt.KeepAspectRatio)
        self.label_photo.setPixmap(self.pixmap)
        
        self.label_photo2 = QLabel()
        self.pixmap2 = QPixmap('srclet/images/icons/eu_logo.jpg')
        self.pixmap2 = self.pixmap2.scaled(400, 100, Qt.KeepAspectRatio)
        self.label_photo2.setPixmap(self.pixmap2)
        
        self.label_photo3 = QLabel()
        self.pixmap3 = QPixmap('srclet/images/icons/unsa_logo.png')
        self.pixmap3 = self.pixmap3.scaled(200, 100, Qt.KeepAspectRatio)
        self.label_photo3.setPixmap(self.pixmap3)
        
        self.label_photo4 = QLabel()
        self.pixmap4 = QPixmap('srclet/images/icons/ppf_logo.png')
        self.pixmap4 = self.pixmap4.scaled(200, 100, Qt.KeepAspectRatio)
        self.label_photo4.setPixmap(self.pixmap4)
        
        self.label_photo5 = QLabel()
        self.pixmap5 = QPixmap('srclet/images/icons/bih_location.png')
        self.pixmap5 = self.pixmap5.scaled(300, 100, Qt.KeepAspectRatio)
        self.label_photo5.setPixmap(self.pixmap5)
        
        self.label1 = QLabel(self.language['development_text1'])
        self.label2 = QLabel(self.language['development_text2'])
        self.label3 = QLabel(self.language['development_text3'])
        
        
        
        self.groupbox2.layout.addWidget(self.label_photo, 0, 0, 1, 1)
        self.groupbox2.layout.addWidget(self.label_photo2, 0, 1, 1, 1)
        self.groupbox2.layout.addWidget(self.label_photo3, 1, 0, 1, 1)
        self.groupbox2.layout.addWidget(self.label_photo4, 1, 1, 1, 1)
        self.groupbox2.layout.addWidget(self.label_photo5, 2, 0, 1, 2)
        self.groupbox2.layout.addWidget(self.label1, 3, 0, 1, 2)
        self.groupbox2.layout.addWidget(self.label2, 4, 0, 1, 2)
        self.groupbox2.layout.addWidget(self.label3, 5, 0, 1, 2)

        self.groupbox2.setLayout(self.groupbox2.layout)
        self.groupbox2.setFlat(True)
        
        self.tab_development.layout.addWidget(self.groupbox2)
        self.tab_development.setLayout(self.tab_development.layout)
        
        
        
        
        # Create tab copyright
        self.tab_copyright.layout = QVBoxLayout(self)
        self.groupbox3 = QGroupBox()
        self.font = self.groupbox3.font()
        self.font.setPointSize(14)
        self.groupbox3.setFont(self.font)
        self.groupbox3.layout = QGridLayout()
        
        self.label1 = QLabel(self.language['copyright_text1'])
        self.label1.setWordWrap(True)
        self.label2 = QLabel(self.language['copyright_text2'])
        self.label2.setWordWrap(True)
        self.label3 = QLabel(self.language['copyright_text3'])
        self.label3.setWordWrap(True)
        self.label4 = QLabel(self.language['copyright_text4'])
        self.label4.setWordWrap(True)
        self.label5 = QLabel(self.language['copyright_text5'])
        self.label5.setWordWrap(True)
        self.label6 = QLabel(self.language['copyright_text6'])
        self.label6.setWordWrap(True)
        
        
        self.groupbox3.layout.addWidget(self.label1, 0, 0)
        self.groupbox3.layout.addWidget(self.label2, 1, 0)
        self.groupbox3.layout.addWidget(self.label3, 2, 0)
        self.groupbox3.layout.addWidget(self.label4, 3, 0)
        self.groupbox3.layout.addWidget(self.label5, 4, 0)
        self.groupbox3.layout.addWidget(self.label6, 5, 0)

        self.groupbox3.setLayout(self.groupbox3.layout)
        self.groupbox3.setFlat(True)
        self.tab_copyright.layout.addWidget(self.groupbox3)
        self.tab_copyright.setLayout(self.tab_copyright.layout)
        
        
        
        
        # Create tab disclamair
        self.tab_disclamair.layout = QGridLayout(self)
        self.groupbox4 = QGroupBox()
        self.font = self.groupbox4.font()
        self.font.setPointSize(14)
        self.groupbox4.setFont(self.font)
        self.groupbox4.layout = QGridLayout()
                      
        self.label1 = QLabel(self.language['disclamair_text1'])
        self.label1.setWordWrap(True)
        self.label2 = QLabel(self.language['disclamair_text2'])
        self.label2.setWordWrap(True)
        self.label3 = QLabel(self.language['disclamair_text3'])
        self.label3.setWordWrap(True)
        
        self.groupbox4.layout.addWidget(self.label1, 0, 0)
        self.groupbox4.layout.addWidget(self.label2, 1, 0)
        self.groupbox4.layout.addWidget(self.label3, 2, 0)
        
        self.groupbox4.setLayout(self.groupbox4.layout)
        self.groupbox4.setFlat(True)
        self.tab_disclamair.layout.addWidget(self.groupbox4)
        self.tab_disclamair.setLayout(self.tab_disclamair.layout)
  
  
  
  
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        

        
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = AboutWindow()
    sys.exit(mainApplication.exec_())