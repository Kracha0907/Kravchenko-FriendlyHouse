import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QDialog


class Profil(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('profil.ui', self)
        self.initUI()

    def initUI(self):
        con = sqlite3.connect("users_db.sqlite")
        cur = con.cursor()
        login = cur.execute("""SELECT login FROM login_now""").fetchall()[0][0] # достается логин пользователя,
        # который зашел
        self.edit_login.setText(login)
        email = cur.execute("""SELECT email from users WHERE login = ?""", (login,)).fetchall()
        self.edit_email.setText(email[0][0])
        countComplaints = cur.execute("""SELECT countComplaint FROM users WHERE login = ?""",
                                      (login,)).fetchall()[0][0]
        self.edit_countComplaints.setText(str(countComplaints))
        self.btn_allComplaintsForUser.clicked.connect(self.allComplaintsForUser)
        self.btn_toMain.clicked.connect(self.toMain)
        con.close()

    def allComplaintsForUser(self): # Вывод всех жалоб для выбранного пользователя
        self.list_allComplaintsForUser.clear()
        con = sqlite3.connect("users_db.sqlite")
        cur = con.cursor()
        login = cur.execute("""SELECT login FROM login_now""").fetchall()[0][0]
        id_userTo = cur.execute("""SELECT id FROM users WHERE login = ?""", (login,)).fetchall()[0][0]
        reasonComplaints = cur.execute("""SELECT reasonComplaint from complaints WHERE id_userTo = ?""",
                                       (id_userTo,)).fetchall()
        for i in reasonComplaints:
            id_userFrom = cur.execute("""SELECT id_userFrom FROM complaints WHERE reasonComplaint = ?""",
                                      (i[0],)).fetchall()[0][0]
            loginFrom = cur.execute("""SELECT login FROM users WHERE id = ?""", (id_userFrom,)).fetchall()[0][0]
            self.list_allComplaintsForUser.addItem(i[0] + "\n" + "Пожаловался пользователь " + loginFrom)

    def toMain(self): # Вернуться на главную
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pr = Profil()
    pr.show()
    sys.exit(app.exec_())