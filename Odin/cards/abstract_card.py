from flask import *


class AbstractCard:
    CARD_IMAGE_URL = 'cards/generic.png'
    CARD_CATEGORIES = []  # will be removed soon
    DESCRIPTION = 'This is a abstract card and should only be used to inherit from. This should never be seen in a game'
    NUMBER_IN_DECK = 0
    NAME = "Abstract card"
    CARD_COLOUR = "Abstract"
    CARD_TYPE = "Abstract"
    CARD_IS_PICKUP = False
    PICK_PLAYER = False
    PICK_TYPE = False

    def __init__(self, game):
        self.game = game
        self.id = self._make_id()

    def play_card(self, player, pick_player=None, picked_type=None):
        """

        :return: None
        """
        pass
    
    def can_be_played_on_this(self, card):
        """
        Can the given card be played on this card
        :param card: 
        :return: True or False
        """
        return not set(card.CARD_CATEGORIES).isdisjoint(set(self.CARD_CATEGORIES))

    def can_be_played_on(self, card, is_players_turn):
        """
        Can this card be played on the given card
        :param card:
        :param is_players_turn: is it the players turn of not
        :return: True or False
        """
        if is_players_turn is False:
            return False
        return card.can_be_played_on_this(self)

    def _make_id(self):
        """
        makes and ID that is unique to itself and is human readable
        """
        the_id = self.NAME.replace(" ", "_") + "_card"

        # remove all HTML unsafe characters
        id_safe = ""
        for character in the_id:
            # if character is a-z, A-Z, 1-9 or is _
            if ord(character) in range(ord("a"), ord("z") + 1)\
                    or ord(character) in range(ord("A"), ord("Z") + 1)\
                    or ord(character) in range(ord("1"), ord("9") + 1)\
                    or character in ("_",):
                id_safe += character

        # if its ID is already in use, add a number to it
        if self.game.find_card(id_safe) is not None:
            num = 2
            while self.game.find_card(id_safe + "_" + str(num)) is not None:
                num += 1
            id_safe += "_" + str(num)

        return id_safe

    def get_url(self):
        return url_for('static', filename=self.CARD_IMAGE_URL)

    def get_id(self):
        return self.id
