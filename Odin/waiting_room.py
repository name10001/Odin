from game import Game
from flask import *
from flask_socketio import *
import flask_server as fs
from time import time
import settings
from util.extended_formatter import extended_formatter


class WaitingRoom:
    """
    This stores information about a waiting room
    """
    def __init__(self, game_id):
        # "player_id": "player_name"
        self._players = {}
        self.running = False
        self.game = None
        self.game_id = game_id
        self.last_modified = time()

    def get_player(self, player_id):
        """
        checks to see if a player exists in this waiting room
        :param player_id: id of player to look for
        :return: returns the player if found, else None
        :return:
        """
        if player_id in self._players:
            return self._players[player_id]
        else:
            return None

    def render(self):
        """
        render the HTML needed to display the waiting room
        :return:
        """
        self.modify()
        if request.method == 'GET':
            if "player_id" in session and session["player_id"] in self._players:
                if self.running:
                    return self.game.render_game()
                else:
                    return render_template("waiting room.html", game=self)
            else:
                return render_template("login.html")
        elif request.method == 'POST':
            name = request.form['player_name'][0:20]  # limit to 20 characters
            player_id = self.make_player_id(name)
            self._players[player_id] = name
            session['player_id'] = player_id
            if self.running is False:
                with fs.app.app_context():
                    fs.socket_io.emit("user joined", name, room=self.game_id)
            else:
                self.game.add_observer(name, player_id)
            return redirect("/" + self.game_id)
        else:
            return "What the Fuck Did You Just Bring Upon This Cursed Land!"

    def joined_waiting_room(self):
        """
        Sends then all the joined players. If new players join latter it will also send them
        :return: None
        """
        self.modify()
        join_room(self.game_id)
        for player in self._players:
            emit("user joined", self._players[player])

    def start(self):
        """
        starts the a new game and tells everyone to refresh
        :return: None
        """
        self.modify()
        self.running = True
        self.game = Game(self.game_id, self._players, self, starting_number_of_cards=settings.starting_cards)
        with fs.app.app_context():
            fs.socket_io.emit("refresh", room=self.game_id)

    def make_player_id(self, player_name):
        """
        makes and ID that is unique to itself and is human readable
        """
        id_safe = extended_formatter.format("{player_name!h}_player", player_name=player_name)

        # if its ID is already in use, add a number to it
        if id_safe in self._players:
            num = 2
            while id_safe + "_" + str(num) in self._players:
                num += 1
            id_safe += "_" + str(num)

        return id_safe

    def modify(self):
        self.last_modified = time()

    def get_id(self):
        return self.game_id

    def get_game(self):
        return self.game

    def is_running(self):
        return self.running

    def get_last_modified(self):
        return self.last_modified

