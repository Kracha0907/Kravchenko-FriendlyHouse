import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from login import Login
from register import Register


class LogOrReg(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('logOrReg.ui', self)
        self.initUI()

    def initUI(self):
        self.btn_login.clicked.connect(self.logining)
        self.btn_register.clicked.connect(self.register)
        self.btn_exit.clicked.connect(self.exit)

    def logining(self): # Переход на автоизацию
        self.lor1 = Login(self)
        self.lor1.show()

    def register(self): # Переход на регистрацию
        self.lor2 = Register(self)
        self.lor2.show()

    def exit(self): # Выход из приложения
        reply = QMessageBox.question(self, 'Message',
                                     "Вы точно хотите выйти из этого приложения?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    lor = LogOrReg()
    lor.show()
    sys.exit(app.exec())