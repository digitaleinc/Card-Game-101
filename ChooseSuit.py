from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget
from PyQt5 import uic
from config import *


class ChooseSuit(QWidget):
    def __init__(self):
        super(ChooseSuit, self).__init__()
        self.choosed_suit = -1

        uic.loadUi("designs/choose_suit.ui", self)
        self.setWindowTitle("Choose a suit")
        self.setWindowIcon(QIcon(f"{icon}"))

        self.text = self.findChild(QLabel, "text")

        self.clubs = self.findChild(QLabel, "clubs")
        self.diamonds = self.findChild(QLabel, "diamonds")
        self.spades = self.findChild(QLabel, "spades")
        self.hearts = self.findChild(QLabel, "hearts")

        self.choose_clubs = self.findChild(QPushButton, "choose_clubs")
        self.choose_diamonds = self.findChild(QPushButton, "choose_diamonds")
        self.choose_spades = self.findChild(QPushButton, "choose_spades")
        self.choose_hearts = self.findChild(QPushButton, "choose_hearts")

        self.initForm()

    def initForm(self):
        pixmap1 = QPixmap(f"images/Q_of_clubs.png")
        pixmap2 = QPixmap(f"images/Q_of_diamonds.png")
        pixmap3 = QPixmap(f"images/Q_of_spades.png")
        pixmap4 = QPixmap(f"images/Q_of_hearts.png")
        self.clubs.setPixmap(pixmap1)
        self.diamonds.setPixmap(pixmap2)
        self.spades.setPixmap(pixmap3)
        self.hearts.setPixmap(pixmap4)

        self.choose_clubs.clicked.connect(self.first)
        self.choose_diamonds.clicked.connect(self.second)
        self.choose_spades.clicked.connect(self.third)
        self.choose_hearts.clicked.connect(self.fourth)

    def first(self):
        self.choosed_suit = 3
        ChooseSuit.hide(self)

    def second(self):
        self.choosed_suit = 2
        ChooseSuit.hide(self)

    def third(self):
        self.choosed_suit = 0
        ChooseSuit.hide(self)

    def fourth(self):
        self.choosed_suit = 1
        ChooseSuit.hide(self)
