from flask import *
import cards


class AbstractCard:
    CARD_IMAGE_URL = 'cards/generic.png'
    COMPATIBILITY_DESCRIPTION = 'This should describe what this card is compatible with'  # generate this using a function
    EFFECT_DESCRIPTION = 'No effects.'  # default description of the cards effects
    NUMBER_IN_DECK = 0
    NAME = "Abstract card"
    CARD_COLOUR = "Abstract"
    CARD_TYPE = "Abstract"
    CAN_BE_ON_PICKUP = False

    def __init__(self, game):
        self.game = game
        self.id = self._make_id()

    def prepare_card(self, player, options, played_on):
        pass
    
    def undo_prepare_card(self, player, played_on):
        pass

    def play_card(self, player, options, played_on):
        """

        :return: None
        """
        pass
    
    def is_compatible_with(self, card, player):
        """
        Can these 2 cards be played together
        :param card: 
        :return: True or False
        """
        if card.get_type() == self.get_type():
            return True
        if card.get_colour() == self.get_colour():
            return True
        if card.get_colour() == "colour swapper":
            return True

        # white cards can be placed on anything that isn't black
        if self.get_colour() == "white":
            return card.get_colour() != "black"
        # black cards can be placed on any colour, but not purple or white.
        elif self.get_colour() == "black":
            return card.get_colour() != "white" and card.get_colour() != "purple"
        # purple cards can only be placed on white cards (if type/colour different)
        elif self.get_colour() == "purple":
            return card.get_colour() == "white"
        # coloured cards can be placed on black or white cards
        else:
            return card.get_colour() == "black" or card.get_colour() == "white"

    def can_be_played_on(self, card, player):
        """
        Can this card be played on the given card
        :param card:
        :param player: is it the players turn of not
        :return: True or False
        """
        if player.is_turn() is False:
            return False
        if self.game.pickup != 0 and self.can_be_on_pickup() is False:
            return False
        return card.is_compatible_with(self, player) and self.is_compatible_with(card, player)

    def can_play_with(self, card, player, is_first_card):
        """
        Can this additional card be played with this card? Considers if this is the first card in the planning pile
        :param card:
        :return:
        """
        if is_first_card:
            return card.get_type() == self.get_type()
        
        return False

    def can_be_played_with(self, planning_pile, player):
        """
        Can this card be played on the given planning pile?
        By default this checks if you can play with ANY of the cards in the planning pile
        :param planning_pile:
        :return:
        """
        is_first_card = True
        for card, options in planning_pile:
            if card.can_play_with(self, player, is_first_card):
                return True
            is_first_card = False
        return False

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

        id_safe += "_" + str(id(self))

        return id_safe

    def get_options(self, player):
        """
        gets all the options for a card
        For example, the 'Fuck you' card requires you to pick a player.
        In that case this function would return a list of players
        :return: a Dictionary where the key is an value and the ID is what the player should see.
                 Or None if no options are needed
        """
        return None

    def is_option_valid(self, player, option, is_player=False):
        """
        Is the given option valid
        :param option: option to test
        :param is_player: Is the given option supposed to be a player id
        :return: True if it is valid, False if its not
        """
        if option is 0:
            return False
        if self.get_options(player) is not None:
            if option not in self.get_options(player):
                False
        if is_player and self.game.get_player(option) is None:
            return False
        return True

    def __gt__(self, other):
        """
        is this card goes after (is greater than) the given other card
        sorts by card category index, then type, then color then name
        :param other: other card
        :return: True if this card is grater
        """
        if self.get_category_index() != other.get_category_index():
            return self.get_category_index() > other.get_category_index()
        elif self.get_type() != other.get_type():
            return self.get_type() > other.get_type()
        elif self.get_colour() != other.get_colour():
            return self.get_colour() > other.get_colour()
        else:
            return self.get_name() > other.get_name()

    def __lt__(self, other):
        return not self.__gt__(other)

    def get_url(self):
        return url_for('static', filename=escape(self.CARD_IMAGE_URL))

    def get_category_index(self):
        return cards.get_card_index(self)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.NAME

    def get_colour(self):
        return self.CARD_COLOUR

    def get_type(self):
        return self.CARD_TYPE

    def can_be_on_pickup(self):
        return self.CAN_BE_ON_PICKUP
