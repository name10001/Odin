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

    def __init__(self, game_id):
        self.game_id = game_id
        self._players = {}
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
        if request.method == 'GET':
            if "player_id" in session and session["player_id"] in self._players:
                if self.running:
                    return "this is the game"
                else:
                    return render_template("waiting room.html", game=self)
            else:
                if self.running:
                    return "Sorry, game has already started"
                else:
                    return render_template("login.html")
        elif request.method == 'POST':
            new_player = Player(self, escape(request.form['player_name']))
            self._players[new_player.get_id()] = new_player
            session['player_id'] = new_player.get_id()
            with fs.app.app_context():
                fs.socket_io.emit("user joined", new_player.get_name(), room=self.game_id)
            return redirect("/games/" + self.game_id)
        else:
            return "What the Fuck Did You Just Bring Upon This Cursed Land!"

    def joined_waiting_room(self):
        """
        Sends then all the joined players. If new players join latter it will also send them
        :return: None
        """
        join_room(self.game_id)
        for player in self._players:
            emit("user joined", self._players[player].get_name())

    def get_id(self):
        return self.game_id

