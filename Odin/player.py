import cards
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
        self.picked_up_this_turn = False
        self.sid = None
        self.planning_pile = CardCollection()
        self.turns_left = 1
        self.state = "not turn"

    def play_cards(self, cards):
        """
        Takes cards out of players hand and adds it to the games played cards
        Also preforms all actions of the card and checks if its aloud to be played
        :param cards: array of card to play. 2d array. e.g. [["id", "option"], ["id", "option"], etc]
        :return: None
        """
        for card in cards:
            self.play_card(card[0], card[1])
        print("from play cards")
        self.card_update()

    def play_card(self, card_id, chosen_option):
        """
        Takes card out of players hand and adds it to the games played cards
        Also preforms all actions of the card and checks if its aloud to be played
        :param card_id:
        :param chosen_option:
        :return: None
        """
        card = self.hand.find_card(card_id)
        if card is None:
            return
        if self._can_be_played(card):
            self.hand.remove_card(card)
            card.set_option(chosen_option)
            self.planning_pile.add_card(card)

            # get the card below
            card_below = self.planning_pile.card_below(card)
            if card_below is None:
                card_below = self.game.played_cards.get_top_card()

            card.prepare_card(self, card_below, self.planning_pile)

    def finish_turn(self):
        """

        :return: boolean, False of the player should have another turn
        """
        # checks if cards can be played:
        for card in self.planning_pile:
            can_play, reason = card.ready_to_play()
            if can_play is False:
                # TODO: send message to player giving them the reason they cant finish
                print("cant finish turn:", reason)
                return False
        # play cards from planing pile
        for card in self.planning_pile:
            # get the card below
            card_below = self.planning_pile.card_below(card)
            if card_below is None:
                card_below = self.game.played_cards.get_top_card()

            card.play_card(self, card_below, self.planning_pile)

            self.game.played_cards.add_card(card)

        # if there is a pickup and the player did not play, make them pick it up
        if len(self.planning_pile) == 0:
            self.pickup()

        self.planning_pile.clear()

        # send wining message to everyone but this player
        if self.had_won():
            self.game.send_to_all_players("message for player", self.name + " has won!")

        self.picked_up_this_turn = False

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
        print("updating player!")
        json_to_send = {
            "cards on deck": [],
            "your cards": [],
            "planning pile": [],
            "direction": self.game.direction,
            "pickup size": self.game.pickup,
            "iteration": self.game.iterate_turn_by,
            "players": [],
        }

        # get first 4 cards from deck that are not in planning pile
        number_of_cards = len(self.game.played_cards)
        for card_index in range(max(number_of_cards - 4, 0), number_of_cards):
            card = self.game.played_cards[card_index]
            json_to_send["cards on deck"].append(
                {
                    "card image url": card.get_url(),
                    "card id": card.get_id(),
                    "card can be undone": False
                }
            )

        # get cards from planning pile
        for card in self.planning_pile:
            json_to_send["planning pile"].append(
                {
                    "card image url": card.get_url(),
                    "card id": card.get_id()
                }
            )

        # get player cards
        for card in self.hand:
            json_to_send["your cards"].append(
                {
                    "card id": card.get_id(),
                    "card image url": card.get_url(),
                    "can be played": self._can_be_played(card),
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

        # send players client
        with fs.app.app_context():
            fs.socket_io.emit("card update", json_to_send, room=self.sid)

    def pickup(self):
        """
        If there is a pickup chain this will pick it up, otherwise it will pickup 1
        only runs if its the players turn
        :return: None
        """
        if self.picked_up_this_turn is True:
            return
        if self.is_turn() is False:
            return
        if self.game.pickup == 0:
            self.add_new_cards(1)
        else:
            self.add_new_cards(self.game.pickup)
            self.game.pickup = 0
        self.picked_up_this_turn = True

    def undo(self):
        """
        If the player has put down a card this turn it will undo the latest one
        :return:
        """
        if len(self.planning_pile) == 0 or not self.is_turn():
            return
        card_to_remove = self.planning_pile.get_top_card()
        self.planning_pile.remove_card(card_to_remove)
        self.hand.add_card(card_to_remove)

        played_on = self.game.played_cards[len(self.game.played_cards)-1]
        card_to_remove.undo_prepare_card(self, played_on, self.planning_pile)

    def undo_all(self):
        """
        If the player has put down a card this turn it will undo the latest one
        :return:
        """
        if not self.is_turn():
            return
        for i in range(0, len(self.planning_pile)):
            self.undo()

    def _can_be_played(self, card):
        """
        Can the given card be played right now
        :return:
        """
        top_card = self.game.played_cards[-1]
        is_first_card = len(self.planning_pile) == 0

        if self.is_turn() and not is_first_card:
            return card.can_be_played_with(self.planning_pile, self)
        elif card.can_be_played_on(top_card, self):
            return True
        else:
            return False

    def add_new_cards(self, number):
        """
        gets new cards from deck and adds them to hand
        Does not update player
        Does not check for pickup chains of weather its the players turn
        if you want that, use pickup(self) instead
        :param number: number of cards to add
        :return: None
        """
        number = min(settings.player_card_limit - len(self.hand), int(number))
        cards_to_add = [card(self.game) for card in self.game.deck.pickup(number)]
        self.hand.add_cards(cards_to_add)

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

    # def is_uno(self):
    #    return self.said_uno_previous_turn or self.said_uno_this_turn

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
