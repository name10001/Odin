from game import AbstractGame
from player import AbstractPlayer
from cards.deck import AbstractDeck


class TestDeck(AbstractDeck):

    def __init__(self, cards):
        self.cards = cards
        self.index = 0

    def get_next_card(self, flags):
        card = self.cards[self.index]

        self.index += 1
        return card


class TestPlayer(AbstractPlayer):

    def __init__(self, game, name, cards, responses=[]):
        super().__init__(game, name, name)

        self.responses = []
        self.index = 0

        for card in cards:
            self.hand.add_card(card)

    def ask_question(self, question):
        """
        Respond to a question using a predetermined array of responses
        """
        response = self.responses[self.index]
        self.index += 1

        return response


class TestGame(AbstractGame):
    def __init__(self):
        super().__init__()

        self.game_over = False
    
    def create_players(self, players):
        for player in players:
            self.add_player(player)

    def create_deck(self, deck):
        self.deck = deck

    def create_top_card(self, top_card):
        self.played_cards.add_card(top_card)


    def end_game(self, winner=None):
        """
        Set some attributes to show that the game is over
        """
        self.winner = winner
        self.game_over = True
