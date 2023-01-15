import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QVBoxLayout, QLabel


class WidgetWithFlatGroupBox(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)

        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 300, 100)
        self.setWindowTitle('PyQt5 Window')

        layout = QVBoxLayout()

        layout.addWidget(self.create_groupbox(), alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def create_groupbox(self):
        groupbox = QGroupBox('Flat Groupbox')
        layout = QVBoxLayout()

        label = QLabel('This Groupbox should be flat.')

        layout.addWidget(label, alignment=Qt.AlignCenter)

        groupbox.setLayout(layout)

        groupbox.setFlat(True)

        return groupbox


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WidgetWithFlatGroupBox()
    ex.show()
    sys.exit(app.exec_())
