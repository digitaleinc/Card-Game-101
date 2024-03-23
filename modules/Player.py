class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def play_card(self, card):
        self.hand.remove(card)

    def draw_card(self, card):
        self.hand.append(card)
