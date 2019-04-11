import cards
import random
from flask import url_for


class Deck:
    def __init__(self, game):
        self.game = game
        self.banned_types = []
        self.not_banned_types = cards.all_types
        self.banned_colours = []
        self.not_banned_colours = cards.all_colours
        self.cards = cards.all_cards.copy()
        self.card_weights = cards.card_weights.copy()

    def pickup(self, number):
        """
        gets a new random card and returns it.
        It will not return banned cards unless all cards have been band
        :return:
        """
        # if all cards have been banned - you would never reach here anyway because the game would end?
        if len(self.cards) == 0:
            picked_card = cards.get_random_cards(number)
        else:
            picked_card = random.choices(self.cards, weights=self.card_weights, k=number)
        return [card(self.game) for card in picked_card]

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
        self.card_weights = [card.NUMBER_IN_DECK for card in self.cards]

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
        self.card_weights = [card.NUMBER_IN_DECK for card in self.cards]

    @staticmethod
    def get_all_urls():
        """
        gets all the complete card urls
        :return: List of strings containing urls
        """
        all_urls = []
        for url in cards.all_urls:
            all_urls.append(url_for('static', filename=url))
        return cards.all_urls
