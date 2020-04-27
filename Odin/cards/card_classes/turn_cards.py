from cards.abstract_card import AbstractCard
from flask import url_for
from cards.effect import FreeTurnEffect, FreezeEffect

# ~~~~~~~~~~~~~~
#    Reverse
# ~~~~~~~~~~~~~~


class Reverse(AbstractCard):
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


class YellowSkip(Skip):
    NAME = "Yellow Skip"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'skip_yellow.png'


class FreeTurn(AbstractCard):
    CARD_TYPE = "Free Turn"
    NAME = "Free Turn"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'free_turn.png'
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Gain an extra turn. If you play multiple Free Turn cards together " \
                         "you will gain multiple extra turns."

    def prepare_card(self, player, allow_cancel):

        effect = player.get_effect("Free Turn")
        
        if effect is None:
            effect = FreeTurnEffect(player, 1)
            player.add_effect(effect)
        else:
            effect.n_turns += 1
        
        return True

    def undo_prepare_card(self, player):
        effect = player.get_effect("Free Turn")
        effect.n_turns -= 1
        if effect.n_turns == 0:
            player.remove_effect(effect)

class Freeze(AbstractCard):
    CARD_TYPE = "Freeze"
    NAME = "Freeze"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = "freeze.png"
    CAN_BE_ON_PICKUP = False
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Choose a player to have their turn skipped for 3 turns."

    def play_card(self, player):
        options = {}

        for other_player in self.game.players:
            if other_player != player:
                options[other_player.get_id()] = other_player.get_name() + \
                    "(" + str(len(other_player.hand)) + ")"

        if len(options) == 0:
            return

        player_id = player.ask(
            "Pick a player to freeze for 3 turns:",
            options,
            allow_cancel=False,
            image=self.get_url()
        )
        chosen_player = self.game.get_player(player_id)

        effect = chosen_player.get_effect("Freeze")
        
        if effect is None:
            effect = FreezeEffect(chosen_player, 3)
            chosen_player.add_effect(effect)
        else:
            effect.n_turns += 3