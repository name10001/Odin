import cards
import flask_server as fs


class Player:
    def __init__(self, game, name, player_id):
        self.name = name
        self.game = game
        self.player_id = player_id
        self.cards = []
        self.name = ''
        self.said_uno = False
        self.sid = None
        self.pickup(game.starting_number_of_cards)

    def say_uno(self):
        """
        Say uno to all the other players and remembers that the player said Uno
        :return:
        """
        self.said_uno = True
        with fs.app.app_context():
            fs.socket_io.emit(
                "message for player",
                self.name + " is on Uno!",
                room=self.game.game_id + "_game",
                include_self=False
            )

    def find_card(self, card_id):
        """
        Finds a card owned by the player
        :param card_id:
        :return: Card if a card is found, None if not found
        """
        for card in self.cards:
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
        if card.can_be_played_on(self.game.played_cards[-1], self == self.game.turn):
            card.play_card(self, chosen_option)
            self.cards.remove(card)
            self.game.add_played_card(card)

    def pickup(self, number):
        for i in range(0, number):
            self.cards.append(self.game.deck.pickup()(self.game))

    def card_update(self):
        """
        sends all cards to client in json from
        :return:
        """
        json_to_send = {
            "cards on deck": [],
            "your cards": [],
        }
        # get first 3 cards from deck
        lim = 3
        for card in self.game.played_cards:
            json_to_send["cards on deck"].append(
                {
                    "card image url": card.get_url()
                }
            )
            if lim == 0:
                break
            lim -= 1

        # get player cards
        for card in self.get_cards():
            json_to_send["your cards"].append(
                {
                    "card id": card.get_id(),
                    "card image url": card.get_url(),
                    "can be played": card.can_be_played_on(self.game.played_cards[-1], self == self.game.turn),
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
        return self.cards

    def get_name(self):
        return self.name

    def get_id(self):
        return self.player_id
