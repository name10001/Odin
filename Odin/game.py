import cards
from player import Player
from flask import *
from flask_socketio import *
import flask_server as fs


class Game:
    """
    This stores information about a game
    """
    _pickup = 0
    _played_cards = []
    _players = {}
    _direction = 1  # 1 or -1
    running = False
    starting_number_of_cards = 10;

    def __init__(self, game_id, players):
        self.game_id = game_id
        for player in players:
            self._players[player] = Player(self, players[player], player)
        self._played_cards = [cards.pickup_from_deck()(self)]

    def get_card(self, card_id):
        """
        checks to see if a card exists in this came
        :param card_id: id of card to look for
        :return: returns the card if found, else None
        """
        for card in self._played_cards:
            if card.id == card_id:
                return card
        print(self._players)
        for player in self._players:
            for card in self._players[player].get_cards():
                if card.id == card_id:
                    return card
        return None

    def get_player(self, player_id):
        """
        checks to see if a player exists in this came
        :param player_id: id of player to look for
        :return: returns the player if found, else None
        :return:
        """
        if player_id in self._players:
            return self._players[player_id]
        else:
            return None

    def render_game(self):
        """
        render the HTML needed to display the game
        :return:
        """
        return render_template("game.html", game=self)

    def message(self, message):
        """
        When a message is sent to a game it comes here then gets sent to all the clients
        :param message: 
        :return: None
        """
        if message == "Uno":
            player = self.get_player(session['player_id'])
            print("message for player", player.get_name() + " is on Uno!")
            print(self.game_id)
            with fs.app.app_context():
                fs.socket_io.emit(
                    "message for player",
                    player.get_name() + " is on Uno!",
                    room=self.game_id + "_game",
                    include_self=False
                )
        else:
            print("got unknown message from player:", message)
            
    def _card_update(self):
        """
        sends all cards to client in json from
        cards example:
        {
            "your cards":
                [
                    {
                        "card id": "blue_zero_card_124",
                        "card image url": "/static/cards/0_blue.png",
                        "can be played": true,
                        "pick a player": false,
                        "pick a card type": false
                    },
                    {
                        "card id": "fuck_you_card_8",
                        "card image url": "/static/cards/fuck_you.png",
                        "can be played": true,
                        "pick a player": true,
                        "pick a card type": false
                    }
                ]
            "cards on deck":
                [
                    {
                        "card image url": "/static/cards/0_green.png"
                    },
                    {
                        "card image url": "/static/cards/1_green.png"
                    },
                    {
                        "card image url": "/static/cards/1_blue.png"
                    },
                ]
        }
        :return: 
        """
        json_to_send = {
            "cards on deck": [],
            "your cards": []
        }
        # get first 3 cards from deck
        lim = 3
        for card in self._played_cards:
            json_to_send["cards on deck"].append(
                {
                    "card image url": card.get_url()
                }
            )
            if lim == 0:
                break
            lim -= 1

        # get player cards
        player = self.get_player(session['player_id'])
        for card in player.get_cards():
            json_to_send["your cards"].append(
                {
                    "card id": card.get_id(),
                    "card image url": card.get_url(),
                    "can be played": card.can_be_played_on(self._played_cards[-1]),
                    "pick a player": False,
                    "pick a card type": False
                }
            )

        # send
        with fs.app.app_context():
            fs.socket_io.emit("card update", json_to_send)

    def initial_connection(self):
        join_room(self.game_id + "_game")
        self._card_update()

    def get_id(self):
        return self.game_id
