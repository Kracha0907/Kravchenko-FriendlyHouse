import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

import difflib


def similarity(s1, s2): # Функция похожести строк
    normalized1 = s1.lower()
    normalized2 = s2.lower()
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()


class Recommend(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('recommend.ui', self)
        self.initUI()

    def display_posts(self): # Отобразить посты
        self.list_text.clear()
        con = sqlite3.connect("users_db.sqlite")
        cur = con.cursor()
        posts = cur.execute("""SELECT title FROM recommend""").fetchall()
        for i in range(len(posts) - 1, -1, -1):
            self.list_text.addItem(posts[i][0])
        con.close()

    def initUI(self):
        self.display_posts()
        self.btn_post.clicked.connect(self.post)
        self.btn_return.clicked.connect(self.display_posts)
        self.btn_search.clicked.connect(self.search)
        self.btn_toMain.clicked.connect(self.toMain)

    def post(self): # Прикрепить пост
        con = sqlite3.connect("users_db.sqlite")
        cur = con.cursor()
        login = cur.execute("""SELECT login FROM login_now""").fetchall()[0][0]
        id_user = cur.execute("""SELECT id FROM users WHERE login = ?""",
                              (login,)).fetchall()
        post = self.input_text.toPlainText()
        cur.execute("""INSERT INTO recommend(title, id_user) VALUES(?, ?)""", (post + "\n" +
                    "Добавлен пользователем: " + login, id_user[0][0]))
        con.commit()
        con.close()
        self.display_posts()
        self.input_text.clear()

    def search(self): # Сделать поиск по постам
        text_search = self.edit_search.toPlainText()
        self.edit_search.clear()
        con = sqlite3.connect("users_db.sqlite")
        cur = con.cursor()
        posts = cur.execute("""SELECT title FROM recommend""").fetchall()
        con.close()
        similarities = []
        for j in range(len(posts)):
            similarities.append((similarity(text_search, posts[j][0]), posts[j][0]))
        similarities.sort()
        self.list_text.clear()
        similarities.reverse()
        for i in similarities:
            self.list_text.addItem(i[1])

    def toMain(self): # Вернуться на главную
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    r = Recommend()
    r.show()
    sys.exit(app.exec_())
