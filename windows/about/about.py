from mortys.language_morty import bind_key, events
from variables import css, var
from mortys.font_morty import read_text_font_size
from PyQt6.QtWidgets import QWidget, QTabWidget, QFormLayout
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QGridLayout, QGroupBox
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

class AboutWindow(QWidget):
    def __init__(self, language):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowCloseButtonHint)
        self.language = language
        self.window_gui()

    def window_gui(self):
        self.setFixedSize(var.about_window_widith, var.about_window_height)
        bind_key(self, "windowTitle", 'about_window_title')
        self.setWindowIcon(QIcon(css.about_icon))
        self.center_gui()
        self.tabovi = MyTabWidget(self, language=self.language)
        self.tabovi.resize(var.about_window_widith, var.about_window_height)
        self.show()

    def center_gui(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class MyTabWidget(QWidget):
    def __init__(self, parent, language):
        super().__init__(parent)
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

        events.changed.connect(self.translate_tabs)

        # Create tab version
        self.tab_version.layout = QGridLayout()
        self.groupbox = QGroupBox()
        self.font = self.groupbox.font()
        self.font.setPointSize(read_text_font_size())
        self.groupbox.setFont(self.font)
        self.groupbox.layout = QGridLayout()
        self.flay = QFormLayout()
        self.label_photo = QLabel()
        self.pixmap = QPixmap(css.about_window_image_srclet)
        self.pixmap = self.pixmap.scaled(700, 400, Qt.AspectRatioMode.KeepAspectRatio)
        self.label_photo.setPixmap(self.pixmap)
        self.flay.addRow(self.label_photo)
        self.label_version = bind_key(QLabel(), "text", 'version_ver')
        self.label_version_ver = bind_key(QLabel(), "text", 'version_version')
        self.flay.addRow(self.label_version, self.label_version_ver)
        self.label_date = bind_key(QLabel(), "text", 'version_date_text')
        self.label_date_date = bind_key(QLabel(), "text", 'version_date_date')
        self.flay.addRow(self.label_date, self.label_date_date)
        self.label_developed = bind_key(QLabel(), "text", 'version_dev_text')
        self.label_dev_by = bind_key(QLabel(), "text", 'version_dev_by')
        self.flay.addRow(self.label_developed, self.label_dev_by)
        self.label_contact = bind_key(QLabel(), "text", 'version_contact')
        self.label_contact_contact = bind_key(QLabel(), "text", 'version_contact_mail')
        self.flay.addRow(self.label_contact, self.label_contact_contact)
        self.label_web = bind_key(QLabel(), "text", 'version_web')
        self.label_web_location = bind_key(QLabel(), "text", 'version_web_location')
        self.flay.addRow(self.label_web, self.label_web_location)
        self.groupbox.setLayout(self.flay)
        self.groupbox.setFlat(True)
        self.tab_version.layout.addWidget(self.groupbox)
        self.tab_version.setLayout(self.tab_version.layout)

        # Create tab development
        self.tab_development.layout = QGridLayout()
        self.groupbox2 = QGroupBox()
        self.font = self.groupbox2.font()
        self.font.setPointSize(read_text_font_size())
        self.groupbox2.setFont(self.font)
        self.groupbox2.layout = QGridLayout()
        self.label_photo = QLabel()
        self.pixmap = QPixmap(css.about_window_image_development)
        self.pixmap = self.pixmap.scaled(400, 100, Qt.AspectRatioMode.KeepAspectRatio)
        self.label_photo.setPixmap(self.pixmap)
        self.label1 = bind_key(QLabel(), "text", 'development_text1')
        self.label1.setWordWrap(True)
        self.label2 = bind_key(QLabel(), "text", 'development_text2')
        self.label2.setWordWrap(True)
        self.label3 = bind_key(QLabel(), "text", 'development_text3')
        self.label3.setWordWrap(True)
        self.groupbox2.layout.addWidget(self.label_photo, 0, 0)
        self.groupbox2.layout.addWidget(self.label1, 1, 0)
        self.groupbox2.layout.addWidget(self.label2, 2, 0)
        self.groupbox2.layout.addWidget(self.label3, 3, 0)
        self.groupbox2.setLayout(self.groupbox2.layout)
        self.groupbox2.setFlat(True)
        self.tab_development.layout.addWidget(self.groupbox2)
        self.tab_development.setLayout(self.tab_development.layout)

        # Create tab copyright
        self.tab_copyright.layout = QGridLayout()
        self.groupbox3 = QGroupBox()
        self.font = self.groupbox3.font()
        self.font.setPointSize(read_text_font_size())
        self.groupbox3.setFont(self.font)
        self.groupbox3.layout = QGridLayout()
        self.label1 = bind_key(QLabel(), "text", 'copyright_text1')
        self.label1.setWordWrap(True)
        self.label2 = bind_key(QLabel(), "text", 'copyright_text2')
        self.label2.setWordWrap(True)
        self.label3 = bind_key(QLabel(), "text", 'copyright_text3')
        self.label3.setWordWrap(True)
        self.label4 = bind_key(QLabel(), "text", 'copyright_text4')
        self.label4.setWordWrap(True)
        self.label5 = bind_key(QLabel(), "text", 'copyright_text5')
        self.label5.setWordWrap(True)
        self.label6 = bind_key(QLabel(), "text", 'copyright_text6')
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
        self.tab_disclamair.layout = QGridLayout()
        self.groupbox4 = QGroupBox()
        self.font = self.groupbox4.font()
        self.font.setPointSize(read_text_font_size())
        self.groupbox4.setFont(self.font)
        self.groupbox4.layout = QGridLayout()
        self.label1 = bind_key(QLabel(), "text", 'disclamair_text1')
        self.label1.setWordWrap(True)
        self.label2 = bind_key(QLabel(), "text", 'disclamair_text2')
        self.label2.setWordWrap(True)
        self.label3 = bind_key(QLabel(), "text", 'disclamair_text3')
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

    def translate_tabs(self):
        for i,key in enumerate(("version","development","copyright","disclamair")):
            self.tabs.setTabText(i,self.language[key])
