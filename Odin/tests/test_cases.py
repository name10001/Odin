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

        deck = JustABlankDeck()

        game.create([player_1, player_2], deck, top_card)

        # Play the game

        game.play_cards([player_1_cards[0].get_id()])
        game.next_turn()
        game.play_cards([player_2_cards[0].get_id()])
        game.next_turn()
        game.play_cards([player_1_cards[1].get_id()])
        game.next_turn()
        game.play_cards([player_2_cards[1].get_id()])
        game.next_turn()
        game.play_cards([player_1_cards[2].get_id()])
        game.next_turn()

        # Check player 1 is the winner
        self.assertEqual(game.winner.get_name(), "player_1")

    def test_numbers(self):
        """
        Tests the compatibility of number cards
        """

        game = TestGame()

        top_card = GreenZero(game)

        cards_to_test = [RedZero(game), GreenZero(game), PurpleZero(game), OrangeZero(game), GreenOne(
            game), GreenSeven(game), YellowOne(game), RedTwo(game), PurpleEight(game), OrangeNine(game), RedOne(game)]
        ids = [card.get_id() for card in cards_to_test]

        player = TestPlayer(game, "player", cards_to_test)

        deck = JustABlankDeck()

        game.create([player], deck, top_card)

        # Test Valid
        for i in range(0, 6):
            game.play_cards([ids[i]])

            self.assertEqual(len(game.planning_pile), 1)

            game.undo()

        # Test Invalid
        for i in range(6, 11):
            game.play_cards([ids[i]])

            self.assertEqual(len(game.planning_pile), 0)

        # Test playing multiple at once (zero)

        game.play_cards([ids[i] for i in range(0, 4)])
        self.assertEqual(len(game.planning_pile), 4)

        game.play_cards([ids[i] for i in range(4, 11)])
        self.assertEqual(len(game.planning_pile), 4)

        game.undo_all()

        # Test playing multiple at once (one)
        game.play_cards([ids[10], ids[6], ids[4]])
        self.assertEqual(len(game.planning_pile), 3)

        game.play_cards([ids[0]])
        self.assertEqual(len(game.planning_pile), 3)

        game.next_turn()

        self.assertEqual(game.get_top_card().get_id(), ids[10])

    def test_jew_card(self):
        """
        Test the Jew Card.

        - Standard use of the card with 3 players.
        - Compatibility
        - Checking that stealing someone's last card ends the game
        """
        # Setup 3 player game
        game = TestGame()

        top_card = GreenZero(game)

        player_1_cards = [Jew(game), Elevator(game)]
        player_2_cards = [CopyCat(game), BlankBro(game), BlankBro(game)]
        player_3_cards = [PurpleFour(game), BlankBro(game), BlankBro(game)]

        steal1 = player_2_cards[1].get_id()
        steal2 = player_3_cards[1].get_id()
        steal3 = player_3_cards[2].get_id()

        test_card_1 = player_1_cards[0].get_id()
        test_card_2 = player_2_cards[2].get_id()
        test_card_3 = player_2_cards[0].get_id()
        test_card_4 = player_3_cards[0].get_id()
        test_card_5 = player_1_cards[1].get_id()

        player_1 = TestPlayer(game, "player_1", player_1_cards, [
                              "player_2", steal1, "player_3", steal3])
        player_2 = TestPlayer(game, "player_2", player_2_cards, [
                              "player_3", steal2])
        player_3 = TestPlayer(game, "player_3", player_3_cards)

        deck = TestDeck([Jew])

        game.create([player_1, player_2, player_3], deck, top_card)

        # Player 1 steal from 2
        game.play_cards([test_card_1])
        game.next_turn()

        self.assertTrue(player_1.hand.find_card(steal1) is not None)
        self.assertTrue(player_2.hand.find_card(steal1) is None)

        # Player 2 steal from 3
        game.play_cards([test_card_2])
        self.assertEqual(len(game.planning_pile), 0)

        game.play_cards([test_card_3])
        game.next_turn()

        self.assertTrue(player_2.hand.find_card(steal2) is not None)
        self.assertTrue(player_3.hand.find_card(steal2) is None)

        game.play_cards([test_card_4])
        game.next_turn()

        # Player 1 steal last card from player 3
        game.play_cards([test_card_5])
        game.next_turn()

        self.assertTrue(player_1.hand.find_card(steal3) is not None)
        self.assertTrue(player_3.hand.find_card(steal3) is None)

        self.assertEqual(len(player_3.hand), 0)
        self.assertEqual(game.winner.get_name(), "player_3")
