from cards.abstract_card import AbstractCard
from cards.card_frequency import CardFrequency
from flask import url_for

# ~~~~~~~~~~~~~~
#    Reverse
# ~~~~~~~~~~~~~~


class Reverse(AbstractCard):
    CARD_FREQUENCY = CardFrequency(2.2, 2, starting=0)
    CARD_COLOUR = "blue"
    CARD_TYPE = "Reverse"
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "Reverses the direction of play."

    def prepare_card(self, player, allow_cancel):
        self.game.direction *= -1
        return True
    
    def undo_prepare_card(self, player):
        self.game.direction *= -1


class BlueReverse(Reverse):
    NAME = "Blue Reverse"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'reverse_blue.png'


class GreenReverse(Reverse):
    NAME = "Green Reverse"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'reverse_green.png'


class PurpleReverse(Reverse):
    NAME = "Purple Reverse"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'reverse_purple.png'


class RedReverse(Reverse):
    NAME = "Red Reverse"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'reverse_red.png'


class WhiteReverse(Reverse):
    NAME = "White Reverse"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'reverse_white.png'


class BlackReverse(Reverse):
    NAME = "Black Reverse"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'reverse_wild.png'


class YellowReverse(Reverse):
    NAME = "Yellow Reverse"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'reverse_yellow.png'





# ~~~~~~~~~~~~~~
#    Skip
# ~~~~~~~~~~~~~~


class Skip(AbstractCard):
    CARD_FREQUENCY = CardFrequency(2.2, 2, starting=0)
    CARD_TYPE = "Skip"
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "Skips the next person's turn."
    
    def prepare_card(self, player, allow_cancel):
        self.game.iterate_turn_by += 1
        return True
    
    def undo_prepare_card(self, player):
        self.game.iterate_turn_by -= 1


class BlueSkip(Skip):
    NAME = "Blue Skip"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'skip_blue.png'


class GreenSkip(Skip):
    NAME = "Green Skip"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'skip_green.png'


class PurpleSkip(Skip):
    NAME = "Purple Skip"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'skip_purple.png'


class RedSkip(Skip):
    NAME = "Red Skip"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'skip_red.png'


class WhiteSkip(Skip):
    NAME = "White Skip"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'skip_white.png'


class BlackSkip(Skip):
    NAME = "Black Skip"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'skip_wild.png'
    NUMBER_IN_DECK = 1


class YellowSkip(Skip):
    NAME = "Yellow Skip"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'skip_yellow.png'


class FreeTurn(AbstractCard):
    CARD_FREQUENCY = CardFrequency(4, 3, 2, 1, max_cards=5, starting=0)
    CARD_TYPE = "Free Turn"
    NAME = "Free Turn"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'free_turn.png'
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Gain an extra turn. If you play multiple Free Turn cards together " \
                         "you will gain multiple extra turns."

    def prepare_card(self, player, allow_cancel):
        player.turns_left += 1
        return True

    def undo_prepare_card(self, player):
        player.turns_left -= 1
