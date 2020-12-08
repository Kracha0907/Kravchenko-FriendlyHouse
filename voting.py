import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
from errors import errors

errors()


class Voting(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.con = sqlite3.connect("users_db.sqlite")
        self.cur = self.con.cursor()
        uic.loadUi('voting.ui', self)
        self.initUI()

    def initUI(self):
        self.list_results.hide()
        self.btn_makeVoting.clicked.connect(self.makeVoting)
        self.hide_objects(True)
        self.btn_vote.clicked.connect(self.vote)
        self.btn_results.clicked.connect(self.results)
        self.btn_finish.clicked.connect(self.finish)
        self.btn_toMain.clicked.connect(self.toMain)

    def hide_objects(self, flag):
        if flag:
            self.label.hide()
            self.label_2.hide()
            self.theme.hide()
            self.btn_make.hide()
            self.answers.hide()
        else:
            self.label.show()
            self.label_2.show()
            self.theme.show()
            self.answers.show()
            self.btn_make.show()

    def makeVoting(self):
        a = self.cur.execute("""SELECT id FROM voting""").fetchall()
        if a:
            answer, ok_pressed = QInputDialog.getItem(
                self, "Подтверждение удаления",
                "Вы точно хотите начать новое голосование? Результаты прошлого голосования будут удалены",
                ("нет", "да"), 1, False)
            if ok_pressed and answer == "да":
                self.clear()
                self.hide_objects(False)
                self.btn_make.clicked.connect(self.make)
        else:
            self.hide_objects(False)
            self.btn_make.clicked.connect(self.make)

    def make(self):
        if self.theme.text == "" or self.answers.toPlainText() == "":
            QMessageBox.about(self, "Ошибка!", "Формы для ввода не могут быть пустыми!")
        else:
            res = self.answers.toPlainText().split("\n")
            for i in range(len(res)):
                self.cur.execute(f"""INSERT INTO voting(id, theme, possible_answers) VALUES({i + 1}, 
                                                '{self.theme.text()}', '{res[i]}')""")
                self.con.commit()
        self.cur.execute("""UPDATE voting SET ind = False""")
        self.hide_objects(True)
        QMessageBox.about(self, "Успешно", "Голосованине создано")

    def vote(self):
        if self.is_finish():
            QMessageBox.about(self, "Ошибка!", "Голосование еще не началось")
        else:
            possible_answers = self.cur.execute("""SELECT possible_answers FROM voting""").fetchall()
            for i in range(len(possible_answers)):
                possible_answers[i] = str(possible_answers[i][0])
            print(possible_answers)
            theme = str(self.cur.execute("""SELECT theme FROM voting WHERE id = 1""").fetchall()[0][0])
            answer, ok_pressed = QInputDialog.getItem(
                self, "Голосование", theme,
                possible_answers, False)
            if ok_pressed:
                login = str(self.cur.execute("""SELECT login FROM login_now WHERE id = 1""").fetchall()[0][0])
                self.cur.execute(f"""UPDATE users SET answer_id=(SELECT id FROM voting WHERE possible_answers = 
                                '{answer}') WHERE login = '{login}'""")
                self.con.commit()
                QMessageBox.about(self, "Успешно", "Ваш ответ записан")

    def clear(self):
        self.cur.execute("""DELETE from voting""")
        self.con.commit()
        self.theme.setText("")
        self.answers.setText("")

    def finish(self):
        self.cur.execute("""UPDATE voting SET ind = True""")
        self.con.commit()
        QMessageBox.about(self, "Успешно", "Голосование заверщено")

    def is_finish(self):
        a = self.cur.execute("""SELECT ind FROM voting WHERE id = 1""").fetchall()
        if len(a) == 0:
            return True
        else:
            return a[0][0]

    def results(self):
        self.list_results.clear()
        self.list_results.show()
        answers = self.cur.execute("""SELECT possible_answers FROM voting""").fetchall()
        for i in range(len(answers)):
            count = len(self.cur.execute(f"""SELECT id FROM users WHERE answer_id = (SELECT id FROM voting WHERE 
                                    possible_answers = '{str(answers[i][0])}')""").fetchall())
            self.list_results.addItem(str(answers[i][0]) + ": " + str(count))

    def toMain(self):  # Вернуться на главную
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    vt = Voting()
    vt.show()
    sys.exit(app.exec_())
