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
        self._add_new_cards(game.starting_number_of_cards)
        self.first_card_of_turn = None

    def say_uno(self):
        """
        Say uno to all the other players and remembers that the player said Uno
        :return:
        """
        if self.game.turn != self:
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

        if self._can_be_played(card):
            card.play_card(self, chosen_option)
            self.hand.remove(card)
            self.game.add_played_card(card)

        if self.first_card_of_turn is None:
            self.first_card_of_turn = card

    def _can_be_played(self, card):
        """
        Can the given card be played right now
        :return:
        """
        top_card = self.game.played_cards[-1]
        is_first_card = self.first_card_of_turn is None

        if self.is_turn() and not is_first_card:
            return card.can_be_played_with(self.first_card_of_turn)
        elif card.can_be_played_on(top_card, self.is_turn()):
            return True
        else:
            return False

    def finish_turn(self):
        """

        :return:
        """
        print("turn finished")
        if self.game.pickup != 0:
            self.pickup()
        if self.said_uno_previous_turn is False and self.had_won() is True:
            self.pickup()
        self.said_uno_previous_turn = self.said_uno_this_turn
        self.said_uno_this_turn = False
        self.picked_up_this_turn = False

        if self.had_won():
            with fs.app.app_context():
                fs.socket_io.emit(
                    "message for player",
                    self.name + " has won!",
                    room=self.game.game_id + "_game",
                    include_self=False
                )

        if self.first_card_of_turn is None:
            self._add_new_cards(1)
        self.first_card_of_turn = None

    def pickup(self):
        """
        If there is a pickup chain this will pick it up, otherwise it will pickup 1
        only runs if its the players turn
        :return: None
        """
        if self.picked_up_this_turn is True:
            return
        if self.game.turn != self:
            return
        if self.game.pickup == 0:
            self._add_new_cards(1)
        else:
            self._add_new_cards(self.game.pickup)
            self.game.pickup = 0
        self.card_update()
        self.picked_up_this_turn = True

    def _add_new_cards(self, number):
        """
        gets new cards from deck and adds them to hand
        Does not update player
        Does not check for pickup chains of weather its the players turn
        if you want that, use pickup(self) instead
        :param number: number of cards to add
        :return: None
        """
        for i in range(0, number):
            self.hand.append(self.game.deck.pickup()(self.game))

    def card_update(self):
        """
        sends all cards to client in json from
        :return:
        """
        json_to_send = {
            "cards on deck": [],
            "your cards": [],
            "Your turn": self.is_turn(),
            "pickup size": self.game.pickup
        }
        # get first 3 cards from deck
        number_of_cards = len(self.game.played_cards)
        for card_index in range(max(number_of_cards - 4, 0), number_of_cards):
            json_to_send["cards on deck"].append(
                {
                    "card image url": self.game.played_cards[card_index].get_url()
                }
            )

        # get player cards
        for card in self.get_cards():
            json_to_send["your cards"].append(
                {
                    "card id": card.get_id(),
                    "card image url": card.get_url(),
                    "can be played": self._can_be_played(card),
                    "options": card.get_options()
                }
            )

        # send
        with fs.app.app_context():
            fs.socket_io.emit("card update", json_to_send, room=self.sid)

    def set_sid(self, sid):
        self.sid = sid

    def get_sid(self):
        return self.sid

    def get_cards(self):
        return self.hand

    def get_name(self):
        return self.name

    def get_id(self):
        return self.player_id
    
    def is_turn(self):
        return self == self.game.turn
