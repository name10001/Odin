from game import AbstractGame
from player import AbstractPlayer
import cards
from cards import BlankBro
from cards.deck import AbstractDeck

class TestDeck(AbstractDeck):
    """
    Deck with a set array of cards
    """

    def __init__(self, cards):
        self.cards = cards
        self.index = 0

    def get_next_card(self, flags):
        card = self.cards[self.index]

        self.index += 1
        return card

class JustABlankDeck(AbstractDeck):
    """
    Deck which only gives JustABlankBros
    """

    def get_next_card(self, flags):
        return BlankBro


class TestPlayer(AbstractPlayer):

    def __init__(self, game, name, cards, responses=[]):
        super().__init__(game, name, name)

        self.responses = responses
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
    
    def create(self, players, deck, top_card):
        for player in players:
            self.add_player(player)

        self.deck = deck

        self.played_cards.add_card(top_card)

        self.start_turn()

    def end_game(self, winner=None, winners=None):
        """
        Set some attributes to show that the game is over
        """
        self.winner = winner
        self.winners = winners
        self.game_over = True
