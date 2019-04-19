import cards
import flask_server as fs
from time import time


class Player:
    def __init__(self, game, name, player_id):
        self.name = name
        self.game = game
        self.player_id = player_id
        self.sorted_hand_list = []
        self.hand_dict = {}
        self.name = name
        # self.said_uno_previous_turn = False
        # self.said_uno_this_turn = False
        self.picked_up_this_turn = False
        self.sid = None
        self.planning_pile = []
        self.turns_left = 1
        self.state = "not turn"

    def play_cards(self, cards):
        """
        Takes cards out of players hand and adds it to the games played cards
        Also preforms all actions of the card and checks if its aloud to be played
        :param cards: array of card to play. 2d array. e.g. [["id", "option"], ["id", "option"], etc]
        :return: None
        """
        for card in cards:
            self.play_card(card[0], card[1], update_player=False)
        print("from play cards")
        self.card_update()
        self.game.update_players(exclude=self)

    def play_card(self, card_id, chosen_option, update_player=True):
        """
        Takes card out of players hand and adds it to the games played cards
        Also preforms all actions of the card and checks if its aloud to be played
        :param card_id:
        :param chosen_option:
        :param update_player: boolean, should the player's client be updated after the card is played
        :return:None
        """
        card = self.find_card(card_id)
        if card is None:
            return
        if self._can_be_played(card):
            self.remove_card(card, update_player=False)
            self.game.add_played_card(card, update_players=False)
            self.planning_pile.append((card, chosen_option))
            card_below = self.game.played_cards[len(self.game.played_cards)-2]
            card.prepare_card(self, chosen_option, card_below)

        if update_player:
            print("from play 1 card")
            self.card_update()
            self.game.update_players(exclude=self)

    def finish_turn(self):
        """

        :return: boolean, True of the player should have another turn
        """
        played_pickup = False
        # play cards from planing pile
        for (card, chosen_option) in self.planning_pile:
            card_below = self.game.played_cards[self.game.played_cards.index(card)-1]
            card.play_card(self, chosen_option, card_below)
            if card.CAN_BE_ON_PICKUP is True:
                played_pickup = True

        # if the player has won but did not say uno in the previous turn, make them pickup
        # if self.said_uno_previous_turn is False and self.had_won() is True:
        #     self.pickup()
        # self.said_uno_previous_turn = self.said_uno_this_turn
        # self.said_uno_this_turn = False

        #
        if self.game.pickup != 0 and played_pickup is False:
            self.pickup()
        # if player did not play any cards, make them pickup
        if len(self.planning_pile) == 0:
            self.pickup()
        self.planning_pile = []

        # send wining message to everyone but this player
        if self.had_won():
            with fs.app.app_context():
                fs.socket_io.emit(
                    "message for player",
                    self.name + " has won!",
                    room=self.game.game_id + "_game",
                    include_self=False
                )

        self.picked_up_this_turn = False

        # check if player has any more turns left.
        self.turns_left -= 1
        if self.turns_left > 0:
            return True
        else:
            self.state = "not turn"
            self.turns_left = 1
            return False

    def card_update(self):
        """
        Sends all the information to the player to render the game.
        This includes but is not limited to, the players hand, the played cards and other player information
        It is sent in the form of JSON to the client where the information is rendered using javascript
        :return: None
        """
        print("updateing player!")
        json_to_send = {
            "cards on deck": [],
            "your cards": [],
            "planning pile": [],
            "direction": self.game.direction,
            "pickup size": self.game.pickup,
            "players": []
        }

        # get first 4 cards from deck that are not in planning pile
        number_of_cards = len(self.game.played_cards) - len(self.planning_pile)
        for card_index in range(max(number_of_cards - 4, 0), number_of_cards):
            card = self.game.played_cards[card_index]
            json_to_send["cards on deck"].append(
                {
                    "card image url": card.get_url(),
                    "card id": card.get_id(),
                    "card can be undone": False,
                }
            )

        # get cards from planning pile
        for card, options in self.planning_pile:
            json_to_send["planning pile"].append(
                {
                    "card image url": card.get_url(),
                    "card id": card.get_id()
                }
            )

        # get player cards
        for card in self.get_hand():
            json_to_send["your cards"].append(
                {
                    "card id": card.get_id(),
                    "card image url": card.get_url(),
                    "can be played": self._can_be_played(card),
                    "options": card.get_options(self),
                }
            )

        # get information all players
        for player in self.game.players:
            json_to_send["players"].append(
                {
                    "name": player.get_name(),
                    "number of cards": player.size_of_hand(),
                    "is turn": player.is_turn(),
                    #"is uno": player.is_uno(),
                    "is you": player == self,
                }
            )

        # send players client
        with fs.app.app_context():
            fs.socket_io.emit("card update", json_to_send, room=self.sid)

    def pickup(self):
        """
        If there is a pickup chain this will pick it up, otherwise it will pickup 1
        only runs if its the players turn
        :return: None
        """
        if self.picked_up_this_turn is True:
            return
        if self.is_turn() is False:
            return
        if self.game.pickup == 0:
            self.add_new_cards(1)
        else:
            self.add_new_cards(self.game.pickup)
            self.game.pickup = 0
        self.picked_up_this_turn = True

    def undo(self, update_players=True):
        """
        If the player has put down a card this turn it will undo the latest one
        :return:
        """
        if len(self.planning_pile) == 0 or not self.is_turn():
            return
        card_to_remove = self.planning_pile.pop()[0]
        self.game.played_cards.remove(card_to_remove)
        self.add_card(card_to_remove)

        played_on = self.game.played_cards[len(self.game.played_cards)-1]
        card_to_remove.undo_prepare_card(self, played_on)

        if update_players:
            self.game.update_players()

    def undo_all(self):
        """
        If the player has put down a card this turn it will undo the latest one
        :return:
        """
        if not self.is_turn():
            return
        for i in range(0, len(self.planning_pile)):
            self.undo(update_players=False)

        self.game.update_players()

    def _can_be_played(self, card):
        """
        Can the given card be played right now
        :return:
        """
        top_card = self.game.played_cards[-1]
        is_first_card = len(self.planning_pile) == 0

        if self.is_turn() and not is_first_card:
            return card.can_be_played_with(self.planning_pile, self)
        elif card.can_be_played_on(top_card, self):
            return True
        else:
            return False

    # def say_uno(self):
    #    """
    #    Say uno to all the other players and remembers that the player said Uno
    #    :return:
    #    """
    #    if self.is_turn() is False:
    #        return
    #    self.said_uno_this_turn = True
    #    with fs.app.app_context():
    #        fs.socket_io.emit(
    #            "message for player",
    #            self.name + " is on Uno!",
    #            room=self.game.game_id + "_game",
    #            include_self=False
    #        )

    def add_new_cards(self, number):
        """
        gets new cards from deck and adds them to hand
        Does not update player
        Does not check for pickup chains of weather its the players turn
        if you want that, use pickup(self) instead
        :param number: number of cards to add
        :return: None
        """
        number = min(1420 - len(self.sorted_hand_list), int(number))
        cards_to_add = [card(self.game) for card in self.game.deck.pickup(number)]
        self.add_cards(cards_to_add, update_player=False)

    def add_card(self, card, sort_after=True, update_player=True):
        """
        adds a single card
        :param card:
        :param sort_after:
        :param update_player:
        :return:
        """
        self.sorted_hand_list.append(card)
        self.hand_dict[card.get_id()] = card
        if sort_after is True:
            self.sorted_hand_list.sort()
        if update_player:
            print("from add_card")
            self.card_update()

    def add_cards(self, cards, sort_after=True, update_player=True):
        """
        adds multiple cards
        :param cards:
        :param sort_after:
        :param update_player:
        :return:
        """
        for card in cards:
            self.add_card(card, update_player=False, sort_after=False)
        if sort_after is True:
            self.sorted_hand_list.sort()
        if update_player:
            print("from add_cards")
            self.card_update()

    def remove_card(self, card, update_player=False):
        """
        removes multiple cards
        :param card:
        :param sort_after:
        :param update_player:
        :return:
        """
        self.sorted_hand_list.remove(card)
        del self.hand_dict[card.get_id()]
        if update_player:
            print("from remove card")
            self.card_update()

    def had_won(self):
        """
        checks if the player has one, if they have then it returns True.
        :return:
        """
        return len(self.sorted_hand_list) == 0

    def find_card(self, card_id):
        """
        Finds a card owned by the player
        :param card_id:
        :return: Card if a card is found, None if not found
        """
        if card_id in self.hand_dict:
            return self.hand_dict[card_id]

    def start_turn(self):
        """
        starts the players turn
        :return:
        """
        self.state = "playing turn"

    # def is_uno(self):
    #    return self.said_uno_previous_turn or self.said_uno_this_turn

    def size_of_hand(self):
        return len(self.sorted_hand_list)

    def set_sid(self, sid):
        self.sid = sid

    def get_sid(self):
        return self.sid

    def set_hand(self, hand):
        self.sorted_hand_list = []
        self.hand_dict.clear()
        self.add_cards(hand, update_player=False)

    def get_hand(self):
        return self.sorted_hand_list

    def get_name(self):
        return self.name

    def get_id(self):
        return self.player_id
    
    def is_turn(self):
        return self.state == "playing turn"
