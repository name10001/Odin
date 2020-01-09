from cards.abstract_card import AbstractCard
from cards.card_frequency import CardFrequency

# ~~~~~~~~~~~~~~
#    Blank
# ~~~~~~~~~~~~~~


class BlankBro(AbstractCard):
    NAME = "Just A Blank Bro"
    CARD_FREQUENCY = CardFrequency(4,4,6,12)
    CARD_TYPE = "Just A Blank Bro"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'black.png'
    MULTI_COLOURED = False


class Happiness(AbstractCard):
    NAME = "Happiness"
    CARD_FREQUENCY = CardFrequency(4,4,6,12)
    CARD_TYPE = "Happiness"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'white.png'
    MULTI_COLOURED = False


# ~~~~~~~~~~~~~~
#    Fuck
# ~~~~~~~~~~~~~~


class Fuck(AbstractCard):
    CARD_FREQUENCY = CardFrequency(1.2, 0.5)
    CARD_TYPE = "Fuckin' M8"
    CARD_COLOUR = "Abstract"
    COMPATIBILITY_DESCRIPTION = "This card is only compatible with other {cls.CARD_COLOUR} cards or " \
                                "other Fuckin' M8 cards."

    def is_compatible_with(self, player, card):
        if card.get_colour() == "colour swapper":
            return card.COLOUR_1 == self.get_colour() or card.COLOUR_2 == self.get_colour()
        return card.get_colour() == self.get_colour() or card.get_type() == self.get_type()


class BlueFuck(Fuck):
    NAME = "Fuckin' Blue M8"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'fuck_blue.png'


class GreenFuck(Fuck):
    NAME = "Fuckin' Green M8"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'fuck_green.png'


class RedFuck(Fuck):
    NAME = "Fuckin' Red M8"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'fuck_red.png'


class BlackFuck(Fuck):
    NAME = "Fuckin' Black M8"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'fuck_black.png'


class YellowFuck(Fuck):
    NAME = "Fuckin' Yellow M8"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'fuck_yellow.png'

