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
        game.finish_turn()
        game.play_cards([player_2_cards[0].get_id()])
        game.finish_turn()
        game.play_cards([player_1_cards[1].get_id()])
        game.finish_turn()
        game.play_cards([player_2_cards[1].get_id()])
        game.finish_turn()
        game.play_cards([player_1_cards[2].get_id()])
        game.finish_turn()

        # Check player 1 is the winner
        self.assertEqual(game.winner.get_name(), "player_1")

    def test_numbers(self):
        """
        Tests the compatibility of number cards
        """

        game = TestGame()

        top_card = GreenZero(game)

        cards_to_test = [RedZero(game), GreenZero(game), PurpleZero(game), OrangeZero(game), GreenSixtyNine(
            game), GreenSeven(game), YellowSixtyNine(game), RedTwo(game), PurpleEight(game), OrangeNine(game), RedSixtyNine(game)]
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

        game.finish_turn()

        self.assertEqual(game.get_top_card().get_id(), ids[10])

    def test_steal_card(self):
        """
        Test the Steal Card.

        - Standard use of the card with 3 players.
        - Compatibility
        - Checking that stealing someone's last card ends the game
        """
        # Setup 3 player game
        game = TestGame()

        top_card = GreenZero(game)

        player_1_cards = [Steal(game), Elevator(game)]
        player_2_cards = [CopyCat(game), BlankBro(game), Happiness(game)]
        player_3_cards = [YellowFour(game), BlankBro(game), BlankBro(game)]

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

        deck = TestDeck([Steal])

        game.create([player_1, player_2, player_3], deck, top_card)

        # Player 1 steal from 2
        game.play_cards([test_card_1])
        game.finish_turn()

        self.assertTrue(player_1.hand.find_card(steal1) is not None)
        self.assertTrue(player_2.hand.find_card(steal1) is None)

        # Player 2 steal from 3
        game.play_cards([test_card_2])
        self.assertEqual(len(game.planning_pile), 0)

        game.play_cards([test_card_3])
        game.finish_turn()

        self.assertTrue(player_2.hand.find_card(steal2) is not None)
        self.assertTrue(player_3.hand.find_card(steal2) is None)

        game.play_cards([test_card_4])
        game.finish_turn()

        # Player 1 steal last card from player 3
        game.play_cards([test_card_5])
        game.finish_turn()

        self.assertTrue(player_1.hand.find_card(steal3) is not None)
        self.assertTrue(player_3.hand.find_card(steal3) is None)

        self.assertEqual(len(player_3.hand), 0)
        self.assertEqual(game.winner.get_name(), "player_3")

    def test_pickup_chain(self):
        """
        Basic test of a pickup chain between 2 people

        Also tests compatibility
        """

        game = TestGame()

        top_card = GreenZero(game)

        player_1_cards = [PurplePickup2(game), YellowPickup2(
            game), BlueEight(game), PickupTimes2(game)]
        ids1 = [card.get_id() for card in player_1_cards]
        player_2_cards = [Pickup4(game), PickupPower2(game), GreenNine(game)]
        ids2 = [card.get_id() for card in player_2_cards]

        player_1 = TestPlayer(game, "player_1", player_1_cards)
        player_2 = TestPlayer(game, "player_2", player_2_cards)

        deck = JustABlankDeck()

        game.create([player_1, player_2], deck, top_card)

        # Pickup
        game.finish_turn()

        self.assertEqual(len(player_1.hand), 5)

        # Play +4

        game.play_cards([ids2[0]])
        game.finish_turn()
        self.assertEqual(game.pickup, 4)

        # Try play some cards that don't work

        game.play_cards([ids1[0]])
        self.assertEqual(len(game.planning_pile), 0)
        game.play_cards([ids1[2]])
        self.assertEqual(len(game.planning_pile), 0)

        # +2, x^2, x2
        game.play_cards([ids1[1]])
        game.finish_turn()
        game.play_cards([ids2[1]])
        game.finish_turn()
        game.play_cards([ids1[3]])
        game.finish_turn()
        self.assertEqual(game.pickup, 72)

        # Pickup 16
        game.finish_turn()

        self.assertEqual(len(player_2.hand), 73)
        self.assertEqual(len(player_1.hand), 3)

        # pickup 1
        game.finish_turn()

        self.assertEqual(len(player_1.hand), 4)

    def test_pickup_chain_end(self):
        """
        Testing possible ending states of a pickup chain (between 3 people).

        Also tests that the "player pickup amount" numbers are accurate

        - Fuck you with nothing
        - Everyone pickup with nothing
        - Pawn with nothing (not possible)

        - Pickup chain fuck you
        - Pickup chain everyone pickup
        - Pickup chain pawn

        - Double fuck you
        - double everyone pickup
        """

        # Setup
        game = TestGame()

        top_card = BlankBro(game)

        player_1_cards = [FuckYou(game), FuckYou(game), Pickup10(
            game), Pickup10(game), Plus(game), Plus(game)]
        player_2_cards = [Plus(game), Pickup10(game), Pawn(
            game), FuckYou(game), FuckYou(game)]
        player_3_cards = [Pickup10(game), Plus(game), Pickup10(game)]
        ids1 = [card.get_id() for card in player_1_cards]
        ids2 = [card.get_id() for card in player_2_cards]
        ids3 = [card.get_id() for card in player_3_cards]

        player_1 = TestPlayer(game, "player_1", player_1_cards, [
                              "player_2", "player_2", "player_2"])
        player_2 = TestPlayer(game, "player_2", player_2_cards, [
                              "player_1", "player_3"])
        player_3 = TestPlayer(game, "player_3", player_3_cards)

        deck = JustABlankDeck()

        game.create([player_1, player_2, player_3], deck, top_card)

        # Begin testing
        # 6, 5, 3
        game.play_cards([ids1[0]])
        self.assertEqual(player_2.player_pickup_amount, 5)
        game.undo()
        self.assertEqual(player_2.player_pickup_amount, 0)
        game.play_cards([ids1[0]])
        game.finish_turn()

        # 5, 10, 3
        self.assertEqual(len(player_2.hand), 10)
        game.play_cards([ids2[2]])
        self.assertEqual(len(game.planning_pile), 0)
        game.play_cards([ids2[0]])
        self.assertEqual(player_1.player_pickup_amount, 2)
        self.assertEqual(player_3.player_pickup_amount, 2)
        game.undo_all()
        self.assertEqual(player_1.player_pickup_amount, 0)
        self.assertEqual(player_3.player_pickup_amount, 0)
        game.play_cards([ids2[0]])

        game.finish_turn()

        #7, 9, 5
        self.assertEqual(len(player_1.hand), 7)
        self.assertEqual(len(player_3.hand), 5)
        game.play_cards([ids3[0]])
        game.finish_turn()
        game.play_cards([ids1[1]])
        game.finish_turn()

        # 6, 19, 4
        self.assertEqual(len(player_2.hand), 19)
        game.play_cards([ids2[1]])
        game.finish_turn()
        game.play_cards([ids3[1]])
        game.finish_turn()

        # 16, 28, 3
        self.assertEqual(len(player_1.hand), 16)
        self.assertEqual(len(player_2.hand), 28)
        self.assertEqual(len(player_3.hand), 3)
        game.play_cards([ids1[2]])
        game.finish_turn()
        game.play_cards([ids2[2]])
        game.finish_turn()
        game.finish_turn()

        # 15 27 4
        self.assertEqual(len(player_3.hand), 4)
        game.play_cards([ids1[3]])
        game.finish_turn()
        game.play_cards([ids2[3], ids2[4]])
        game.finish_turn()

        # 24 25 14
        self.assertEqual(len(player_1.hand), 24)
        self.assertEqual(len(player_2.hand), 25)
        self.assertEqual(len(player_3.hand), 14)

        game.play_cards([ids3[2]])
        game.finish_turn()
        game.play_cards([ids1[4], ids1[5]])
        self.assertEqual(player_2.player_pickup_amount, 20)
        self.assertEqual(player_3.player_pickup_amount, 20)
        game.finish_turn()

        # 22 45 33
        self.assertEqual(len(player_1.hand), 22)
        self.assertEqual(len(player_2.hand), 45)
        self.assertEqual(len(player_3.hand), 33)

    def test_free_turn_card(self):
        """
        Tests the free turn card.
        - Test undoing the free turn card.

        - Test on its own


        - Test 2 at once

        - Test 1 from an elevator
        """

        # Setup
        game = TestGame()

        top_card = BlankBro(game)

        player_1_cards = [FreeTurn(game), Elevator(game)]
        player_2_cards = [FreeTurn(game), FreeTurn(game)]
        ids1 = [card.get_id() for card in player_1_cards]
        ids2 = [card.get_id() for card in player_2_cards]

        player_1 = TestPlayer(game, "player_1", player_1_cards)
        player_2 = TestPlayer(game, "player_2", player_2_cards)

        deck = TestDeck([BlankBro, BlankBro, BlankBro, BlankBro, BlankBro, FreeTurn, BlankBro])

        game.create([player_1, player_2], deck, top_card)

        
        
        self.assertEqual(game.get_turn().get_id(), "player_1")
        game.finish_turn()
        self.assertEqual(game.get_turn().get_id(), "player_2")

        # Test undo
        game.play_cards([ids2[0], ids2[1]])
        self.assertEqual(player_2.effects[0].n_turns, 2)
        game.undo()
        self.assertEqual(player_2.effects[0].n_turns, 1)
        game.undo()
        self.assertEquals(len(player_2.effects), 0)

        game.finish_turn()
        self.assertEqual(game.get_turn().get_id(), "player_1")
        
        # Test one on its own
        game.play_cards([ids1[0]])
        game.finish_turn()
        self.assertEqual(game.get_turn().get_id(), "player_1")
        game.finish_turn()
        self.assertEqual(game.get_turn().get_id(), "player_2")

        # Test 2
        game.play_cards([ids2[0], ids2[1]])
        game.finish_turn()
        self.assertEqual(game.get_turn().get_id(), "player_2")
        game.finish_turn()
        self.assertEqual(game.get_turn().get_id(), "player_2")
        game.finish_turn()
        self.assertEqual(game.get_turn().get_id(), "player_1")

        # Test elevator
        game.play_cards([ids1[1]])
        game.finish_turn()
        self.assertEqual(game.get_turn().get_id(), "player_1")
        game.finish_turn()
        self.assertEqual(game.get_turn().get_id(), "player_2")

        # Check number of cards per player
        self.assertEqual(len(player_1.hand), 3)
        self.assertEqual(len(player_2.hand), 3)


