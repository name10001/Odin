from cards.abstract_card import AbstractCard

# ~~~~~~~~~~~~~~
#    Reverse
# ~~~~~~~~~~~~~~


class Reverse:
    def play_card(self, player, options):
        self.game.direction *= -1


class BlueReverse(Reverse, AbstractCard):
    NAME = "Blue Reverse"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "blue"
    CARD_TYPE = "reverse"
    CARD_IMAGE_URL = 'cards/reverse_blue.png'


class GreenReverse(Reverse, AbstractCard):
    NAME = "Green Reverse"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "green"
    CARD_TYPE = "reverse"
    CARD_IMAGE_URL = 'cards/reverse_green.png'


class PurpleReverse(Reverse, AbstractCard):
    NAME = "Purple Reverse"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "purple"
    CARD_TYPE = "reverse"
    CARD_IMAGE_URL = 'cards/reverse_purple.png'


class RedReverse(Reverse, AbstractCard):
    NAME = "Red Reverse"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "red"
    CARD_TYPE = "reverse"
    CARD_IMAGE_URL = 'cards/reverse_red.png'


class WhiteReverse(Reverse, AbstractCard):
    NAME = "White Reverse"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "white"
    CARD_TYPE = "reverse"
    CARD_IMAGE_URL = 'cards/reverse_white.png'


class BlackReverse(Reverse, AbstractCard):
    NAME = "Black Reverse"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "black"
    CARD_TYPE = "reverse"
    CARD_IMAGE_URL = 'cards/reverse_wild.png'


class YellowReverse(Reverse, AbstractCard):
    NAME = "Yellow Reverse"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "yellow"
    CARD_TYPE = "reverse"
    CARD_IMAGE_URL = 'cards/reverse_yellow.png'


# ~~~~~~~~~~~~~~
#    Pickup2
# ~~~~~~~~~~~~~~


class Pickup2:
    def play_card(self, player, options):
        self.game.pickup += 2


class BluePickup2(Pickup2, AbstractCard):
    NAME = "Blue Pickup2"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "blue"
    CARD_TYPE = "pickup2"
    CARD_IMAGE_URL = 'cards/pickup2_blue.png'


class GreenPickup2(Pickup2, AbstractCard):
    NAME = "Green Pickup2"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "green"
    CARD_TYPE = "pickup2"
    CARD_IMAGE_URL = 'cards/pickup2_green.png'


class PurplePickup2(Pickup2, AbstractCard):
    NAME = "Purple Pickup2"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "purple"
    CARD_TYPE = "pickup2"
    CARD_IMAGE_URL = 'cards/pickup2_purple.png'


class RedPickup2(Pickup2, AbstractCard):
    NAME = "Red Pickup2"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "red"
    CARD_TYPE = "pickup2"
    CARD_IMAGE_URL = 'cards/pickup2_red.png'


class WhitePickup2(Pickup2, AbstractCard):
    NAME = "White Pickup2"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "white"
    CARD_TYPE = "pickup2"
    CARD_IMAGE_URL = 'cards/pickup2_white.png'


class BlackPickup2(Pickup2, AbstractCard):
    NAME = "Black Pickup2"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "black"
    CARD_TYPE = "pickup2"
    CARD_IMAGE_URL = 'cards/pickup2_wild.png'


class YellowPickup2(Pickup2, AbstractCard):
    NAME = "Yellow Pickup2"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "yellow"
    CARD_TYPE = "pickup2"
    CARD_IMAGE_URL = 'cards/pickup2_yellow.png'


# ~~~~~~~~~~~~~~
#    Skip
# ~~~~~~~~~~~~~~


class Skip:
    def play_card(self, player, options):
        self.game.slip_next = True


class BlueSkip(Skip, AbstractCard):
    NAME = "Blue Skip"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "blue"
    CARD_TYPE = "skip"
    CARD_IMAGE_URL = 'cards/skip_blue.png'


class GreenSkip(Skip, AbstractCard):
    NAME = "Green Skip"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "green"
    CARD_TYPE = "skip"
    CARD_IMAGE_URL = 'cards/skip_green.png'


class PurpleSkip(Skip, AbstractCard):
    NAME = "Purple Skip"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "purple"
    CARD_TYPE = "skip"
    CARD_IMAGE_URL = 'cards/skip_purple.png'


class RedSkip(Skip, AbstractCard):
    NAME = "Red Skip"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "red"
    CARD_TYPE = "skip"
    CARD_IMAGE_URL = 'cards/skip_red.png'


class WhiteSkip(Skip, AbstractCard):
    NAME = "White Skip"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "white"
    CARD_TYPE = "skip"
    CARD_IMAGE_URL = 'cards/skip_white.png'


class BlackSkip(Skip, AbstractCard):
    NAME = "Black Skip"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "black"
    CARD_TYPE = "skip"
    CARD_IMAGE_URL = 'cards/skip_wild.png'


class YellowSkip(Skip, AbstractCard):
    NAME = "Yellow Skip"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "yellow"
    CARD_TYPE = "skip"
    CARD_IMAGE_URL = 'cards/skip_yellow.png'

