import cards
from player import Player, Observer
from flask import *
from flask_socketio import leave_room
import random
from time import time
from cards.deck import AbstractDeck, WeightedDeck
from cards.card_collection import CardCollection
import settings


class AbstractGame:
    """
    Defines how a game should behave and implements some methods that do not depend on any front-end implementation.
    """

    def __init__(self, max_cards=settings.default_card_limit):
        """
        Initializes the game.

        No players or cards are dealt.
        """
        self.players = []

        self.deck = AbstractDeck()
        self.played_cards = CardCollection()
        self.planning_pile = CardCollection()

        self.max_cards = max_cards

        self.pickup = 0
        self.direction = 1  # 1 or -1
        self.iterate_turn_by = 1

        self.player_turn_index = 0

        self.inactivity = 0

    def get_turn(self):
        """
        Get the player who is taking their turn right now
        """
        return self.players[self.player_turn_index]

    def next_turn(self):
        """
        Proceeds to the next player
        :return: None
        """

        # increment player index
        self.player_turn_index += self.direction * self.iterate_turn_by
        self.player_turn_index %= len(self.players)

        self.iterate_turn_by = 1

        self.start_turn()
        self.update_users()

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
        """
        Gets the card below the given card in the planning pile/played cards pile.
        :param card: must be in the planning pile, or this will just return the top card.
        """
        card_below = self.planning_pile.card_below(card)
        if card_below is None:
            card_below = self.played_cards.get_top_card()
        return card_below

    def get_player(self, player_id):
        """
        Gets the player from this game with the given id
        :param player_id: id of player to look for
        :return: returns the player if found, else None
        """
        for player in self.players:
            if player.get_id() == player_id:
                return player

    def add_player(self, player):
        """
        Append a new player object to the list of players
        """
        self.players.append(player)

    def remove_player(self, player):
        """
        Removes a player from the game
        :param player: the player to remove
        :return: None
        """

        # adjust current player index to fit with removed player
        player_index = self.players.index(player)
        if player.playing_as is not None:
            player_index = self.players.index(player.playing_as)

        if player_index < self.player_turn_index or (player_index == self.player_turn_index and self.direction == 1):
            self.player_turn_index -= 1

        # remove the player
        self.players.remove(player)

        # end the game if this was the only player
        if len(self.players) == 0:
            self.end_game()
        # continue the game without that player
        else:
            # if the player is being possessed right now, change the possessor playing_as to be None
            if len(player.possessions) > 0:
                player.possessions[0].playing_as = None

            # remove all possessions caused by this player
            for other_player in self.players:
                i = 0
                while i < len(other_player.possessions):
                    if other_player.possessions[i] == player:
                        other_player.possessions.pop(i)
                    else:
                        i += 1

            if player.playing_as is not None:
                player = player.playing_as

            # check if the player is having their turn right now and move to the next player
            if player.is_turn():
                player.undo_all()  # undo all cards because they left

                self.player_turn_index += self.direction
                self.player_turn_index %= len(self.players)

                self.start_turn()

            self.update_users()

    def start_turn(self):
        """
        Begin the next player's turn
        """
        self.get_turn().start_turn()

    def check_winner(self):
        """
        Check if someone has won the game. If more than one player has one then a tie occurs.
        """

        winners = []

        for player in self.players:
            if player.had_won():
                winners.append(player)

        if len(winners) == 1:
            self.end_game(winner=winners[0])
        elif len(winners) > 1:
            self.end_game(winners=winners)

    def undo(self):
        """
        Undo the top prepared card
        """
        self.get_turn().undo()
        self.get_turn().show_undo()
        self.update_users()

    def undo_all(self):
        """
        Undo all prepared cards
        """
        self.get_turn().undo_all()
        self.get_turn().show_undo_all()
        self.update_users()

    def play_cards(self, cards):
        """
        Prepare an arrary of cards
        """
        self.get_turn().prepare_cards(cards)
        self.update_users()

    def finish_turn(self):
        """
        Finish the current player's turn
        """
        self.get_turn().finish_turn()
        self.update_users()

    def end_game(self, winner=None, winners=None):
        pass

    def update_users(self, exclude=None):
        pass

    def animate_card_transfer(self, cards, cards_from="deck", cards_to="deck"):
        pass

    def send_animation(self, json_to_send):
        pass

    def __str__(self):
        game_str = "GAME (" + str(len(self.players)) + "players)\n"

        for player in self.players:
            game_str += str(player) + '\n'

        game_str += "Turn: " + self.get_turn().get_name() + " Iteration: " + \
            str(self.iterate_turn_by) + '\n'
        game_str += "Pickup: " + str(self.pickup) + \
            " Direction: " + str(self.direction)

        return game_str


class Game(AbstractGame):
    """
    A regular game of Odin.
    It has a game ID and waiting room.
    Everyone is dealt random cards from a given starting amount.

    """

    def __init__(self, game_id, players, waiting_room, settings):
        """
        :param game_id: The ID of the game.
        :param players: A dict of players with the key as player id and the player name as the value.
        :param waiting_room: The waiting room that the game was made in.
        :param starting_number_of_cards: The number of cards each player starts with.
        """
        super().__init__(max_cards=settings['Maximum number of cards'])

        self.game_id = game_id
        self.waiting_room = waiting_room
        self.settings = settings
        self.starting_number_of_cards = settings['Starting number of cards']
        self.turn_timer = settings['Turn timer']
        self.chat = []

        self.observers = []

        # setting up cards
        self.deck = WeightedDeck(self)
        top_card = self.deck.get_next_card(
            {"card collection": None, "elevator": None})(self)

        self.played_cards.add_card(top_card)

        # setup players and turn system
        if len(players) < 2:
            print("WARNING: 2 or more players are needed to make the game work properly")
        for player in players:
            new_player = Player(self, players[player], player)
            self.players.append(new_player)
            new_player.pickup(self.starting_number_of_cards, show_pickup=False)
        self.player_turn_index = random.randint(0, len(self.players) - 1)

        self.start_turn()

    def find_card(self, card_id):
        """
        Checks to see if a card exists in this game
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

        return None

    def render_game(self):
        """
        render the HTML needed to display the game
        :return:
        """
        self.waiting_room.modify()
        return render_template("game.html", game=self, cards=cards, theme=settings.get_theme())

    def update_users(self, exclude=None):
        """
        Sends updates to all the players and observers in this game
        :return:
        """
        start_time = time()
        for player in self.players:
            if player != exclude:
                player.card_update()
        for observer in self.observers:
            if observer != exclude:
                observer.card_update()
        if settings.debug_enabled:
            print("Card update, took: " + str(time() - start_time) + "s")
            print(str(self))

    def message(self, message, data):
        """
        When a message is sent to a game it comes here then gets sent to all the clients
        :param message: the message to send to the server, e.g. "pickup" or "uno"
        :param data: data that gone along with it, e.g. message="play card", data=("swap_hand_card_15", "Jeff")
        :return: None
        """
        self.waiting_room.modify()

        if message == "initialise":
            self.initial_connection()
            return

        # Game user messages from here and below
        player = self.get_user(session['player_id'])
        if player is None:
            return

        # stop a player from having their turn if they're possessed
        if len(player.possessions) > 0 and player.is_turn() and message != "quit":
            if settings.debug_enabled:
                print(player.get_id(), "tried to play but is possessed.")
            return

        if settings.debug_enabled:
            print(player.get_name(), message, data)  # for debugging

        if player.is_turn() and message != "chat":
            # reset inactivity - chat counts as inactivity.
            self.inactivity = 0


        if message == "answer":
            player.answer_question(data)
        elif message == "quit":
            player.send_message("quit", None)

            self.waiting_room.leave_room()

            self.remove_user(player)
        elif message == "chat":
            self.send_chat_message(player.get_name(), data)
        else:
            # override player due to possession
            if player.playing_as is not None:
                player = player.playing_as

            if player != self.get_turn():
                print("got message from player, but it is not their turn.")
            elif message == "play cards":
                self.play_cards(data)
            elif message == "finished turn":
                self.finish_turn()
            elif message == "undo":
                self.undo()
            elif message == "undo all":
                self.undo_all()
            else:
                print("got unknown message from player:", message)

    def send_chat_message(self, player_name, message):
        data = {"player": player_name, "message": message if len(
            message) <= 256 else message[:256]}
        self.send_to_all_users("chat", data)
        self.chat.append(data)
        if len(self.chat) > 100:
            self.chat.pop(0)

    def animate_card_transfer(self, cards, cards_from="deck", cards_to="deck"):
        """
        Animate a card being transferred from one place to another
        This method should not be used for custom animations
        Locations:
        - "deck"
        - "planning"
        - "discard"
        - player object
        :param cards: list of cards being transferred
        :param cards_from: location where the cards are from
        :param cards_to: location where the cards are going to
        """
        if isinstance(cards_from, Player):
            if isinstance(cards_to, Player):
                # Player to player transfer
                remove_message = {  # remove
                    "type": "remove cards",
                    "to": cards_to.get_id(),
                    "cards": [
                        {
                            "id": card.get_id(),
                            "name": card.get_name(),
                            "url": card.get_url()
                        } for card in cards
                    ]
                }
                pickup_message = {  # pickup
                    "type": "pickup",
                    "from": cards_from.get_id(),
                    "cards": [
                        {
                            "id": card.get_id(),
                            "name": card.get_name(),
                            "url": card.get_url()
                        } for card in cards
                    ]
                }
                transfer_message = {  # everyone else
                    "type": "player pickup",
                    "from": cards_from.get_id(),
                    "player": cards_to.get_id(),
                    "count": len(cards)
                }

                for player in self.get_users():
                    if player is cards_from:
                        player.send_animation(remove_message)
                    elif player is cards_to:
                        player.send_animation(pickup_message)
                    else:
                        player.send_animation(transfer_message)
            elif cards_to == "deck":
                # REMOVE CARDS
                remove_message = {
                    "type": "remove cards",
                    "to": None,
                    "cards": [
                        {
                            "id": card.get_id(),
                            "name": card.get_name(),
                            "url": card.get_url()
                        } for card in cards
                    ]
                }

                transfer_message = {
                    "type": "player remove cards",
                    "to": None,
                    "player": cards_from.get_id(),
                    "count": len(cards)
                }

                for player in self.get_users():
                    if player is cards_from:
                        player.send_animation(remove_message)
                    else:
                        player.send_animation(transfer_message)

            elif cards_to == "planning":
                # card prepare animation from player
                json_to_send = {
                    "type": "play cards",
                    "from deck": False,
                    "cards": [
                        {
                            "id": card.get_id(),
                            "name": card.get_name(),
                            "url": card.get_url()
                        } for card in cards
                    ]
                }

                self.send_to_all_users("animate", json_to_send)
        elif cards_from == "deck":
            if isinstance(cards_to, Player):
                # PICKUP
                pickup_message = {
                    "type": "pickup",
                    "from": None,
                    "cards": [{
                        "id": card.get_id(),
                        "name": card.get_name(),
                        "url": card.get_url()
                    } for card in cards]
                }

                transfer_message = {
                    "type": "player pickup",
                    "from": None,
                    "player": cards_to.get_id(),
                    "count": len(cards)
                }

                for player in self.get_users():
                    if player is cards_to:
                        player.send_animation(pickup_message)
                    else:
                        player.send_animation(transfer_message)

            elif cards_to == "planning":
                # card prepare animation from the deck
                json_to_send = {
                    "type": "play cards",
                    "from deck": True,
                    "cards": [
                        {
                            "id": card.get_id(),
                            "name": card.get_name(),
                            "url": card.get_url()
                        } for card in cards
                    ]
                }

                self.send_to_all_users("animate", json_to_send)
        elif cards_from == "planning":
            if cards_to == "discard":
                # card play animation - from prepare to discard pile
                json_to_send = {
                    "type": "finish cards",
                    "cards": [
                        {
                            "id": card.get_id(),
                            "name": card.get_name(),
                            "url": card.get_url()
                        } for card in cards
                    ]
                }

                self.send_to_all_users("animate", json_to_send)

        self.update_players()

    def update_players(self):
        """
        A smaller card_update method which only updates the details about players and current effects in action.

        The cost saving is due to not sending the cards again.

        Send to everyone
        """
        json_to_send = {
            "direction": self.direction,
            "pickup size": self.pickup,
            "iteration": self.iterate_turn_by,
            "players": []
        }

        for player in self.players:
            json_to_send["players"].append(player.get_player_json())

        self.send_to_all_users("card update", json_to_send)

    def send_animation(self, json_to_send):
        self.send_to_all_users("animate", json_to_send)

    def remove_user(self, player, message=" has quit the game!"):
        if not isinstance(player, Observer):
            self.send_to_all_users(
                "popup message", player.get_name() + message)
            self.remove_player(player)
        else:
            self.observers.remove(player)

    def get_users(self):
        """
        Get a list of all users including observers
        """
        users = []
        for player in self.players:
            users.append(player)
        for observer in self.observers:
            users.append(observer)

        return users

    def end_game(self, winner=None, winners=None):
        """
        Finish the game and return to the lobby

        TODO add end screen

        :return: None
        """

        if winner is not None:
            self.send_to_all_users(
                "popup message", winner.name + " has won!")
        elif winners is not None:
            for winner in winners:
                self.send_to_all_users(
                    "popup message", winner.name + " has won!")

        self.waiting_room.running = False
        self.waiting_room.game = None

        self.send_to_all_users("refresh", None)

    def add_new_player(self, name, player_id):
        """
        Adds a player into the game
        :param name: The name of the player to add
        :param player_id: The ID of the player to add
        :return: None
        """

        player = Player(self, name, player_id)

        player.pickup(self.starting_number_of_cards, False)
        self.add_player(player)

        self.update_players()

    def add_observer(self, name, player_id):
        """
        Adds an observer to this game
        :param name: The name of the player to add
        :param player_id: The ID of the player to add
        :return: None
        """
        self.observers.append(Observer(self, name, player_id))

    def turn_countdown(self):
        """
        Countdown the inactivity, activative the consequence once the timer reaches the timer amount
        """
        self.inactivity += 1
        print("Inactivity time: " + str(self.inactivity))

        if self.inactivity == self.turn_timer:
            consequence = self.settings['Turn timer consequence']
            # play a sound and show a message
            if consequence == "Sound + Notification":
                player = self.get_turn()
                if len(player.possessions) > 0:
                    player = player.possessions[0]
                
                player.send_animation({"type": "sound", "sound": "/static/sounds/hurry_up.mp3"});
                player.send_message("popup message", "Hurry up! You are taking too long!");

            # kick the player
            elif consequence == "Kick":
                self.inactivity = 0
                player = self.get_turn()
                if len(player.possessions) > 0:
                    player = player.possessions[0]
                
                player.send_message("quit", None)
                self.waiting_room.kick_player(player.get_id(), message=" was kicked for taking too long!")
            # auto-play
            elif consequence == "Auto play":
                self.inactivity = 0

                player = self.get_turn()
                if len(player.possessions) > 0:
                    player = player.possessions[0]
                
                if player.is_question_active():
                    # answer question
                    player.auto_answer_question()
                else:
                    # play cards
                    self.get_turn().auto_play_and_finish()

    def get_id(self):
        return self.game_id

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # NETWORKING STUFF

    def send_to_all_users(self, message_type, data):
        """
        Send to all players, including observers
        """
        for player in self.players:
            player.send_message(message_type, data)
        for observer in self.observers:
            observer.send_message(message_type, data)

    def initial_connection(self):
        """
        subscribes the player to game updates
        :return: None
        """
        self.waiting_room.modify()

        self.waiting_room.set_sid()
        user = self.get_user(session['player_id'])
        if user is not None:
            user.initial_connection()
