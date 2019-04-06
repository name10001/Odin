from cards.abstract_card import AbstractCard
import random

# ~~~~~~~~~~~~~~
#    Reverse
# ~~~~~~~~~~~~~~


class Reverse(AbstractCard):
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "blue"
    CARD_TYPE = "reverse"
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
    CARD_TYPE = "pickup +2"
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
    CARD_TYPE = "pickup +10"
    CARD_TYPE_ID = 21
    NAME = "Pickup 10"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup10_wild.png'
    CAN_BE_ON_PICKUP = True

    def play_card(self, player, options, played_on):
        self.game.pickup += 10


class Pickup4(AbstractCard):
    NUMBER_IN_DECK = 4
    CARD_TYPE = "pickup +4"
    CARD_TYPE_ID = 20
    NAME = "Pickup 4"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup4_wild.png'
    CAN_BE_ON_PICKUP = True

    def play_card(self, player, options, played_on):
        self.game.pickup += 4


class PickupTimes2(AbstractCard):
    NUMBER_IN_DECK = 4
    CARD_TYPE = "pickup x2"
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
    CARD_TYPE = "skip"
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
    NAME = "JUST A BLANK BRO"
    NUMBER_IN_DECK = 3
    CARD_TYPE = "blank bro"
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
    CARD_TYPE = "fuck"

    def is_compatible_with(self, card, player):
        return card.CARD_COLOUR == self.CARD_COLOUR or card.CARD_TYPE == self.CARD_TYPE


class BlueFuck(Fuck):
    NAME = "Blue Fuck"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/fuck_blue.png'


class GreenFuck(Fuck):
    NAME = "Green Fuck"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/fuck_green.png'


class RedFuck(Fuck):
    NAME = "Red Fuck"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/fuck_red.png'


class BlackFuck(Fuck):
    NAME = "Black Fuck"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/fuck_black.png'


class YellowFuck(Fuck):
    NAME = "Yellow Fuck"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/fuck_yellow.png'


# ~~~~~~~~~~~~~~
# all of same colour
# ~~~~~~~~~~~~~~

class AllOfSameColour(AbstractCard):
    NAME = "Pawn"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pawn.png'
    NUMBER_IN_DECK = 1
    CARD_TYPE = "pawn"

    def can_be_played_with(self, card, player):
        return card.CARD_COLOUR == self.CARD_COLOUR


class ManOfTheDay(AllOfSameColour):
    NAME = "Man of the day"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/man_of_the_day.png'
    CARD_TYPE = "Man of the day"


class LadyOfTheNight(AllOfSameColour):
    NAME = "Lady of the night"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/lady_of_the_night.png'
    CARD_TYPE = "Lady of the night"


# ~~~~~~~~~~~~~~
#    Other
# ~~~~~~~~~~~~~~


class Pawn(AbstractCard):
    NAME = "Pawn"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pawn.png'
    NUMBER_IN_DECK = 1
    CARD_TYPE = "pawn"
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
    NAME = "Communism"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'cards/communist.png'
    NUMBER_IN_DECK = 1
    CARD_TYPE = "communism"

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
    CARD_TYPE = "capitalist"

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
    CARD_TYPE = "swap"

    def get_options(self, player):
        options = {}
        for other_player in self.game.players:
            if other_player != player:
                cards = other_player.get_hand();
                options[other_player.get_id()] = other_player.get_name() + "(" + str(len(cards)) + ")"
        return options

    def play_card(self, player, options, played_on):
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
    CARD_TYPE = "feeling blue"

    def play_card(self, player, options, played_on):
        player.add_new_cards(5)
        player.card_update()


class Plus(AbstractCard):
    NAME = "Plus"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/plus_wild.png'
    NUMBER_IN_DECK = 2
    CARD_TYPE = "plus"
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
    CARD_TYPE = "fuck you"
    CAN_BE_ON_PICKUP = True

    def get_options(self, player):
        options = {}
        for other_player in self.game.players:
            if other_player != player:
                cards = other_player.get_hand();
                options[other_player.get_id()] = other_player.get_name() + "(" + str(len(cards)) + ")"
        return options

    def play_card(self, player, options, played_on):
        if options is 0:
            print("no option given")
            return
        other_player = self.game.get_player(options)
        if other_player is None:
            print("no player of that id was found")
            return
        
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
    NUMBER_IN_DECK = 1
    CARD_TYPE = "Genocide"

    def get_options(self, player):
        options = {}
        for card_types in self.game.deck.not_banded_types:
            options["type " + card_types] = "Type: " + card_types
        for card_colour in self.game.deck.not_banded_colours:
            options["colour " + card_colour] = "Colour: " + card_colour
        return options

    def play_card(self, player, options, played_on):
        if options is 0:
            print("no option given")
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
                if (category == "colour" and card.CARD_COLOUR == to_ban) \
                        or (category == "type" and card.CARD_TYPE == to_ban):
                    to_remove.append(card)
            for card in to_remove:
                game_player.remove_card(card)


class Jesus(AbstractCard):
    NAME = "Jesus"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/jesus.png'
    NUMBER_IN_DECK = 2
    CARD_TYPE = "jesus"

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
        if options is 0:
            print("no option given")
            return
        other_player = self.game.get_player(options)
        if other_player is None:
            print("no player of that id was found")
            return

        other_player.set_hand([])
        other_player.add_new_cards(self.game.starting_number_of_cards)
        other_player.card_update()


class FreeTurn(AbstractCard):
    NUMBER_IN_DECK = 4
    CARD_TYPE = "free turn"
    NAME = "Free Turn"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/free_turn.png'

    def play_card(self, player, options, played_on):
        self.game.iterate_turn_by = 0
