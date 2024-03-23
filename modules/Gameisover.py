from main import *
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget
from PyQt5 import uic
from config import *


class Gameisover(QWidget):
    def __init__(self):
        super(Gameisover, self).__init__()

        uic.loadUi("designs/gameover.ui", self)
        self.setWindowTitle("The game is over!")
        self.setWindowIcon(QIcon(f"{icon}"))

        self.label = self.findChild(QLabel, "label")
        self.label_2 = self.findChild(QLabel, "label_2")
        self.close_game = self.findChild(QPushButton, "close_game")

        self.close_game.clicked.connect(self.end)

    def end(self):
        self.hide()
        sys.exit(app.exec_())
