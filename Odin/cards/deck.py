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
        self.number_of_cards = cards.size_of_deck

    def pickup(self):
        """
        gets a new random card and returns it.
        It will not return banned cards unless all cards have been band
        :return:
        """
        # if all cards have been banned - you would never reach here anyway because the game would end?
        if len(self.cards) == 0:
            return cards.get_random_card()
        else:
            place_in_deck = random.uniform(0, self.number_of_cards - 1)
            up_to = 0.0
            for card in self.cards:
                if up_to <= place_in_deck < up_to + card.NUMBER_IN_DECK:
                    return card(self.game)
                else:
                    up_to += card.NUMBER_IN_DECK
        raise RuntimeError("no card found")

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

        cards_copy = self.cards.copy()
        for card in cards_copy:
            if card.CARD_COLOUR == card_color:
                self.cards.remove(card)
                self.number_of_cards -= card.NUMBER_IN_DECK

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

        cards_copy = self.cards.copy()
        for card in cards_copy:
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
