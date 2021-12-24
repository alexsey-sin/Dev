import os
import sys
from time import sleep
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class SenderMessage(QObject):
    text_value = pyqtSignal(str)
    int_value = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def run(self):
        self.text_value.emit("Привет!")
        sleep(1.5)
        self.text_value.emit("Я PyQt5.")
        sleep(1.5)
        self.text_value.emit("Мы сегодня тестируем...")
        sleep(1.5)
        self.text_value.emit("Класс QThread.")
        for i in range(10, 101, 1):
            sleep(0.1)
            self.int_value.emit(i)
        self.text_value.emit("Тест завершён.")
        sleep(1.5)
        self.text_value.emit("Приложение будет закрыто.")

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        try:
            self.setWindowTitle("Многопоточность")
            self.setGeometry(400, 200, 350, 80)

            self.label = QLabel(self)
            self.label.setGeometry(0, 0, 350, 50)
            self.label.setStyleSheet("color: rgb(25, 156, 25);\
                font: italic 18pt MS Shell Dlg 2; border: 5px solid red;")

            self.progress_bar = QProgressBar(self)
            self.progress_bar.setValue(10)
            self.progress_bar.setGeometry(0, 50, 350, 30)

            self.thread = QThread()

            self.sender_message = SenderMessage()

            self.timer = QTimer(self)
            self.timer.timeout.connect(self.close)
            self.timer.start(17000)

            self.sender_message.moveToThread(self.thread)
            self.sender_message.text_value.connect(self.signalHandlerText)
            self.sender_message.int_value.connect(self.signalHandlerInt)

            self.thread.started.connect(self.sender_message.run)
            self.thread.start()
        except Exception as exc:
            print(exc)
    def signalHandlerText(self, text):
        self.label.setText(text)

    def signalHandlerInt(self, value):
        self.progress_bar.setValue(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())