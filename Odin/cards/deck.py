import cards
import random


class Deck:
    def __init__(self, game):
        self.game = game
        self.cards = []
        # dictionaries with all types/colours as keys and the values being
        # a set of indexes pointing to the locations of all the cards of that type/color in self.cards
        # e.g. {"blue": {1, 5, 6}, "green", {0, 4, 10}}
        self.all_types = {}
        self.all_colours = {}

        self.unbanned_colours = set()
        self.banned_colours = set()
        self.unbanned_types = set()
        self.banned_types = set()

        self.set_cards(cards.all_cards.copy())
    
    def get_weights(self, card_collection=None, ignore_limit=False):
        """
        Calculates the weights for all the cards. Banned cards will be given a probability of 0
        :param card_collection: The card_collection to calculate the weights for.
        If its None, it will calculate the weights for a medium hand
        :return: an array of card weights. The order is the same as Deck.cards
        :param ignore_limit: Should the card limit be ignored
        I.e. weights[0] is the weight for Deck.cards[0]
        """
        return [self.get_weight(card, card_collection, ignore_limit=ignore_limit) for card in self.cards]

    def get_weight(self, card, card_collection=None, ignore_limit=False):
        """
        Calculates the weights for the given card. Banned cards will be given a probability of 0
        :param card_collection: The card_collection to calculate the weights for.
        If its None, it will calculate the weights for a medium hand
        :param ignore_limit: Should the card limit be ignored
        :return: The weight of the given card.
        """
        if card_collection is None:
            return card.CARD_FREQUENCY.medium_hand
        else:
            if card.CARD_TYPE in self.banned_types or card.CARD_COLOUR in self.banned_colours:
                return 0
            else:
                n_cards = len(card_collection)
                n_this_type = card_collection.number_of_type(card.CARD_TYPE)
                return card.CARD_FREQUENCY.get_frequency(n_cards, n_this_type, ignore_limit=ignore_limit)

    def set_cards(self, cards):
        """
        Set the list of all cards
        Used when undoing a genocide card or initialization
        :param cards: card class list to pickup future cards from
        :return: None
        """
        if len(cards) == 0:
            raise ValueError("There are no cards")

        self.cards = list(cards)

        self.all_types.clear()
        self.all_colours.clear()
        i = 0
        for card in self.cards:
            if card.CARD_TYPE not in self.all_types:
                self.all_types[card.CARD_TYPE] = set()
            self.all_types[card.CARD_TYPE].add(i)
            if card.CARD_COLOUR not in self.all_colours:
                self.all_colours[card.CARD_COLOUR] = set()
            self.all_colours[card.CARD_COLOUR].add(i)
            i += 1

        self.unban_all()

    def get_random_card(self, card_weights):
        """
        Gets a new random card and returns it.
        :param card_weights: An array of the weights of the cards
        :return: A card class or None if all the weights are zero
        """
        try:
            return random.choices(self.cards, weights=card_weights)[0]
        except IndexError:
            return None

    def add_random_cards_to(self, card_collection, number):
        """
        Adds cards at the proper proportion to the given CardCollection
        :param card_collection: the CardCollection to added the cards to
        :param number: The number of new cards to add
        :return: The list of cards added
        """
        added_cards = []
        ignore_limit = False
        # calculate weights
        card_weights = self.get_weights(card_collection=card_collection, ignore_limit=ignore_limit)

        picked_up = 0
        while picked_up < number:
            # get a random card based upon the weights
            card_class = self.get_random_card(card_weights)

            # If it can't pick up anything, ignore the pickup limit, if it still cant pickup anything, unban all cards
            # This should only happen if all the cards have been banned or all the unbaned cards are at there limit
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

            # update weights of cards with the same type as the one that was picked up
            for index in self.all_types[card_class.CARD_TYPE]:
                card_weights[index] = self.get_weight(self.cards[index], card_collection, ignore_limit=ignore_limit)

            picked_up += 1

        return added_cards

    def ban_colour(self, card_colour):
        """
        Stops a colour from being picked up from the deck
        :param card_colour: color to ban
        :return: None
        """
        if card_colour in self.all_colours:
            self.banned_colours.add(card_colour)
            self.unbanned_colours.remove(card_colour)
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
            self.unbanned_types.remove(card_type)
        else:
            raise ValueError("that is not a valid card type")

    def unban_colour(self, card_colour):
        """
        Allows a colour from being picked up from the deck
        :param card_colour: color to allow
        :return: None
        """
        if card_colour in self.all_colours:
            self.banned_colours.remove(card_colour)
            self.unbanned_colours.add(card_colour)
        else:
            raise ValueError("that is not a valid card colour")

    def unban_type(self, card_type):
        """
        Allows a type from being picked up from the deck
        :param card_type: type to allow
        :return: None
        """
        if card_type in self.all_types:
            self.banned_types.remove(card_type)
            self.unbanned_types.add(card_type)
        else:
            raise ValueError("that is not a valid card type")

    def unban_all(self):
        """
        Unbans all colours and types
        :return: None
        """
        self.unbanned_colours = set(self.all_colours)
        self.banned_colours.clear()
        self.unbanned_types = set(self.all_types)
        self.banned_types.clear()

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
