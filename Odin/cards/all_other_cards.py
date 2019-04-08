from cards.abstract_card import AbstractCard
import random


# ~~~~~~~~~~~~~~
#    Reverse
# ~~~~~~~~~~~~~~


class Reverse(AbstractCard):
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "blue"
    CARD_TYPE = "Reverse"
    CARD_TYPE_ID = 16
    CAN_BE_ON_PICKUP = True

    def play_card(self, player, options, played_on):
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
    NUMBER_IN_DECK = 1


class YellowReverse(Reverse):
    NAME = "Yellow Reverse"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/reverse_yellow.png'


# ~~~~~~~~~~~~~~
#    Pickup2
# ~~~~~~~~~~~~~~


class Pickup2(AbstractCard):
    NUMBER_IN_DECK = 2
    CARD_TYPE = "+2"
    CAN_BE_ON_PICKUP = True
    CARD_TYPE_ID = 19

    def play_card(self, player, options, played_on):
        self.game.pickup += 2


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
    NUMBER_IN_DECK = 3


class YellowPickup2(Pickup2):
    NAME = "Yellow Pickup 2"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/pickup2_yellow.png'


# ~~~~~~~~~~~~~~
# Other pickups
# ~~~~~~~~~~~~~~


class Pickup10(AbstractCard):
    NUMBER_IN_DECK = 2
    CARD_TYPE = "+10"
    CARD_TYPE_ID = 21
    NAME = "Pickup 10"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup10_wild.png'
    CAN_BE_ON_PICKUP = True

    def play_card(self, player, options, played_on):
        self.game.pickup += 10


class Pickup4(AbstractCard):
    NUMBER_IN_DECK = 4
    CARD_TYPE = "+4"
    CARD_TYPE_ID = 20
    NAME = "Pickup 4"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup4_wild.png'
    CAN_BE_ON_PICKUP = True

    def play_card(self, player, options, played_on):
        self.game.pickup += 4


class PickupTimes2(AbstractCard):
    NUMBER_IN_DECK = 4
    CARD_TYPE = "x2"
    CARD_TYPE_ID = 22
    NAME = "Pickup x2"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/multiply2_wild.png'
    CAN_BE_ON_PICKUP = True

    def play_card(self, player, options, played_on):
        self.game.pickup *= 2


# ~~~~~~~~~~~~~~
#    Skip
# ~~~~~~~~~~~~~~


class Skip(AbstractCard):
    NUMBER_IN_DECK = 2
    CARD_TYPE = "Skip"
    CARD_TYPE_ID = 17
    CAN_BE_ON_PICKUP = True
    
    def play_card(self, player, options, played_on):
        self.game.iterate_turn_by += 1


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
    NUMBER_IN_DECK = 3
    CARD_TYPE = "Just A Blank Bro"
    CARD_TYPE_ID = 12
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/black.png'


class Happiness(AbstractCard):
    NAME = "Happiness"
    NUMBER_IN_DECK = 3
    CARD_TYPE = "Happiness"
    CARD_TYPE_ID = 11
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/white.png'


# ~~~~~~~~~~~~~~
#      EA
# ~~~~~~~~~~~~~~

class EA(AbstractCard):
    CARD_COLOUR = "black"
    NUMBER_IN_DECK = 1
    CARD_TYPE = "EA"
    NUMBER_NEEDED = 0

    def can_be_played_on(self, card, player):
        """
        Must have enough cards in hand
        """
        if len(player.get_hand()) < self.NUMBER_NEEDED:
            return False
        else:
            return super().can_be_played_on(card, player)

    def can_be_played_with(self, card, player):
        """
        Must have enough cards in hand
        """
        if len(player.get_hand()) < self.NUMBER_NEEDED:
            return False
        else:
            return super().can_be_played_with(card, player)


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
    CARD_TYPE_ID = 13
    CARD_TYPE = "Fuckin' M8"

    def is_compatible_with(self, card, player):
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
    NUMBER_IN_DECK = 1

    def can_be_played_with(self, card, player):
        return card.get_colour() == self.get_colour()


class ManOfTheDay(AllOfSameColour):
    NAME = "Man Of The Day"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/man_of_the_day.png'
    CARD_TYPE = "Man Of The Day"


class LadyOfTheNight(AllOfSameColour):
    NAME = "Lady Of The Night"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/lady_of_the_night.png'
    CARD_TYPE = "Lady Of The Night"


class Smurf(AllOfSameColour):
    NAME = "Smurf"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/smurf.png'
    CARD_TYPE = "Smurf"


class Creeper(AllOfSameColour):
    NAME = "Creeper"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/creeper.png'
    CARD_TYPE = "Creeper"


class FilthySharon(AllOfSameColour):
    NAME = "Filthy Sharon"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/filthy_sharon.png'
    CARD_TYPE = "Filthy Sharon"
        

# ~~~~~~~~~~~~~~
#    Other
# ~~~~~~~~~~~~~~


class Nazi(AbstractCard):
    NUMBER_IN_DECK = 1
    NAME = "Nazi"
    CARD_TYPE = "Nazi"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/nazi.png'

    def can_be_played_on(self, card, player):
        if player.is_turn() is False:
            return False
        if self.game.pickup != 0 and self.can_be_on_pickup() is False:
            return False
        return card.get_colour() == "white"

    def can_be_played_with(self, card, player):
        return card.get_type() == self.get_type() or card.get_colour() == "black"


class AtomicBomb(AbstractCard):
    NUMBER_IN_DECK = 1
    NAME = "Atomic Bomb"
    CARD_TYPE = "Atomic Bomb"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = "cards/explosion.png"
    pickupCards = ["Atomic Bomb", "+2", "+4", "+10", "x2", "Plus", "Fuck You", "Pawn"]

    def play_card(self, player, options, played_on):
        """
        TODO cause this to automatically make the next person pickup?
        Idk if this is necessary cause you can combine it with fuck you

        """
        pass

    def can_be_played_with(self, card, player):
        return card.get_type() in self.pickupCards


class Pawn(AbstractCard):
    NAME = "Pawn"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pawn.png'
    NUMBER_IN_DECK = 1
    CARD_TYPE = "Pawn"
    CAN_BE_ON_PICKUP = True

    def can_be_played_on(self, card, player):
        """
        Update method which only lets you place when it's a pickup chain
        """
        if self.game.pickup == 0:  # won't let you place outside of pickup chain
            return False
        return super().can_be_played_on(card, player)

    def play_card(self, player, options, played_on):
        self.game.pickup = 0


class Communist(AbstractCard):
    NAME = "Communist"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/communist.png'
    NUMBER_IN_DECK = 1
    CARD_TYPE = "Communist"

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

        self.game.update_players()


class Capitalist(AbstractCard):
    NAME = "Capitalist"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/capitalist.png'
    NUMBER_IN_DECK = 1
    CARD_TYPE = "Capitalist"

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

        self.game.update_players()


class SwapHand(AbstractCard):
    NAME = "Swap Hand"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/swap_hand.png'
    NUMBER_IN_DECK = 1
    CARD_TYPE = "Swap Hand"

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

    def play_card(self, player, options, played_on):
        amount = self.game.pickup
        if amount == 0:
            amount = 2
        
        for other_player in self.game.players:
            if other_player != player:
                other_player.add_new_cards(amount)
                other_player.card_update()

        self.game.pickup = 0


class FuckYou(AbstractCard):
    NAME = "Fuck You"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/fuck_you.png'
    NUMBER_IN_DECK = 2
    CARD_TYPE = "Fuck You"
    CAN_BE_ON_PICKUP = True

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
        
        amount = self.game.pickup
        if amount == 0:
            amount = 5

        other_player.add_new_cards(amount)
        other_player.card_update()
        self.game.pickup = 0


class Genocide(AbstractCard):
    NAME = "Genocide"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/genocide.png'
    NUMBER_IN_DECK = 0.5
    CARD_TYPE = "Genocide"

    def get_options(self, player):
        options = {}
        for card_types in self.game.deck.not_banned_types:
            options["type " + card_types] = "Type: " + card_types
        for card_colour in self.game.deck.not_banned_colours:
            options["colour " + card_colour] = "Colour: " + card_colour
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
        other_player.add_new_cards(self.game.starting_number_of_cards)
        other_player.card_update()


class FreeTurn(AbstractCard):
    NUMBER_IN_DECK = 4
    CARD_TYPE = "Free Turn"
    NAME = "Free Turn"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/free_turn.png'
    CAN_BE_ON_PICKUP = True

    def play_card(self, player, options, played_on):
        player.turns_left += 1


class Thanos(AbstractCard):
    NAME = "Thanos"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'cards/thanos.png'
    NUMBER_IN_DECK = 1
    CARD_TYPE = "Thanos"

    def play_card(self, player, options, played_on):
        """
        removes half the players cards at random
        """
        hand = player.get_hand()
        random.shuffle(hand)
        player.set_hand(hand[0:int(len(hand) / 2)])
        player.card_update()


class ColourChooser(AbstractCard):
    NAME = "Colour Chooser"
    CARD_IMAGE_URL = 'cards/color_swapper.png'
    NUMBER_IN_DECK = 4
    CARD_TYPE = "Colour Chooser"

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
        This compatiblity method is used to prevent white cards from being able to be played ontop
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
    NUMBER_IN_DECK = 50
    CARD_TYPE = "Colour Swapper"
    COLOUR_1 = "black"
    COLOUR_2 = "black"

    def __init__(self, game):
        super().__init__(game)
        self.colour = "colour swapper"  # gets changed to a particular colour after being played

    def get_options(self, player):
        if self.game.get_top_card().get_colour() in ("black", "white"):
            return {
                self.COLOUR_1: self.COLOUR_1.capitalize(),
                self.COLOUR_2: self.COLOUR_2.capitalize(),
            }
        else:
            return None

    def is_compatible_with(self, card, player):
        if self.colour == "colour swapper":
            if card.get_colour() in (self.COLOUR_1, self.COLOUR_2, "black", "white"):
                return True
        else:
            return super().is_compatible_with(card, player)

    def play_card(self, player, options, played_on):
        # change colour to the opposite of the one you played on
        if played_on.get_colour() == self.COLOUR_1:
            self.colour = self.COLOUR_2
        elif played_on.get_colour() == self.COLOUR_2:
            self.colour = self.COLOUR_1
        else:
            if self.is_option_valid(player, options) is False:
                print(options, "is not a valid option for", self.get_name())
                return
            self.colour = options

    def get_colour(self):
        return self.colour


class RedBlueSwapper(ColourSwapper):
    NAME = "Red/Blue Colour Swapper"
    CARD_IMAGE_URL = 'cards/blue_red.png'
    COLOUR_1 = "red"
    COLOUR_2 = "blue"
