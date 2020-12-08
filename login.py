import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from main import Main


class Login(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.initUI()

    def initUI(self):
        self.btn_exit.clicked.connect(self.exit)
        self.btn_continue.clicked.connect(self.login)

    def login(self): # Аутентификация пользователя
        con = sqlite3.connect("users_db.sqlite")
        cur = con.cursor()
        login = cur.execute("""SELECT login from users WHERE login = ?""", (self.edit_login.text(),)).fetchall()
        if not login:
            QMessageBox.about(self, "Ошибка!", "Пользователя с таким логином не существует. Попробуйте еще "
                              "раз или зарегестрируйтесь")
            con.close()
        else:
            password = cur.execute("""SELECT password from users WHERE login = ?""",
                                   (self.edit_login.text(),)).fetchall()
            cur.execute("""UPDATE login_now SET login = ? WHERE id = ?""", (self.edit_login.text(), 1))
            con.commit()
            if str(password[0][0]) != str(self.edit_password.text()):
                QMessageBox.about(self, "Ошибка!", "Неверный пароль. Попробуйте еще раз")
            else:
                self.log1 = Main(self)
                self.log1.show()
            con.close()

    def exit(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    log = Login()
    log.show()
    sys.exit(app.exec())