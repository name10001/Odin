import flask_server as fs
from cards.card_collection import CardCollection
import settings


class Player:
    def __init__(self, game, name, player_id):
        self.name = name
        self.game = game
        self.player_id = player_id
        self.hand = CardCollection(sort=True)
        self.name = name
        self.sid = None
        self.turns_left = 1
        self.state = "not turn"
        self._play_cards_queue = []  # see self.play_card()

    def play_card(self, card_to_play=None, card_id_to_play=None, chosen_option=None, card_array=None):
        """
        Takes card out of players hand and adds it to the games played cards.
        Also preforms all actions of the card.
        It will only play the card if it is allowed to be played and the option is valid
        You can specify a card by its ID with the card itself.
        Can be called again before previous card(s) have finished being played.
        :param card_to_play: The card to play. Can not be used with card_id_to_play or card_array
        :param card_id_to_play: The ID of the card to play. Can not be used with card_to_play or card_array
        :param chosen_option: The card's chosen option. Can not be used with card_array.
        :param card_array: A 2D array of cards and there options. E.g [[card, option], [card, options], ...]
        You can use ether the card's ID or the card itself.
        Can not be used with card_to_play, card_id_to_play or chosen_option
        :return: None
        """
        # error checking
        ways = (card_array is not None) + (card_to_play is not None) + (card_id_to_play is not None)
        if ways != 1:
            raise ValueError("Exactly one of the following needs to be specified: "
                             "card_to_play, card_id_to_play and card_array. Got: " + ways + " ways")
        if card_array is not None and chosen_option is not None:
            raise ValueError("card_array and chosen_option can not be used together.")

        # add all the cards into card array
        if card_array is None:
            if card_to_play is not None:
                card_array = [[card_to_play, chosen_option]]
            else:
                card_array = [[card_id_to_play, chosen_option]]

        # Go through card_array, if its a valid card add it to cards_to_play and set its options.
        # If its not, raise an error
        cards_to_play = []
        for card, option in card_array:
            if self.hand.contains(card):
                card = self.hand.find_card(card)
                if card is None:
                    raise ValueError("One of the given cards is not valid")
            if card.is_option_valid(self, option):
                card.set_option(option)
                cards_to_play.append(card)

        # add all cards to self.cards_to_play. If self.play_card already running, stop
        was_empty = len(self._play_cards_queue) == 0
        for card in cards_to_play:
            self._play_cards_queue.append(card)
        if was_empty is False:
            return

        # play all the cards
        cards_played = []
        while len(self._play_cards_queue) > 0:
            card = self._play_cards_queue[0]
            if not self._can_be_played(card):
                self._play_cards_queue.pop(0)
                continue

            # do not change order
            self.hand.remove_card(card)
            card.prepare_card(self)
            self.game.planning_pile.add_card(card)
            cards_played.append(card)

            self._play_cards_queue.pop(0)

        # send animation message to all players
        json_to_send = {
            "type": "play cards",
            "data": [
                {
                    "id": card.get_id(),
                    "card image url": card.get_url()
                } for card in cards_played
            ]
        }
        self.game.send_to_all_players("animate", json_to_send)

    def finish_turn(self):
        """
        Call this to finish the players turn
        :return: boolean, False of the player should have another turn
        """
        # checks if cards can be played:
        for card in self.game.planning_pile:
            can_play, reason = card.ready_to_play()
            if can_play is False:
                return False
        # play cards from planing pile
        for card in self.game.planning_pile:
            card.play_card(self)
            self.game.played_cards.add_card(card)

        # if there is a pickup and the player did not play, make them pick it up
        if len(self.game.planning_pile) == 0:
            self.pickup()

        self.game.planning_pile.clear()

        # send wining message to everyone but this player
        if self.had_won():
            self.game.send_to_all_players("popup message", self.name + " has won!")

        # check if player has any more turns left.
        self.turns_left -= 1
        if self.turns_left > 0:
            return False
        else:
            self.state = "not turn"
            self.turns_left = 1
            return True

    def card_update(self):
        """
        Sends all the information to the player to render the game.
        This includes but is not limited to, the players hand, the played cards and other player information
        It is sent in the form of JSON to the client where the information is rendered using javascript
        :return: None
        """
        json_to_send = {
            "cards on deck": [],
            "your cards": [],
            "planning pile": [],
            "direction": self.game.direction,
            "pickup size": self.game.pickup,
            "iteration": self.game.iterate_turn_by,
            "players": [],
            "cant play reason": None,
        }

        # get first 4 cards from deck that are not in planning pile
        for card in self.game.played_cards[-settings.played_cards_to_show:]:
            json_to_send["cards on deck"].append(
                {
                    "card image url": card.get_url(),
                    "card id": card.get_id(),
                    "name": card.get_name(),
                    "card can be undone": False
                }
            )

        # get cards from planning pile
        for card in self.game.planning_pile:
            can_play, reason = card.ready_to_play()
            if can_play is False:
                json_to_send["cant play reason"] = reason
            
            json_to_send["planning pile"].append(
                {
                    "card image url": card.get_url(),
                    "name": card.get_name(),
                    "card id": card.get_id()
                }
            )

        # get player cards
        for card in self.hand:
            json_to_send["your cards"].append(
                {
                    "card id": card.get_id(),
                    "card image url": card.get_url(),
                    "name": card.get_name(),
                    "can be played": self._can_be_played(card),
                    "pick options separately": card.pick_options_separately(),
                    "options": card.get_options(self)
                }
            )

        # get information all players
        for player in self.game.players:
            json_to_send["players"].append(
                {
                    "name": player.get_name(),
                    "number of cards": len(player.hand),
                    "is turn": player.is_turn(),
                    "is you": player == self,
                    "turns left": player.turns_left
                }
            )

        self.send_message("card update", json_to_send)

    def send_message(self, message_type, data):
        """
        Sends the players web browser a message
        :param message_type: e.g. "card update" or "popup message"
        :param data: data to send the client with the message. Can be None
        :return: None
        """
        with fs.app.app_context():
            fs.socket_io.emit(message_type, data, room=self.sid)

    def pickup(self):
        """
        If there is a pickup chain this will pick it up, otherwise it will pickup 1
        only runs if its the players turn
        :return: None
        """
        if self.is_turn() is False:
            return
        if self.game.pickup == 0:
            self.add_new_cards(1)
        else:
            self.add_new_cards(self.game.pickup)
            self.game.pickup = 0

    def undo(self, send_message=True):
        """
        If the player has put down a card this turn it will undo the latest one
        :return:
        """
        if len(self.game.planning_pile) == 0 or not self.is_turn():
            return
        card_to_remove = self.game.planning_pile.get_top_card()
        # do not change order
        self.game.planning_pile.remove_card(card_to_remove)
        card_to_remove.undo_prepare_card(self)
        self.hand.add_card(card_to_remove)

        if send_message is True:
            # send a message to all players
            json_to_send = {
                "type": "undo"
            }

            self.game.send_to_all_players("animate", json_to_send)

    def undo_all(self):
        """
        If the player has put down a card this turn it will undo the latest one
        :return:
        """
        if not self.is_turn():
            return
        for i in range(0, len(self.game.planning_pile)):
            self.undo(False)
        
        # send a message to all players
        json_to_send = {
            "type": "undo all"
        }

        self.game.send_to_all_players("animate", json_to_send)

    def _can_be_played(self, card):
        """
        Can the given card be played right now
        :return:
        """
        top_card = self.game.played_cards[-1]
        is_first_card = len(self.game.planning_pile) == 0

        if self.is_turn() and not is_first_card:
            return card.can_be_played_with(self)
        elif card.can_be_played_on(self, top_card):
            return True
        else:
            return False

    def add_new_cards(self, number, display_pickup=True):
        """
        gets new cards from deck and adds them to hand
        Does not check for pickup chains of weather its the players turn
        if you want that, use pickup(self) instead
        :param number: number of cards to add
        :return: None
        """
        number = min(settings.player_card_limit - len(self.hand), int(number))
        cards = self.game.deck.add_random_cards_to(self.hand, number)

        # send you an animation message to show you picking up the cards
        json_to_send = {
            "type": "pickup",
            "from": None,  # use this same message for picking up cards from other players
            "data": []
        }

        for card in cards:
            json_to_send["data"].append(card.get_url())
        
        self.send_message("animate", json_to_send)

    def had_won(self):
        """
        checks if the player has one, if they have then it returns True.
        :return:
        """
        return len(self.hand) == 0

    def start_turn(self):
        """
        starts the players turn
        :return:
        """
        self.state = "playing turn"

    def set_sid(self, sid):
        self.sid = sid

    def get_sid(self):
        return self.sid

    def get_name(self):
        return self.name

    def get_id(self):
        return self.player_id
    
    def is_turn(self):
        return self.state == "playing turn"
