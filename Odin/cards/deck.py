import cards
from random import randint
from flask import url_for


class Deck:
    def __init__(self):
        self.banded_types = []
        self.not_banded_types = cards.all_types
        self.banded_colours = []
        self.not_banded_colours = cards.all_colours
        self.cards = cards.all_cards.copy()
        self.number_of_cards = cards.size_of_deck

    def pickup(self):
        """
        gets a new random card and returns it.
        It will not return banned cards unless all cards have been band
        :return:
        """
        if len(self.cards) == 0:  # if all cards have been banded
            return cards.get_random_card()
        else:
            place_in_deck = randint(0, self.number_of_cards)
            up_to = 0
            for card in self.cards:
                if place_in_deck in range(up_to, up_to + card.NUMBER_IN_DECK):
                    return card
                else:
                    up_to += card.NUMBER_IN_DECK

    def ban_color(self, card_color):
        """
        removes a color from the deck
        :param card_color: color to remove
        :return:
        """
        self.banded_colours.append(card_color)
        self.not_banded_colours.remove(card_color)
        for card in self.cards:
            if card.CARD_COLOUR == card_color:
                self.cards.remove(card)
                self.number_of_cards -= card.NUMBER_IN_DECK

    def ban_type(self, card_type):
        """
        removes a type from the deck
        :param card_type: type to remove
        :return:
        """
        self.banded_types.append(card_type)
        self.not_banded_colours.remove(card_type)
        for card in self.cards:
            if card.CARD_TYPE == card_type:
                self.cards.remove(card)
                self.number_of_cards -= card.NUMBER_IN_DECK

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
