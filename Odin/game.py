import cards
from player import Player
from flask import *
from flask_socketio import *
import flask_server as fs
import random


class Game:
    """
    This stores information about a game
    """

    def __init__(self, game_id, players):
        self.pickup = 0
        self.played_cards = []
        self.players = []
        self.direction = 1  # 1 or -1
        self.starting_number_of_cards = 100
        self.game_id = game_id
        self.deck = cards.Deck()
        self.skip_next = False
        self.say_uno_needed = False

        for player in players:
            self.players.append(Player(self, players[player], player))
        self.player_turn_index = random.randint(0, len(self.players)-1)
        self.turn = self.players[self.player_turn_index]
        self.played_cards = [self.deck.pickup()(self)]

    def find_card(self, card_id):
        """
        checks to see if a card exists in this came
        :param card_id: id of card to look for
        :return: returns the card if found, else None
        """
        for card in self.played_cards:
            if card.id == card_id:
                return card
        for player in self.players:
            for card in player.get_cards():
                if card.id == card_id:
                    return card
        return None

    def get_player(self, player_id):
        """
        gets a player from this game with the given id
        :param player_id: id of player to look for
        :return: returns the player if found, else None
        :return:
        """
        for player in self.players:
            if player.get_id() == player_id:
                return player

    def render_game(self):
        """
        render the HTML needed to display the game
        :return:
        """
        return render_template("game.html", game=self)

    def next_turn(self):
        """
        proceeds to the next player
        :return: None
        """
        self.turn.finish_turn()

        if self.skip_next is True:
            increment_by = 2
            self.skip_next = False
        else:
            increment_by = 1

        # increment player index
        for i in range(0, increment_by):
            self.player_turn_index += self.direction
            if self.player_turn_index == -1:
                self.player_turn_index = len(self.players) - 1
            elif self.player_turn_index == len(self.players):
                self.player_turn_index = 0

        self.turn = self.players[self.player_turn_index]

        self.update_players()

    def update_players(self):
        """
        sends updates to all the players
        :return:
        """
        for player in self.players:
            player.card_update()

    def message(self, message, data):
        """
        When a message is sent to a game it comes here then gets sent to all the clients
        :param message:
        :param data:
        :return: None
        """
        player = self.get_player(session['player_id'])
        if player is None:
            return

        if message == "uno":
            player.say_uno()
        elif message == "play card":
            player.play_card(data[0], data[1])
        elif message == "finished turn":
            if player == self.turn:
                self.next_turn()
        elif message == "pickup":
            player.pickup()
        elif message == "undo":
            player.undo()
        else:
            print("got unknown message from player:", message)

    def add_played_card(self, card):
        """
        adds a card to the list of played cards and sends message to all game players
        :param card: Card object to add
        :return: None
        """
        self.played_cards.append(card)
        for player in self.players:
            player.card_update()

    def initial_connection(self):
        """

        :return:
        """
        self.get_player(session['player_id']).set_sid(request.sid)
        join_room(self.game_id + "_game")
        self.get_player(session['player_id']).card_update()

    def get_id(self):
        return self.game_id
