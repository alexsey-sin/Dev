import os, sys
from dotenv import load_dotenv
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
# python -m pip install --upgrade pip
# pip install PyQt5
# pip install pyqt5-tools
# pip install PyQt5Desiner

load_dotenv()


token = os.getenv('token')



# print(token)
# print(len(token))
 
# app = QApplication([])
# win = uic.loadUi('design.ui') # расположение вашего файла .ui

# # label = 
# win.show()
# sys.exit(app.exec())
class Win(QWidget):
    def __init__(self):
        super().__init__()
        self.win = uic.loadUi('design.ui')
        self.win.show()
        # self.initUI()
        self.win.pushButton2.clicked.connect(lambda: self.accept(1))

    # def initUI(self):


    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()

    def accept(self, hh):
        print('accept')
        # self.win.label_1.SetText('kkkk')
        self.win.statusBar().showMessage(f' was pressed{hh}')
        self.win.label_1.setText('somfing text')

    def mousePressEvent(self, event):
        print('mouse')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Win()
    sys.exit(app.exec_())