import sys

from PyQt5 import uic
from recommend import Recommend
from complain import Complain
from profil import Profil
from PyQt5.QtWidgets import QApplication, QMainWindow


class Main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        self.btn_recommend.setStyleSheet('QPushButton {background-color: #A3C1DA}')
        self.btn_recommend.clicked.connect(self.recommend)
        self.btn_complain.setStyleSheet('QPushButton {background-color: #A3C1DA}')
        self.btn_complain.clicked.connect(self.complain)
        self.btn_profil.setStyleSheet('QPushButton {background-color: #A3C1DA}')
        self.btn_profil.clicked.connect(self.profil)
        self.btn_backToAutentification.setStyleSheet('QPushButton {background-color: #A3C1DA}')
        self.btn_backToAutentification.clicked.connect(self.backToAutentification)

    def recommend(self): # Переход в рубрику "Рекомендую"
        self.m1 = Recommend(self)
        self.m1.show()

    def complain(self): # Переход в рубрику "Пожаловаться"
        self.m2 = Complain(self)
        self.m2.show()

    def profil(self): # Переход во вкладку "Профиль"
        self.m3 = Profil(self)
        self.m3.show()

    def backToAutentification(self):  # Вернуться назад
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = Main()
    m.show()
    sys.exit(app.exec_())
