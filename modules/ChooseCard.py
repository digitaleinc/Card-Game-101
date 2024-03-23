from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QMessageBox, QWidget, QTextEdit
from PyQt5 import uic
from config import *


class ChooseCard(QWidget):
    def __init__(self):
        super(ChooseCard, self).__init__()
        self.choosed_card_2 = 0
        self.is_take_card = 3
        self.mytext = None

        uic.loadUi("designs/choose_card.ui", self)
        self.setWindowTitle("Choose a card")
        self.setWindowIcon(QIcon(f"{icon}"))

        self.info_label = self.findChild(QLabel, "info_label")
        self.to_choose_card = self.findChild(QPushButton, "to_choose_card")
        self.card_num = self.findChild(QTextEdit, "card_num")
        self.take_card = self.findChild(QPushButton, "take_card")

        self.initCard()

    def initCard(self):
        self.to_choose_card.clicked.connect(self.send_card)
        self.take_card.clicked.connect(self.send_take_card)

    def send_take_card(self):
        self.is_take_card = 1
        ChooseCard.hide(self)

    def send_card(self):
        self.mytext = self.card_num.toPlainText()
        res = self.mytext.isnumeric()
        if res:
            self.is_take_card = 0
            self.choosed_card_2 = self.mytext
            self.card_num.setPlainText("")
            self.mytext = None
            ChooseCard.hide(self)
        else:
            QMessageBox.information(self, "Attention!", "Incorrect use, try again")
