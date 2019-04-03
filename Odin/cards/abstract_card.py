from flask import *


class AbstractCard:
    CARD_IMAGE_URL = 'cards/generic.png'
    DESCRIPTION = 'This is a abstract card and should only be used to inherit from. This should never be seen in a game'
    NUMBER_IN_DECK = 0
    NAME = "Abstract card"
    CARD_COLOUR = "Abstract"
    CARD_TYPE = "Abstract"
    CARD_IS_PICKUP = False

    def __init__(self, game):
        self.game = game
        self.id = self._make_id()

    def play_card(self, player, options):
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
        # if same color or type
        if self.CARD_COLOUR == card.CARD_COLOUR or self.CARD_TYPE == card.CARD_TYPE:
            return True
        # black can go on anything as long as its not white
        elif card.CARD_COLOUR == "black" and self.CARD_COLOUR != "white":
            return True
        # white cards can go on anything as long as its not black
        elif card.CARD_COLOUR == "white" and self.CARD_COLOUR != "black":
            return True
        else:
            return False

    def can_be_played_on(self, card, is_players_turn):
        """
        Can this card be played on the given card
        :param card:
        :param is_players_turn: is it the players turn of not
        :return: True or False
        """
        if self.game.pickup != 0:
            return False
        if is_players_turn is False:
            return False
        return card.can_be_played_on_this(self)

    def can_be_played_with(self, card):
        """
        If this card is the first card played in a turn, can the given card be played with it
        :param card:
        :return:
        """
        return self.CARD_TYPE == card.CARD_TYPE

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

    def get_options(self):
        """
        gets all the options for a card
        For example, the 'Fuck you' card requires you to pick a player.
        In that case this function would return a list of players
        :return: a Dictionary where the key is an ID and the value is what the player should see.
                 Or None if no options are needed
        """
        return None

    def get_url(self):
        return url_for('static', filename=self.CARD_IMAGE_URL)

    def get_id(self):
        return self.id
