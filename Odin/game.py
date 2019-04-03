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
        self.players = {}
        self._direction = 1  # 1 or -1
        self.running = False
        self.starting_number_of_cards = 10
        self.game_id = game_id
        self.deck = cards.Deck()
        for player in players:
            self.players[player] = Player(self, players[player], player)
        self.turn = random.choice(list(self.players.values()))
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
            for card in self.players[player].get_cards():
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
        if player_id in self.players:
            return self.players[player_id]
        else:
            return None

    def render_game(self):
        """
        render the HTML needed to display the game
        :return:
        """
        return render_template("game.html", game=self)

    def message(self, message, data):
        """
        When a message is sent to a game it comes here then gets sent to all the clients
        :param message:
        :param data:
        :return: None
        """
        print(self.played_cards)
        player = self.get_player(session['player_id'])
        if message == "uno":
            player.say_uno()
        elif message == "play card":
            player.play_card(data[0], data[1])
        elif message == "finished turn":
            pass
        else:
            print("got unknown message from player:", message)
        print(self.played_cards)

    def add_played_card(self, card):
        """
        adds a card to the list of played cards and sends message to all game players
        :param card: Card object to add
        :return: None
        """
        self.played_cards.append(card)
        for player in self.players.values():
            player.card_update()

    def initial_connection(self):
        self.get_player(session['player_id']).set_sid(request.sid)
        join_room(self.game_id + "_game")
        self.get_player(session['player_id']).card_update()

    def get_id(self):
        return self.game_id
