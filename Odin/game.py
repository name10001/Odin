import cards
from player import Player, Observer
from flask import *
import random
from time import time
from cards.card_collection import CardCollection


class Game:
    """
    This stores information about a game
    """

    def __init__(self, game_id, players, waiting_room, starting_number_of_cards=50):
        """

        :param game_id:
        :param players: A dict of players with the key as player id and the player name as the value
        :param waiting_room:
        :param starting_number_of_cards:
        """
        self.game_id = game_id
        self.waiting_room = waiting_room
        self.starting_number_of_cards = starting_number_of_cards

        self.players = []
        self.observers = []

        # setting up cards
        self.deck = cards.Deck(self)
        self.played_cards = CardCollection()
        self.deck.add_random_cards_to(self.played_cards, 1, dynamic_weights=False)
        self.planning_pile = CardCollection()
        self.pickup = 0

        # setup players and turn system
        if len(players) < 2:
            print("WARNING: 2 or more players are needed to make the game work properly")
        for player in players:
            new_player = Player(self, players[player], player)
            self.players.append(new_player)
            new_player.add_new_cards(self.starting_number_of_cards, False)
        self.player_turn_index = random.randint(0, len(self.players) - 1)
        self.turn = self.players[self.player_turn_index]
        self.turn.start_turn()
        self.direction = 1  # 1 or -1
        self.iterate_turn_by = 1

    def find_card(self, card_id):
        """
        Checks to see if a card exists in this came
        :param card_id: id of card to look for
        :return: returns the card if found, else None
        """
        for card in self.played_cards:
            if card.get_id() == card_id:
                return card
        for player in self.players:
            card = player.hand.find_card(card_id)
            if card is not None:
                return card
        return None

    def get_player(self, player_id):
        """
        Gets the player from this game with the given id
        :param player_id: id of player to look for
        :return: returns the player if found, else None
        """
        for player in self.players:
            if player.get_id() == player_id:
                return player

    def get_user(self, user_id):
        """
        Gets the player or observer from this game with the given id
        :param user_id: id of player or observer to look for
        :return: returns the player if found, else None
        """
        for player in self.players:
            if player.get_id() == user_id:
                return player
        for observer in self.observers:
            if observer.get_id() == user_id:
                return observer

    def render_game(self):
        """
        render the HTML needed to display the game
        :return:
        """
        self.waiting_room.modify()
        return render_template("game.html", game=self, cards=cards)

    def next_turn(self):
        """
        Proceeds to the next player
        :return: None
        """
        # if player has another turn
        is_finished = self.turn.finish_turn()
        if is_finished is False:
            self.update_users()
            return

        # increment player index
        for i in range(0, self.iterate_turn_by):
            self.player_turn_index += self.direction
            if self.player_turn_index == -1:
                self.player_turn_index = len(self.players) - 1
            elif self.player_turn_index == len(self.players):
                self.player_turn_index = 0

        self.iterate_turn_by = 1

        self.turn = self.players[self.player_turn_index]
        self.turn.start_turn()

    def update_users(self, exclude=None):
        """
        Sends updates to all the players and observers in this game
        :return:
        """
        for player in self.players:
            if player != exclude:
                player.card_update()
        for observer in self.observers:
            if observer != exclude:
                observer.card_update()

    def message(self, message, data):
        """
        When a message is sent to a game it comes here then gets sent to all the clients
        :param message: the message to send to the server, e.g. "pickup" or "uno"
        :param data: data that gone along with it, e.g. message="play card", data=("swap_hand_card_15", "Jeff")
        :return: None
        """
        self.waiting_room.modify()
        player = self.get_user(session['player_id'])
        if player is None:
            return

        print(player.get_name(), message, data)

        start_time = time()

        if message == "play card":
            player.play_card(card_id_to_play=data[0])
        elif message == "play cards":
            player.play_card(card_array=data)
        elif message == "finished turn":
            if player == self.turn:
                self.next_turn()
        elif message == "undo":
            player.undo()
        elif message == "undo all":
            player.undo_all()
        elif message == "answer":
            player.answer_question(data)
            return
        else:
            print("got unknown message from player:", message)

        print("processed message, took: " + str(time() - start_time) + "s")
        start_time = time()
        self.update_users()
        print("updated player, took: " + str(time() - start_time) + "s")
    
    def animate_card_transfer(self, cards, cards_from="deck", cards_to="deck"):
        """
        Animate a card being transferred from one place to another
        This method should not be used for custom animations
        Locations:
        - "deck"
        - "discard"
        - player object
        :param cards: list of cards being transferred
        :param cards_from: location where the cards are from
        :param cards_to: location where the cards are going to
        """
        if isinstance(cards_from, Player):
            if isinstance(cards_to, Player):
                # TODO have a separate animation for this (PLAYER TO PLAYER TRANSFER)
                self.animate_card_transfer(cards, cards_from=cards_from)
                self.animate_card_transfer(cards, cards_to=cards_to)
            elif cards_to == "deck":
                # card remove
                json_to_send = {
                    "type": "remove cards",
                    "cards": [
                        {
                            "id": card.get_id(),
                            "card image url": card.get_url()
                        } for card in cards
                    ]
                }
                cards_from.send_message("animate", json_to_send)
                return
            elif cards_to == "discard":
                # card play animation - atm this doesn't even need a player id
                json_to_send = {
                    "type": "play cards",
                    "cards": [
                        {
                            "id": card.get_id(),
                            "card image url": card.get_url()
                        } for card in cards
                    ]
                }

                self.send_to_all_players("animate", json_to_send)
        elif cards_from == "deck":
            if isinstance(cards_to, Player):
                # picking up from the deck
                json_to_send = {
                    "type": "pickup",
                    "from": None,
                    "cards": [{
                        "id": card.get_id(),
                        "name": card.get_name(),
                        "card image url": card.get_url()
                     } for card in cards]
                }
                cards_to.send_message("animate", json_to_send)
            elif cards_to == "discard":
                # elevator card or other similar cards TODO
                return

    def get_top_card(self):
        """
        Gets the top card from the planning pile.
        If there is no card there, then it gets the top card from the played cards pile
        :return:
        """
        if len(self.planning_pile) > 0:
            return self.planning_pile[-1]
        return self.played_cards[-1]

    def get_card_below(self, card):
        card_below = self.planning_pile.card_below(card)
        if card_below is None:
            card_below = self.played_cards.get_top_card()
        return card_below

    def add_observer(self, name, player_id):
        """
        Adds an observer to this game
        :param name: The name of the player to add
        :param player_id: The ID of the player to add
        :return: None
        """
        self.observers.append(Observer(self, name, player_id))

    def get_id(self):
        return self.game_id

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # NETWORKING STUFF

    def send_to_all_players(self, message_type, data):
        for player in self.players:
            player.send_message(message_type, data)

    def initial_connection(self):
        """
        subscribes the player to game updates
        :return: None
        """
        self.waiting_room.modify()
        user = self.get_user(session['player_id'])
        user.initial_connection()
