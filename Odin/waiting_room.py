from game import Game
from flask import *
from flask_socketio import *
import flask_server as fs
from time import time
import settings
from settings import IntSetting
from util.extended_formatter import extended_formatter


class WaitingRoom:
    """
    This stores information about a waiting room
    """

    def __init__(self, game_id):
        # "player_id": name
        self._player_names = {}
        # "player_id": sid
        self._sessions = {}
        self.running = False
        self.game = None
        self.game_id = game_id
        self.last_modified = time()
        self.settings = [
            IntSetting('Starting number of cards', 25,
                       settings.min_player_card_limit, settings.max_player_card_limit),
            IntSetting('Maximum number of cards', 500,
                       settings.min_max_player_card_limit, settings.max_player_card_limit)
        ]
        self.chosen_settings = {setting.name: setting.default_value for setting in self.settings}

    def _settings_json(self):
        return [setting.to_json(index) for index, setting in enumerate(self.settings)]

    def message(self, message_type, data):
        """

        :param message_type: The type of message that
        :param data:
        :return:
        """

        # check that the message is coming from a valid session
        if "player_id" not in session:
            return
        if session['player_id'] not in self._player_names:
            # this usually occurs when the player was kicked
            return

        # parse message
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
            if "player_id" in session and session["player_id"] in self._player_names:
                if self.running:
                    return self.game.render_game()
                else:
                    return render_template("waiting room.html", waiting_room=self)
            else:
                return render_template("login.html")
        elif request.method == 'POST':
            name = request.form['player_name'][0:10]  # limit to 20 characters
            player_id = self._make_player_id(name)
            self._player_names[player_id] = name
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
        if data['index'] is None or data['value'] is None:
            return

        index = data['index']
        value = data['value']

        # check if valid
        if not isinstance(value, int):
            return
        if index < 0 or index >= len(self.settings):
            return

        setting = self.settings[index]

        # check if within bounds
        if value < setting.min_value or value > setting.max_value:
            return
        
        # change setting
        self.chosen_settings[setting.name] = value

        # emit
        fs.socket_io.emit("setting changed", {'index': index, 'value': value}, room=self.game_id, include_self=False)

    def _joined_waiting_room(self):
        """
        Sends them all the joined players. If new players join later it will also send them
        :return: None
        """
        self.modify()

        self.set_sid()

        emit("add settings", self._settings_json())

        for index in range(len(self.settings)):
            emit("setting changed", {'index': index, 'value': self.chosen_settings[self.settings[index].name]})

        join_room(self.game_id)

        for player in self._player_names:
            if player == session['player_id']:
                emit("user joined", self._player_names[player] + " (You)")
            else:
                emit("user joined", self._player_names[player])

    def _left_waiting_room(self):
        """
        Tells players that a player has left the game.
        Returns the player to the index page 
        :return: None
        """
        self.modify()

        player_id = session['player_id']
        name = self._player_names[player_id]

        self.leave_room()

        with fs.app.app_context():
            fs.socket_io.emit("user quit", name, room=self.game_id)

        emit("quit")

    def kick_player(self, player_id):
        """
        Kick a player from the game after timing out
        """
        # let game handle removing player
        if self.running:
            player = self.game.get_user(player_id)
            self.game.send_to_all_players(
                "popup message", player.get_name() + " has quit the game!")

            del self._player_names[player_id]
            del self._sessions[player_id]

            self.game.remove_player(player)

        # let waiting room handle removing player
        else:
            name = self._player_names[player_id]

            fs.socket_io.emit("user quit", name, room=self.game_id)

            del self._player_names[player_id]
            del self._sessions[player_id]

    def leave_room(self):
        player_id = session['player_id']

        del session['player_id']
        leave_room(self.game_id)

        del self._player_names[player_id]
        del self._sessions[player_id]

    def _start(self):
        """
        starts the a new game and tells everyone to refresh
        :return: None
        """
        self.modify()
        self.running = True
        self.game = Game(self.game_id, self._player_names, self,
                         starting_number_of_cards=self.chosen_settings['Starting number of cards'], max_cards=self.chosen_settings['Maximum number of cards'])
        with fs.app.app_context():
            fs.socket_io.emit("refresh", room=self.game_id)

    def _make_player_id(self, player_name):
        """
        makes and ID that is unique to itself and is human readable
        """
        id_safe = extended_formatter.format(
            "{player_name!h}_player", player_name=player_name)

        # if its ID is already in use, add a number to it
        if id_safe in self._player_names:
            num = 2
            while id_safe + "_" + str(num) in self._player_names:
                num += 1
            id_safe += "_" + str(num)

        return id_safe

    def set_sid(self):
        """
        When a new session is established: create a new entry in the sessions dictionary with the session id
        """
        self._sessions[session['player_id']] = {
            'sid': request.sid, 'timeout': 0}

    def get_sessions(self):
        return self._sessions

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
