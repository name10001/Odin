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
            return cards.get_random_cards(number)
        else:
            return random.choices(self.cards, weights=self.card_weights, k=number)

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

    #@staticmethod
    #def get_all_cards():
    #    """
    #    gets all the cards with their name, URL and description
    #    :return: List of strings containing urls
    #    """
    #    card_list = []
    #    for card in cards.all_cards:
    #        json_to_send = {
    #            "url":url_for('static', filename=card.CARD_IMAGE_URL),
    #            "name": card.NAME,
    #            "type": card.CARD_TYPE,
    #            "colour": card.CARD_COLOUR,
    #            "can be on pickup": card.CAN_BE_ON_PICKUP,
    #            "effect description": card.EFFECT_DESCRIPTION,
    #            "compatibility description": card.COMPATIBILITY_DESCRIPTION
    #        }
    #        card_list.append(json_to_send)
    #    return card_list
