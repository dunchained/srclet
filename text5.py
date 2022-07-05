import sys

from PyQt5.QtWidgets import QApplication, QTextEdit

def main():    
    app = QApplication(sys.argv)

    w = QTextEdit()
    w.setWindowTitle('Manipulate cursor')
    cursor = w.textCursor()
    cursor.insertText("Hello World")
    # neither of the following commands have any effect
    cursor.setPosition(cursor.position() - 5)
    cursor.movePosition(cursor.movePosition(cursor.Left, cursor.KeepAnchor,  3))

    w.show()   
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()