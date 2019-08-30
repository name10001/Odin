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
        self.settings = {
            "number-of-cards": 25
        }

    def message(self, message_type, data):
        """

        :param message_type: The type of message that
        :param data:
        :return:
        """
        if message_type == "join":
            self._joined_waiting_room()
        elif message_type == "start":
            self._start()
        elif message_type == "setting change":
            self._handle_change_setting(data)
        elif message_type == "quit":
            self._left_waiting_room()
        else:
            print("got unknown message:", message_type, data)

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
                    return render_template("waiting room.html", waiting_room=self, settings=settings)
            else:
                return render_template("login.html")
        elif request.method == 'POST':
            name = request.form['player_name'][0:10]  # limit to 20 characters
            player_id = self._make_player_id(name)
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

    def _handle_change_setting(self, data):
        """
        Change a setting about the game from data given by the player
        :param data: the message data sent from the client
        :return:
        """
        if not isinstance(data, list) or len(data) != 2:
            return

        setting, value = data

        if setting not in self.settings or type(self.settings[setting]) != type(value):
            return

        self.settings[setting] = value

        fs.socket_io.emit("setting changed", [setting, value], room=self.game_id, include_self=False)

    def _joined_waiting_room(self):
        """
        Sends them all the joined players. If new players join later it will also send them
        :return: None
        """
        self.modify()
        for setting in self.settings:
            fs.socket_io.emit("setting changed", [setting, self.settings[setting]])
        join_room(self.game_id)

        for player in self._players:
            if player == session['player_id']:
                emit("user joined", self._players[player] + " (You)")
            else:
                emit("user joined", self._players[player])
    
    def _left_waiting_room(self):
        """
        Tells players that a player has left the game.
        Returns the player to the index page 
        :return: None
        """
        self.modify()

        leave_room(self.game_id)

        player_id = session['player_id']
        name = self._players[player_id]

        del self._players[player_id]

        with fs.app.app_context():
            fs.socket_io.emit("user quit", name, room=self.game_id)

        emit("quit")


    def _start(self):
        """
        starts the a new game and tells everyone to refresh
        :return: None
        """
        self.modify()
        self.running = True
        self.game = Game(self.game_id, self._players, self, starting_number_of_cards=self.settings["number-of-cards"])
        with fs.app.app_context():
            fs.socket_io.emit("refresh", room=self.game_id)

    def _make_player_id(self, player_name):
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

    def get_player(self, player_id):
        """
        checks to see if a player exists in this waiting room
        :param player_id: id of player to look for
        :return: returns the player if found, else None
        """
        if player_id in self._players:
            return self._players[player_id]
        else:
            return None

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

