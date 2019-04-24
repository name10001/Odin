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
    
    def play_cards(self, data):
        """
        Plays a list of cards as given by a message
        Sends a list of all the successfully played cards to all players to show an animation
        """
        played_cards = []
        for card_data in data:
            card = self.play_card(card_data[0], card_data[1])
            if card is not None:
                played_cards.append(card)
        
        # send a message to all players
        json_to_send = {
            "type": "play cards",
            "data": []
        }

        for card in played_cards:
            json_to_send["data"].append({
                "id": card.get_id(),
                "card image url": card.get_url()
            })
        
        self.game.send_to_all_players("animate", json_to_send)


    def play_card(self, card_id, chosen_option):
        """
        Takes card out of players hand and adds it to the games played cards
        Also preforms all actions of the card and checks if its allowed to be played
        :param card_id:
        :param chosen_option:
        :return: Returns the card object that was played
        """
        card = self.hand.find_card(card_id)
        if card is None:
            return None
        
        if self._can_be_played(card):
            # do not change order
            self.hand.remove_card(card)
            card.set_option(chosen_option)
            card.prepare_card(self)
            self.game.planning_pile.add_card(card)
            return card
        return None
        
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

    def add_new_cards(self, number):
        """
        gets new cards from deck and adds them to hand
        Does not check for pickup chains of weather its the players turn
        if you want that, use pickup(self) instead
        :param number: number of cards to add
        :return: None
        """
        number = min(settings.player_card_limit - len(self.hand), int(number))
        self.game.deck.add_random_cards_to(self.hand, number)

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
