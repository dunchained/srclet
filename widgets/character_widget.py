#from variables import var
import var
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QComboBox, QHBoxLayout, QLineEdit, QTabWidget
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QDesktopWidget, QGridLayout, QGroupBox, QLabel, QPushButton, QFormLayout, QDateEdit
import sys
import json
import os
cwd = os.path.curdir


class InputCharacterWidget(QTabWidget):
    #def __init__(self, language, columns, title):
    def __init__(self, columns=3, title='hue hue'):
        super().__init__()
        self.columns = columns
        self.input_title = title
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.language = {
            "//": "Basic Parameters Widget",
            "basic_parameters_widget_title": "Parameters",
            "basic_parameters_new_addition": "_new",
            "language_description": "en",
            "basic_parameters_widget_caption": "List of available parameters:",
            "basic_parameters_widget_btn_add_new": "Add new parameter",
            "basic_parameters_widget_btn_add_new_inherit": "Add new parameter based on selected",
            "basic_parameters_widget_btn_delete": "Delete selected parameter",
            "basic_parameters_widget_parameter_caption": "Parameter information:",
            "basic_parameters_widget_parameter_btn_save_changes": "Save changes",
            "basic_parameters_widget_parameter_btn_cancel_changes": "Cancel changes",
            "basic_parameters_widget_delete_msg_title": "Delete parameter...",
            "basic_parameters_widget_delete_msg_message": "Are you sure you want to delete selected parameter?",
            "basic_parameters_widget_delete_msg_yes": "Yes",
            "basic_parameters_widget_delete_msg_cancel": "Cancel",
            "basic_parameters_widget_save_changes_message": "Parameter must have name...",
            "basic_parameters_widget_save_changes_message_caption": "Changes...",
            "//": "Basic Parameters Widget END"
        }
        self.widget_gui()

    def widget_gui(self):
        self.setWindowState(Qt.WindowMaximized)
        main_layout = QGridLayout()
        self.setLayout(main_layout)
        self.categories_list = self.read_character_categories()
        self.tabs = QTabWidget()
        for category in self.categories_list:
            self.tab = QWidget()
            self.tab.layout = QGridLayout()
            self.sc_groupbox = QGroupBox()
            self.sc_layout = QGridLayout()
            self.sc_scroll = QWidget()
            file_name_to_send = category['category']
            self.characters_list, self.opisi_list, self.rows, self.columns = self.read_characters_file(
                file_name=file_name_to_send, columns=self.columns)
            i = 0
            print(self.opisi_list)
            for row in range(self.rows):
                for column in range(self.columns):
                    self.button = QPushButton(self.characters_list[i])
                    self.button.setToolTip(self.opisi_list[i])
                    self.button.clicked.connect(self.special_character_clicked)
                    self.sc_layout.addWidget(self.button, row+1, column)
                    i += 1
                    if i == len(self.characters_list):
                        break
            self.sc_scroll.setLayout(self.sc_layout)
            sc = QScrollArea()
            sc.setWidget(self.sc_scroll)
            sc.setWidgetResizable(1)
            self.sc_groupbox.layout = QVBoxLayout()
            self.sc_groupbox.layout.addWidget(sc)
            self.sc_groupbox.setLayout(self.sc_groupbox.layout)
            self.tab.layout.addWidget(self.sc_groupbox)
            self.tab.setLayout(self.tab.layout)
            self.tabs.addTab(self.tab, category['name'])
        self.label_caption = QLabel(self.input_title)
        main_layout.addWidget(self.label_caption)
        main_layout.addWidget(self.tabs)
        QApplication.instance().focusChanged.connect(self.on_focus_changed)
        self.show()

    def read_character_categories(self):
        self.cat = open(os.path.join(cwd + var.language_folder +
                        self.language['language_description'] + '/' + var.c_cat_file))
        self.cat_file_data = json.load(self.cat)
        self.cat_list = []
        for category in self.cat_file_data:
            dict_to_send = {
                "category": category,
                "name": self.cat_file_data[category]
            }
            self.cat_list.append(dict_to_send)
        return self.cat_list

    def read_characters_file(self, file_name, columns):
        file = os.path.join(cwd + var.charactes_loc + 'special_characters_' + file_name + '.json')
        open_file = open(file)
        data_file = json.load(open_file)
        category_list = []
        description_list = []
        for key, character in data_file.items():
            print(key, character)
            category_list.append(character)
            description_list.append(key)
        if len(category_list) % columns == 0:
            rows = len(category_list) // columns
        else:
            rows = len(category_list) // columns + 1
        return category_list, description_list, rows, columns

    def on_focus_changed(self, widget):
        self.on_focused_change = widget

    def special_character_clicked(self, i):
        sender = self.sender()
        sender_text = sender.text()
        if self.on_focused_change.__class__.__name__ == 'QTextEdit':
            self.on_focused_change.setPlainText(
                self.on_focused_change.toPlainText() + sender_text)
        elif self.on_focused_change.__class__.__name__ == 'QLineEdit':
            self.on_focused_change.setText(
                self.on_focused_change.text() + sender_text)
        else:
            pass


if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = InputCharacterWidget()
    sys.exit(mainApplication.exec_())
