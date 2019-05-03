from cards.card_frequency import CardFrequency
import cards
import random


class Deck:
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

    def add_random_cards_to(self, card_collection, number, dynamic_weights=True):
        """
        Adds cards at the proper proportion to the given CardCollection.
        :param card_collection: The CardCollection to added the cards to.
        :param number: The number of new cards to add.
        :param dynamic_weights: Weather of not to take into account the number of cards already in the collection
        :return: The list of cards added.
        """
        added_cards = []
        ignore_limit = False
        # calculate weights
        if dynamic_weights:
            card_weights = self.get_weights(card_collection=card_collection, ignore_limit=ignore_limit)
        else:
            card_weights = self.get_weights()

        picked_up = 0
        while picked_up < number:
            # get a random card based upon the weights
            card_class = self.get_random_card(card_weights)

            # If it can't pick up anything, ignore the pickup limit, if it still cant pickup anything, unban all cards.
            # This should only happen if all the cards have been banned or all the unbaned cards are at there limit.
            if card_class is None:
                if ignore_limit is False:
                    ignore_limit = True
                else:
                    self.unban_all()
                continue

            # add card to card_collection
            card = card_class(self.game)
            card_collection.add_card(card)
            added_cards.append(card)

            if dynamic_weights:
                # if the amount of cards has surpassed a milestone
                # as set in the card frequency class, update all frequencies
                if len(card_collection) in (
                        CardFrequency.SMALL_HAND+1,
                        CardFrequency.MEDIUM_HAND+1,
                        CardFrequency.LARGE_HAND+1
                ):
                    card_weights = self.get_weights(card_collection, ignore_limit)
                else:
                    # update weights of cards with the same type as the one that was picked up
                    for index in self.all_types[card_class.CARD_TYPE]:
                        card_weights[index] = self.get_weight(self.cards[index], card_collection, ignore_limit)

            picked_up += 1

        return added_cards
    
    def get_weights(self, card_collection=None, elevator=False, ignore_limit=False):
        """
        Calculates the weights for all the cards.
        :param card_collection: The card_collection to calculate the weights for.
        If its None, it will calculate the weights for a medium hand.
        :return: an array of card weights. The order is the same as Deck.cards.
        :param ignore_limit: Should the card limit be ignored
        :return: The weight of the given cards. The order its the unchanged,
        I.e. weights[0] is the weight for Deck.cards[0].
        """
        return [self.get_weight(card, card_collection, elevator=elevator, ignore_limit=ignore_limit) for card in self.cards]

    def get_weight(self, card, card_collection=None, elevator=False, ignore_limit=False):
        """
        Calculates the weights for the given card.
        :param card: The card to get the weight of.
        :param card_collection: The card_collection to calculate the weights for.
        If its None, it will calculate the weights for a medium hand.
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

    def get_random_card(self, card_weights=None, elevator=False):
        """
        Gets a new random card and returns it.
        :param card_weights: An array of the weights of the cards
        :return: A card class or None if all the weights are zero
        """
        if card_weights is None:
            card_weights = self.get_weights(elevator=elevator)
        try:
            return random.choices(self.cards, weights=card_weights)[0]
        except IndexError:
            return None

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
