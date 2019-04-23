import cards
import random


class Deck:
    def __init__(self, game):
        self.game = game
        self.cards = []
        self.all_types = []
        self.all_colours = []
        self.set_cards(cards.all_cards.copy())
    
    def get_weights(self, card_collection=None):
        """
        Calculates the weights for each card that can still be picked up
        :param card_collection: The card_collection to calculate the weights for.
        If its None, it will calculate the weights for a medium hand
        :return: an array of card weights. The order is the same as Deck.cards
        I.e. weights[0] is the weight for Deck.cards[0]
        """
        if card_collection is None:
            # None player just use the medium hand size by default
            card_weights = [card.CARD_FREQUENCY.medium_hand for card in self.cards]
        else:
            card_weights = []
            n_cards = len(card_collection)
            for card in self.cards:
                n_this_type = card_collection.number_of_type(card.CARD_TYPE)
                card_weights.append(card.CARD_FREQUENCY.get_frequency(n_cards, n_this_type))

        return card_weights
    
    def update_remaining_cards(self):
        """
        After banning cards, calculate the remaining types and colours left
        """
        self.all_types.clear()
        self.all_colours.clear()
        for card in self.cards:
            if card.CARD_TYPE not in self.all_types:
                self.all_types.append(card.CARD_TYPE)
            if card.CARD_COLOUR not in self.all_colours:
                self.all_colours.append(card.CARD_COLOUR)

    def set_cards(self, cards):
        """
        Set the list of all cards
        Used when undoing a genocide card or initialization
        """
        self.cards = cards
        self.update_remaining_cards()

    def get_random_card(self, weights):
        """
        Gets a new random card and returns it.
        It will not return banned card unless all cards have been banned
        :return:
        """
        # if all cards have been banned - you would never reach here anyway because the game would end?
        if len(self.cards) == 0:
            return cards.get_random_card()
        else:
            return random.choices(self.cards, weights=weights)[0]

    def add_random_cards_to(self, card_collection, number):
        """
        Adds cards at the proper proportion to the given CardCollection
        :param card_collection: the CardCollection to added the cards to
        :param number: The number of new cards to add
        :return: None
        """
        for i in range(number):
            # calculate weights
            card_weights = self.get_weights(card_collection=card_collection)
            # add a random card based upon the weights
            card_collection.add_card(self.get_random_card(card_weights)(self.game))

    def ban_colour(self, card_colour):
        """
        removes a color from the deck
        :param card_colour: color to remove
        :return:
        """
        for card in self.cards.copy():
            if card.CARD_COLOUR == card_colour:
                self.cards.remove(card)

        self.update_remaining_cards()

    def ban_type(self, card_type):
        """
        removes a type from the deck
        :param card_type: type to remove
        :return:
        """
        for card in self.cards.copy():
            if card.CARD_TYPE == card_type:
                self.cards.remove(card)

        self.update_remaining_cards()

