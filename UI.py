from Gameisover import *
from Deck import *
from Player import *
from ChooseCard import *
from ChooseSuit import *
import threading
import time
from functions import *
from PyQt5.QtWidgets import QMainWindow


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        self.deck = Deck()
        self.choose_suit = ChooseSuit()
        self.choose_card = ChooseCard()
        self.game_results = Gameisover()

        self.choosed_card = 0
        self.modes = 0
        self.num_players = 4
        self.players = []
        self.trick_pile = []
        self.current_player = 0
        self.round_number = 1
        self.current_suit = None
        self.ai_choosed = None
        self.is_end_game = None
        self.names = []

        # Ініціалізація UI
        uic.loadUi("designs/window.ui", self)
        self.setWindowTitle("101 Card game")
        self.setWindowIcon(QIcon(f"{icon}"))

        players = ["player1", "player2", "player3", "player4"]
        cards = ["card" + str(i) for i in range(1, 22)]

        for player in players:
            for card in cards:
                label_name = card + "_" + player
                setattr(self, label_name, self.findChild(QLabel, label_name))

        self.which_player = self.findChild(QLabel, "which_player")

        self.deck_card = self.findChild(QLabel, "deck_card")
        self.deck_card_turned = self.findChild(QLabel, "deck_card_turned")

        self.playername1 = self.findChild(QLabel, "playername1")
        self.playername2 = self.findChild(QLabel, "playername2")
        self.playername3 = self.findChild(QLabel, "playername3")
        self.playername4 = self.findChild(QLabel, "playername4")

        self.points_player1 = self.findChild(QLabel, "points_player1")
        self.points_player2 = self.findChild(QLabel, "points_player2")
        self.points_player3 = self.findChild(QLabel, "points_player3")
        self.points_player4 = self.findChild(QLabel, "points_player4")

        self.faq = self.findChild(QPushButton, "faq")
        self.start_game = self.findChild(QPushButton, "start_game")
        self.end_game = self.findChild(QPushButton, "end_game")
        self.dev_mode = self.findChild(QPushButton, "dev_mode")
        self.first_button = self.findChild(QPushButton, "first_button")
        self.second_button = self.findChild(QPushButton, "second_button")
        self.save_game_results = self.findChild(QPushButton, "save_game_results")

        self.initUI()
        UI.show(self)

    def initUI(self):
        with open("players.txt", 'r') as file:
            self.names = [line.strip() for line in file.readlines()]

        for i in range(4):
            self.players.append(Player(self.names[i]))

        self.second_button.setEnabled(False)
        self.first_button.setEnabled(False)
        self.save_game_results.setEnabled(False)
        self.dev_mode.setEnabled(False)

        self.playername1.setText(self.names[0])
        self.playername2.setText(self.names[1])
        self.playername3.setText(self.names[2])
        self.playername4.setText(self.names[3])

        self.save_game_results.clicked.connect(self.save_game)
        self.start_game.clicked.connect(self.game_enable)
        self.faq.clicked.connect(self.faq_out)
        self.end_game.clicked.connect(self.turn_game_off)
        self.dev_mode.clicked.connect(self.view_mode)
        self.first_button.clicked.connect(self.first)
        self.second_button.clicked.connect(self.second)

    def save_game(self):
        self.game_results.show()

    def faq_out(self):
        QMessageBox.information(self, "Game rules", text)

    def first(self):
        self.choose_card.show()

    def second(self):
        self.choose_suit.show()

    def turn_game_off(self):
        # NEW CODE
        UI.close(self)

    def game_enable(self):
        self.setWindowTitle(f"The game was started. Round {self.round_number}")
        self.make_game_run()
        game = threading.Thread(target=self.run, name="game_logic", daemon=True)
        game.start()

    def make_game_run(self):
        self.start()
        self.trick_pile.append(self.deck.draw_card())
        ui_threads = threading.Thread(target=self.treading_design, name="kurwa")
        ui_threads.start()
        ui_threads.join()
        self.start_game.setEnabled(False)
        time.sleep(1)

    def view_mode(self):
        if self.modes == 0:
            self.modes = 1
            self.dev_mode.setText("Normal mode")
            view_mode_0 = threading.Thread(target=self.view_mode_do)
            view_mode_0.start()
        else:
            self.modes = 0
            self.dev_mode.setText("Developer mode")
            view_mode_1 = threading.Thread(target=self.update_design)
            view_mode_1.start()

    def standart_mode(self):
        self.modes = 0
        self.dev_mode.setText("Developer mode")
        defaultmode_thread = threading.Thread(target=self.update_design)
        defaultmode_thread.start()

    def view_mode_do(self):
        if self.modes == 1:
            pass
        else:
            self.standart_mode()
            return

        card = self.trick_pile[-1]
        pixmap = QPixmap(f"images/{card[0]}_of_{card[1]}.png")
        self.deck_card.setPixmap(pixmap)

        empty = QPixmap(f"images/empty.png")
        self.change_labels()
        try:
            deck_card_2 = self.trick_pile[-2]
            another = QPixmap(f"images/{deck_card_2[0]}_of_{deck_card_2[1]}.png")
            self.deck_card_turned.setPixmap(another)
        except IndexError:
            pass

        if self.deck.get_deck_size() == 0:
            deck_pix = QPixmap(f"images/empty.png")
            self.deck_card_turned.setPixmap(deck_pix)
        else:
            deck_pix2 = QPixmap(f"{turned}")
            self.deck_card_turned.setPixmap(deck_pix2)

        player_hand = self.players[0].hand

        for i, card in enumerate(player_hand[:21]):
            if len(card) > 1:
                pixmap1 = QPixmap(f"images/{card[0]}_of_{card[1]}.png")
                getattr(self, f"card{i + 1}_player1").setPixmap(pixmap1)

        for index in range(len(player_hand), 21):
            getattr(self, f"card{index + 1}_player1").setPixmap(empty)

        player_hand = self.players[1].hand

        for i, card in enumerate(player_hand[:21]):
            if len(card) > 1:
                pixmap2 = QPixmap(f"images/{card[0]}_of_{card[1]}.png")
                getattr(self, f"card{i + 1}_player2").setPixmap(pixmap2)

        for index in range(len(player_hand), 21):
            getattr(self, f"card{index + 1}_player2").setPixmap(empty)

        player_hand = self.players[2].hand

        for i, card in enumerate(player_hand[:21]):
            if len(card) > 1:
                pixmap3 = QPixmap(f"images/{card[0]}_of_{card[1]}.png")
                getattr(self, f"card{i + 1}_player3").setPixmap(pixmap3)

        for index in range(len(player_hand), 21):
            getattr(self, f"card{index + 1}_player3").setPixmap(empty)

        player_hand = self.players[3].hand

        for i, card in enumerate(player_hand[:21]):
            if len(card) > 1:
                pixmap4 = QPixmap(f"images/{card[0]}_of_{card[1]}.png")
                getattr(self, f"card{i + 1}_player4").setPixmap(pixmap4)

        for index in range(len(player_hand), 21):
            getattr(self, f"card{index + 1}_player4").setPixmap(empty)

    def update_design_ingame(self):
        self.change_labels()
        if self.modes == 0:
            random_number = random.randint(1, 10000)
            thread_name = f"thread_update_{random_number}"
            thread_update = threading.Thread(target=self.update_design, name=thread_name)
            thread_update.start()
        else:
            random_number = random.randint(1, 10000)
            thread_name = f"thread_update_{random_number}"
            thread_view = threading.Thread(target=self.view_mode_do, name=thread_name)
            thread_view.start()

    def treading_design(self):
        self.update_design()

    def func(self):
        empty = QPixmap("images/empty.png")

        player_hand = self.players[0].hand

        for i, card in enumerate(player_hand[:21]):
            if len(card) > 1:
                pixmap = QPixmap(f"images/{card[0]}_of_{card[1]}.png")
                getattr(self, f"card{i + 1}_player1").setPixmap(pixmap)

        for index in range(len(player_hand), 21):
            getattr(self, f"card{index + 1}_player1").setPixmap(empty)

        pixmap = QPixmap(f"{turned}")

        player_hand = self.players[1].hand

        for i, card in enumerate(player_hand[:21]):
            if len(card) > 1:
                getattr(self, f"card{i + 1}_player2").setPixmap(pixmap)

        for index in range(len(player_hand), 21):
            getattr(self, f"card{index + 1}_player2").setPixmap(empty)

        player_hand = self.players[2].hand

        for i, card in enumerate(player_hand[:21]):
            if len(card) > 1:
                getattr(self, f"card{i + 1}_player3").setPixmap(pixmap)

        for index in range(len(player_hand), 21):
            getattr(self, f"card{index + 1}_player3").setPixmap(empty)

        player_hand = self.players[3].hand

        for i, card in enumerate(player_hand[:21]):
            if len(card) > 1:
                getattr(self, f"card{i + 1}_player4").setPixmap(pixmap)

        for index in range(len(player_hand), 21):
            getattr(self, f"card{index + 1}_player4").setPixmap(empty)

    def update_design(self):
        card = self.trick_pile[-1]
        pixmap = QPixmap(f"images/{card[0]}_of_{card[1]}.png")
        self.deck_card.setPixmap(pixmap)

        if self.deck.get_deck_size() == 0:
            pixmap = QPixmap(f"images/empty.png")
            self.deck_card_turned.setPixmap(pixmap)
        else:
            pixmap = QPixmap(f"{turned}")
            self.deck_card_turned.setPixmap(pixmap)

        self.func()

    def start(self):
        self.deck.shuffle()
        self.deal_cards()

    def deal_cards(self):
        for i in range(self.num_players):
            num_cards = 5 if i != self.current_player else 4

            for _ in range(num_cards):
                card = self.deck.draw_card()
                self.players[i].add_card(card)

    def get_card(self):
        time.sleep(2)
        action = "0"
        if self.choose_card.is_take_card == 1:
            action = "2"
        elif self.choose_card.is_take_card == 0:
            action = "1"
        elif self.choose_card.is_take_card != 0 and self.choose_card.is_take_card != 1:
            pass
        self.choose_card.is_take_card = 3
        return action

    def change_labels(self):
        if self.current_player == 0:
            self.playername1.setText(f"{self.names[0]} (turn)")
            self.playername2.setText(self.names[1])
            self.playername3.setText(self.names[2])
            self.playername4.setText(self.names[3])
        elif self.current_player == 1:
            self.playername1.setText(self.names[0])
            self.playername2.setText(f"{self.names[1]} (turn)")
            self.playername3.setText(self.names[2])
            self.playername4.setText(self.names[3])
        elif self.current_player == 2:
            self.playername1.setText(self.names[0])
            self.playername2.setText(self.names[1])
            self.playername3.setText(f"{self.names[2]} (turn)")
            self.playername4.setText(self.names[3])
        elif self.current_player == 3:
            self.playername1.setText(self.names[0])
            self.playername2.setText(self.names[1])
            self.playername3.setText(self.names[2])
            self.playername4.setText(f"{self.names[3]} (turn)")

    def play_round(self):
        self.setWindowTitle(f"The game was started. Round {self.round_number}")
        time.sleep(1)
        self.current_player = self.apply_additional_rules()
        self.update_design_ingame()
        check_round = True
        while check_round:
            time.sleep(3)
            if self.check_game_over():
                break

            if self.is_end_game:
                break

            if self.current_player != 0:
                if self.ai_strategy(self.current_player):
                    self.current_player = self.apply_additional_rules()
                    self.change_labels()
                else:
                    self.current_player = (self.current_player + 1) % 4
                    self.change_labels()
            else:
                last_card = self.trick_pile[-1]
                if last_card[0] == 'Q':
                    self.change_labels()
                    self.setWindowTitle(f"Увага! Масть змінено на: {self.deck.suits[self.ai_choosed]}")
                self.first_button.setEnabled(True)
                choosing_action = True
                while choosing_action:
                    time.sleep(2)
                    action = self.get_card()
                    if action == "1":
                        choosing_action = False
                        if self.play_card_action():
                            self.current_player = self.apply_additional_rules()
                            choosing_action = False
                    elif action == "2":
                        if not self.draw_card(self.current_player):
                            check_round = False
                            choosing_action = False
                        else:
                            time.sleep(0.5)
                            self.update_design_ingame()
                            time.sleep(0.5)
                            self.first_button.setEnabled(False)
                            self.secound_chance()
                            choosing_action = False
                self.setWindowTitle(f"The game was started. Round {self.round_number}")

            if self.check_game_over():
                break

            if self.is_end_game:
                break

            self.update_design_ingame()
            time.sleep(2)

    def secound_chance(self):
        time.sleep(1)
        self.first_button.setEnabled(True)
        choosing_action2 = True
        while choosing_action2:
            action = self.get_card()
            if action == "1":
                if self.play_card_action():
                    self.current_player = self.apply_additional_rules()
                    self.first_button.setEnabled(False)
                    choosing_action2 = False
            elif action == "2":
                self.current_player = (self.current_player + 1) % self.num_players
                self.first_button.setEnabled(False)
                choosing_action2 = False

    def ai_strategy(self, player):
        valid_cards = [card for card in self.players[player].hand if
                       card[1] == self.trick_pile[-1][1] or
                       card[0] == self.trick_pile[-1][0] or
                       card[1] == self.current_suit or
                       card[0] == 'Q']

        if valid_cards:
            card = random.choice(valid_cards)
            if self.check_rule(card):
                self.play_card(player, card)
                return True
            else:
                if not self.draw_card(player):
                    return False
                if self.ai_strategy_second(player):
                    return True
                else:
                    return False
        else:
            if not self.draw_card(player):
                return False
            if self.ai_strategy_second(player):
                return True
            else:
                return False

    def ai_strategy_second(self, player):
        valid_cards = [card for card in self.players[player].hand if
                       card[1] == self.trick_pile[-1][1] or
                       card[0] == self.trick_pile[-1][0] or
                       card[1] == self.current_suit
                       ]

        if len(valid_cards) > 0:
            card = random.choice(valid_cards)
            if self.check_rule(card):
                self.play_card(player, card)
                return True
        return False

    def check_rule(self, card):
        last_card = self.trick_pile[-1]
        if card[0] == 'Q':
            return True
        if last_card[0] == 'Q' and card[1] == self.current_suit:
            return True
        if last_card[0] != 'Q' and (card[1] == self.trick_pile[-1][1] or card[0] == self.trick_pile[-1][0]):
            return True
        return False

    def play_card(self, player, card):
        self.players[player].play_card(card)
        self.trick_pile.append(card)

    def shaffle_deck_ingame(self):
        last_card = self.trick_pile.pop(-1)
        random.shuffle(self.trick_pile)
        self.deck.cards = self.trick_pile + self.deck.cards
        self.trick_pile = [last_card]

    def draw_card(self, player):
        if self.deck.get_deck_size() <= 0:
            if len(self.trick_pile) > 1:
                self.shaffle_deck_ingame()
                card = self.deck.draw_card()
                self.players[player].draw_card(card)
                return True
            else:
                return False
        else:
            card = self.deck.draw_card()
            self.players[player].draw_card(card)
            return True

    def play_card_action(self):
        self.first_button.setEnabled(True)
        card_choosing = True
        while card_choosing:
            time.sleep(2)
            card_number = self.choose_card.choosed_card_2
            card_number = int(card_number) - 1
            if card_number == -1:
                self.choose_card.choosed_card_2 = 0
                if self.choose_card.is_take_card == 1:
                    return False
            else:
                if card_number < len(self.players[self.current_player].hand):
                    card = self.players[self.current_player].hand[card_number]
                    if self.check_rule(card):
                        self.play_card(self.current_player, card)
                        if card[0] == '9':
                            self.current_player = self.apply_additional_rules()
                        self.choose_card.choosed_card_2 = 0
                        self.choose_card.is_take_card = 3
                        self.first_button.setEnabled(False)
                        return True
                    else:
                        self.choose_card.choosed_card_2 = 0
                        self.choose_card.is_take_card = 3
                        if self.choose_card.is_take_card == 1:
                            return False
                else:
                    self.choose_card.is_take_card = 3
                    self.choose_card.choosed_card_2 = 0
                    if self.choose_card.is_take_card == 1:
                        return False
                self.update_design_ingame()
            self.choose_card.is_take_card = 3
            self.choose_card.choosed_card_2 = 0
            time.sleep(2)
        self.first_button.setEnabled(False)

    def get_card_checked(self):
        if self.deck.get_deck_size() <= 0:
            if len(self.trick_pile) > 1:
                self.shaffle_deck_ingame()
                card = self.deck.draw_card()
                self.players[self.current_player].draw_card(card)
            else:
                self.is_end_game = True
        else:
            card = self.deck.draw_card()
            self.players[self.current_player].draw_card(card)

    def apply_additional_rules(self):
        some_index = self.names[self.current_player]
        self.which_player.setText(f"{some_index}")
        check = False
        for player in self.players:
            if len(player.hand) == 0:
                last_card = self.trick_pile[-1]
                if last_card[0] == '9':
                    check = False
                else:
                    check = True
            else:
                check = False
        if check:
            return (self.current_player + 1) % self.num_players

        card = self.trick_pile[-1]
        rank = card[0]
        suit = card[1]

        if rank == 'A':
            self.current_player = (self.current_player + 1) % self.num_players

        elif rank == 'Q':
            self.update_design_ingame()
            suit_choosing = True
            while suit_choosing:
                time.sleep(2)
                if self.current_player == 0:
                    self.second_button.setEnabled(True)
                    suit = self.choose_suit.choosed_suit
                    if suit == -1:
                        pass
                    else:
                        self.current_suit = self.deck.suits[suit]
                        self.choose_suit.choosed_suit = -1
                        suit_choosing = False
                elif self.current_player != 0:
                    suit = random.randint(0, 3)
                    self.current_suit = self.deck.suits[suit]
                    self.ai_choosed = suit
                    suit_choosing = False
            self.second_button.setEnabled(False)

        elif rank == 'K' and suit == 'spades':
            self.current_player = (self.current_player + 1) % self.num_players
            for _ in range(4):
                self.get_card_checked()

        elif rank == '9':
            self.nine_card()

        elif rank == '7':
            self.current_player = (self.current_player + 1) % self.num_players

            for _ in range(2):
                self.get_card_checked()

        elif rank == '6':
            self.current_player = (self.current_player + 1) % self.num_players
            self.get_card_checked()

        # returns the next player
        time.sleep(0.5)
        self.update_design_ingame()
        time.sleep(0.5)
        return (self.current_player + 1) % self.num_players

    def nine_card(self):
        self.update_design_ingame()
        time.sleep(1)
        if self.current_player == 0:
            self.first_button.setEnabled(True)
            choosing_action = True
            while choosing_action:
                time.sleep(2)
                action = self.get_card()
                if action == "1":
                    if self.play_card_action():
                        self.add_rules_ninecard()
                        choosing_action = False
                elif action == "2":
                    if not self.draw_card(self.current_player):
                        choosing_action = False
                    else:

                        self.nine_card()
                        choosing_action = False
        elif self.current_player != 0:
            time.sleep(2)
            valid_cards = [card for card in self.players[self.current_player].hand if
                           card[1] == self.trick_pile[-1][1] or
                           card[0] == self.trick_pile[-1][0] or
                           card[0] == 'Q']
            if len(valid_cards) > 0:
                card = random.choice(valid_cards)
                self.play_card(self.current_player, card)
                if card[0] == '9':
                    time.sleep(1)
                    self.update_design_ingame()
                    self.nine_card()
                else:
                    self.add_rules_ninecard()
                    self.update_design_ingame()
                    time.sleep(1)
            else:
                if self.is_end_game:
                    time.sleep(1)
                    self.update_design_ingame()
                    time.sleep(1)
                else:
                    self.get_card_checked()
                    self.update_design_ingame()
                    time.sleep(1)
                    self.nine_card()

    def add_rules_ninecard(self):
        self.update_design_ingame()
        time.sleep(0.5)
        card = self.trick_pile[-1]
        rank = card[0]
        suit = card[1]

        if rank == 'A':
            self.current_player = (self.current_player + 1) % self.num_players

        elif rank == 'Q':
            self.update_design_ingame()
            suit_choosing = True
            while suit_choosing:
                time.sleep(2)
                if self.current_player == 0:
                    self.second_button.setEnabled(True)
                    suit = self.choose_suit.choosed_suit
                    if suit == -1:
                        pass
                    else:
                        self.current_suit = self.deck.suits[suit]
                        self.choose_suit.choosed_suit = -1
                        suit_choosing = False
                elif self.current_player != 0:
                    suit = random.randint(0, 3)
                    self.current_suit = self.deck.suits[suit]
                    self.ai_choosed = suit
                    suit_choosing = False
            self.second_button.setEnabled(False)

        elif rank == 'K' and suit == 'spades':
            self.current_player = (self.current_player + 1) % self.num_players
            self.update_design_ingame()
            for _ in range(4):
                self.get_card_checked()

        elif rank == '7':
            self.current_player = (self.current_player + 1) % self.num_players
            self.update_design_ingame()

            for _ in range(2):
                self.get_card_checked()

        elif rank == '6':
            self.current_player = (self.current_player + 1) % self.num_players
            self.update_design_ingame()

            self.get_card_checked()

    def check_game_over(self):
        for player in self.players:
            if len(player.hand) == 0:
                return True

        if len(self.deck.cards) == 0 and all(len(player.hand) == 0 for player in self.players):
            return True
        return False

    def update_scores(self, scores):
        for i, player in enumerate(self.players):
            score = calculate_score(player.hand)
            scores[i] = score
        self.current_player = 0
        self.current_player = (self.current_player + self.round_number) % self.num_players
        self.round_number = self.round_number + 1
        return scores

    def reset_settings(self):
        player_names = [player.name for player in self.players]

        self.players.clear()

        for name in player_names:
            self.players.append(Player(name))

        self.choosed_card = 0
        self.modes = 0
        self.num_players = 4
        self.trick_pile = []

        self.current_suit = None
        self.ai_choosed = None
        self.is_end_game = None
        self.deck = Deck()
        self.deck.shuffle()
        self.deal_cards()
        self.trick_pile.append(self.deck.draw_card())

    def display_scores(self, scores):
        self.points_player1.setText(f"Score: {scores[0]}")
        self.points_player2.setText(f"Score: {scores[1]}")
        self.points_player3.setText(f"Score: {scores[2]}")
        self.points_player4.setText(f"Score: {scores[3]}")

    def run(self):
        self.dev_mode.setEnabled(True)
        game_scores = [0, 0, 0, 0]

        game_over = False
        while not game_over:
            last_scores = [0, 0, 0, 0]
            time.sleep(1)
            self.play_round()
            last_scores = self.update_scores(last_scores)
            self.reset_settings()
            for i in range(0, 4):
                game_scores[i] = game_scores[i] + last_scores[i]
            game_scores = check_scores(game_scores)
            game_over = is_game_over(game_scores)
            self.display_scores(game_scores)

        final_winners, final_scores = determine_winner(game_scores)
        save_results(final_winners, final_scores, self.players)
        self.setWindowTitle(f"The game is over. The winner is: {final_winners}")

        self.faq.setEnabled(False)
        self.start_game.setEnabled(False)
        self.end_game.setEnabled(False)
        self.dev_mode.setEnabled(False)
        self.first_button.setEnabled(False)
        self.second_button.setEnabled(False)
        self.save_game_results.setEnabled(True)
