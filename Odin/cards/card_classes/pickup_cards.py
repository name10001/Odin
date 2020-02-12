from cards.abstract_card import AbstractCard
from cards import CopyCat
from cards.card_frequency import CardFrequency
from decimal import Decimal

from flask import url_for
import math

# ~~~~~~~~~~~~~~
#    Pickup2
# ~~~~~~~~~~~~~~


class Pickup2(AbstractCard):
    CARD_FREQUENCY = CardFrequency(2.75, 2.25, 1.2, 0.6, starting=0)
    CARD_TYPE = "+2"
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "Begins, or continues a pickup chain by adding 2 to the pickup chain value."

    def prepare_card(self, player, allow_cancel):
        self.game.pickup += 2
        return True

    def undo_prepare_card(self, player):
        self.game.pickup -= 2


class BluePickup2(Pickup2):
    NAME = "Blue Pickup 2"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'pickup2_blue.png'


class GreenPickup2(Pickup2):
    NAME = "Green Pickup 2"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'pickup2_green.png'


class PurplePickup2(Pickup2):
    NAME = "Purple Pickup 2"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'pickup2_purple.png'


class RedPickup2(Pickup2):
    NAME = "Red Pickup 2"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'pickup2_red.png'


class WhitePickup2(Pickup2):
    NAME = "White Pickup 2"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'pickup2_white.png'


class BlackPickup2(Pickup2):
    NAME = "Black Pickup 2"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'pickup2_wild.png'


class YellowPickup2(Pickup2):
    NAME = "Yellow Pickup 2"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'pickup2_yellow.png'


# ~~~~~~~~~~~~~~
# Other pickups
# ~~~~~~~~~~~~~~


class Pickup10(AbstractCard):
    CARD_FREQUENCY = CardFrequency(3, 2, 1, 0.5, starting=0)
    CARD_TYPE = "+10"
    NAME = "Pickup 10"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'pickup10_wild.png'
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Begins, or continues a pickup chain by adding 10 to the pickup chain value."

    def prepare_card(self, player, allow_cancel):
        self.game.pickup += 10
        return True

    def undo_prepare_card(self, player):
        self.game.pickup -= 10


class Pickup100(AbstractCard):
    CARD_FREQUENCY = CardFrequency(0.1, 0.05, 0.05, 0.01, starting=0)
    CARD_TYPE = "+100"
    NAME = "Pickup 100"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'pickup100_wild.png'
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Begins, or continues a pickup chain by adding 100 to the pickup chain value."

    def prepare_card(self, player, allow_cancel):
        self.game.pickup += 100
        return True

    def undo_prepare_card(self, player):
        self.game.pickup -= 100


class Pickup4(AbstractCard):
    CARD_FREQUENCY = CardFrequency(6, 4, 2, 1, starting=0)
    CARD_TYPE = "+4"
    NAME = "Pickup 4"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'pickup4_wild.png'
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Begins, or continues a pickup chain by adding 4 to the pickup chain value."

    def prepare_card(self, player, allow_cancel):
        self.game.pickup += 4
        return True

    def undo_prepare_card(self, player):
        self.game.pickup -= 4


class PickupTimes2(AbstractCard):
    CARD_FREQUENCY = CardFrequency(4, 2, 1, 0.5, starting=0)
    CARD_TYPE = "x2"
    NAME = "Pickup x2"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'multiply2_wild.png'
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "If a pickup chain is active, this card will double the pickup chain's value. " \
                         "If played outside of a pickup chain this will do nothing."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_pickup = None

    def prepare_card(self, player, allow_cancel):
        self.old_pickup = self.game.pickup
        self.game.pickup *= 2
        return True

    def undo_prepare_card(self, player):
        if self.old_pickup is not None:
            self.game.pickup = self.old_pickup


class PickupPower2(AbstractCard):
    CARD_FREQUENCY = CardFrequency(0.1, 0.05, 0.05, 0.01, starting=0)
    CARD_TYPE = "x Squared"
    NAME = "Pickup x Squared"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'power2_wild.png'
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "If a pickup chain is active, this card will square the pickup chain's value. " \
                         "If played outside of a pickup chain this will do nothing."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_pickup = None

    def prepare_card(self, player, allow_cancel):
        self.old_pickup = self.game.pickup
        # Only way of checking for "infinite" numbers that seemed to work
        if '%.2E' % Decimal(self.game.pickup) == "INF":
            return True
        self.game.pickup *= self.game.pickup
        return True

    def undo_prepare_card(self, player):
        if self.old_pickup is not None:
            # float conversion doesn't work on very large numbers so we have to do this
            self.game.pickup = self.old_pickup


class PickupFactorial(AbstractCard):
    CARD_FREQUENCY = CardFrequency(0.01, 0.005, 0.005, 0.001, starting=0)
    CARD_TYPE = "Factorial"
    NAME = "Pickup Factorial"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'factorial.png'
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "If a pickup chain is active, this card will take the factorial of the pickup chain's value. "\
                         "If played outside of a pickup chain this will begin a pickup chain of value 1, since 0! = 1."
    MAX_FACTORIAL = 171  # 171! is when it reaches infinity

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_pickup = None

    def prepare_card(self, player, allow_cancel):
        self.old_pickup = self.game.pickup
        if self.game.pickup > self.MAX_FACTORIAL:
            self.game.pickup = self.MAX_FACTORIAL

        self.game.pickup = math.factorial(self.game.pickup)
        return True

    def undo_prepare_card(self, player):
        if self.old_pickup is not None:
            self.game.pickup = self.old_pickup


class AtomicBomb(AbstractCard):
    CARD_FREQUENCY = CardFrequency(
        0, 0.5, 1, 1, starting=0, elevator=0, max_cards=1)
    NAME = "Atomic Bomb"
    CARD_TYPE = "Atomic Bomb"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = "explosion.png"
    PICKUP_CARDS = ["Atomic Bomb", "^2", "+2", "+4", "+10", "+100", "x2",
                    "x Squared", "Factorial", "Plus", "Fuck You", "Copy Cat", "Pawn"]
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Allows you to place as many pickup cards as you like with this card on your turn."

    def can_play_with(self, player, card, is_first_card):
        return card.get_type() in self.PICKUP_CARDS


class Pawn(AbstractCard):
    NAME = "Pawn"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'pawn.png'
    CARD_FREQUENCY = CardFrequency(0.5, starting=0, elevator=0, max_cards=1)
    CARD_TYPE = "Pawn"
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "Ends a pickup chain and causes no one to pickup."
    COMPATIBILITY_DESCRIPTION = "This card can ONLY be used on a pickup chain. " \
                                "During a pickup chain, regular black rules apply such that this " \
                                "is compatible with any red, green, blue, yellow or black cards."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_pickup = 0

    def can_be_played_on(self, player, card):
        """
        Update method which only lets you place when it's a pickup chain
        """
        if self.game.pickup == 0:  # won't let you place outside of pickup chain
            return False
        return super().can_be_played_on(player, card)

    def prepare_card(self, player, allow_cancel):
        self.old_pickup = self.game.pickup
        self.game.pickup = 0
        return True

    def undo_prepare_card(self, player):
        self.game.pickup = self.old_pickup


class Plus(AbstractCard):
    NAME = "Plus"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'plus_wild.png'
    CARD_FREQUENCY = CardFrequency(0.75, 0.75, 0.5, 0.25, starting=0)
    CARD_TYPE = "Plus"
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "If you play this card inside a pickup chain, everyone except yourself " \
                         "will be forced to pickup the pickup chain value. Outside of a pickup chain, " \
                         "everyone except yourself is forced to pickup 2 cards."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pickup_amount = 0
        self.old_pickup = 0

    def prepare_card(self, player, allow_cancel):
        self.old_pickup = self.game.pickup
        self.pickup_amount = self.game.pickup

        played_on = self.game.get_top_card()

        # allows you to place multiple and duplicate the effects
        if hasattr(played_on, 'pickup_amount'):
            self.pickup_amount = played_on.pickup_amount
        elif isinstance(played_on, CopyCat):  # copycat copy pickup amount
            if hasattr(played_on.copied, 'pickup_amount'):
                self.pickup_amount = played_on.copied.pickup_amount

        if self.pickup_amount == 0:
            self.pickup_amount = 2

        self.game.pickup = 0

        for other_player in self.game.players:
            if other_player != player:
                other_player.player_pickup_amount += self.pickup_amount

        return True

    def undo_prepare_card(self, player):
        self.game.pickup = self.old_pickup

        for other_player in self.game.players:
            if other_player != player:
                other_player.player_pickup_amount -= self.pickup_amount

    def play_card(self, player):
        player.refresh_card_play_animation()
        for other_player in self.game.players:
            if other_player != player:
                other_player.pickup(self.pickup_amount)

        self.pickup_amount = 0  # prevent people from duplicating the pickup amount


class FuckYou(AbstractCard):
    NAME = "Fuck You"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'fuck_you.png'
    CARD_FREQUENCY = CardFrequency(2, 1.5, 1, 0.15, starting=0)
    CARD_TYPE = "Fuck You"
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "If you play this card inside a pickup chain, one person of your choosing will be " \
                         "forced to pickup the pickup chain value. Outside of a pickup chain, " \
                         "the person of your choosing is forced to pickup 5 cards."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pickup_amount = 0
        self.old_pickup = 0
        self.chosen_player = None

    def prepare_card(self, player, allow_cancel):
        self.old_pickup = self.game.pickup
        self.pickup_amount = self.game.pickup

        played_on = self.game.get_top_card()

        # allows you to place multiple and duplicate the effects
        if hasattr(played_on, 'pickup_amount'):
            self.pickup_amount = played_on.pickup_amount
        elif isinstance(played_on, CopyCat):  # copycat copy pickup amount
            if hasattr(played_on.copied, 'pickup_amount'):
                self.pickup_amount = played_on.copied.pickup_amount

        if self.pickup_amount == 0:
            self.pickup_amount = 5

        options = {}

        for other_player in self.game.players:
            if other_player != player:
                options[other_player.get_id()] = other_player.get_name() + \
                    "(" + str(len(other_player.hand)) + ")"

        if len(options) > 0:
            chosen_player_id = player.ask(
                "Select player to pickup cards:",
                options,
                allow_cancel=allow_cancel,
                image=self.get_url()
            )
            if chosen_player_id is None:
                self.chosen_player = None
                return False

            self.chosen_player = self.game.get_player(chosen_player_id)
            self.chosen_player.player_pickup_amount += self.pickup_amount
        else:
            self.chosen_player = None

        self.game.pickup = 0

        return True

    def undo_prepare_card(self, player):
        self.game.pickup = self.old_pickup

        if self.chosen_player is not None:
            self.chosen_player.player_pickup_amount -= self.pickup_amount

    def play_card(self, player):
        if len(self.game.players) == 1:
            return None

        if self.chosen_player is not None:
            player.refresh_card_play_animation()
            self.chosen_player.pickup(self.pickup_amount)

        self.pickup_amount = 0
