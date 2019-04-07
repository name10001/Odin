import cards
import flask_server as fs


class Player:
    def __init__(self, game, name, player_id):
        self.name = name
        self.game = game
        self.player_id = player_id
        self.hand = []
        self.name = name
        self.said_uno_previous_turn = False
        self.said_uno_this_turn = False
        self.picked_up_this_turn = False
        self.sid = None
        self.add_new_cards(game.starting_number_of_cards)
        self.planning_pile = []
        self.turns_left = 1
        self.state = "not turn"

    def say_uno(self):
        """
        Say uno to all the other players and remembers that the player said Uno
        :return:
        """
        if self.is_turn() is False:
            return
        self.said_uno_this_turn = True
        with fs.app.app_context():
            fs.socket_io.emit(
                "message for player",
                self.name + " is on Uno!",
                room=self.game.game_id + "_game",
                include_self=False
            )

    def had_won(self):
        """
        checks if the player has one, if they have then it returns True.
        :return:
        """
        return len(self.hand) == 0

    def find_card(self, card_id):
        """
        Finds a card owned by the player
        :param card_id:
        :return: Card if a card is found, None if not found
        """
        for card in self.hand:
            if card.get_id() == card_id:
                return card

    def play_card(self, card_id, chosen_option):
        """
        Takes card out of players hand and adds it to the games played cards
        Also preforms all actions of the card and checks if its aloud to be played
        :param card_id:
        :param chosen_option:
        :return:
        """
        card = self.find_card(card_id)
        if card is None:
            return

        if self._can_be_played(card):
            self.hand.remove(card)
            self.game.add_played_card(card)
            self.planning_pile.append((card, chosen_option))
        self.card_update()

    def undo(self):
        """
        If the player has put down a card this turn it will undo the latest one
        :return:
        """
        if len(self.planning_pile) == 0 or not self.is_turn():
            return
        card_to_remove = self.planning_pile.pop()[0]
        self.game.played_cards.remove(card_to_remove)
        self.hand.append(card_to_remove)

        self.game.update_players()

    def _can_be_played(self, card):
        """
        Can the given card be played right now
        :return:
        """
        top_card = self.game.played_cards[-1]
        is_first_card = len(self.planning_pile) == 0

        if self.is_turn() and not is_first_card:
            return self.planning_pile[0][0].can_be_played_with(card, self)
        elif card.can_be_played_on(top_card, self):
            return True
        else:
            return False

    def start_turn(self):
        """
        starts the players turn
        :return:
        """
        self.state = "playing turn"

    def finish_turn(self):
        """

        :return: boolean, True of the player should have another turn
        """
        played_pickup = False
        for (card, chosen_option) in self.planning_pile:
            card_below = self.game.played_cards[self.game.played_cards.index(card)]
            card.play_card(self, chosen_option, card_below)
            if card.CAN_BE_ON_PICKUP is True:
                played_pickup = True

        if self.game.pickup != 0 and played_pickup is False:
            self.pickup()

        if self.said_uno_previous_turn is False and self.had_won() is True:
            self.pickup()
        self.said_uno_previous_turn = self.said_uno_this_turn
        self.said_uno_this_turn = False

        if len(self.planning_pile) == 0:
            self.pickup()
        self.planning_pile = []

        if self.had_won():
            with fs.app.app_context():
                fs.socket_io.emit(
                    "message for player",
                    self.name + " has won!",
                    room=self.game.game_id + "_game",
                    include_self=False
                )

        self.picked_up_this_turn = False

        self.turns_left -= 1
        if self.turns_left > 0:
            return True
        else:
            self.state = "not turn"
            self.turns_left = 1
            return False

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
        self.card_update()
        self.picked_up_this_turn = True

    def add_new_cards(self, number):
        """
        gets new cards from deck and adds them to hand
        Does not update player
        Does not check for pickup chains of weather its the players turn
        if you want that, use pickup(self) instead
        :param number: number of cards to add
        :return: None
        """
        # TODO: this keeps giving errors sometimes
        for i in range(0, number):
            self.hand.append(self.game.deck.pickup())

    def card_update(self):
        """
        sends all cards to client in json from
        :return:
        """
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
        self.hand.sort()
        for card in self.get_hand():
            json_to_send["your cards"].append(
                {
                    "card id": card.get_id(),
                    "card image url": card.get_url(),
                    "can be played": self._can_be_played(card),
                    "options": card.get_options(self),
                }
            )

        # get all players
        for player in self.game.players:
            json_to_send["players"].append(
                {
                    "name": player.get_name(),
                    "number of cards": player.size_of_hand(),
                    "is turn": player.is_turn(),
                    "is uno": player.is_uno(),
                    "is you": player == self,
                }
            )

        # send
        with fs.app.app_context():
            fs.socket_io.emit("card update", json_to_send, room=self.sid)

    def is_uno(self):
        return self.said_uno_previous_turn or self.said_uno_this_turn

    def size_of_hand(self):
        return len(self.hand)

    def set_sid(self, sid):
        self.sid = sid

    def get_sid(self):
        return self.sid

    def set_hand(self, hand):
        self.hand = hand

    def remove_card(self, card):
        self.hand.remove(card)

    def get_hand(self):
        return self.hand

    def get_name(self):
        return self.name

    def get_id(self):
        return self.player_id
    
    def is_turn(self):
        return self.state == "playing turn"
