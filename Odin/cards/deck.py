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

        self.unbanned_colours = []
        self.unbanned_types = []
        self.banned_cards = set()
        self.set_cards(cards.all_cards.copy())
    
    def get_weights(self, card_collection=None):
        """
        Calculates the weights for all the cards. Banned cards will be given a probability of 0
        :param card_collection: The card_collection to calculate the weights for.
        If its None, it will calculate the weights for a medium hand
        :return: an array of card weights. The order is the same as Deck.cards
        I.e. weights[0] is the weight for Deck.cards[0]
        """
        return [self.get_weight(card, card_collection) for card in self.cards]

    def get_weight(self, card, card_collection=None):
        """
        Calculates the weights for the given card. Banned cards will be given a probability of 0
        :param card_collection: The card_collection to calculate the weights for.
        If its None, it will calculate the weights for a medium hand
        :return: The weight of the given card.
        """
        if card_collection is None:
            return card.CARD_FREQUENCY.medium_hand
        else:
            if card in self.banned_cards:
                return 0
            else:
                n_cards = len(card_collection)
                n_this_type = card_collection.number_of_type(card.CARD_TYPE)
                return card.CARD_FREQUENCY.get_frequency(n_cards, n_this_type)

    def set_cards(self, cards):
        """
        Set the list of all cards
        Used when undoing a genocide card or initialization
        :param cards: Card list to pickup future cards from
        :return: None
        """
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

        self._update_unbanned()

    def get_random_card(self, card_weights):
        """
        Gets a new random card and returns it.
        :param card_weights: An array of the weights of the cards
        :return: A Card
        """
        return random.choices(self.cards, weights=card_weights)[0]

    def add_random_cards_to(self, card_collection, number):
        """
        Adds cards at the proper proportion to the given CardCollection
        :param card_collection: the CardCollection to added the cards to
        :param number: The number of new cards to add
        :return: The list of cards added
        """
        added_cards = []
        # calculate weights
        card_weights = self.get_weights(card_collection=card_collection)

        for i in range(number):
            # get a random card based upon the weights
            card = self.get_random_card(card_weights)

            # update weights of cards with the same type as the one that was picked up
            for index in self.all_types[card.CARD_TYPE]:
                card_weights[index] = self.get_weight(self.cards[index], card_collection)

            # add card to card_collection
            card = card(self.game)
            card_collection.add_card(card)
            added_cards.append(card)
        
        return added_cards

    def ban_colour(self, card_colour):
        """
        Stops a colour from being picked up from the deck
        Can be undone with unban_cards and the list of cards that are returned
        :param card_colour: color to ban
        :return: list of the Cards that were banned.
        """
        banned_cards = []
        for card in self.cards.copy():
            if card not in self.banned_cards and card.CARD_COLOUR == card_colour:
                self.ban_card(card, update_unbanned=False)
                banned_cards.append(card)

        self._update_unbanned()

        return banned_cards

    def ban_type(self, card_type):
        """
        Stops a type from being picked up from the deck
        Can be undone with unban_cards and the list of cards that are returned
        :param card_type: type to ban
        :return: list of the Cards that were banned
        """
        banned_cards = []
        for card in self.cards.copy():
            if card not in self.banned_cards and card.CARD_TYPE == card_type:
                self.ban_card(card, update_unbanned=False)
                banned_cards.append(card)

        self._update_unbanned()

        return banned_cards

    def _update_unbanned(self):
        """
        Updates the list of unbanned types and colours
        :return: None
        """
        self.unbanned_colours.clear()
        for card_colour in self.all_colours:
            banned = True
            for index in self.all_colours[card_colour]:
                if self.cards[index] not in self.banned_cards:
                    banned = False
            if not banned:
                self.unbanned_colours.append(card_colour)

        self.unbanned_types.clear()
        for card_type in self.all_types:
            banned = True
            for index in self.all_types[card_type]:
                if self.cards[index] not in self.banned_cards:
                    banned = False
            if not banned:
                self.unbanned_types.append(card_type)

        # if all the cards have been banned, unban all cards
        if len(self.unbanned_colours) == 0 and len(self.unbanned_types) == 0:
            self.banned_cards.clear()
            self.unbanned_types = self.all_types.copy()
            self.unbanned_colours = self.all_colours.copy()

    def ban_card(self, card, update_unbanned=True):
        """
        Stops a card from being picked up from the deck
        :param card: Card class to remove
        :param update_unbanned: Only for internal use! This updates the array of unbanned types and colours
        :return: None
        """
        self.banned_cards.add(card)
        if update_unbanned:
            self._update_unbanned()

    def unban_card(self, card, update_unbanned=True):
        """
        Allows a Card back into the deck
        This can be used to undo 'ban_card', 'ban_type' or 'ban_colour'
        :param card: The Card to add back
        :param update_unbanned: Only for internal use! This updates the array of unbanned types and colours
        :return: None
        """
        self.banned_cards.remove(card)
        if update_unbanned:
            self._update_unbanned()

    def unban_cards(self, cards):
        """
        Allows the given Cards to be picked up from the deck
        This can be used to undo 'ban_card', 'ban_type' or 'ban_colour'
        :param cards: An array of Cards to add back
        :return: None
        """
        for card in cards:
            self.unban_card(card, update_unbanned=False)
        self._update_unbanned()

    def get_unbanned_types(self):
        """
        Gets all the unbanned card types
        :return: An array of card types that have not been banned
        """
        return self.unbanned_types

    def get_unbanned_colours(self):
        """
        Gets all the unbanned card colours
        :return: An array of card colours that have not been banned
        """
        return self.unbanned_colours
