from cards.abstract_card import AbstractCard

# ~~~~~~~~~~~~~~
#    Reverse
# ~~~~~~~~~~~~~~


class Reverse:
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "blue"
    CARD_TYPE = "reverse"

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


class YellowReverse(Reverse, AbstractCard):
    NAME = "Yellow Reverse"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/reverse_yellow.png'


# ~~~~~~~~~~~~~~
#    Pickup2
# ~~~~~~~~~~~~~~


class Pickup2:
    NUMBER_IN_DECK = 1
    CARD_TYPE = "pickup2"

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


class YellowPickup2(Pickup2, AbstractCard):
    NAME = "Yellow Pickup 2"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/pickup2_yellow.png'


# ~~~~~~~~~~~~~~
# Other pickups
# ~~~~~~~~~~~~~~

class Pickup10:
    NUMBER_IN_DECK = 1
    CARD_TYPE = "pickup10"
    NAME = "Pickup 10"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup10_wild.png'

    def play_card(self, player, options):
        self.game.pickup += 10


class Pickup4:
    NUMBER_IN_DECK = 1
    CARD_TYPE = "pickup4"
    NAME = "Pickup 4"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup4_wild.png'

    def play_card(self, player, options):
        self.game.pickup += 4


class PickupTimes2:
    NUMBER_IN_DECK = 1
    CARD_TYPE = "pickupTimes2"
    NAME = "Pickup x2"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/multiply2_wild.png'

    def play_card(self, player, options):
        self.game.pickup *= 2

# ~~~~~~~~~~~~~~
#    Skip
# ~~~~~~~~~~~~~~


class Skip:
    NUMBER_IN_DECK = 1
    CARD_TYPE = "skip"
    
    def play_card(self, player, options):
        self.game.slip_next = True


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


class YellowSkip(Skip, AbstractCard):
    NAME = "Yellow Skip"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/skip_yellow.png'


# ~~~~~~~~~~~~~~
#    Fuck
# ~~~~~~~~~~~~~~


class Fuck:
    NUMBER_IN_DECK = 1
    CARD_TYPE = "fuck"

    def is_compatible_with(self, card):
        return card.CARD_COLOUR == self.CARD_COLOUR


class BlueFuck(Fuck, AbstractCard):
    NAME = "Blue Fuck"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/fuck_blue.png'


class GreenFuck(Fuck, AbstractCard):
    NAME = "Green Fuck"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/fuck_green.png'


class PurpleFuck(Fuck, AbstractCard):
    NAME = "Purple Fuck"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'cards/fuck_purple.png'


class RedFuck(Fuck, AbstractCard):
    NAME = "Red Fuck"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/fuck_red.png'


class WhiteFuck(Fuck, AbstractCard):
    NAME = "White Fuck"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/fuck_white.png'


class BlackFuck(Fuck, AbstractCard):
    NAME = "Black Fuck"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/fuck_wild.png'


class YellowFuck(Fuck, AbstractCard):
    NAME = "Yellow Fuck"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/fuck_yellow.png'


