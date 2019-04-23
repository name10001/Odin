from cards.abstract_card import AbstractCard
from cards.card_frequency import CardFrequency
import random
import math
from flask import *
from decimal import Decimal
import settings

# ~~~~~~~~~~~~~~
#    Reverse
# ~~~~~~~~~~~~~~


class Reverse(AbstractCard):
    CARD_FREQUENCY = CardFrequency(2.2, 2)
    CARD_COLOUR = "blue"
    CARD_TYPE = "Reverse"
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "Reverses the direction of play."

    def prepare_card(self, player):
        self.game.direction *= -1
    
    def undo_prepare_card(self, player):
        self.game.direction *= -1


class BlueReverse(Reverse):
    NAME = "Blue Reverse"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/reverse_blue.png'


class GreenReverse(Reverse):
    NAME = "Green Reverse"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/reverse_green.png'


class PurpleReverse(Reverse):
    NAME = "Purple Reverse"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'cards/reverse_purple.png'


class RedReverse(Reverse):
    NAME = "Red Reverse"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/reverse_red.png'


class WhiteReverse(Reverse):
    NAME = "White Reverse"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/reverse_white.png'


class BlackReverse(Reverse):
    NAME = "Black Reverse"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/reverse_wild.png'


class YellowReverse(Reverse):
    NAME = "Yellow Reverse"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/reverse_yellow.png'


# ~~~~~~~~~~~~~~
#    Pickup2
# ~~~~~~~~~~~~~~


class Pickup2(AbstractCard):
    CARD_FREQUENCY = CardFrequency(2.5, 2, 1.5, 0.5)
    CARD_TYPE = "+2"
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "Begins, or continues a pickup chain by adding 2 to the pickup chain value."

    def prepare_card(self, player):
        self.game.pickup += 2
    
    def undo_prepare_card(self, player):
        self.game.pickup -= 2


class BluePickup2(Pickup2):
    NAME = "Blue Pickup 2"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/pickup2_blue.png'


class GreenPickup2(Pickup2):
    NAME = "Green Pickup 2"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/pickup2_green.png'


class PurplePickup2(Pickup2):
    NAME = "Purple Pickup 2"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'cards/pickup2_purple.png'


class RedPickup2(Pickup2):
    NAME = "Red Pickup 2"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/pickup2_red.png'


class WhitePickup2(Pickup2):
    NAME = "White Pickup 2"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/pickup2_white.png'


class BlackPickup2(Pickup2):
    NAME = "Black Pickup 2"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup2_wild.png'


class YellowPickup2(Pickup2):
    NAME = "Yellow Pickup 2"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/pickup2_yellow.png'


# ~~~~~~~~~~~~~~
# Other pickups
# ~~~~~~~~~~~~~~


class Pickup10(AbstractCard):
    CARD_FREQUENCY = CardFrequency(3, 2, 1.5, 0.5)
    CARD_TYPE = "+10"
    NAME = "Pickup 10"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup10_wild.png'
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Begins, or continues a pickup chain by adding 10 to the pickup chain value."

    def prepare_card(self, player):
        self.game.pickup += 10
    
    def undo_prepare_card(self, player):
        self.game.pickup -= 10


class Pickup100(AbstractCard):
    CARD_FREQUENCY = CardFrequency(0.1, 0.05, 0.05, 0.01)
    CARD_TYPE = "+100"
    NAME = "Pickup 100"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup100_wild.png'
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Begins, or continues a pickup chain by adding 100 to the pickup chain value."

    def prepare_card(self, player):
        self.game.pickup += 100

    def undo_prepare_card(self, player):
        self.game.pickup -= 100


class Pickup4(AbstractCard):
    CARD_FREQUENCY = CardFrequency(5, 3, 2, 1)
    CARD_TYPE = "+4"
    NAME = "Pickup 4"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup4_wild.png'
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Begins, or continues a pickup chain by adding 4 to the pickup chain value."

    def prepare_card(self, player):
        self.game.pickup += 4
    
    def undo_prepare_card(self, player):
        self.game.pickup -= 4


class PickupTimes2(AbstractCard):
    CARD_FREQUENCY = CardFrequency(5, 3, 2, 1)
    CARD_TYPE = "x2"
    NAME = "Pickup x2"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/multiply2_wild.png'
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "If a pickup chain is active, this card will double the pickup chain's value. " \
                         + "If played outside of a pickup chain this will do nothing."

    def prepare_card(self, player):
        self.old_pickup = self.game.pickup
        self.game.pickup *= 2
    
    def undo_prepare_card(self, player):
        self.game.pickup = self.old_pickup


class PickupPower2(AbstractCard):
    CARD_FREQUENCY = CardFrequency(0.1, 0.05, 0.05, 0.01)
    CARD_TYPE = "x Squared"
    NAME = "Pickup x Squared"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/power2_wild.png'
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "If a pickup chain is active, this card will square the pickup chain's value. " \
                         + "If played outside of a pickup chain this will do nothing."

    def prepare_card(self, player):
        self.old_pickup = self.game.pickup
        if '%.2E' % Decimal(self.game.pickup) == "INF":  # Only way of checking for "infinite" numbers that seemed to work
            return
        self.game.pickup *= self.game.pickup

    def undo_prepare_card(self, player):
        self.game.pickup = self.old_pickup  # float conversion doesn't work on very large numbers so we have to do this

class PickupFactorial(AbstractCard):
    CARD_FREQUENCY = CardFrequency(0.01, 0.005, 0.005, 0.001)
    CARD_TYPE = "Factorial"
    NAME = "Pickup Factorial"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/factorial.png'
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "If a pickup chain is active, this card will take the factorial of the pickup chain's value. " \
                         + "If played outside of a pickup chain this will begin a pickup chain of value 1, since 0! = 1."
    MAX_FACTORIAL = 171  # 171! is when it reaches infinity

    def prepare_card(self, player):
        self.old_pickup = self.game.pickup
        if self.game.pickup > self.MAX_FACTORIAL:
            self.game.pickup = self.MAX_FACTORIAL
        
        self.game.pickup = math.factorial(self.game.pickup)

    def undo_prepare_card(self, player):
        self.game.pickup = self.old_pickup


# ~~~~~~~~~~~~~~
#    Skip
# ~~~~~~~~~~~~~~


class Skip(AbstractCard):
    CARD_FREQUENCY = CardFrequency(2.2, 2)
    CARD_TYPE = "Skip"
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "Skips the next person's turn."
    
    def prepare_card(self, player):
        self.game.iterate_turn_by += 1
    
    def undo_prepare_card(self, player):
        self.game.iterate_turn_by -= 1


class BlueSkip(Skip):
    NAME = "Blue Skip"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/skip_blue.png'


class GreenSkip(Skip):
    NAME = "Green Skip"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/skip_green.png'


class PurpleSkip(Skip):
    NAME = "Purple Skip"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'cards/skip_purple.png'


class RedSkip(Skip):
    NAME = "Red Skip"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/skip_red.png'


class WhiteSkip(Skip):
    NAME = "White Skip"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/skip_white.png'


class BlackSkip(Skip):
    NAME = "Black Skip"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/skip_wild.png'
    NUMBER_IN_DECK = 1


class YellowSkip(Skip):
    NAME = "Yellow Skip"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/skip_yellow.png'

# ~~~~~~~~~~~~~~
#    Blank
# ~~~~~~~~~~~~~~


class BlankBro(AbstractCard):
    NAME = "Just A Blank Bro"
    CARD_FREQUENCY = CardFrequency(3)
    CARD_TYPE = "Just A Blank Bro"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/black.png'
    MULTI_COLOURED = False


class Happiness(AbstractCard):
    NAME = "Happiness"
    CARD_FREQUENCY = CardFrequency(3)
    CARD_TYPE = "Happiness"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/white.png'
    MULTI_COLOURED = False


# ~~~~~~~~~~~~~~
#      EA
# ~~~~~~~~~~~~~~

class EA(AbstractCard):
    CARD_COLOUR = "black"
    CARD_TYPE = "EA"
    NUMBER_NEEDED = 0
    EFFECT_DESCRIPTION = "Requires a fee to be able to play. You must pay the fee when you pay this card with " \
                         + "any number cards such that they all add up to {cls.NUMBER_NEEDED}."
    MULTI_COLOURED = False

    def __init__(self, game):
        self.still_needs = self.NUMBER_NEEDED
        super().__init__(game)

    def can_play_with(self, player, card, is_first_card):
        if card.get_type() == 'EA':
            return True
        if card.get_type().isnumeric() is False:
            return False
        num = int(card.get_type())
        if self.game.planning_pile[0].still_needs - num < 0:
            return False
        return True

    def ready_to_play(self):
        if self.game.planning_pile[0].still_needs != 0:
            return False, "$" + str(self.game.planning_pile[0].still_needs) + " remaining..."
        else:
            return True, None

    def prepare_card(self, player):
        if len(self.game.planning_pile) == 0:
            return
        if hasattr(self.game.planning_pile[0], 'still_needs'):
            self.game.planning_pile[0].still_needs += self.NUMBER_NEEDED
        else:  # In this case it's either a nazi card or a filthy sharon card. Give the bottom card the "still_needs" attribute.
            self.game.planning_pile[0].still_needs = self.NUMBER_NEEDED
        self.still_needs = 0

    def undo_prepare_card(self, player):
        if len(self.game.planning_pile) == 0:
            return
        self.game.planning_pile[0].still_needs -= self. NUMBER_NEEDED
        self.still_needs = self.NUMBER_NEEDED


class EA15(EA):
    CARD_FREQUENCY = CardFrequency(2,1)
    NAME = "EA $15"
    CARD_IMAGE_URL = 'cards/ea_15.png'
    NUMBER_NEEDED = 15


class EA20(EA):
    CARD_FREQUENCY = CardFrequency(1)
    NAME = "EA $20"
    CARD_IMAGE_URL = 'cards/ea_20.png'
    NUMBER_NEEDED = 20


class EA30(EA):
    CARD_FREQUENCY = CardFrequency(1)
    NAME = "EA $30"
    CARD_IMAGE_URL = 'cards/ea_30.png'
    NUMBER_NEEDED = 30


class EA100(EA):
    CARD_FREQUENCY = CardFrequency(0.05)
    NAME = "EA $100"
    CARD_IMAGE_URL = 'cards/ea_100.png'
    NUMBER_NEEDED = 100


# ~~~~~~~~~~~~~~
#    Fuck
# ~~~~~~~~~~~~~~


class Fuck(AbstractCard):
    CARD_FREQUENCY = CardFrequency(1)
    CARD_TYPE = "Fuckin' M8"
    CARD_COLOUR = "Abstract"
    COMPATIBILITY_DESCRIPTION = "This card is only compatible with other {cls.CARD_COLOUR} cards or " \
                                + "other Fuckin' M8 cards."

    def is_compatible_with(self, player, card):
        if card.get_colour() == "colour swapper":
            return card.COLOUR_1 == self.get_colour() or card.COLOUR_2 == self.get_colour()
        return card.get_colour() == self.get_colour() or card.get_type() == self.get_type()


class BlueFuck(Fuck):
    NAME = "Fuckin' Blue M8"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/fuck_blue.png'


class GreenFuck(Fuck):
    NAME = "Fuckin' Green M8"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/fuck_green.png'


class RedFuck(Fuck):
    NAME = "Fuckin' Red M8"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/fuck_red.png'


class BlackFuck(Fuck):
    NAME = "Fuckin' Black M8"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/fuck_black.png'


class YellowFuck(Fuck):
    NAME = "Fuckin' Yellow M8"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/fuck_yellow.png'


# ~~~~~~~~~~~~~~
# all of same colour
# ~~~~~~~~~~~~~~


class AllOfSameColour(AbstractCard):
    CARD_FREQUENCY = CardFrequency(1, max_cards=1)
    MULTI_COLOURED = False

    def can_play_with(self, player, card, is_first_card):
        return card.get_colour() == self.get_colour()


class ManOfTheDay(AllOfSameColour):
    NAME = "Man Of The Day"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/man_of_the_day.png'
    CARD_TYPE = "Man Of The Day"
    EFFECT_DESCRIPTION = "Allows you to place as many yellow cards as you like with this card on your turn."


class LadyOfTheNight(AllOfSameColour):
    NAME = "Lady Of The Night"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/lady_of_the_night.png'
    CARD_TYPE = "Lady Of The Night"
    EFFECT_DESCRIPTION = "Allows you to place as many red cards as you like with this card on your turn."


class Smurf(AllOfSameColour):
    NAME = "Smurf"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/smurf.png'
    CARD_TYPE = "Smurf"
    EFFECT_DESCRIPTION = "Allows you to place as many blue cards as you like with this card on your turn."


class Creeper(AllOfSameColour):
    NAME = "Creeper"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/creeper.png'
    CARD_TYPE = "Creeper"
    EFFECT_DESCRIPTION = "Allows you to place as many green cards as you like with this card on your turn."


class FilthySharon(AllOfSameColour):
    NAME = "Filthy Sharon"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/filthy_sharon.png'
    CARD_TYPE = "Filthy Sharon"
    EFFECT_DESCRIPTION = "Allows you to place as many white cards as you like with this card on your turn."
        

# ~~~~~~~~~~~~~~
#    Other
# ~~~~~~~~~~~~~~


class Nazi(AbstractCard):
    CARD_FREQUENCY = CardFrequency(0.5, max_cards=1)
    NAME = "Nazi"
    CARD_TYPE = "Nazi"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/nazi.png'
    EFFECT_DESCRIPTION = "Allows you to place as many black cards as you like with this card on your turn."
    COMPATIBILITY_DESCRIPTION = "Before play: This card is only compatible with white cards. " \
                                + "After play: Regular white card rules apply, such that it is compatible with " \
                                + "any red, green, yellow, blue, purple or white cards."

    def can_be_played_on(self, player, card):
        if player.is_turn() is False:
            return False
        if self.game.pickup != 0 and self.can_be_on_pickup() is False:
            return False
        return card.get_colour() == "white"

    def can_play_with(self, player, card, is_first_card):
        return card.get_type() == self.get_type() or card.get_colour() == "black"


class AtomicBomb(AbstractCard):
    CARD_FREQUENCY = CardFrequency(0, 0.5, 1, 1, max_cards=1)
    NAME = "Atomic Bomb"
    CARD_TYPE = "Atomic Bomb"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = "cards/explosion.png"
    PICKUPCARDS = ["Atomic Bomb", "^2", "+2", "+4", "+10", "+100", "x2", "x Squared", "Factorial", "Plus", "Fuck You", "Pawn"]
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Allows you to place as many pickup cards as you like with this card on your turn."

    def can_play_with(self, player, card, is_first_card):
        return card.get_type() in self.PICKUPCARDS


class Pawn(AbstractCard):
    NAME = "Pawn"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pawn.png'
    CARD_FREQUENCY = CardFrequency(0.5, max_cards=1)
    CARD_TYPE = "Pawn"
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "Ends a pickup chain and causes no one to pickup."
    COMPATIBILITY_DESCRIPTION = "This card can ONLY be used on a pickup chain. " \
                                + "During a pickup chain, regular black rules apply such that this " \
                                + "is compatible with any red, green, blue, yellow or black cards."

    def __init__(self, game):
        self.old_pickup = 0
        super().__init__(game)

    def can_be_played_on(self, player, card):
        """
        Update method which only lets you place when it's a pickup chain
        """
        if self.game.pickup == 0:  # won't let you place outside of pickup chain
            return False
        return super().can_be_played_on(player, card)

    def prepare_card(self, player):
        self.old_pickup = self.game.pickup
        self.game.pickup = 0
    
    def undo_prepare_card(self, player):
        self.game.pickup = self.old_pickup


class Communist(AbstractCard):
    NAME = "Communist"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/communist.png'
    CARD_FREQUENCY = CardFrequency(0, 1, max_cards=1)
    CARD_TYPE = "Communist"
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Equally distributes all cards each player has randomly. Remainders are discarded."

    def play_card(self, player):
        # stop the card from playing multiple times
        card_below = self.game.planning_pile.card_below(self)
        if card_below is not None and card_below.get_type() == "Communist":
            return

        all_cards = []
        for player in self.game.players:
            all_cards += player.hand.get_cards()

        random.shuffle(all_cards)

        # remove any remaining cards
        while len(all_cards) % len(self.game.players) != 0:
            all_cards.pop()

        # divide it evenly between everyone
        number_of_cards_each = int(len(all_cards) / len(self.game.players))
        i = 0
        for player in self.game.players:
            player.hand.set_cards(all_cards[i:i+number_of_cards_each])
            i += number_of_cards_each


class Capitalist(AbstractCard):
    NAME = "Capitalist"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/capitalist.png'
    CARD_FREQUENCY = CardFrequency(1, 0.8, 0.1, 0, max_cards=2)
    CARD_TYPE = "Capitalist"
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "The player with the most cards has the amount of cards in their hand doubled."

    def play_card(self, player):
        """
        finds the player with the most cards and doubles it
        """
        # finding richest player
        richest_player = None
        number_of_cards = 0
        for player in self.game.players:
            if len(player.hand) > number_of_cards:
                richest_player = player
                number_of_cards = len(player.hand)

        richest_player.add_new_cards(number_of_cards)


class SwapHand(AbstractCard):
    NAME = "Swap Hand"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/swap_hand.png'
    CARD_FREQUENCY = CardFrequency(0, 10, max_cards=2)
    CARD_TYPE = "Swap Hand"
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Choose a player and you will swap your entire hand with theirs upon play."

    def get_options(self, player):
        for card in self.game.planning_pile:
            if isinstance(card, SwapHand):
                return None

        options = {}
        for other_player in self.game.players:
            if other_player != player:
                options[other_player.get_id()] = other_player.get_name() + "(" + str(len(other_player.hand)) + ")"
        return options

    def play_card(self, player):
        if self.option is None:
            return
        
        if self.is_option_valid(player, self.option, is_player=True) is False:
            print(self.option, "is not a valid option for", self.get_name())
            return
        other_player = self.game.get_player(self.option)
        if other_player is None:
            print("no player of that id was found")
            return

        hand = player.hand
        player.hand = other_player.hand
        other_player.hand = hand


class FeelingBlue(AbstractCard):
    NAME = "Feeling Blue"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/feeling_blue.png'
    CARD_FREQUENCY = CardFrequency(2)
    CARD_TYPE = "Feeling Blue"
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Upon playing this card, you will be forced to pickup 5 cards."

    def play_card(self, player):
        player.add_new_cards(5)


class Plus(AbstractCard):
    NAME = "Plus"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/plus_wild.png'
    CARD_FREQUENCY = CardFrequency(1, 1, 0.5, 0.1)
    CARD_TYPE = "Plus"
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "If you play this card inside a pickup chain, everyone except yourself " \
                         + "will be forced to pickup the pickup chain value. Outside of a pickup chain, " \
                         + "everyone except yourself is forced to pickup 2 cards."

    def __init__(self, game):
        self.pickup_amount = 0
        self.old_pickup = 0
        super().__init__(game)

    def prepare_card(self, player):
        self.old_pickup = self.game.pickup
        self.pickup_amount = self.game.pickup

        played_on = self.game.get_top_card()

        if hasattr(played_on, 'pickup_amount'):  # allows you to place multiple and duplicate the effects
            self.pickup_amount = played_on.pickup_amount
        
        if self.pickup_amount == 0:
            self.pickup_amount = 2
        
        self.game.pickup = 0
    
    def undo_prepare_card(self, player):
        self.game.pickup = self.old_pickup

    def play_card(self, player):
        for other_player in self.game.players:
            if other_player != player:
                other_player.add_new_cards(self.pickup_amount)
        
        self.pickup_amount = 0  # prevent people from duplicating the pickup amount


class FuckYou(AbstractCard):
    NAME = "Fuck You"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/fuck_you.png'
    CARD_FREQUENCY = CardFrequency(2, 1.5, 0.75, 0.15)
    CARD_TYPE = "Fuck You"
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "If you play this card inside a pickup chain, one person of your choosing will be " \
                         + "forced to pickup the pickup chain value. Outside of a pickup chain, " \
                         + "the person of your choosing is forced to pickup 5 cards."

    def __init__(self, game):
        self.pickup_amount = 0
        self.old_pickup = 0
        super().__init__(game)

    def get_options(self, player):
        options = {}
        for other_player in self.game.players:
            if other_player != player:
                options[other_player.get_id()] = other_player.get_name() + "(" + str(len(other_player.hand)) + ")"
        return options

    def prepare_card(self, player):
        self.old_pickup = self.game.pickup
        self.pickup_amount = self.game.pickup

        played_on = self.game.get_top_card()

        if hasattr(played_on, 'pickup_amount'):  # allows you to place multiple and duplicate the effects
            self.pickup_amount = played_on.pickup_amount
        
        if self.pickup_amount == 0:
            self.pickup_amount = 2
        
        self.game.pickup = 0
    
    def undo_prepare_card(self, player):
        self.game.pickup = self.old_pickup

    def play_card(self, player):
        if self.is_option_valid(player, self.option, is_player=True) is False:
            print(self.option, "is not a valid option for", self.get_name())
            return
        other_player = self.game.get_player(self.option)

        other_player.add_new_cards(self.pickup_amount)
        self.pickup_amount = 0


class Genocide(AbstractCard):
    NAME = "Genocide"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/genocide.png'
    CARD_FREQUENCY = CardFrequency(0.4, max_cards=2)
    MULTI_COLOURED = False
    CARD_TYPE = "Genocide"
    EFFECT_DESCRIPTION = "Pick any colour or type of card to entirely removed from the game. " \
                         + "All cards of this colour/type will be removed from everyone's hand " \
                         + "and will never be able to be picked up in the future of this game."
    UNBANNABLE_COLOURS = ["black","colour swapper"]  # colour swapper is banned by type instead
    UNBANNABLE_TYPES = []

    def get_options(self, player):
        options = {}
        for card_colour in self.game.deck.all_colours:
            if card_colour not in self.UNBANNABLE_COLOURS:
                options["colour " + card_colour] = "Colour: " + card_colour.capitalize()
        for card_type in self.game.deck.all_types:
            if card_type not in self.UNBANNABLE_TYPES:
                options["type " + card_type] = "Type: " + card_type
        return options

    def prepare_card(self, player):
        """
        This will update the list of available cards
        """
        self.old_cards = self.game.deck.cards.copy()

        if self.is_option_valid(player, self.option) is False:
            print(self.option, "is not a valid option for", self.get_name())
            return

        category, to_ban = self.option.split(' ', 1)

        # remove from deck and players hands
        if category == "type":
            self.game.deck.ban_type(to_ban)
        elif category == "colour":
            self.game.deck.ban_colour(to_ban)
        else:
            print("Warning: got unknown category:", category)
    
    def undo_prepare_card(self, player):        
        self.game.deck.set_cards(self.old_cards)
    
    def play_card(self, player):
        """
        On play this will remove all the types from everyone's hands
        """
        category, to_ban = self.option.split(' ', 1)

        # remove from deck and players hands
        if category == "type":
            for game_player in self.game.players:
                game_player.hand.remove_type(to_ban)
        elif category == "colour":
            for game_player in self.game.players:
                game_player.hand.remove_colour(to_ban)
        else:
            print("Warning: got unknown category:", category)


class Jesus(AbstractCard):
    NAME = "Jesus"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/jesus.png'
    CARD_FREQUENCY = CardFrequency(1, 1, 0.5, 0.5, max_cards=2)
    CARD_TYPE = "Jesus"
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Choose any person (including yourself) to reset their entire hand " \
                         + "back to a value of 15 cards."

    def get_options(self, player):
        options = {}
        for other_player in self.game.players:
            if other_player != player:
                options[other_player.get_id()] = other_player.get_name() + "(" + str(len(other_player.hand)) + ")"
            else:
                options[other_player.get_id()] = other_player.get_name() + "(You)"

        return options

    def play_card(self, player):
        if self.is_option_valid(player, self.option, is_player=True) is False:
            print(self.option, "is not a valid option for", self.get_name())
            return

        other_player = self.game.get_player(self.option)
        other_player.hand.clear()
        other_player.add_new_cards(settings.jesus_card_number)


class FreeTurn(AbstractCard):
    CARD_FREQUENCY = CardFrequency(4, 3, 1, 1, max_cards=4)
    CARD_TYPE = "Free Turn"
    NAME = "Free Turn"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/free_turn.png'
    CAN_BE_ON_PICKUP = True
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Gain an extra turn. If you play multiple Free Turn cards together " \
                         + "you will gain multiple extra turns."

    def prepare_card(self, player):
        player.turns_left += 1

    def undo_prepare_card(self, player):
        player.turns_left -= 1


class Odin(AbstractCard):
    NAME = "Odin"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/back.png'
    CARD_FREQUENCY = CardFrequency(20, max_cards=3)
    CARD_TYPE = "Odin"
    MULTI_COLOURED = False
    COMPATIBILITY_DESCRIPTION = "Can only be played as your last card. When it becomes your last card, regular black card rules apply, such that it can be played on red, green, yellow blue and black cards."

    def can_be_played_on(self, player, card):
        if player.is_turn() is False:
            return False
        if self.game.pickup != 0 and self.can_be_on_pickup() is False:
            return False
        
        for your_card in player.hand:
            if not isinstance(your_card, Odin):
                return False

        return card.is_compatible_with(player, self) and self.is_compatible_with(player, card)


class Thanos(AbstractCard):
    NAME = "Thanos"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'cards/thanos.png'
    CARD_FREQUENCY = CardFrequency(0, 0, 1, 1, max_cards=2)
    CARD_TYPE = "Thanos"
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Upon play, half of the cards in your hand will randomly disappear."

    def play_card(self, player):
        """
        removes half the players cards at random
        """
        total = len(player.hand)
        num_to_remove = math.floor(total/2)
        for i in range(0, num_to_remove):
            index = random.randrange(0, total)
            player.hand.remove_card(index=index)
            total -= 1


class CopyCat(AbstractCard):
    NAME = "Copy Cat"
    CARD_IMAGE_URL = 'cards/copy_cat.png'
    CARD_FREQUENCY = CardFrequency(3, 2, 1, 1, max_cards=3)
    MULTI_COLOURED = False
    CARD_COLOUR = "black"  # keep this as black, otherwise it shows up as Abstract in the genocide card
    CARD_TYPE = "Copy Cat"
    EFFECT_DESCRIPTION = "When you play this card, it becomes whatever card it is placed on and all effects apply for that card."
    COMPATIBILITY_DESCRIPTION = "Can be played on any card. After play, the compatibility rules of the card below are copied."
    CAN_BE_ON_PICKUP = True

    def __init__(self, game):
        super().__init__(game)
        self.copied = None
        self.colour = "black"
        self.type = "Copy Cat"

    def can_be_played_on(self, player, card):
        return player.is_turn()
    
    def prepare_card(self, player):
        top_card = self.game.get_top_card()
        if isinstance(top_card, CopyCat):
            copy_class = top_card.copied.__class__
        else:
            copy_class = top_card.__class__
        self.copied = copy_class(self.game)  # copied card is re-initialized
        self.copied.set_option(self.option)
        self.copied.prepare_card(player)

    def undo_prepare_card(self, player):
        self.copied.undo_prepare_card(player)
        self.copied = None
    
    def play_card(self, player):
        self.copied.play_card(player)
        self.colour = self.copied.get_colour()
        self.type = self.copied.get_type()
    
    def ready_to_play(self):
        return self.copied.ready_to_play()
    
    def can_play_with(self, player, card, is_first_card):
        """
        Can play with other copycats and whatever the copyed card can be played with
        """
        return isinstance(card, CopyCat) or self.copied.can_play_with(player, card, is_first_card)
    
    def is_compatible_with(self, player, card):
        if self.copied is None:
            return True
        else:
            return self.copied.is_compatible_with(player, card)

    def get_options(self, player):
        if self.copied is not None:
            return self.copied.get_options(player)
        elif self.game.get_top_card() is self:  # needed for when game starts with a copy cat card on the played pile
            return None
        else:
            return self.game.get_top_card().get_options(player)

    def get_colour(self):
        return self.colour

    def get_type(self):
        return self.type


class ColourChooser(AbstractCard):
    NAME = "Colour Chooser"
    CARD_IMAGE_URL = 'cards/color_swapper.png'
    CARD_COLOUR = "black"
    CARD_FREQUENCY = CardFrequency(4)
    CARD_TYPE = "Colour Chooser"
    EFFECT_DESCRIPTION = "Allows you to change the colour to any of the 4 given colours: red, green, yellow or blue."
    COMPATIBILITY_DESCRIPTION = "Before play: Regular black card, compatible with any black, red, green, blue or " \
                                + "yellow cards. After play: Compatible any cards of the colour picked and black cards."
    ADDITIONAL_URLS = ['cards/choose_yellow.png','cards/choose_blue.png','cards/choose_red.png','cards/choose_green.png']

    def __init__(self, game):
        super().__init__(game)
        self.colour = "black"
        self.url = self.CARD_IMAGE_URL

    def get_options(self, player):
        return {
            "red": "Red",
            "green": "Green",
            "blue": "Blue",
            "yellow": "Yellow"
        }
    
    def is_compatible_with(self, player, card):
        """
        This compatibility method is used to prevent white cards from being able to be played on top
        """
        if card.get_colour() == "white" or card.get_colour() == "purple":
            return False
        else:
            return True

    def prepare_card(self, player):
        if self.is_option_valid(player, self.option) is False:
            print(self.option, "is not a valid option for", self.get_name())
            return
        self.colour = self.option
        self.url = 'cards/choose_' + self.option + '.png'

    def undo_prepare_card(self, player):
        self.url = self.CARD_IMAGE_URL
        self.colour = "black"

    def get_colour(self):
        return self.colour
    
    def get_url(self):
        return url_for('static', filename=escape(self.url))
    

class ColourSwapper(AbstractCard):
    """
    Abstract double-colour swapper card
    """
    CARD_FREQUENCY = CardFrequency(1)
    CARD_TYPE = "Colour Swapper"
    COLOUR_1 = "black"
    COLOUR_2 = "black"
    CARD_COLOUR = "colour swapper"
    EFFECT_DESCRIPTION = "When played on one of the colours shown on the card, this card will swap to the " \
                         + "opposite card. If played on a colour that is not shown on the card " \
                         + "you get to choose the colour it switches to."
    COMPATIBILITY_DESCRIPTION = "Before play: Compatible with any {cls.COLOUR_1}, {cls.COLOUR_2}, white or black cards. \n" \
                                + "After play: Compatible with any cards of the chosen colour, white or black cards. " \
                                + "Note: when playing multiple, the colours must be compatible too."

    def __init__(self, game):
        super().__init__(game)
        self.colour = "colour swapper"  # gets changed to a particular colour after being played
        self.url = self.CARD_IMAGE_URL

    def get_options(self, player):
        # get the top card
        top_card = self.game.get_top_card()

        if self.colours_are_compatible(top_card.get_colour(), self.COLOUR_1) \
                and self.colours_are_compatible(top_card.get_colour(), self.COLOUR_2):
            # if both colours are compatible with the bottom, then you get to choose the outcome
            return {
                self.COLOUR_1: self.COLOUR_1.capitalize(),
                self.COLOUR_2: self.COLOUR_2.capitalize(),
            }
        else:
            return None

    def is_compatible_with(self, player, card):
        if self.colour == "colour swapper":  # compatible if either of the card colours are compatible
            if self.colours_are_compatible(card.get_colour(), self.COLOUR_1) \
                    or self.colours_are_compatible(card.get_colour(), self.COLOUR_2):
                return True
        else:
            return super().is_compatible_with(player, card)

    def prepare_card(self, player):
        played_on = self.game.get_top_card()

        # change colour to the opposite of the one you played on
        first_compatible = self.colours_are_compatible(played_on.get_colour(), self.COLOUR_1)
        second_compatible = self.colours_are_compatible(played_on.get_colour(), self.COLOUR_2)
        if first_compatible and not second_compatible:
            self.colour = self.COLOUR_2
        elif second_compatible and not first_compatible:
            self.colour = self.COLOUR_1
        else:
            if self.is_option_valid(player, self.option) is False:
                print(self.option, "is not a valid option for", self.get_name())
                return
            self.colour = self.option
        
        self.url = 'cards/switch_' + self.colour + '.png'
    
    def undo_prepare_card(self, player):
        self.colour = "colour swapper"
        self.url = self.CARD_IMAGE_URL

    def get_colour(self):
        return self.colour
    
    def can_be_played_with(self, player):
        """
        Can only play multiple if the card is compatible with the top card in the planning pile
        """
        card = self.game.planning_pile.get_top_card()

        if card.get_type() != self.get_type():
            return False
        
        return self.colours_are_compatible(card.get_colour(), self.COLOUR_1) \
            or self.colours_are_compatible(card.get_colour(), self.COLOUR_2)
    
    def get_url(self):
        return url_for('static', filename=escape(self.url))

    @staticmethod
    def colours_are_compatible(colour_1, colour_2):
        if colour_1 == colour_2:
            return True
        elif colour_1 == "white":
            return colour_2 != "black"
        elif colour_1 == "black":
            return colour_2 != "white" and colour_2 != "purple"
        elif colour_1 == "purple":
            return colour_2 == "white"
        else:
            return colour_2 == "white" or colour_2 == "black"


class RedBlueSwapper(ColourSwapper):
    NAME = "Red/Blue Colour Swapper"
    CARD_IMAGE_URL = 'cards/blue_red.png'
    COLOUR_1 = "red"
    COLOUR_2 = "blue"


class RedYellowSwapper(ColourSwapper):
    NAME = "Red/Yellow Colour Swapper"
    CARD_IMAGE_URL = 'cards/red_yellow.png'
    COLOUR_1 = "red"
    COLOUR_2 = "yellow"


class RedGreenSwapper(ColourSwapper):
    NAME = "Red/Green Colour Swapper"
    CARD_IMAGE_URL = 'cards/green_red.png'
    COLOUR_1 = "red"
    COLOUR_2 = "green"


class GreenBlueSwapper(ColourSwapper):
    NAME = "Green/Blue Colour Swapper"
    CARD_IMAGE_URL = 'cards/green_blue.png'
    COLOUR_1 = "green"
    COLOUR_2 = "blue"


class BlueYellowSwapper(ColourSwapper):
    NAME = "Yellow/Blue Colour Swapper"
    CARD_IMAGE_URL = 'cards/yellow_blue.png'
    COLOUR_1 = "yellow"
    COLOUR_2 = "blue"


class YellowGreenSwapper(ColourSwapper):
    NAME = "Yellow/Green Colour Swapper"
    CARD_IMAGE_URL = 'cards/green_yellow.png'
    COLOUR_1 = "yellow"
    COLOUR_2 = "green"


class BlackWhiteSwapper(ColourSwapper):
    NAME = "Black/White Colour Swapper"
    CARD_FREQUENCY = CardFrequency(1.5)
    CARD_IMAGE_URL = 'cards/black_white.png'
    COLOUR_1 = "black"
    COLOUR_2 = "white"
    COMPATIBILITY_DESCRIPTION = "Before play: Compatible with all colours. " \
                                + "After play: Depends on the colour you selected. Black is compatible with any red, " \
                                + "blue, green, yellow and black cards. " \
                                + "White is compatible with any red, blue, green, yellow, purple and white cards. "
    ADDITIONAL_URLS = ['cards/switch_black.png','cards/switch_white.png','cards/switch_red.png','cards/switch_yellow.png','cards/switch_green.png','cards/switch_blue.png']
