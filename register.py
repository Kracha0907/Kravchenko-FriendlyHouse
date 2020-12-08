import sys
import sqlite3
import smtplib
import random

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from main import Main


class Register(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('register.ui', self)
        self.initUI()

    def initUI(self):
        self.label_code.hide()
        self.edit_code.hide()
        self.btn_verify.hide()
        self.label_login.hide()
        self.edit_login.hide()
        self.label_password.hide()
        self.edit_password.hide()
        self.btn_register.hide()
        self.message = str(random.randint(1000, 9999))
        self.btn_getCode.clicked.connect(self.getCode)
        self.btn_exit.clicked.connect(self.exit)

    def getCode(self): # Отправка кода на почту
        try:
            smtpObj = smtplib.SMTP('smtp.mail.ru', 25)
            smtpObj.starttls()
            smtpObj.login('alexei2004@inbox.ru', 'tuttocapelli')
            smtpObj.sendmail("alexei2004@inbox.ru", self.edit_mail.text(), self.message)
            smtpObj.quit()
            self.label_code.show()
            self.edit_code.show()
            self.btn_verify.show()
            self.btn_verify.clicked.connect(self.verify) # Если нажата кнопка войти происходит проверка кода
        except:
            QMessageBox.about(self, "Ошибка!", "Проверьте соединение с Интернетом или правильность почтового адреса")
        return False

    def verify(self): # Проверка кода
        if self.message == self.edit_code.text():
            self.label_login.show()
            self.edit_login.show()
            self.label_password.show()
            self.edit_password.show()
            self.btn_register.show()
            self.btn_register.clicked.connect(self.register)
        else:
            QMessageBox.about(self, "Ошибка!", "Неверный код. Попробуйте еще раз")

    def register(self): # Регистрация пользователя
        con = sqlite3.connect("users_db.sqlite")
        cur = con.cursor()
        login = cur.execute("""SELECT login from users WHERE login = ?""", (self.edit_login.text(),)).fetchall()
        print(login)
        if not login:
            cur.execute("""INSERT INTO users(login, password, email, countComplaint) VALUES(?, ?, ?, ?)""",
                        (self.edit_login.text(),
                         self.edit_password.text(), self.edit_mail.text(), 0))
            cur.execute("""UPDATE login_now SET login = ? WHERE id = ?""", (self.edit_login.text(), 1))
            con.commit()
            con.close()
            self.reg1 = Main(self) # Переход на главную страницу
            self.reg1.show()
        else:
            QMessageBox.about(self, "Ошибка!", "Пользователь с таким логином уже существует. "
                                               "Вернитесь назад и войдите в свою учетную запись")

    def exit(self): # Возвращение назад
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    reg = Register()
    reg.show()
    sys.exit(app.exec())