from PyQt5 import QtWidgets, QtCore, QtGui
import sys

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App,self).__init__()
        app = QtWidgets.QApplication.instance()
        screen = app.primaryScreen().size()
        self.title = 'Restaurant Application'
        width = screen.width()
        height = screen.height()
        self.left = 0
        self.top = 0
        self.width = width
        self.height = height
        self.setMouseTracking(True)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.initUI()
        self.show()

    def initUI(self):
        # window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # statusbar
        self.statusBar().showMessage('Welcome to el restaurante')

    def mousePressEvent(self, event):
        print('Mouse coords: ( %d : %d )' % (event.x(), event.y()))


class MyTableWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(MyTableWidget, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout()
        self.validUser = False

        # Initialize tab screen
        self.tabs = QtWidgets.QTabWidget()
        self.login = QtWidgets.QWidget()
        self.menu = QtWidgets.QWidget()
        self.checkOut = QtWidgets.QWidget()
        self.tabs.resize(500, 200)

        # Add tabs
        self.tabs.addTab(self.login, "Login")
        self.tabs.addTab(self.menu, "Menu")
        self.tabs.addTab(self.checkOut, "Check out")

        # Create login tab
        self.login.layout = QtWidgets.QVBoxLayout()
        self.menu.layout = QtWidgets.QVBoxLayout()

        # login text
        self.loginPrompt = QtWidgets.QLabel("Please provide a valid login")
        self.loginPrompt.setFixedSize(315,30)
        self.loginPromptFont = QtGui.QFont("Times", 27, QtGui.QFont.Bold)
        self.loginPrompt.setFont(self.loginPromptFont)
        self.login.layout.addWidget(self.loginPrompt)
        self.login.setLayout(self.login.layout)

        # Create textbox
        self.loginTextbox = QtWidgets.QLineEdit()
        self.loginTextbox.returnPressed.connect(self.on_click_login)
        self.loginTextbox.setFixedSize(170,20)

        # Create a button in the window
        self.loginButton = QtWidgets.QPushButton('Login button')
        self.loginButton.clicked.connect(self.on_click_login)
        self.loginButton.setFixedSize(100,40)
        self.login.layout.addWidget(self.loginTextbox,alignment=QtCore.Qt.AlignCenter)
        self.login.layout.addWidget(self.loginButton,alignment=QtCore.Qt.AlignCenter)


        #widget code i use to decide which widget to add
        self.menuInvalidUserLogin = QtWidgets.QLabel("Please login in to view")
        self.menuValidUserLogin = QtWidgets.QLabel("Here's the menu")

        if(self.validUser):
            self.menu.layout.addWidget(self.menuValidUserLogin)
        else:
            self.menu.layout.addWidget(self.menuInvalidUserLogin)
        self.menu.setLayout(self.menu.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def on_click_login(self):
        textboxValue = self.loginTextbox.text()
        if(textboxValue.lower() == 'pass'):
            self.validUser=True
            for i in reversed(range(self.menu.layout.count())): 
                widgetToRemove = self.menu.layout.itemAt(i).widget()
                self.menu.layout.removeWidget(widgetToRemove)
                widgetToRemove.deleteLater()
            self.menu.layout.addWidget(self.menuValidUserLogin)
            QtWidgets.QMessageBox.question(self, 'Response', "Login successful: Welcome", QtWidgets.QMessageBox.Ok,QtWidgets.QMessageBox.Ok)
            self.tabs.setCurrentIndex(1)
        else:
            self.validUser=False
            QtWidgets.QMessageBox.question(self, 'Response', "Login unsuccessful: EXPLAIN YOURSELF", QtWidgets.QMessageBox.Ok,QtWidgets.QMessageBox.Ok)
        self.loginTextbox.setText("")

def main():        
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()