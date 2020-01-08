from cards.card_frequency import CardFrequency
import cards
import random


class AbstractDeck:
    """
    This a very abstracted version of a deck which only has a method to get the next card in the deck and has no implementation

    TODO: Allow card banning through this class instead of WeightedDeck


    """

    def get_next_card(self, flags):
        """
        Returns the next card in the deck. This abstracted deck does not have any cards in it.
        :param flags: any information on how the card was obtained in a dictionary, this can be used to blacklist certain cards from appearing or alter how often certain cards appear.
        """
        return None


class WeightedDeck(AbstractDeck):
    """
    A weighted deck will pick the next card based on a weight given to each card.
    The weight adjusts based on the cards that the player is already holding.

    TODO make the flag a private field and update it
    """

    def __init__(self, game):
        self.game = game
        self.cards = []
        # dictionaries with all types/colours that are not banned as keys and the values being
        # a set of indexes pointing to the locations of all the cards of that type/color in self.cards
        # e.g. {"blue": {1, 5, 6}, "green", {0, 4, 10}}
        self.all_types = {}
        self.all_colours = {}

        # An ordered array with all the unbanned types/colours
        self.unbanned_types = []
        self.unbanned_colours = []

        # types and colours not included in all_types and all_colours. Remove and add from these
        self.banned_types = set()
        self.banned_colours = set()

        self._flags = {
            "card collection": None,
            "elevator": False
        }

        self._update_cards()

    def _update_cards(self):
        """
        Updates the list of cards, unbanned types and unbanned colours.
        They will not include any of the banned types or colours.
        This should be called after a card is banned or unbanned.
        :return: None
        """

        self.cards = []
        self.all_types = {}
        self.all_colours = {}
        self.unbanned_colours.clear()
        self.unbanned_types.clear()

        i = 0
        for card in cards.all_cards.copy():
            if card.CARD_TYPE not in self.banned_types and card.CARD_COLOUR not in self.banned_colours:
                self.cards.append(card)

                # add to all types and unbanned types
                if card.CARD_TYPE not in self.unbanned_types:
                    self.unbanned_types.append(card.CARD_TYPE)
                    self.all_types[card.CARD_TYPE] = set()
                self.all_types[card.CARD_TYPE].add(i)

                # add to all colours and unbanned colours
                if card.CARD_COLOUR not in self.unbanned_colours:
                    self.unbanned_colours.append(card.CARD_COLOUR)
                    self.all_colours[card.CARD_COLOUR] = set()
                self.all_colours[card.CARD_COLOUR].add(i)

                i += 1

        self._update_weights()

    def get_next_card(self, flags):
        """
        Get the next card in the deck.
        :param flags: Dictionary which should contain a card collection and whether or not the card was obtained via an elevator card.

        """
        self._flags = flags
        self._update_weights()

        try:
            return random.choices(self.cards, weights=self._weights)[0]
        except IndexError:
            return None

    def _update_weights(self):
        """
        Calculates the weights for all the cards given the values self._flags
        :return: 
        """

        self._weights = [
            self.get_weight(card, self._flags["card collection"],
                            elevator=self._flags["elevator"], ignore_limit=False)
            for card in self.cards
        ]

        # Check that at least one weight is > 0
        for weight in self._weights:
            if weight != 0:
                return

        # Get the weights with ignoring the limit
        self._weights = [
            self.get_weight(card, self._flags["card collection"],
                            elevator=self._flags["elevator"], ignore_limit=True)
            for card in self.cards
        ]

    def get_weight(self, card, card_collection=None, elevator=False, ignore_limit=False):
        """
        Calculates the weights for the given card.
        :param card: The card to get the weight of.
        :param card_collection: The card_collection to calculate the weights for.
        If its None, it will calculate the weights for a medium hand.
        :param elevator: If this card was obtained via an elevator card
        :param ignore_limit: Should the card limit be ignored.
        :return: The weight of the given card.
        """
        if card_collection is None:
            if elevator is True:
                return card.CARD_FREQUENCY.get_elevator_weight()
            else:
                return card.CARD_FREQUENCY.get_starting_weight()
        else:
            n_cards = len(card_collection)
            n_this_type = card_collection.number_of_type(card.CARD_TYPE)
            return card.CARD_FREQUENCY.get_weight(n_cards, n_this_type, ignore_limit=ignore_limit)

    def ban_colour(self, card_colour):
        """
        Stops a colour from being picked up from the deck
        :param card_colour: color to ban
        :return: None
        """
        if card_colour in self.unbanned_colours:
            self.banned_colours.add(card_colour)
            self._update_cards()
        else:
            raise ValueError("that is not a valid card colour")

    def ban_type(self, card_type):
        """
        Stops a type from being picked up from the deck
        :param card_type: type to ban
        :return: None
        """
        if card_type in self.all_types:
            self.banned_types.add(card_type)
            self._update_cards()
        else:
            raise ValueError("that is not a valid card type")

    def unban_colour(self, card_colour):
        """
        Allows a colour from being picked up from the deck
        :param card_colour: color to allow
        :return: None
        """
        if card_colour in self.banned_colours:
            self.banned_colours.remove(card_colour)
            self._update_cards()
        else:
            raise ValueError("that is not a valid card colour")

    def unban_type(self, card_type):
        """
        Allows a type from being picked up from the deck
        :param card_type: type to allow
        :return: None
        """
        if card_type in self.banned_types:
            self.banned_types.remove(card_type)
            self._update_cards()
        else:
            raise ValueError("That is not a valid card type")

    def unban_all(self):
        """
        Unbans all colours and types
        :return: None
        """
        self.banned_colours.clear()
        self.banned_types.clear()
        self._update_cards()

    def get_unbanned_types(self):
        """
        Gets all the unbanned card types
        :return: A set of card types that have not been banned
        """
        return self.unbanned_types

    def get_unbanned_colours(self):
        """
        Gets all the unbanned card colours
        :return: A set of card colours that have not been banned
        """
        return self.unbanned_colours
