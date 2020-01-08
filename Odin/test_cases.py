import unittest
from cards import *
from tests import *
from cards.deck import *



class CardTester(unittest.TestCase):

    def test_simple_game(self):
        """
        A simple 2 player game, each beginning with 3 cards.
        The game goes until completion, where player 1 wins.
        """


        # Setup
        game = TestGame()
        
        top_card = GreenZero(game)

        player_1_cards = [YellowZero(game), YellowEight(game), BlueEight(game)]
        player_2_cards = [YellowFour(game), RedEight(game), GreenNine(game)]

        player_1 = TestPlayer(game, "player_1", player_1_cards)
        player_2 = TestPlayer(game, "player_2", player_2_cards)

        deck = WeightedDeck(game)

        game.create_deck(deck)
        game.create_players([player_1, player_2])
        game.create_top_card(top_card)

        # Play the game
        game.start_turn()
        game.play_cards([player_1_cards[0]])
        game.next_turn()
        game.play_cards([player_2_cards[0]])
        game.next_turn()
        game.play_cards([player_1_cards[1]])
        game.next_turn()
        game.play_cards([player_2_cards[1]])
        game.next_turn()
        game.play_cards([player_1_cards[2]])
        game.next_turn()

        # Check player 1 is the winner
        self.assertEquals(game.winner.get_name(), "player_1")
