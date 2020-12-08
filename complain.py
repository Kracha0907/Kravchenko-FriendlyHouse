import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox


class Complain(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('complain.ui', self)
        self.initUI()

    def initUI(self):
        self.list_reputation.clear()
        self.list_allComplaintsForUser.clear()
        self.btn_complain.clicked.connect(self.complain)
        self.btn_reputation.clicked.connect(self.reputation)
        self.btn_allComplaintsForUser.clicked.connect(self.allComplaintsForUser)
        self.btn_toMain.clicked.connect(self.toMain)

    def complain(self): # Пожаловаться
        self.list_reputation.clear()
        self.list_allComplaintsForUser.clear()
        con = sqlite3.connect("users_db.sqlite")
        cur = con.cursor()
        logins = cur.execute("""SELECT login from users""").fetchall()
        for i in range(len(logins)):
            logins[i] = logins[i][0]
        login, ok_pressed1 = QInputDialog.getItem(
            self, "Жалоба", "Выберете пользователя", logins, 0, False)
        if ok_pressed1:
            reason, ok_pressed2 = QInputDialog.getText(
                self, "Жалоба", "По какой причине вы жалуетесь на пользователя " + login)
            if ok_pressed2:
                old_complain = cur.execute("""SELECT countComplaint FROM users WHERE login = ?""", (login,)).fetchall()
                cur.execute("""UPDATE users SET countComplaint = ? WHERE login = ?""",
                            (old_complain[0][0] + 1,  login))

                login_now = cur.execute("""SELECT login FROM login_now""").fetchall()[0][0]
                id_userFrom = cur.execute("""SELECT id FROM users WHERE login = ?""", (login_now,)).fetchall()[0][0]
                id_userTo = cur.execute("""SELECT id FROM users WHERE login = ?""", (login,)).fetchall()[0][0]
                cur.execute("""INSERT INTO complaints(reasonComplaint, id_userFrom, id_userTo) VALUES(?, ?, ?)""",
                            (reason, id_userFrom, id_userTo))
                con.commit()
                con.close()

    def reputation(self): # Отобразить репутацию всех пользователей
        self.list_reputation.clear()
        self.list_allComplaintsForUser.clear()
        con = sqlite3.connect("users_db.sqlite")
        cur = con.cursor()
        reputation = []
        logins = cur.execute("""SELECT login from users""").fetchall()
        for i in range(len(logins)):
            countComplaints = cur.execute("""SELECT countComplaint FROM users WHERE login = ?""",
                                          (logins[i][0],)).fetchall()[0][0]
            reputation.append((countComplaints, logins[i][0]))
        if len(reputation) == 0:
            QMessageBox.about(self, "Сообщние", "Пока еще нет никаких жалоб")
        else:
            reputation.sort()
            reputation.reverse()
            for i in reputation:
                if i[0] % 10 == 1:
                    self.list_reputation.addItem("Пользователь " + i[1] + " имеет " + str(i[0]) + " жалобу")
                elif i[0] % 10 == 0 or i[0] % 10 >= 5:
                    self.list_reputation.addItem("Пользователь " + i[1] + " имеет " + str(i[0]) + " жалоб")
                else:
                    self.list_reputation.addItem("Пользователь " + i[1] + " имеет " + str(i[0]) + " жалобы")
        con.close()

    def allComplaintsForUser(self): # Все жалобы для одного пользователя
        self.list_reputation.clear()
        self.list_allComplaintsForUser.clear()
        con = sqlite3.connect("users_db.sqlite")
        cur = con.cursor()
        logins = cur.execute("""SELECT login from users""").fetchall()
        for i in range(len(logins)):
            logins[i] = logins[i][0]
        login, ok_pressed = QInputDialog.getItem(
            self, "Все жалобы на пользователя", "Выберете пользователя, жалбы на которого хотите посмотреть",
            logins, 0, False)
        if ok_pressed:
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
    ex = Complain()
    ex.show()
    sys.exit(app.exec_())