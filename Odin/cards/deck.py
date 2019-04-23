import cards
import random


class Deck:
    def __init__(self, game):
        self.game = game
        self.banned_types = []
        self.not_banned_types = cards.all_types
        self.banned_colours = []
        self.not_banned_colours = cards.all_colours
        self.cards = cards.all_cards.copy()
        self.card_weights = []
    
    def calculate_weights(self, player=None):
        card_weights = []
        if player is None:
            for card in self.cards:
                card_weights.append(card.CARD_FREQUENCY.medium_hand)  # null player just use the medium hand size by default
        else:
            n_cards = len(player.hand)
            for card in self.cards:
                n_this_type = player.hand.number_of_type(card.CARD_TYPE)
                card_weights.append(card.CARD_FREQUENCY.get_frequency(n_cards, n_this_type))
        return card_weights

    def get_random_card(self, weights):
        """
        gets a new random card and returns it.
        It will not return banned card unless all cards have been banned
        :return:
        """
        # if all cards have been banned - you would never reach here anyway because the game would end?
        if len(self.cards) == 0:
            return cards.get_random_card()
        else:
            return random.choices(self.cards, weights=weights)[0]

    def ban_colour(self, card_color):
        """
        removes a color from the deck
        :param card_color: color to remove
        :return:
        """
        if card_color in self.banned_colours:
            return
        self.banned_colours.append(card_color)
        self.not_banned_colours.remove(card_color)

        for card in self.cards.copy():
            if card.CARD_COLOUR == card_color:
                self.cards.remove(card)
        self.calculate_weights()

    def ban_type(self, card_type):
        """
        removes a type from the deck
        :param card_type: type to remove
        :return:
        """
        if card_type in self.banned_types:
            return
        self.banned_types.append(card_type)
        self.not_banned_types.remove(card_type)

        for card in self.cards.copy():
            if card.CARD_TYPE == card_type:
                self.cards.remove(card)
        self.calculate_weights()
