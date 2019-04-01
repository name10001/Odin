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

    def initial_connection(self):
        join_room(self.game_id + "_game")

    def get_id(self):
        return self.game_id
