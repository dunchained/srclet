import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
import test2 as t02


class win01(QWidget):
    def __init__(self, parent=None):
        super(win01, self).__init__(parent)

        self.win02 = t02.win02()
        self.win02.clicked.connect(self.func)
        self.button = QPushButton("open win02", self)
        self.button.move(100, 100)
        self.button.clicked.connect(self.show_t02)

    def show_t02(self):
        self.win02.show()

    def func(self):
        print("yes!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = win01()
    ex.show()
    sys.exit(app.exec_())
