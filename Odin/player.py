import flask_server as fs
from cards.card_collection import CardCollection
import cards
import settings
from eventlet import event
from flask import request
import textwrap


class AbstractPlayer:
    """
    Abstraction for a player which contains most methods a player should be able to do.

    Note that all instances of "game" in this class must only use methods and fields from the AbstractGame class.
    """

    def __init__(self, game, name, player_id):
        self.name = name
        self.game = game
        self.player_id = player_id
        self.hand = CardCollection(sort=True)

        self.possessions = []
        self.effects = []

        self.playing_as = None
        self.state = "not turn"
        self._play_cards_stack = []  # see self.play_card()
        # Shows how many cards this player will pick up at the end of their turn
        self.player_pickup_amount = 0

    def start_turn(self):
        """
        starts the players turn
        :return:
        """
        self.state = "playing turn"

        # if possessed - let person possessing you have your turn
        if len(self.possessions) > 0:
            possession = self.possessions[0]
            possession.playing_as = self

        # Apply all effects
        for effect in self.effects:
            effect.begin_turn()

    def prepare_cards(self, card_array):
        """
        Play an array of cards in order.
        :param card_array: an array of all cards to play in order by their id
        """

        # Check that the cards supplied in card_array are contained within this player's hand, and build a new array of card objects.
        cards_to_play = []
        for card in card_array:
            # check if its a card id
            if self.hand.contains(card):
                card = self.hand.find_card(card)
                if card is None:
                    raise ValueError(
                        "One of the given card IDs cant be found in the players hand")
            if not isinstance(card, cards.AbstractCard):
                raise ValueError("One of the given cards is not valid")
            if self.hand.contains(card.get_id()):
                cards_to_play.append(card)
            else:
                raise ValueError(
                    "One of the given cards cant be found in the players hand")

        # Add cards to the stack of cards being prepared right now, exit this method to avoid issues with concurrency if other cards are already being played.
        was_empty = len(self._play_cards_stack) == 0
        for card in cards_to_play:
            self._play_cards_stack.append(card)
        if was_empty is False:
            return

        # prepare all the cards
        while len(self._play_cards_stack) > 0:
            index = len(self._play_cards_stack) - 1
            card = self._play_cards_stack[index]

            if not self._can_be_played(card):
                self._play_cards_stack.pop(index)
                continue

            # do not change order
            self.hand.remove_card(card)
            successful = card.prepare_card(self, True)

            if successful:
                self.game.planning_pile.add_card(card)
                self.show_prepare_card(card)
            else:
                # cancel
                card.undo_prepare_card(self)
                self.hand.add_card(card)

            self._play_cards_stack.pop(index)

        self.show_prepare_cards()

    def undo(self):
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

    def undo_all(self):
        """
        If the player has put down a card this turn it will undo the latest one
        :return:
        """
        if not self.is_turn():
            return
        for i in range(0, len(self.game.planning_pile)):
            self.undo()

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
        if self.is_turn() and len(self.possessions) > 0:
            return self.possessions[0].ask(title, options, options_type, number_to_pick, allow_cancel, image)

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
        (self if self.playing_as is None else self.playing_as).refresh_card_play_animation()

        question_answer = None
        # Only ask the question if there are more options avaliable
        if len(options_as_dict) > number_to_pick:
            # generate json for question
            question = {
                "title": str(title),
                "number to pick": int(number_to_pick),
                "type": options_type,
                "options": options_as_dict,
                "allow cancel": allow_cancel,
                "image": str(image)
            }

            question_answer = self.ask_question(question)
        else:
            # Automatically choose all answers if not enough options avaliable
            # cases where this occur like:
            # - there's only 1 option - pick the first one
            # - there's 3 options and you need to pick 3 - pick all 3
            # - there's 0 options - return the selected option as an empty array
            # - less options than the number to pick - eg -3 card when you've got 2 cards left
            question_answer = [option for option in options_as_dict]

        if question_answer is None:
            return None

        if len(question_answer) == 1:
            return question_answer[0]
        else:
            return question_answer

    def finish_turn(self):
        """
        Call this to play all cards in the planning pile or pickup, then move onto the next turn if the player does not have any extra turns.
        """

        if self.is_turn() is False:
            return

        # checks if cards can be played:
        for card in self.game.planning_pile:
            can_play, reason = card.ready_to_play()
            if can_play is False:
                return

        # play cards from planning pile
        for card in self.game.planning_pile:
            self.show_finished_card(card)
            card.play_card(self)
            self.game.played_cards.add_card(card)

        self.show_finished_cards()

        # if there is a pickup and the player did not play, make them pick it up
        if len(self.game.planning_pile) == 0:
            if self.game.pickup == 0:
                self.pickup(1)
            else:
                self.pickup(self.game.pickup)
                self.game.pickup = 0

        self.game.planning_pile.clear()

        for player in self.game.players:
            player.player_pickup_amount = 0

        # send wining message to everyone but this player
        if self.had_won():
            self.game.end_game(winner=self)
        else:
            # check if anyone else won as a result of playing the card
            self.game.check_winner()

        # check if player has any more turns left.
        self.next_turn()

    def next_turn(self):
        """
        After the turn is over, apply all effects and remove possessions.
        Then move onto the next turn
        """

        # Begin to remove effects from the player
        effect_index = 0
        next_turn = True

        while effect_index < len(self.effects):
            effect = self.effects[effect_index]

            if not effect.end_turn():
                next_turn = False

            effect.n_turns -= 1
            if effect.n_turns <= 0:
                self.effects.pop(effect_index)
            else:
                effect_index += 1

        if next_turn:
            self.state = "not turn"
            
            # remove possession
            if len(self.possessions) > 0:
                possession = self.possessions[0]
                possession.playing_as = None
                self.possessions.pop(0)

            self.game.next_turn()

    def pickup(self, number, show_pickup=True):
        """
        Pickup the given number of cards from the deck.
        :param number: number of cards to pickup
        :param show_pickup: if the show_pickup function should be called (usually animation)
        """
        number = min(self.game.max_cards - len(self.hand), int(number))

        cards = self.hand.add_cards_from_deck(self.game, number)

        if show_pickup is True:
            self.show_pickup(cards)

    def add_effect(self, effect):
        """
        Add an effect.
        """
        self.effects.append(effect)

    def remove_effect(self, effect):
        """
        Remove an effect.
        """

        self.effects.remove(effect)

    def get_effect(self, effect_type):
        """
        Get an effect by its type.
        :return: The effect. None if it does not exist
        """

        for effect in self.effects:
            if effect.get_type() == effect_type:
                return effect

        return None

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

    def is_turn(self):
        return self.state == "playing turn"

    def had_won(self):
        """
        checks if the player has one, if they have then it returns True.
        :return:
        """
        return len(self.hand) == 0

    def get_possessed_by(self):
        """
        Returns the player that is taking their turn if their turn is currently being possessed
        """
        return None if len(self.possessions) == 0 or not self.is_turn() else self.possessions[0]

    def get_name(self):
        return self.name

    def get_id(self):
        return self.player_id

    def ask_question(self, question):
        """
        Get the response of question, this may be overridden to prrovide any answer.
        :param question: The question to ask, in a format that can be used by the player object.
        :return: The answer to the question
        """
        return []

    def show_pickup(self, cards):
        """
        When cards have been picked up, run this method (useful for animation)
        :param cards: array of cards picked up
        """

        pass

    def show_prepare_card(self, card):
        """
        When a card is successfully prepared, run this method (useful for animation)
        :param card: Card successfully prepared
        """
        pass

    def show_prepare_cards(self):
        """
        When all cards are successfully prepared, run this method (useful for animation)
        """
        pass

    def show_finished_card(self, card):
        """
        When a card is successfully discarded, run this method (useful for animation)
        :param card: Card successfully discarded
        """
        pass

    def show_finished_cards(self):
        """
        When all cards are successfully discarded, run this method (useful for animation)
        """
        pass

    def show_undo(self):
        """
        When a card is undone, run this method (useful for animation)
        """
        pass

    def show_undo_all(self):
        """
        When all cards are successfully undone, run this method (useful for animation)
        """
        pass

    def refresh_card_play_animation(self):
        pass
    

    def __str__(self):
        player_str = '-- ' + self.name + ' --\n'
        player_str += "nCards: " + str(len(self.hand)) + '\n'
        player_str += "Playing As: " + (self.playing_as.get_name() if self.playing_as is not None else "None") + '\n'
        player_str += "Possessed By: " + (self.possessions[0].name if len(self.possessions) > 0 else "None") + '\n'
        for effect in self.effects:
            player_str += "- " + effect.get_type() + "(" + str(effect.n_turns) + ")\n"\
        
        return player_str


class Player(AbstractPlayer):
    """
    A player that is controlled by a client of a webserver.

    Has the ability to see animations and answer questions.
    """

    def __init__(self, game, name, player_id):
        super().__init__(game, name, player_id)

        self.game = game
        self.sid = None

        # setting up question stuff see self.ask()
        self._answer_event = None
        self._question = None

        # animation stuff
        # animate all the cards either before a question is asked or at the end of the play_card method
        self._cards_played_to_animate = []
        self._cards_finished_to_animate = []

    def show_prepare_card(self, card):
        """
        Prepare a card for animation
        :param card: Card successfully prepared
        """
        self._cards_played_to_animate.append(card)

    def show_prepare_cards(self):
        """
        Finish preparing cards by playing the animation of cards transferring to the planning pile
        """
        self.game.animate_card_transfer(
            self._cards_played_to_animate, cards_from=self, cards_to="planning")
        self._cards_played_to_animate.clear()

    def show_finished_card(self, card):
        """
        Prepare a card for the discarding animation
        :param card: Card successfully discarded
        """
        self._cards_finished_to_animate.append(card)

    def show_finished_cards(self):
        """
        Finish playing cards by playing the animation of cards transferring to the discard pile
        """
        if len(self._cards_finished_to_animate) > 0:
            self.game.animate_card_transfer(
                self._cards_finished_to_animate, cards_from="planning", cards_to="discard")
            self._cards_finished_to_animate.clear()

    def refresh_card_play_animation(self):
        """
        Whenever an animation or question is asked, update the card play animation
        so the player can see what card is on top and what is left
        """
        # send play cards animation before you send the options
        if len(self._cards_played_to_animate) > 0:
            self.game.animate_card_transfer(
                self._cards_played_to_animate, cards_from=self, cards_to="planning")
            self._cards_played_to_animate.clear()
        if len(self._cards_finished_to_animate) > 0:
            self.game.animate_card_transfer(
                self._cards_finished_to_animate, cards_from="planning", cards_to="discard")
            self._cards_finished_to_animate.clear()

    def ask_question(self, question):
        """
        Given a question, ask the player and get the response as user input.
        Send the question and wait for a reply. If the reply is not valid, send it again
        :param question: the question to ask, in the same format as the message to be sent.
        :return: the answer to the
        """

        question_answer = None
        # if the player leaves and comes back, this will be asked again
        self._question = question

        valid_answer = False
        while valid_answer is False:
            self.send_message("ask", question)

            self._answer_event = event.Event()
            question_answer = self._answer_event.wait()

            valid_answer = len(question_answer) == question["number to pick"]
            for choice in question_answer:
                if choice is None and question["allow cancel"] is True:
                    valid_answer = True
                    question_answer = None
                    break
                if choice not in question['options']:
                    valid_answer = False
                    break

        # clear the question
        self._question = None
        return question_answer

    def answer_question(self, question_answer):
        """
        This will answer the current question with the given answer
        :param question_answer: An array of the players chosen choices for the current question
        :return: None
        """
        if self._answer_event is not None:
            self._answer_event.send(question_answer)

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
            "your id": self.get_id(),
            "playing as": "" if self.playing_as is None else self.playing_as.get_id(),
            "planning pile": [],
            "direction": self.game.direction,
            "pickup size": self.game.pickup,
            "iteration": self.game.iterate_turn_by,
            "players": [],
            "cant play reason": "",
            "player type": type(self).__name__
        }

        # get first 4 cards from deck that are not in planning pile
        for card in self.game.played_cards[-settings.played_cards_to_show:]:
            json_to_send["cards on deck"].append(
                {
                    "url": card.get_url(),
                    "id": card.get_id(),
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
                    "url": card.get_url(),
                    "name": card.get_name(),
                    "id": card.get_id()
                }
            )

        # get player cards
        for card in (self.hand if self.playing_as is None else self.playing_as.hand):
            json_to_send["your cards"].append(
                {
                    "id": card.get_id(),
                    "url": card.get_url(),
                    "name": card.get_name(),
                    "can be played": (self if self.playing_as is None else self.playing_as)._can_be_played(card)
                }
            )

        # get information all players
        for player in self.game.players:
            json_to_send["players"].append(player.get_player_json())

        self.send_message("card update", json_to_send)

    def get_player_json(self):
        # all effect icons
        effect_json = []
        for effect in self.effects:
            effect_json.append(
                {
                    "url": effect.get_url(),
                    "amount left": effect.n_turns
                }
            )

        # possession effect
        if len(self.possessions) > 0:
            effect_json.append(
                {
                    "url": '/static/effects/possess.png',
                    "amount left": len(self.possessions)
                }
            )

        return {
            "name": self.get_name(),
            "id": self.get_id(),
            "number of cards": len(self.hand),
            "is turn": self.is_turn(),
            "possessed by": self.possessions[0].name if len(self.possessions) > 0 else "",
            "effects": effect_json,
            "pickup amount": self.player_pickup_amount
        }

    def send_message(self, message_type, data):
        """
        Sends the players web browser a message
        :param message_type: e.g. "card update" or "popup message"
        :param data: data to send the client with the message. Can be None
        :return: None
        """
        with fs.app.app_context():
            fs.socket_io.emit(message_type, data, room=self.sid)

    def send_animation(self, data):
        """
        Send an animation message
        If the player is possessed then the message will be sent to the possessor too.
        If a player is possessing another player they will not recieve animations
        :return: If a message was sent
        """
        if self.playing_as is None:
            self.send_message("animate", data)
            if len(self.possessions) > 0 and self.is_turn():
                self.possessions[0].send_message("animate", data)

            return True

        return False

    def show_undo(self):
        # send a message to all players
        json_to_send = {
            "type": "undo"
        }

        self.game.send_to_all_users("animate", json_to_send)

    def show_undo_all(self):
        # send a message to all players
        json_to_send = {
            "type": "undo all"
        }

        self.game.send_to_all_users("animate", json_to_send)

    def show_pickup(self, cards):
        """
        Animate picking up the cards
        :param cards: list of cards to animate
        :return: None
        """

        self.game.animate_card_transfer(cards, cards_to=self)

    def initial_connection(self):
        self.set_sid(request.sid)
        self.card_update()

        # Get all chat messages
        # TODO: send everything in one message
        for chat in self.game.chat:
            self.send_message("chat", chat)

        # Reask question
        if self._question is not None:
            self.send_message("ask", self._question)

    def set_sid(self, sid):
        self.sid = sid

    def get_sid(self):
        return self.sid


class Observer (Player):
    """
    Observes a game, but does not interact with it. 
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hand.clear()

    def start_turn(self, *args, **kwargs):
        pass

    def prepare_cards(self, *args, **kwargs):
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
