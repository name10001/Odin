from flask import *


class AbstractCard:
    CARD_IMAGE_URL = 'cards/generic.png'
    DESCRIPTION = 'This is a abstract card and should only be used to inherit from. This should never be seen in a game'
    NUMBER_IN_DECK = 0
    NAME = "Abstract card"
    CARD_COLOUR = "Abstract"
    CARD_TYPE = "Abstract"
    CAN_BE_ON_PICKUP = False
    CARD_TYPE_ID = 0  # TODO: might delete latter if not needed

    def __init__(self, game):
        self.game = game
        self.id = self._make_id()

    def play_card(self, player, options):
        """

        :return: None
        """
        pass
    
    def is_compatible_with(self, card):
        """
        Can these 2 cards be played together
        :param card: 
        :return: True or False
        """
        if card.CARD_TYPE == self.CARD_TYPE:
            return True
        if card.CARD_COLOUR == self.CARD_COLOUR:
            return True
        
        # white cards can be placed on anything that isn't black
        if self.CARD_COLOUR == "white":
            return card.CARD_COLOUR != "black"
        # black cards can be placed on any colour, but not purple or white.
        elif self.CARD_COLOUR == "black":
            return card.CARD_COLOUR != "white" and card.CARD_COLOUR != "purple"
        # purple cards can only be placed on white cards (if type/colour different)
        elif self.CARD_COLOUR == "purple":
            return card.CARD_COLOUR == "white"
        # coloured cards can be placed on black or white cards
        else:
            return card.CARD_COLOUR == "black" or card.CARD_COLOUR == "white"

    def can_be_played_on(self, card, is_players_turn):
        """
        Can this card be played on the given card
        :param card:
        :param is_players_turn: is it the players turn of not
        :return: True or False
        """
        if is_players_turn is False:
            return False
        if self.game.pickup != 0 and self.CAN_BE_ON_PICKUP is False:
            return False
        return card.is_compatible_with(self) and self.is_compatible_with(card)

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

    def __gt__(self, other):
        """
        if this card goes after the given other card
        Order is number cards, other cards, black cards, white cards
        Then each is sorted by color then type
        :param other: other card
        :return: True if this card is grater
        """
        
        if self.CARD_TYPE_ID < other.CARD_TYPE_ID:
            return False
        elif self.CARD_TYPE_ID > other.CARD_TYPE_ID:
            return True
        else:
            # compare colours
            return self.CARD_COLOUR > other.CARD_COLOUR

        """
        numbers = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '69')
        if self.CARD_TYPE in numbers and other.CARD_TYPE not in numbers:
            return False
        if self.CARD_TYPE not in numbers and other.CARD_TYPE in numbers:
            return True

        good_colors = ("black", "white")
        if self.CARD_COLOUR in good_colors and other.CARD_COLOUR not in good_colors:
            return True
        if self.CARD_COLOUR not in good_colors and other.CARD_COLOUR in good_colors:
            return False

        if self.CARD_COLOUR == other.CARD_COLOUR:
            return self.CARD_TYPE > other.CARD_TYPE
        else:
            return self.CARD_COLOUR > other.CARD_COLOUR
        """

    def __lt__(self, other):
        return not self.__gt__(other)

    def get_url(self):
        return url_for('static', filename=self.CARD_IMAGE_URL)

    def get_id(self):
        return self.id
