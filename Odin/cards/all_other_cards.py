from cards.abstract_card import AbstractCard
import random

# ~~~~~~~~~~~~~~
#    Reverse
# ~~~~~~~~~~~~~~


class Reverse:
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "blue"
    CARD_TYPE = "reverse"
    CARD_TYPE_ID = 16
    CAN_BE_ON_PICKUP = True

    def play_card(self, player, options, played_on):
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

    def play_card(self, player, options, played_on):
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

    def play_card(self, player, options, played_on):
        self.game.pickup += 10


class Pickup4(AbstractCard):
    NUMBER_IN_DECK = 5
    CARD_TYPE = "pickup4"
    CARD_TYPE_ID = 20
    NAME = "Pickup 4"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'cards/pickup4_wild.png'
    CAN_BE_ON_PICKUP = True

    def play_card(self, player, options, played_on):
        self.game.pickup += 4


class PickupTimes2(AbstractCard):
    NUMBER_IN_DECK = 5
    CARD_TYPE = "pickupTimes2"
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


class Skip:
    NUMBER_IN_DECK = 2
    CARD_TYPE = "skip"
    CARD_TYPE_ID = 17
    CAN_BE_ON_PICKUP = True
    
    def play_card(self, player, options, played_on):
        self.game.skip_next_turn += 1


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
                options[other_player.get_name()] = other_player.get_id()
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
    CARD_TYPE = "feeling blue"
    CAN_BE_ON_PICKUP = True

    def play_card(self, player, options, played_on):
        for other_player in self.game.players:
            if other_player != player:
                other_player.add_new_cards(self.game.pickup)
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
                options[other_player.get_name()] = other_player.get_id()
        return options

    def play_card(self, player, options, played_on):
        if options is 0:
            print("no option given")
            return
        other_player = self.game.get_player(options)
        if other_player is None:
            print("no player of that id was found")
            return

        other_player.add_new_cards(self.game.pickup)
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
            options["Type: " + card_types] = "type " + card_types
        for card_colour in self.game.deck.not_banded_colours:
            options["Colours: " + card_colour] = "colour " + card_colour
        return options

    def play_card(self, player, options, played_on):
        if options is 0:
            print("no option given")
            return
        catagory, to_ban = options.split(' ', 1)
        if catagory == "type":
            self.game.deck.ban_type(to_ban)
            for game_player in self.game.players:
                deck = game_player.get_deck()
                for card in deck:
                    if card.CARD_TYPE == to_ban:
                        deck.remove(card)
        elif catagory == "colour":
            self.game.deck.ban_colour(to_ban)
            for game_player in self.game.players:
                deck = game_player.get_deck()
                for card in deck:
                    if card.CARD_COLOUR == to_ban:
                        deck.remove(card)


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
                options[other_player.get_name()] = other_player.get_id()
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