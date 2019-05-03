import flask_server as fs
from cards.card_collection import CardCollection
import cards
import settings
from eventlet import event
from flask import request
import textwrap


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
        self._play_cards_stack = []  # see self.play_card()
        self.player_pickup_amount = 0  # 

        # setting up question stuff see self.ask()
        self._answer_event = None
        self._question = None

        # animation stuff
        self._cards_played_to_animate = []  # animate all the cards either before a question is asked or at the end of the play_card method
        self._cards_finished_to_animate = []

    def play_card(self, card_to_play=None, card_id_to_play=None, card_array=None):
        """
        Takes card out of players hand and adds it to the games played cards.
        Also preforms all actions of the card.
        It will only play the card if it is allowed to be played
        You can specify a card by its ID with the card itself.
        Can be called again before previous card(s) have finished being played.
        :param card_to_play: The card to play. Can not be used with card_id_to_play or card_array
        :param card_id_to_play: The ID of the card to play. Can not be used with card_to_play or card_array
        :param card_array: An array of cards.
        You can use ether the card's ID or the card itself.
        Can not be used with card_to_play, card_id_to_play
        :return: None
        """
        # error checking
        ways = (card_array is not None) + (card_to_play is not None) + (card_id_to_play is not None)
        if ways != 1:
            raise ValueError("Exactly one of the following needs to be specified: "
                             "card_to_play, card_id_to_play and card_array. Got: " + ways + " ways")

        # add all the cards into card array
        if card_array is None:
            if card_to_play is not None:
                card_array = [card_to_play]
            else:
                card_array = [card_id_to_play]

        # Go through card_array, if its a valid card add it to cards_to_play.
        # If its not, raise an error
        cards_to_play = []
        for card in card_array:
            # check if its a card id
            if self.hand.contains(card):
                card = self.hand.find_card(card)
                if card is None:
                    raise ValueError("One of the given card IDs cant be found in the players hand")
            if not isinstance(card, cards.AbstractCard):
                raise ValueError("One of the given cards is not valid")
            if self.hand.contains(card.get_id()):
                cards_to_play.append(card)
            else:
                raise ValueError("One of the given cards cant be found in the players hand")

        # add all cards to self.cards_to_play. If self.play_card already running, stop
        was_empty = len(self._play_cards_stack) == 0
        for card in cards_to_play:
            self._play_cards_stack.append(card)
        if was_empty is False:
            return

        # play all the cards
        try:
            while len(self._play_cards_stack) > 0:
                index = len(self._play_cards_stack) - 1
                card = self._play_cards_stack[index]

                if not self._can_be_played(card):
                    self._play_cards_stack.pop(index)
                    continue

                # do not change order
                self.hand.remove_card(card)
                card.prepare_card(self)
                self.game.planning_pile.add_card(card)
                self._cards_played_to_animate.append(card)

                self._play_cards_stack.pop(index)
        finally:
            self._play_cards_stack.clear()
            self.game.animate_card_transfer(self._cards_played_to_animate, cards_from=self, cards_to="planning")
            self._cards_played_to_animate.clear()
    
    def refresh_card_play_animation(self):
        """
        Whenever an animation or question is asked, update the card play animation so the player can see what card is on top and what is left
        """
        # send play cards animation before you send the options
        if len(self._cards_played_to_animate) > 0:
            self.game.animate_card_transfer(self._cards_played_to_animate, cards_from=self, cards_to="planning")
            self._cards_played_to_animate.clear()
        if len(self._cards_finished_to_animate) > 0:
            self.game.animate_card_transfer(self._cards_finished_to_animate, cards_from="planning", cards_to="discard")
            self._cards_finished_to_animate.clear()


    def ask(self, title, options, options_type="buttons", number_to_pick=1, allow_cancel=True, image=None):
        """
        Asks the player a question. This can be done at any time.
        :param title: The title of the question or the question itself. E.g. "Pick a card"
        :param options: The choices to give the player.
        This can be a dictionary, list, set or CardCollection or anything iterable.
        If its a directory the value is what to shown the player and the key is what gets returned.
        If its a set or list, the items are what is shown to the player and what get returned.
        If its a card collection, an images of the cards is what the player sees and the card_id(s) is whats returned.
        :param options_type: The type of choice. Available types are "buttons", "vertical scroll" and "cards".
        "Buttons" shows a list of buttons without a scroll
        "Cards" shows a list of cards
        "vertical scroll" shows a list of buttons with a scrollbar
        :param number_to_pick: The number of choices to pick. Usual 1
        :param allow_cancel: Should the player be allowed to cancel the question. If they do, None is returned
        :param image: An image url to go along with the question.
        If this is being called from a card, the cards image is a good thing to put here.
        :return: A List of the chosen choices or the choice itself if number_to_pick is 0.
        E.g. "Blue_Six_card_12345" or "server" or ["Green_Two_card_54321", "Blue_Pickup_2_card_56443", ...]
        It will return None if and only if the player cancels
        """

        title = textwrap.fill(title, 25)
    
        options_as_dict = {}

        # convert everything to a dict
        if isinstance(options, dict):
            options_as_dict = options
        elif options_type == "cards":
            for card in options:
                # TODO: once implemented in front change "card.get_name()" to "card.get_url()"
                options_as_dict[card.get_id()] = card.get_name()
        elif isinstance(options, CardCollection):
            for card in options:
                options_as_dict[card.get_id()] = card.get_name()
        else:
            for item in options:
                options_as_dict[item] = item

        # send play cards animation before you send the options
        self.refresh_card_play_animation()

        # generate json for question
        self._question = {
            "title": str(title),
            "number to pick": int(number_to_pick),
            "type": options_type,
            "options": options_as_dict,
            "allow cancel": allow_cancel,
            "image": str(image)
        }

        # send the question and wait for a reply. If the reply is not valid, send it again
        valid_answer = False
        question_answer = None
        while valid_answer is False:
            self.send_message("ask", self._question)

            self._answer_event = event.Event()
            question_answer = self._answer_event.wait()

            valid_answer = len(question_answer) == number_to_pick
            for choice in question_answer:
                if choice not in self._question['options'] or (choice is None and allow_cancel is True):
                    valid_answer = False
                    break

        # clear the question
        self._question = None

        if number_to_pick == 1:
            return question_answer[0]
        else:
            return question_answer

    def answer_question(self, question_answer):
        """
        This will answer the current question with the given answer
        :param question_answer: An array of the players chosen choices for the current question
        :return: None
        """
        if self._answer_event is not None:
            self._answer_event.send(question_answer)

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
            self._cards_finished_to_animate.append(card)
            card.play_card(self)
            self.game.played_cards.add_card(card)
        
        if len(self._cards_finished_to_animate) > 0:
            self.game.animate_card_transfer(self._cards_finished_to_animate, cards_from="planning", cards_to="discard")
            self._cards_finished_to_animate.clear()

        # if there is a pickup and the player did not play, make them pick it up
        if len(self.game.planning_pile) == 0:
            self.pickup()

        self.game.planning_pile.clear()

        for player in self.game.players:
            player.player_pickup_amount = 0

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
            "player type": type(self).__name__
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
                    # TODO: remove the following. Can be done once client no longer uses them
                    "pick options separately": False,
                    "options": None
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
                    "turns left": player.turns_left,
                    "pickup amount": player.player_pickup_amount
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
        :param display_pickup: if there should be an animation sent
        :return: None
        """
        number = min(settings.player_card_limit - len(self.hand), int(number))
        cards = self.game.deck.add_random_cards_to(self.hand, number)

        if display_pickup is False:
            return

        self.game.animate_card_transfer(cards, cards_to=self)

    def initial_connection(self):
        self.set_sid(request.sid)
        self.card_update()
        if self._question is not None:
            self.send_message("ask", self._question)

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


class Observer (Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hand.clear()

    def start_turn(self, *args, **kwargs):
        pass

    def add_new_cards(self, *args, **kwargs):
        pass

    def play_card(self, *args, **kwargs):
        pass

    def finish_turn(self, *args, **kwargs):
        pass

    def pickup(self, *args, **kwargs):
        pass

    def undo(self, *args, **kwargs):
        pass

    def undo_all(self, *args, **kwargs):
        pass

    def had_won(self, *args, **kwargs):
        return False

    def is_turn(self, *args, **kwargs):
        return False
