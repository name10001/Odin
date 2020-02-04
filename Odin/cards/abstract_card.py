from flask import *
import cards
from cards.card_frequency import CardFrequency
from util.extended_formatter import extended_formatter


class AbstractCard:
    CARD_IMAGE_URL = 'generic.png'
    COMPATIBILITY_DESCRIPTION = None  # generate this using get_compatibility_description()
    EFFECT_DESCRIPTION = 'No effects.'  # default description of the cards effects
    CARD_FREQUENCY = CardFrequency(0)
    NAME = "Abstract card"
    CARD_COLOUR = "Abstract"
    CARD_TYPE = "Abstract"
    ADDITIONAL_URLS = []  # if any card additional urls need to be loaded, add these here 
    CAN_BE_ON_PICKUP = False
    # Used for generating compatibility description, set to False if there's only 1 colour of this type.
    MULTI_COLOURED = True

    def __init__(self, game):
        self.game = game
        self.id = self._make_id()

    def ready_to_play(self):
        """
        Can the player finish there turn
        :return: returns (True, None) if they can, returns (False, "reason") if they cant
        """
        return True, None

    def prepare_card(self, player, allow_cancel):
        """
        Prepares the card in the planning pile
        :return: returns if the card should be played (False is usually if you press a cancel button)
        """
        return True
    
    def undo_prepare_card(self, player):
        pass

    def play_card(self, player):
        pass

    def get_play_with(self, player):
        pass
    
    def is_compatible_with(self, player, card):
        """
        Can these 2 cards be played together
        :param card:
        :param player:
        :return: True or False
        """
        if card.get_type() == self.get_type():
            return True
        if card.get_colour() == "colour swapper":
            return True

        return self.colours_are_compatible(self.get_colour(), card.get_colour())

    def can_be_played_on(self, player, card):
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
        return card.is_compatible_with(player, self) and self.is_compatible_with(player, card)

    def can_play_with(self, player, card, is_first_card):
        """
        Can this additional card be played with this card? Considers if this is the first card in the planning pile
        :param card:
        :param player:
        :param is_first_card:
        :return:
        """
        if is_first_card:
            return card.get_type() == self.get_type()
        
        return False

    def can_be_played_with(self, player):
        """
        Can this card be played on the given planning pile?
        By default this checks if you can play with ANY of the cards in the planning pile
        :param player:
        :return:
        """
        is_first_card = True
        for card in self.game.planning_pile:
            if card.can_play_with(player, self, is_first_card):
                return True
            is_first_card = False
        return False

    def _make_id(self):
        """
        makes and ID that is unique to itself and is human readable
        """
        return extended_formatter.format("{cls.NAME!h}_card_{id}", cls=self, id=id(self))

    @classmethod
    def get_compatibility_description(cls):
        if cls.COMPATIBILITY_DESCRIPTION is not None:
            to_return = cls.COMPATIBILITY_DESCRIPTION
        elif cls.CARD_COLOUR == "black":
            to_return = "This is a regular black card. Compatible with all black, red, green, yellow and blue cards."
        elif cls.CARD_COLOUR == "white":
            to_return = "This is a regular white card. Compatible with all white, " \
                        "purple, red, green, yellow and blue cards."
        elif cls.CARD_COLOUR == "rainbow":
            to_return = "This is a regular rainbow card. Compatible with all cards."
        elif cls.CARD_COLOUR == "orange":
            to_return = "This is a regular orange card. Only compatible with other orange cards."
        elif cls.CARD_COLOUR == "purple":
            to_return = "This is a regular purple card. Compatible with all purple and white cards."
        else:
            to_return = "This is a regular {cls.CARD_COLOUR} card. " \
                        "Compatible with all {cls.CARD_COLOUR}, black and white cards."

        if cls.MULTI_COLOURED:
            to_return += " Also compatible with {cls.CARD_TYPE} cards of any colour."

        return extended_formatter.format(to_return, cls=cls)

    def __gt__(self, other):
        """
        Is this card greater than (goes after) the given other card.
        This is used for sorting.
        Sorts by card category index, then type, then color then name then id
        :param other: other card
        :return: True if this card is grater
        """
        if self.get_category_index() != other.get_category_index():
            return self.get_category_index() > other.get_category_index()
        elif self.get_type() != other.get_type():
            return self.get_type() > other.get_type()
        elif self.get_colour() != other.get_colour():
            return self.get_colour() > other.get_colour()
        elif self.get_name() != other.get_name():
            return self.get_name() > other.get_name()
        else:
            return self.get_id() > other.get_id()

    def __lt__(self, other):
        return not self.__gt__(other)

    def get_url(self):
        return '/static/cards/' + escape(self.CARD_IMAGE_URL)

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

    @staticmethod
    def colours_are_compatible(colour_1, colour_2):
        if colour_1 == colour_2:
            return True
        elif colour_1 == "rainbow" or colour_2 == "rainbow":
            return True
        elif colour_1 == "orange" or colour_2 == "orange":
            return False
        elif colour_1 == "white":
            return colour_2 != "black"
        elif colour_1 == "black":
            return colour_2 != "white" and colour_2 != "purple"
        elif colour_1 == "purple":
            return colour_2 == "white"
        else:
            return colour_2 == "white" or colour_2 == "black"
