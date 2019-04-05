from cards.abstract_card import AbstractCard

# ~~~~~~~~~~~~~~
#    Reverse
# ~~~~~~~~~~~~~~


class Reverse:
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "blue"
    CARD_TYPE = "reverse"
    CARD_TYPE_ID = 16
    CAN_BE_ON_PICKUP = True

    def play_card(self, player, options):
        self.game.direction *= -1


class BlueReverse(Reverse, AbstractCard):
    NAME = "Blue Reverse"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/reverse_blue.png'


class GreenReverse(Reverse, AbstractCard):
    NAME = "Green Reverse"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/reverse_green.png'


class PurpleReverse(Reverse, AbstractCard):
    NAME = "Purple Reverse"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'cards/reverse_purple.png'


class RedReverse(Reverse, AbstractCard):
    NAME = "Red Reverse"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/reverse_red.png'


class WhiteReverse(Reverse, AbstractCard):
    NAME = "White Reverse"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/reverse_white.png'


class BlackReverse(Reverse, AbstractCard):
    NAME = "Black Reverse"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/reverse_wild.png'
    NUMBER_IN_DECK = 1


class YellowReverse(Reverse, AbstractCard):
    NAME = "Yellow Reverse"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/reverse_yellow.png'


# ~~~~~~~~~~~~~~
#    Pickup2
# ~~~~~~~~~~~~~~


class Pickup2:
    NUMBER_IN_DECK = 2
    CARD_TYPE = "pickup2"
    CAN_BE_ON_PICKUP = True
    CARD_TYPE_ID = 19

    def play_card(self, player, options):
        self.game.pickup += 2


class BluePickup2(Pickup2, AbstractCard):
    NAME = "Blue Pickup 2"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/pickup2_blue.png'


class GreenPickup2(Pickup2, AbstractCard):
    NAME = "Green Pickup 2"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/pickup2_green.png'


class PurplePickup2(Pickup2, AbstractCard):
    NAME = "Purple Pickup 2"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'cards/pickup2_purple.png'


class RedPickup2(Pickup2, AbstractCard):
    NAME = "Red Pickup 2"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/pickup2_red.png'


class WhitePickup2(Pickup2, AbstractCard):
    NAME = "White Pickup 2"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/pickup2_white.png'


class BlackPickup2(Pickup2, AbstractCard):
    NAME = "Black Pickup 2"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup2_wild.png'
    NUMBER_IN_DECK = 3


class YellowPickup2(Pickup2, AbstractCard):
    NAME = "Yellow Pickup 2"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/pickup2_yellow.png'


# ~~~~~~~~~~~~~~
# Other pickups
# ~~~~~~~~~~~~~~

class Pickup10(AbstractCard):
    NUMBER_IN_DECK = 2
    CARD_TYPE = "pickup10"
    CARD_TYPE_ID = 21
    NAME = "Pickup 10"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup10_wild.png'
    CAN_BE_ON_PICKUP = True

    def play_card(self, player, options):
        self.game.pickup += 10


class Pickup4(AbstractCard):
    NUMBER_IN_DECK = 5
    CARD_TYPE = "pickup4"
    CARD_TYPE_ID = 20
    NAME = "Pickup 4"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup4_wild.png'
    CAN_BE_ON_PICKUP = True

    def play_card(self, player, options):
        self.game.pickup += 4


class PickupTimes2(AbstractCard):
    NUMBER_IN_DECK = 5
    CARD_TYPE = "pickupTimes2"
    CARD_TYPE_ID = 22
    NAME = "Pickup x2"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/multiply2_wild.png'
    CAN_BE_ON_PICKUP = True

    def play_card(self, player, options):
        self.game.pickup *= 2

# ~~~~~~~~~~~~~~
#    Skip
# ~~~~~~~~~~~~~~


class Skip:
    NUMBER_IN_DECK = 2
    CARD_TYPE = "skip"
    CARD_TYPE_ID = 17
    CAN_BE_ON_PICKUP = True
    
    def play_card(self, player, options):
        self.game.skip_next = True


class BlueSkip(Skip, AbstractCard):
    NAME = "Blue Skip"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/skip_blue.png'


class GreenSkip(Skip, AbstractCard):
    NAME = "Green Skip"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/skip_green.png'


class PurpleSkip(Skip, AbstractCard):
    NAME = "Purple Skip"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'cards/skip_purple.png'


class RedSkip(Skip, AbstractCard):
    NAME = "Red Skip"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/skip_red.png'


class WhiteSkip(Skip, AbstractCard):
    NAME = "White Skip"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/skip_white.png'


class BlackSkip(Skip, AbstractCard):
    NAME = "Black Skip"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/skip_wild.png'
    NUMBER_IN_DECK = 1


class YellowSkip(Skip, AbstractCard):
    NAME = "Yellow Skip"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/skip_yellow.png'

# ~~~~~~~~~~~~~~
#    Blank
# ~~~~~~~~~~~~~~


class BlankBro(AbstractCard):
    NAME = "JUST A BLANK BRO"
    NUMBER_IN_DECK = 3
    CARD_TYPE = "blankbro"
    CARD_TYPE_ID = 12
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/black.png'


class Happiness(AbstractCard):
    NAME = "HAPPINESS"
    NUMBER_IN_DECK = 3
    CARD_TYPE = "happiness"
    CARD_TYPE_ID = 11
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/white.png'


# ~~~~~~~~~~~~~~
#    Fuck
# ~~~~~~~~~~~~~~


class Fuck:
    NUMBER_IN_DECK = 1
    CARD_TYPE_ID = 13
    CARD_TYPE = "fuck"

    def is_compatible_with(self, card):
        return card.CARD_COLOUR == self.CARD_COLOUR or card.CARD_TYPE == self.CARD_TYPE


class BlueFuck(Fuck, AbstractCard):
    NAME = "Blue Fuck"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/fuck_blue.png'


class GreenFuck(Fuck, AbstractCard):
    NAME = "Green Fuck"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/fuck_green.png'


class RedFuck(Fuck, AbstractCard):
    NAME = "Red Fuck"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/fuck_red.png'


class BlackFuck(Fuck, AbstractCard):
    NAME = "Black Fuck"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/fuck_black.png'


class YellowFuck(Fuck, AbstractCard):
    NAME = "Yellow Fuck"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/fuck_yellow.png'


