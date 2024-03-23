import random


class Deck:
    def __init__(self):
        self.cards = []
        self.suits = ['spades', 'hearts', 'diamonds', 'clubs']
        self.ranks = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.create_deck()
        self.shuffle()

    def create_deck(self):
        self.cards = [(rank, suit) for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop(0)

    def get_deck_size(self):
        return len(self.cards)
