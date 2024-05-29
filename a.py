from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(400,200,400,500)
        self.setWindowTitle("Python GUI")
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Hello World")
        self.label.move(20,50)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Click me")
        self.b1.move(10,20)
        self.b1.clicked.connect(self.clicked)
    
    def clicked(self):
        self.label.setText("YOU HAVE CLICKED THE BUTTON")
        self.update()

    def update(self):
        self.label.adjustSize()
        self.label.setAlignment(Qt.AlignCenter) 

def window():
    app = QApplication(sys.argv)
    win= MyWindow()
    

    win.show()
    sys.exit(app.exec_())

window()

