from game import Game
from flask import *
from flask_socketio import *
import flask_server as fs
from time import time
import settings
from player import *
from settings import IntSetting, BoolSetting, OptionSetting
from util.extended_formatter import extended_formatter


class LobbyPlayer:
    """
    Information about a player in a waiting room
    """

    def __init__(self, waiting_room, player_id, name):
        self.waiting_room = waiting_room

        self.player_id = player_id
        self.name = name
        self.wins = 0

        self.sid = None
        self.timeout = 0

    def get_json(self, for_player_id):
        """
        Return Json to be used for the waiting player list
        """

        return {'name': self.name, 'id': self.player_id, 'wins': self.wins, 'is you': self.player_id == for_player_id, 'is host': self.waiting_room.host_id == self.player_id}


class WaitingRoom:
    """
    This stores information about a waiting room
    """

    def __init__(self, game_id):
        # "player_id": name
        self._player_names = {}
        # "player_id": {'sid', 'timeout'}
        self._sessions = {}

        # players
        self._player_ids = []

        # dictionary of player_id: LobbyPlayer
        self._players = {}

        self.running = False
        self.game = None
        self.game_id = game_id
        self.last_modified = time()
        self.settings = [
            OptionSetting('Mid-game joining', 'Request the host',
                          ['Lock', 'Spectate only', 'Request the host', 'Allow']),
            IntSetting('Turn timer', settings.default_turn_timer,
                       settings.min_turn_timer, settings.max_turn_timer),
            OptionSetting('Turn timer consequence', 'Auto play', [
                          'Nothing', 'Sound + Notification', 'Auto play', 'Kick']),
            IntSetting('Maximum players', settings.default_max_players,
                       settings.min_max_players, settings.max_max_players),
            IntSetting('Starting number of cards', settings.default_starting_cards,
                       settings.min_starting_cards, settings.max_card_limit),
            IntSetting('Maximum number of cards', settings.default_card_limit,
                       settings.min_card_limit, settings.max_card_limit)
        ]
        # 1 player is selected host, they are the first person to join. (usually the person to make the game).
        # By default, only the host can change the settings
        self.host_id = None
        self.chosen_settings = {
            setting.name: setting.default_value for setting in self.settings}
        
        self.chosen_settings["Deck frequencies"] = settings.default_dynamic_deck

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
        if session['player_id'] not in self._players:
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
        elif message_type == "kick":
            self._host_kick(data['id'])
        elif message_type == "make host":
            self._make_host(data['id'])
        else:
            print("got unknown message:", message_type, data)

    def render(self):
        """
        render the HTML needed to display the waiting room
        :return:
        """
        self.modify()

        # Get request - when you GET the game
        if request.method == 'GET':

            # Already logged in
            if "player_id" in session and session["player_id"] in self._players:
                if self.running:
                    return self.game.render_game()
                else:
                    return render_template("waiting room.html", waiting_room=self, theme=settings.get_theme())
            # not logged in - send login template if allowed
            else:
                # don't allow login when a game is already running and these options are disabled
                if self.running and self.chosen_settings['Mid-game joining'] == 'Lock':
                    return render_template("index.html", message="You cannot join this game mid-game.", theme=settings.get_theme())

                # login
                return render_template("login.html", theme=settings.get_theme())
        elif request.method == 'POST':
            # don't allow login when a game is already running and these options are disabled
            if self.running and self.chosen_settings['Mid-game joining'] == 'Lock':
                return render_template("index.html", message="You cannot join this game mid-game.", theme=settings.get_theme())

            # successful login
            name = request.form['player_name'][0:10]  # limit to 20 characters
            player_id = self._make_player_id(name)

            self._player_ids.append(player_id)
            self._players[player_id] = LobbyPlayer(self, player_id, name)

            # establish host if this is the first person
            if len(self._players) == 1:
                self.set_host(player_id)

            session['player_id'] = player_id
            # join waiting room
            if self.running is True:
                # mid-game join - game must not be full AND Mid-game joining must be set to allow.
                if self.chosen_settings['Mid-game joining'] == 'Allow' and len(self.game.players) < self.chosen_settings['Maximum players']:
                    self.game.add_new_player(name, player_id)
                # spectate
                else:
                    self.game.add_observer(name, player_id)
            return redirect("/" + self.game_id)
        else:
            return "What the Fuck Did You Just Bring Upon This Cursed Land!"

    def _send_user_list(self):
        """
        Send a list of all users in the waiting room
        """

        for for_player_id in self._player_ids:
            player_list = []

            for player_id in self._player_ids:
                player_list.append(
                    self._players[player_id].get_json(for_player_id))

            with fs.app.app_context():
                fs.socket_io.emit("players", {'is host': self.host_id == for_player_id, 'players': player_list},
                                  room=self._players[for_player_id].sid)

    def _handle_change_setting(self, data):
        """
        Change a setting about the game from data given by the player
        :param data: the message data sent from the client
        :return:
        """
        if data['index'] is None or data['value'] is None:
            return

        # check if host setting lock is enabled and the user is not the host
        if session['player_id'] != self.host_id:
            return

        index = data['index']
        value = data['value']

        setting = self.settings[index]

        if settings.debug_enabled:
            print("Setting " + str(index) + " changed to " + str(value))

        # check if valid
        if not isinstance(value, bool) and isinstance(value, int):
            if index < 0 or index >= len(self.settings):
                return

            # check if within bounds
            if value < setting.min_value or value > setting.max_value:
                return

        # option valid check
        if isinstance(value, str):
            if value not in setting.values:
                return

        # change setting
        self.chosen_settings[setting.name] = value

        # emit
        fs.socket_io.emit("setting changed", {
                          'index': index, 'value': value}, room=self.game_id, include_self=False)

    def _joined_waiting_room(self):
        """
        Sends them all the joined players. If new players join later it will also send them
        :return: None
        """
        self.modify()

        self.set_sid()

        emit("add settings", self._settings_json())

        for index in range(len(self.settings)):
            emit("setting changed", {
                 'index': index, 'value': self.chosen_settings[self.settings[index].name]})
            emit('setting lock', {
                 'lock': session['player_id'] != self.host_id})

        join_room(self.game_id)

        self._send_user_list()

    def _left_waiting_room(self):
        """
        Tells players that a player has left the game.
        Returns the player to the index page 
        :return: None
        """
        self.modify()

        self.leave_room()

        self._send_user_list()

        emit("quit")

    def _host_kick(self, player_id):
        """
        When you try to kick a player in the waiting room
        """
        if session['player_id'] != self.host_id:
            return
        if player_id not in self._players:
            return

        fs.socket_io.emit("quit", room=self._players[player_id].sid)
        self.kick_player(player_id)

    def _make_host(self, player_id):
        """
        When you try to kick a player in the waiting room
        """
        if session['player_id'] != self.host_id:
            return
        if player_id not in self._players:
            return

        # update host
        self.set_host(player_id)

        # unlock settings
        emit('setting lock', {
            'lock': True})
        fs.socket_io.emit(
            "setting lock", {'lock': False}, room=self._players[player_id].sid)

        # update player list
        self._send_user_list()

    def kick_player(self, player_id, message=" has quit the game!"):
        """
        Kick a player from the game after timing out
        """
        # let game handle removing player
        if self.running:
            player = self.game.get_user(player_id)

            self.game.remove_user(player, message)

            self.remove_player(player_id)

        # let waiting room handle removing player
        else:
            self.remove_player(player_id)

            self._send_user_list()

    def add_player_win(self, player_id):
        player = self._players[player_id]
        player.wins += 1

    def remove_player(self, player_id):
        del self._players[player_id]
        self._player_ids.remove(player_id)

    def leave_room(self):
        player_id = session['player_id']

        del session['player_id']
        leave_room(self.game_id)

        self.remove_player(player_id)

        # if this is the host - determine the new host
        if player_id == self.host_id:
            if len(self._players) == 0:
                self.host_id = None
            else:
                # new host - allow them to edit settings
                self.set_host(self._player_ids[0])

                fs.socket_io.emit('setting lock', {
                    'lock': False}, room=self._players[self.host_id].sid)

    def _start(self):
        """
        starts the a new game and tells everyone to refresh
        :return: None
        """
        # only the host can start the game in this instance
        if self.host_id != session["player_id"]:
            return

        self.modify()
        self.running = True

        self.game = Game(self.game_id, [self._players[player_id] for player_id in self._player_ids],
                         self, self.chosen_settings)
        with fs.app.app_context():
            fs.socket_io.emit("refresh", room=self.game_id)

    def _make_player_id(self, player_name):
        """
        makes and ID that is unique to itself and is human readable
        """
        id_safe = extended_formatter.format(
            "{player_name!h}_player", player_name=player_name)

        # if its ID is already in use, add a number to it
        if id_safe in self._player_ids:
            num = 2
            while id_safe + "_" + str(num) in self._player_ids:
                num += 1
            id_safe += "_" + str(num)

        return id_safe

    def kick_inactive_sessions(self, sessions):
        """
        kick players who have exited their tab
        :param sessions: All active sessions
        """

        for player_id in self._players.copy():
            sid = self._players[player_id].sid

            if sid in sessions:
                self._players[player_id].timeout = 0
            else:
                self._players[player_id].timeout += 1

                kick = settings.session_inactivity_kick - \
                    self._players[player_id].timeout

                if kick <= 0:
                    if settings.debug_enabled:
                        print("PLAYER KICKED", player_id)
                    self.kick_player(player_id)

    def set_host(self, player_id):
        self.host_id = player_id

        # move host to front of the list
        if self._player_ids[0] != player_id:
            self._player_ids.remove(player_id)
            self._player_ids.insert(0, player_id)

    def set_sid(self):
        """
        When a new session is established: create a new entry in the sessions dictionary with the session id
        """
        self._players[session['player_id']].sid = request.sid
        self._players[session['player_id']].timeout = 0

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
