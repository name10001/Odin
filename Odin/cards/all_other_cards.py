from cards.abstract_card import AbstractCard
import cards
import random
import math
from time import time

# ~~~~~~~~~~~~~~
#    Reverse
# ~~~~~~~~~~~~~~


class Reverse(AbstractCard):
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "blue"
    CARD_TYPE = "Reverse"
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "Reverses the direction of play."

    def play_card(self, player, options, played_on):
        self.game.direction *= -1


class BlueReverse(Reverse):
    NAME = "Blue Reverse"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/reverse_blue.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"Reverse")


class GreenReverse(Reverse):
    NAME = "Green Reverse"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/reverse_green.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"Reverse")


class PurpleReverse(Reverse):
    NAME = "Purple Reverse"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'cards/reverse_purple.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"Reverse")


class RedReverse(Reverse):
    NAME = "Red Reverse"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/reverse_red.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"Reverse")


class WhiteReverse(Reverse):
    NAME = "White Reverse"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/reverse_white.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"Reverse")


class BlackReverse(Reverse):
    NAME = "Black Reverse"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/reverse_wild.png'
    NUMBER_IN_DECK = 1
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"Reverse")


class YellowReverse(Reverse):
    NAME = "Yellow Reverse"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/reverse_yellow.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"Reverse")


# ~~~~~~~~~~~~~~
#    Pickup2
# ~~~~~~~~~~~~~~


class Pickup2(AbstractCard):
    NUMBER_IN_DECK = 2
    CARD_TYPE = "+2"
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "Begins, or continues a pickup chain by adding 2 to the pickup chain value."

    def prepare_card(self, player, options, played_on):
        self.game.pickup += 2
    
    def undo_prepare_card(self, player, played_on):
        self.game.pickup -= 2


class BluePickup2(Pickup2):
    NAME = "Blue Pickup 2"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/pickup2_blue.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"+2")


class GreenPickup2(Pickup2):
    NAME = "Green Pickup 2"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/pickup2_green.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"+2")


class PurplePickup2(Pickup2):
    NAME = "Purple Pickup 2"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'cards/pickup2_purple.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"+2")


class RedPickup2(Pickup2):
    NAME = "Red Pickup 2"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/pickup2_red.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"+2")


class WhitePickup2(Pickup2):
    NAME = "White Pickup 2"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/pickup2_white.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"+2")


class BlackPickup2(Pickup2):
    NAME = "Black Pickup 2"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup2_wild.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"+2")
    NUMBER_IN_DECK = 3


class YellowPickup2(Pickup2):
    NAME = "Yellow Pickup 2"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/pickup2_yellow.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"+2")


# ~~~~~~~~~~~~~~
# Other pickups
# ~~~~~~~~~~~~~~


class Pickup10(AbstractCard):
    NUMBER_IN_DECK = 2
    CARD_TYPE = "+10"
    NAME = "Pickup 10"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup10_wild.png'
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "Begins, or continues a pickup chain by adding 10 to the pickup chain value."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)

    def prepare_card(self, player, options, played_on):
        self.game.pickup += 10
    
    def undo_prepare_card(self, player, played_on):
        self.game.pickup -= 10


class Pickup4(AbstractCard):
    NUMBER_IN_DECK = 4
    CARD_TYPE = "+4"
    NAME = "Pickup 4"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup4_wild.png'
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "Begins, or continues a pickup chain by adding 4 to the pickup chain value."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


    def prepare_card(self, player, options, played_on):
        self.game.pickup += 4
    
    def undo_prepare_card(self, player, played_on):
        self.game.pickup -= 4


class PickupTimes2(AbstractCard):
    NUMBER_IN_DECK = 4
    CARD_TYPE = "x2"
    NAME = "Pickup x2"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/multiply2_wild.png'
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "If a pickup chain is active, this card will double the pickup chain's value. If played outside of a pickup chain this will do nothing."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)

    def prepare_card(self, player, options, played_on):
        self.game.pickup *= 2
    
    def undo_prepare_card(self, player, played_on):
        self.game.pickup /= 2


# ~~~~~~~~~~~~~~
#    Skip
# ~~~~~~~~~~~~~~


class Skip(AbstractCard):
    NUMBER_IN_DECK = 2
    CARD_TYPE = "Skip"
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "Skips the next person's turn."
    
    def play_card(self, player, options, played_on):
        self.game.iterate_turn_by += 1


class BlueSkip(Skip):
    NAME = "Blue Skip"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/skip_blue.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"Skip")


class GreenSkip(Skip):
    NAME = "Green Skip"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/skip_green.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"Skip")


class PurpleSkip(Skip):
    NAME = "Purple Skip"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'cards/skip_purple.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"Skip")


class RedSkip(Skip):
    NAME = "Red Skip"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/skip_red.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"Skip")


class WhiteSkip(Skip):
    NAME = "White Skip"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/skip_white.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"Skip")


class BlackSkip(Skip):
    NAME = "Black Skip"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/skip_wild.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"Skip")
    NUMBER_IN_DECK = 1


class YellowSkip(Skip):
    NAME = "Yellow Skip"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/skip_yellow.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,"Skip")

# ~~~~~~~~~~~~~~
#    Blank
# ~~~~~~~~~~~~~~


class BlankBro(AbstractCard):
    NAME = "Just A Blank Bro"
    NUMBER_IN_DECK = 3
    CARD_TYPE = "Just A Blank Bro"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/black.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class Happiness(AbstractCard):
    NAME = "Happiness"
    NUMBER_IN_DECK = 3
    CARD_TYPE = "Happiness"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/white.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


# ~~~~~~~~~~~~~~
#      EA
# ~~~~~~~~~~~~~~

class EA(AbstractCard):
    CARD_COLOUR = "black"
    NUMBER_IN_DECK = 1
    CARD_TYPE = "EA"
    NUMBER_NEEDED = 0
    EFFECT_DESCRIPTION = "This card hasn't even been implemented properly so it does nothing at the moment."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)

    #TODO implement this card properly, this will just be a blank at the moment

    #def can_be_played_on(self, card, player):
    #    """
    #    Must have enough cards in hand
    #    """
    #    if len(player.get_hand()) < self.NUMBER_NEEDED:
    #        return False
    #    else:
    #        return super().can_be_played_on(card, player)

    #def can_be_played_with(self, card, player):
    #    """
    #    Must have enough cards in hand
    #    """
    #    if len(player.get_hand()) < self.NUMBER_NEEDED:
    #        return False
    #    else:
    #        return super().can_be_played_with(card, player)


class EA15(EA):
    NAME = "EA $15"
    CARD_IMAGE_URL = 'cards/ea_15.png'
    NUMBER_NEEDED = 15


class EA20(EA):
    NAME = "EA $20"
    CARD_IMAGE_URL = 'cards/ea_20.png'
    NUMBER_NEEDED = 20


class EA30(EA):
    NAME = "EA $30"
    CARD_IMAGE_URL = 'cards/ea_30.png'
    NUMBER_NEEDED = 30


# ~~~~~~~~~~~~~~
#    Fuck
# ~~~~~~~~~~~~~~


class Fuck(AbstractCard):
    NUMBER_IN_DECK = 1
    CARD_TYPE = "Fuckin' M8"

    def is_compatible_with(self, card, player):
        if card.get_colour() == "colour swapper":
            return card.COLOUR_1 == self.get_colour() or card.COLOUR_2 == self.get_colour()
        return card.get_colour() == self.get_colour() or card.get_type() == self.get_type()


class BlueFuck(Fuck):
    NAME = "Fuckin' Blue M8"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/fuck_blue.png'
    COMPATIBILITY_DESCRIPTION = "This card is only compatible with other blue cards. However, this is always compatible and can be played with other Fuckin' M8 cards"


class GreenFuck(Fuck):
    NAME = "Fuckin' Green M8"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/fuck_green.png'
    COMPATIBILITY_DESCRIPTION = "This card is only compatible with other green cards. However, this is always compatible and can be played with other Fuckin' M8 cards"


class RedFuck(Fuck):
    NAME = "Fuckin' Red M8"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/fuck_red.png'
    COMPATIBILITY_DESCRIPTION = "This card is only compatible with other red cards. However, this is always compatible and can be played with other Fuckin' M8 cards"


class BlackFuck(Fuck):
    NAME = "Fuckin' Black M8"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/fuck_black.png'
    COMPATIBILITY_DESCRIPTION = "This card is only compatible with other black cards. However, this is always compatible and can be played with other Fuckin' M8 cards"


class YellowFuck(Fuck):
    NAME = "Fuckin' Yellow M8"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/fuck_yellow.png'
    COMPATIBILITY_DESCRIPTION = "This card is only compatible with other yellow cards. However, this is always compatible and can be played with other Fuckin' M8 cards"


# ~~~~~~~~~~~~~~
# all of same colour
# ~~~~~~~~~~~~~~


class AllOfSameColour(AbstractCard):
    NUMBER_IN_DECK = 1

    def can_play_with(self, card, player, is_first_card):
        return card.get_colour() == self.get_colour()


class ManOfTheDay(AllOfSameColour):
    NAME = "Man Of The Day"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/man_of_the_day.png'
    CARD_TYPE = "Man Of The Day"
    EFFECT_DESCRIPTION = "Allows you to place as many yellow cards as you like with this card on your turn."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class LadyOfTheNight(AllOfSameColour):
    NAME = "Lady Of The Night"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/lady_of_the_night.png'
    CARD_TYPE = "Lady Of The Night"
    EFFECT_DESCRIPTION = "Allows you to place as many red cards as you like with this card on your turn."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class Smurf(AllOfSameColour):
    NAME = "Smurf"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/smurf.png'
    CARD_TYPE = "Smurf"
    EFFECT_DESCRIPTION = "Allows you to place as many blue cards as you like with this card on your turn."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class Creeper(AllOfSameColour):
    NAME = "Creeper"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/creeper.png'
    CARD_TYPE = "Creeper"
    EFFECT_DESCRIPTION = "Allows you to place as many green cards as you like with this card on your turn."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class FilthySharon(AllOfSameColour):
    NAME = "Filthy Sharon"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/filthy_sharon.png'
    CARD_TYPE = "Filthy Sharon"
    EFFECT_DESCRIPTION = "Allows you to place as many white cards as you like with this card on your turn."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)
        

# ~~~~~~~~~~~~~~
#    Other
# ~~~~~~~~~~~~~~


class Nazi(AbstractCard):
    NUMBER_IN_DECK = 1
    NAME = "Nazi"
    CARD_TYPE = "Nazi"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/nazi.png'
    EFFECT_DESCRIPTION = "Allows you to place as many black cards as you like with this card on your turn."
    COMPATIBILITY_DESCRIPTION = "This card can only be played on white cards. While you are allowed to play black cards WITH this card, this card will act like a regular white card after play, such that all cards except black cards can be played on it."

    def can_be_played_on(self, card, player):
        if player.is_turn() is False:
            return False
        if self.game.pickup != 0 and self.can_be_on_pickup() is False:
            return False
        return card.get_colour() == "white"

    def can_play_with(self, card, player, is_first_card):
        return card.get_type() == self.get_type() or card.get_colour() == "black"


class AtomicBomb(AbstractCard):
    NUMBER_IN_DECK = 1
    NAME = "Atomic Bomb"
    CARD_TYPE = "Atomic Bomb"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = "cards/explosion.png"
    pickupCards = ["Atomic Bomb", "+2", "+4", "+10", "x2", "Plus", "Fuck You", "Pawn"]
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "Allows you to place as many pickup cards as you like with this card on your turn."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)

    def play_card(self, player, options, played_on):
        """
        TODO cause this to automatically make the next person pickup?
        Idk if this is necessary cause you can combine it with fuck you
        """
        pass

    def can_play_with(self, card, player, is_first_card):
        return card.get_type() in self.pickupCards


class Pawn(AbstractCard):
    NAME = "Pawn"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pawn.png'
    NUMBER_IN_DECK = 1
    CARD_TYPE = "Pawn"
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "Ends a pickup chain and causes no one to pickup."
    COMPATIBILITY_DESCRIPTION = "This card can only be used on a pickup chain. During a pickup chain, regular black rules apply such that this can be played on anything that isn't white or purple."

    old_pickup = 0

    def can_be_played_on(self, card, player):
        """
        Update method which only lets you place when it's a pickup chain
        """
        if self.game.pickup == 0:  # won't let you place outside of pickup chain
            return False
        return super().can_be_played_on(card, player)

    def prepare_card(self, player, options, played_on):
        self.old_pickup = self.game.pickup
        self.game.pickup = 0
    
    def undo_prepare_card(self, player, played_on):
        self.game.pickup = self.old_pickup


class Communist(AbstractCard):
    NAME = "Communist"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/communist.png'
    NUMBER_IN_DECK = 1
    CARD_TYPE = "Communist"
    EFFECT_DESCRIPTION = "Equally distributes all cards each player has randomly. Remainders are discarded."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)

    def play_card(self, player, options, played_on):
        all_cards = []
        for player in self.game.players:
            all_cards += player.get_hand()

        random.shuffle(all_cards)

        # remove any remaining cards
        while len(all_cards) % len(self.game.players) != 0:
            all_cards.pop()

        # divide it evenly between everyone
        number_of_cards_each = int(len(all_cards) / len(self.game.players))
        i = 0
        for player in self.game.players:
            player.set_hand(all_cards[i:i+number_of_cards_each])
            i += number_of_cards_each


class Capitalist(AbstractCard):
    NAME = "Capitalist"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/capitalist.png'
    NUMBER_IN_DECK = 1
    CARD_TYPE = "Capitalist"
    EFFECT_DESCRIPTION = "The player with the most cards has the amount of cards in their hand doubled."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)

    def play_card(self, player, options, played_on):
        """
        finds the player with the most cards and doubles it
        """
        # finding richest player
        richest_player = None
        number_of_cards = 0
        for player in self.game.players:
            if len(player.get_hand()) > number_of_cards:
                richest_player = player
                number_of_cards = len(player.get_hand())

        richest_player.add_new_cards(number_of_cards)


class SwapHand(AbstractCard):
    NAME = "Swap Hand"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/swap_hand.png'
    NUMBER_IN_DECK = 1
    CARD_TYPE = "Swap Hand"
    EFFECT_DESCRIPTION = "Choose a player and you will swap your entire hand with theirs upon play."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)

    def get_options(self, player):
        options = {}
        for other_player in self.game.players:
            if other_player != player:
                cards = other_player.get_hand();
                options[other_player.get_id()] = other_player.get_name() + "(" + str(len(cards)) + ")"
        return options

    def play_card(self, player, options, played_on):
        if self.is_option_valid(player, options, is_player=True) is False:
            print(options, "is not a valid option for", self.get_name())
            return
        other_player = self.game.get_player(options)
        if other_player is None:
            print("no player of that id was found")
            return

        hand = player.get_hand()
        player.set_hand(other_player.get_hand())
        other_player.set_hand(hand)


class FeelingBlue(AbstractCard):
    NAME = "Feeling Blue"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/feeling_blue.png'
    NUMBER_IN_DECK = 1
    CARD_TYPE = "Feeling Blue"
    EFFECT_DESCRIPTION = "Upon playing this card, you will be forced to pickup 5 cards."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)

    def play_card(self, player, options, played_on):
        player.add_new_cards(5)
        player.card_update()


class Plus(AbstractCard):
    NAME = "Plus"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/plus_wild.png'
    NUMBER_IN_DECK = 2
    CARD_TYPE = "Plus"
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "If you play this card inside a pickup chain, everyone except yourself will be forced to pickup the pickup chain value. Outside of a pickup chain, everyone except yourself is forced to pickup 2 cards."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)

    pickup_amount = 0

    def prepare_card(self, player, options, played_on):
        self.pickup_amount = self.game.pickup
        if self.pickup_amount == 0:
            self.pickup_amount = 2

    def play_card(self, player, options, played_on):
        for other_player in self.game.players:
            if other_player != player:
                other_player.add_new_cards(self.pickup_amount)
                other_player.card_update()

        self.game.pickup = 0


class FuckYou(AbstractCard):
    NAME = "Fuck You"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/fuck_you.png'
    NUMBER_IN_DECK = 2
    CARD_TYPE = "Fuck You"
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "If you play this card inside a pickup chain, one person of your choosing will be forced to pickup the pickup chain value. Outside of a pickup chain, the person of your choosing is forced to pickup 5 cards."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)

    def get_options(self, player):
        options = {}
        for other_player in self.game.players:
            if other_player != player:
                cards = other_player.get_hand();
                options[other_player.get_id()] = other_player.get_name() + "(" + str(len(cards)) + ")"
        return options
    
    pickup_amount = 0

    def prepare_card(self, player, options, played_on):
        self.pickup_amount = self.game.pickup
        if self.pickup_amount == 0:
            self.pickup_amount = 2

    def play_card(self, player, options, played_on):
        if self.is_option_valid(player, options, is_player=True) is False:
            print(options, "is not a valid option for", self.get_name())
            return
        other_player = self.game.get_player(options)

        other_player.add_new_cards(self.pickup_amount)
        other_player.card_update()
        self.game.pickup = 0


class Genocide(AbstractCard):
    NAME = "Genocide"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/genocide.png'
    NUMBER_IN_DECK = 0.5
    CARD_TYPE = "Genocide"
    EFFECT_DESCRIPTION = "Pick any colour or type of card to entirely removed from the game. All cards of this colour/type will be removed from everyone's hand and will never be able to be picked up in the future of this game."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)
    UNBANNABLE_COLOURS = ["black"]
    UNBANNABLE_TYPES = []

    def get_options(self, player):
        options = {}
        for card_colour in self.game.deck.not_banned_colours:
            if card_colour not in self.UNBANNABLE_COLOURS:
                options["colour " + card_colour] = "Colour: " + card_colour.capitalize()
        for card_type in self.game.deck.not_banned_types:
            if card_type not in self.UNBANNABLE_TYPES:
                options["type " + card_type] = "Type: " + card_type
        return options

    def play_card(self, player, options, played_on):
        if self.is_option_valid(player, options) is False:
            print(options, "is not a valid option for", self.get_name())
            return

        category, to_ban = options.split(' ', 1)

        # remove from deck
        if category == "type":
            self.game.deck.ban_type(to_ban)
        elif category == "colour":
            self.game.deck.ban_colour(to_ban)

        # remove from players
        for game_player in self.game.players:
            to_remove = []
            for card in game_player.get_hand():
                if (category == "colour" and card.get_colour() == to_ban) \
                        or (category == "type" and card.get_type() == to_ban):
                    to_remove.append(card)
            for card in to_remove:
                game_player.remove_card(card)


class Jesus(AbstractCard):
    NAME = "Jesus"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/jesus.png'
    NUMBER_IN_DECK = 2
    CARD_TYPE = "Jesus"
    EFFECT_DESCRIPTION = "Choose any person (including yourself) to reset their entire hand back to a value of 15 cards."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)

    def get_options(self, player):
        options = {}
        for other_player in self.game.players:
            if other_player != player:
                cards = other_player.get_hand()
                options[other_player.get_id()] = other_player.get_name() + "(" + str(len(cards)) + ")"
            else:
                options[other_player.get_id()] = other_player.get_name() + "(You)"

        return options

    def play_card(self, player, options, played_on):
        if self.is_option_valid(player, options, is_player=True) is False:
            print(options, "is not a valid option for", self.get_name())
            return

        other_player = self.game.get_player(options)
        other_player.set_hand([])
        other_player.add_new_cards(15)
        other_player.card_update()


class FreeTurn(AbstractCard):
    NUMBER_IN_DECK = 4
    CARD_TYPE = "Free Turn"
    NAME = "Free Turn"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/free_turn.png'
    CAN_BE_ON_PICKUP = True
    EFFECT_DESCRIPTION = "Gain an extra turn. If you play multiple Free Turn cards together you will gain multiple extra turns."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)

    def play_card(self, player, options, played_on):
        if player.turns_left < 10:
            player.turns_left += 1


class Thanos(AbstractCard):
    NAME = "Thanos"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'cards/thanos.png'
    NUMBER_IN_DECK = 1
    CARD_TYPE = "Thanos"
    EFFECT_DESCRIPTION = "Upon play, half of the cards in your hand will randomly disappear."
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)

    def play_card(self, player, options, played_on):
        """
        removes half the players cards at random
        """
        hand = player.get_hand()
        random.shuffle(hand)
        player.set_hand(hand[0:int(math.ceil(len(hand) / 2))])
        player.card_update()


class ColourChooser(AbstractCard):
    NAME = "Colour Chooser"
    CARD_IMAGE_URL = 'cards/color_swapper.png'
    CARD_COLOUR = "black"
    NUMBER_IN_DECK = 4
    CARD_TYPE = "Colour Chooser"
    EFFECT_DESCRIPTION = "Allows you to change the colour to any of the 4 given colours: red, green, yellow or blue."
    COMPATIBILITY_DESCRIPTION = "Initially, this card acts like a black card, where it can be played on anything that isn't white or purple. You get to decide on the colour it changes to after play, such that only other cards of that colour are compatible. Do note that after play, black cards will remain compatible with this card."

    def __init__(self, game):
        super().__init__(game)
        self.colour = "black"

    def get_options(self, player):
        return {
            "red": "Red",
            "green": "Green",
            "blue": "Blue",
            "yellow": "Yellow"
        }
    
    def is_compatible_with(self, card, player):
        """
        This compatibility method is used to prevent white cards from being able to be played on top
        """
        if card.get_colour() == "white" or card.get_colour() == "purple":
            return False
        
        return True

    def play_card(self, player, options, played_on):
        if self.is_option_valid(player, options) is False:
            print(options, "is not a valid option for", self.get_name())
            return
        self.colour = options

    def get_colour(self):
        return self.colour
    

class ColourSwapper(AbstractCard):
    """
    Abstract double-colour swapper card
    """
    NUMBER_IN_DECK = 1
    CARD_TYPE = "Colour Swapper"
    COLOUR_1 = "black"
    COLOUR_2 = "black"
    CARD_COLOUR = "colour swapper"
    EFFECT_DESCRIPTION = "When played on one of the colours shown on the card, this card will swap to the opposite colour. If played on a colour that is not shown on the card you get to choose the colour."

    def __init__(self, game):
        super().__init__(game)
        self.colour = "colour swapper"  # gets changed to a particular colour after being played

    def get_options(self, player):
        top_colour = self.game.get_top_card().get_colour()

        if cards.colours_are_compatible(top_colour, self.COLOUR_1) and cards.colours_are_compatible(top_colour, self.COLOUR_2):
            # if both colours are compatible with the bottom, then you get to choose the outcome
            return {
                self.COLOUR_1: self.COLOUR_1.capitalize(),
                self.COLOUR_2: self.COLOUR_2.capitalize(),
            }
        else:
            return None

    def is_compatible_with(self, card, player):
        if self.colour == "colour swapper":  # compatible if either of the card colours are compatible
            if cards.colours_are_compatible(card.get_colour(), self.COLOUR_1) \
                    or cards.colours_are_compatible(card.get_colour(), self.COLOUR_2):
                return True
        else:
            return super().is_compatible_with(card, player)

    def prepare_card(self, player, options, played_on):
        # change colour to the opposite of the one you played on
        first_compatible = cards.colours_are_compatible(played_on.get_colour(), self.COLOUR_1)
        second_compatible = cards.colours_are_compatible(played_on.get_colour(), self.COLOUR_2)
        if first_compatible and not second_compatible:
            self.colour = self.COLOUR_2
        elif second_compatible and not first_compatible:
            self.colour = self.COLOUR_1
        else:
            if self.is_option_valid(player, options) is False:
                print(options, "is not a valid option for", self.get_name())
                return
            self.colour = options
    
    def undo_prepare_card(self, player, played_on):
        self.colour = "colour swapper"

    def get_colour(self):
        return self.colour
    
    def can_be_played_with(self, planning_pile, player):
        """
        can only play multiple if the card is compatible with the top card in the planning pile
        """
        card = planning_pile[len(planning_pile)-1][0]

        if card.get_type() != self.get_type():
            return False
        
        return cards.colours_are_compatible(card.get_colour(), self.COLOUR_1) \
               or cards.colours_are_compatible(card.get_colour(), self.COLOUR_2)


def default_colour_swapper_description(colour1, colour2):
    return "Compatible with any " + colour1 + " or " + colour2 + " card. After play, this card switches to the opposite colour shown on the card as what was placed previously. " + \
        "This card is also compatible with black cards and white cards. In situations where you place on a black or a white card, you get to decide what colour this card becomes. " + \
            "If you play multiple colour swapper cards, the colours must be compatible as you place them."


class RedBlueSwapper(ColourSwapper):
    NAME = "Red/Blue Colour Swapper"
    CARD_IMAGE_URL = 'cards/blue_red.png'
    COLOUR_1 = "red"
    COLOUR_2 = "blue"
    COMPATIBILITY_DESCRIPTION = default_colour_swapper_description(COLOUR_1,COLOUR_2)

class RedYellowSwapper(ColourSwapper):
    NAME = "Red/Yellow Colour Swapper"
    CARD_IMAGE_URL = 'cards/red_yellow.png'
    COLOUR_1 = "red"
    COLOUR_2 = "yellow"
    COMPATIBILITY_DESCRIPTION = default_colour_swapper_description(COLOUR_1,COLOUR_2)


class RedGreenSwapper(ColourSwapper):
    NAME = "Red/Green Colour Swapper"
    CARD_IMAGE_URL = 'cards/green_red.png'
    COLOUR_1 = "red"
    COLOUR_2 = "green"
    COMPATIBILITY_DESCRIPTION = default_colour_swapper_description(COLOUR_1,COLOUR_2)


class GreenBlueSwapper(ColourSwapper):
    NAME = "Green/Blue Colour Swapper"
    CARD_IMAGE_URL = 'cards/green_blue.png'
    COLOUR_1 = "green"
    COLOUR_2 = "blue"
    COMPATIBILITY_DESCRIPTION = default_colour_swapper_description(COLOUR_1,COLOUR_2)


class BlueYellowSwapper(ColourSwapper):
    NAME = "Yellow/Blue Colour Swapper"
    CARD_IMAGE_URL = 'cards/yellow_blue.png'
    COLOUR_1 = "yellow"
    COLOUR_2 = "blue"
    COMPATIBILITY_DESCRIPTION = default_colour_swapper_description(COLOUR_1,COLOUR_2)


class YellowGreenSwapper(ColourSwapper):
    NAME = "Yellow/Green Colour Swapper"
    CARD_IMAGE_URL = 'cards/green_yellow.png'
    COLOUR_1 = "yellow"
    COLOUR_2 = "green"
    COMPATIBILITY_DESCRIPTION = default_colour_swapper_description(COLOUR_1,COLOUR_2)


class BlackWhiteSwapper(ColourSwapper):
    NAME = "Black/White Colour Swapper"
    NUMBER_IN_DECK = 2
    CARD_IMAGE_URL = 'cards/black_white.png'
    COLOUR_1 = "black"
    COLOUR_2 = "white"
    COMPATIBILITY_DESCRIPTION = "This card can be played on any card. If you play on a black or a white card, this card will switch colours to the opposite colour of what you placed on. " + \
        "If you play this on another colour, you will get to decide what colour this switches to. If you play with a purple card, since black cards are not compatible with purple cards, the white part of this card is used and switches the colour to black. " + \
            "This can be played with other colour swapper cards."
