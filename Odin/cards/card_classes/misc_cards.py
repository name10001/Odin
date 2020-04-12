from cards.abstract_card import AbstractCard
from cards.card_frequency import CardFrequency
from cards.effect import FireEffect
import random
import math
from decimal import Decimal
import settings


# ~~~~~~~~~~~~~~
#      EA
# ~~~~~~~~~~~~~~

class EA(AbstractCard):
    CARD_COLOUR = "black"
    CARD_TYPE = "EA"
    NUMBER_NEEDED = 0
    MULTI_COLOURED = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.still_needs = self.NUMBER_NEEDED

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

    def prepare_card(self, player, allow_cancel):
        needs = self.still_needs

        if len(self.game.planning_pile) > 0:
            if hasattr(self.game.planning_pile[0], 'still_needs'):
                self.game.planning_pile[0].still_needs += self.NUMBER_NEEDED
            else:
                # In this case it's either a nazi card or a filthy sharon card.
                # Give the bottom card the "still_needs" attribute.
                self.game.planning_pile[0].still_needs = self.NUMBER_NEEDED
            self.still_needs = 0
            needs = self.game.planning_pile[0].still_needs

        # asks the player if they want to play the cards
        option = player.ask(
            "Would you like the game to automatically pick cards?",
            {
                "pick for me": "Yes",
                "let me pick": "No, let me pick"
            },
            image=self.get_url(), allow_cancel=allow_cancel
        )
        if option is None:
            return False

        # play cards
        if option != "pick for me":
            return True

        card_numbers = []
        number_cards = {}
        for card in player.hand:
            if card.get_type().isnumeric():
                num = int(card.get_type())
                if num not in number_cards:
                    number_cards[num] = []
                number_cards[num].append(card)
                card_numbers.append(num)

        number_played_with = []

        try:
            found = False
            for i in range(0, len(card_numbers)):
                found = self._find_cards_to_play(
                    number_played_with, card_numbers, needs, i)
                if found is True:
                    break

            if not found:
                return True
        except OverflowError:
            print("Warning: Got over flow error in EA card")

        for num in number_played_with:
            player.prepare_cards([number_cards[num].pop().get_id()])

        return True

    def undo_prepare_card(self, player):
        if len(self.game.planning_pile) == 0:
            return
        self.game.planning_pile[0].still_needs -= self.NUMBER_NEEDED
        self.still_needs = self.NUMBER_NEEDED

    def _find_cards_to_play(self, played_with, all_cards, needs, index=0):
        """
        When given an array of numbers and a number of aim for,
        this will try find a combination of thoughts numbers that sums to exactly the given number.
        :param played_with: List of cards to put the found numbers in
        :param all_cards: The array of numbers to try find the combination of
        :param needs: The number (sum) to aim for
        :param index:
        :return: True if a combination was found, False if one was not
        """
        # TODO make iterative. Python is not optimised for recursion
        card = all_cards[index]
        played_with.append(card)
        number = card
        needs -= number
        if needs == 0:
            return True
        elif needs > 0:
            for i in range(index+1, len(all_cards)):
                found = self._find_cards_to_play(
                    played_with, all_cards, needs, i)
                if found is True:
                    return True
        needs += number
        played_with.pop(-1)
        return False


class EA15(EA):
    CARD_FREQUENCY = CardFrequency(0.7, 1.5, starting=0, elevator=0)
    EFFECT_DESCRIPTION = "Requires a fee to be able to play. You must pay the fee when you pay this card with " \
                         "any number cards such that they all add up to 15."
    NAME = "EA $15"
    CARD_IMAGE_URL = 'ea_15.png'
    NUMBER_NEEDED = 15


class EA20(EA):
    CARD_FREQUENCY = CardFrequency(0.5, 0.7, 1, starting=0, elevator=0)
    EFFECT_DESCRIPTION = "Requires a fee to be able to play. You must pay the fee when you pay this card with " \
                         "any number cards such that they all add up to 20."
    NAME = "EA $20"
    CARD_IMAGE_URL = 'ea_20.png'
    NUMBER_NEEDED = 20


class EA30(EA):
    CARD_FREQUENCY = CardFrequency(0.25, 0.5, 1, starting=0, elevator=0)
    EFFECT_DESCRIPTION = "Requires a fee to be able to play. You must pay the fee when you pay this card with " \
                         "any number cards such that they all add up to 30."
    NAME = "EA $30"
    CARD_IMAGE_URL = 'ea_30.png'
    NUMBER_NEEDED = 30


class EA100(EA):
    CARD_FREQUENCY = CardFrequency(0, 0, 0.05, starting=0, elevator=0)
    EFFECT_DESCRIPTION = "Requires a fee to be able to play. You must pay the fee when you pay this card with " \
                         "any number cards such that they all add up to 100."
    NAME = "EA $100"
    CARD_IMAGE_URL = 'ea_100.png'
    NUMBER_NEEDED = 100


# ~~~~~~~~~~~~~~
# Card removal
# ~~~~~~~~~~~~~~


class TrashCard(AbstractCard):
    CARD_FREQUENCY = CardFrequency(1.2, 0.5, starting=0, max_cards=8)
    MULTI_COLOURED = True
    CARD_TYPE = "Trash"
    EFFECT_DESCRIPTION = "Choose any card to be removed from your hand. The effects of this card do not apply."
    NUMBER_TO_REMOVE = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cards_removed = []

    def play_card(self, player):
        title = "Pick a card to remove:"
        if self.NUMBER_TO_REMOVE > 1:
            title = "Pick " + str(self.NUMBER_TO_REMOVE) + " cards to remove:"

        options = player.ask(
            title,
            player.hand,
            options_type="cards",
            allow_cancel=False,
            number_to_pick=self.NUMBER_TO_REMOVE,
            image=self.get_url()
        )
        if options is None:
            return

        cards_to_remove = options
        if not isinstance(options, list):
            cards_to_remove = [options]

        for option in cards_to_remove:
            card = player.hand.find_card(option)
            if card is None:
                continue

            self.cards_removed.append(card)
            player.hand.remove_card(card=card)

        self.game.animate_card_transfer(self.cards_removed, cards_from=player)


class BlueTrash(TrashCard):
    NAME = "Blue Trash"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = "trash_blue.png"


class GreenTrash(TrashCard):
    NAME = "Green Trash"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = "trash_green.png"


class RedTrash(TrashCard):
    NAME = "Red Trash"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = "trash_red.png"


class YellowTrash(TrashCard):
    NAME = "Yellow Trash"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = "trash_yellow.png"


class BlackTrash(TrashCard):
    NUMBER_TO_REMOVE = 3
    CARD_FREQUENCY = CardFrequency(1, starting=0, max_cards=8)
    NAME = "Black Trash"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = "trash_wild.png"


class DoJustly(AbstractCard):
    CARD_FREQUENCY = CardFrequency(1.2, starting=0, max_cards=10)
    CARD_TYPE = "Do Justly"
    CARD_COLOUR = "black"
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Choose a card from your hand to give to another player of your choice."
    NUMBER_TO_GIVE = 1

    def play_card(self, player):
        options = {}
        for other_player in self.game.players:
            if other_player != player:
                options[other_player.get_id()] = other_player.get_name() + \
                    "(" + str(len(other_player.hand)) + ")"
        if len(options) == 0:
            return
        other_player_id = player.ask(
            "Select player to give cards to:",
            options,
            options_type="buttons",
            allow_cancel=False,
            image=self.get_url()
        )
        if other_player_id is None:
            return
        other_player = self.game.get_player(other_player_id)

        title = "Pick a card to give:"
        if self.NUMBER_TO_GIVE > 1:
            title = "Pick " + str(self.NUMBER_TO_GIVE) + " cards to give:"

        cards_to_give = player.ask(
            title,
            player.hand,
            options_type="cards",
            allow_cancel=False,
            number_to_pick=self.NUMBER_TO_GIVE,
            image=self.get_url()
        )
        if cards_to_give is None:
            return

        if not isinstance(cards_to_give, list):
            cards_to_give = [cards_to_give]

        cards_given = []
        for card_id in cards_to_give:
            card = player.hand.find_card(card_id)
            cards_given.append(card)
            player.hand.remove_card(card)
            other_player.hand.add_card(card)

        self.game.animate_card_transfer(
            cards_given, cards_to=other_player, cards_from=player)


class DoJustly1(DoJustly):
    NAME = "Do Justly -1"
    NUMBER_TO_GIVE = 1
    CARD_IMAGE_URL = "do_justly_1.png"


class DoJustly3(DoJustly):
    NAME = "Do Justly -3"
    CARD_FREQUENCY = CardFrequency(0.7, starting=0, max_cards=10)
    NUMBER_TO_GIVE = 3
    EFFECT_DESCRIPTION = "Choose 3 cards from your hand to give to another player of your choice."
    CARD_IMAGE_URL = "do_justly_3.png"


# ~~~~~~~~~~~~~~
#    Other
# ~~~~~~~~~~~~~~


class Communist(AbstractCard):
    NAME = "Communist"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'communist.png'
    CARD_FREQUENCY = CardFrequency(
        0, 0.8, 0.5, 0.1, starting=0, max_cards=1, elevator=1)
    CARD_TYPE = "Communist"
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Equally distributes all cards each player has randomly. Remainders are discarded."

    def play_card(self, player):
        # stop the card from playing multiple times
        if self.game.planning_pile.contains(self):
            card_below = self.game.planning_pile.card_below(self)
            if card_below is not None and card_below.get_type() == "Communist":
                return
        player.refresh_card_play_animation()

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

            json_to_send = {
                "type": "communist",
                "cards": [{
                    "id": card.get_id(),
                    "name": card.get_name(),
                    "url": card.get_url()
                } for card in player.hand]
            }

            player.send_animation(json_to_send)

            i += number_of_cards_each

        self.game.update_players()


class Capitalist(AbstractCard):
    NAME = "Capitalist"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'capitalist.png'
    CARD_FREQUENCY = CardFrequency(
        0.8, 0.6, 0.3, 0, starting=0, max_cards=10, elevator=1)
    CARD_TYPE = "Capitalist"
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "The player with the most cards has the amount of cards in their hand doubled."

    def play_card(self, player):
        """
        finds the player with the most cards and doubles it
        """
        player.refresh_card_play_animation()
        # finding richest player
        richest_player = None
        number_of_cards = 0
        for player in self.game.players:
            if len(player.hand) > number_of_cards:
                richest_player = player
                number_of_cards = len(player.hand)

        json_to_send = {
            "type": "sound",
            "sound": "/static/sounds/capitalist_card.mp3"
        }
        self.game.send_animation(json_to_send)
        richest_player.pickup(number_of_cards)


class SwapHand(AbstractCard):
    NAME = "Swap Hand"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'swap_hand.png'
    CARD_FREQUENCY = CardFrequency(0, 0.6, 0.3, starting=0, max_cards=1)
    CARD_TYPE = "Swap Hand"
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Choose a player and you will swap your entire hand with theirs upon play."

    def play_card(self, player):
        options = {}

        for other_player in self.game.players:
            if other_player != player:
                options[other_player.get_id()] = other_player.get_name() + \
                    "(" + str(len(other_player.hand)) + ")"

        if len(options) == 0:
            return

        player_id = player.ask(
            "Pick a player to swap hands with:",
            options,
            allow_cancel=False,
            image=self.get_url()
        )
        swap_with = self.game.get_player(player_id)

        if swap_with is None:
            return

        # TODO custom animation for this
        self.game.animate_card_transfer(
            player.hand, cards_to=swap_with, cards_from=player)
        self.game.animate_card_transfer(
            swap_with.hand, cards_to=player, cards_from=swap_with)
        hand = player.hand
        player.hand = swap_with.hand
        swap_with.hand = hand


class FeelingBlue(AbstractCard):
    NAME = "Feeling Blue"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'feeling_blue.png'
    CARD_FREQUENCY = CardFrequency(1.5, starting=0, max_cards=10)
    CARD_TYPE = "Feeling Blue"
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Upon playing this card, you will be forced to pickup 5 cards."

    def prepare_card(self, player, allow_cancel):
        player.player_pickup_amount += 5

        return True

    def undo_prepare_card(self, player):
        player.player_pickup_amount -= 5

    def play_card(self, player):
        player.refresh_card_play_animation()
        player.pickup(5)


class Genocide(AbstractCard):
    NAME = "Genocide"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'genocide.png'
    CARD_FREQUENCY = CardFrequency(0.7, max_cards=8, starting=0)
    MULTI_COLOURED = False
    CARD_TYPE = "Genocide"
    EFFECT_DESCRIPTION = "Pick any colour or type of card to entirely removed from the game. " \
                         "All cards of this colour/type will be removed from everyone's hand " \
                         "and will never be able to be picked up in the future of this game."
    # colour swapper is banned by type instead
    UNBANNABLE_COLOURS = ["black", "colour swapper"]
    UNBANNABLE_TYPES = []

    def play_card(self, player):
        """
        On play this will remove all the types from everyone's hands
        """
        # generate options
        options = {}
        for card_colour in self.game.deck.get_unbanned_colours():
            if card_colour not in self.UNBANNABLE_COLOURS:
                options["colour " + card_colour] = "Colour: " + \
                    card_colour.capitalize()
        for card_type in self.game.deck.get_unbanned_types():
            if card_type not in self.UNBANNABLE_TYPES:
                options["type " + card_type] = "Type: " + card_type

        option = player.ask(
            "Select card type/colour to ban:",
            options,
            allow_cancel=False,
            image=self.get_url()
        )

        category, to_ban = option.split(' ', 1)

        # remove from deck
        if category == "type":
            self.game.deck.ban_type(to_ban)
        elif category == "colour":
            self.game.deck.ban_colour(to_ban)

        player.refresh_card_play_animation()

        json_to_send = {
            "type": "genocide",
            "cards": [],
            "banned": to_ban
        }

        # remove from deck and players hands
        if category == "type":
            for game_player in self.game.players:
                removed_cards = game_player.hand.remove_type(to_ban)
                json_to_send["cards"] = [
                    {
                        "id": card.get_id(),
                        "url": card.get_url(),
                        "name": card.get_name()
                    } for card in removed_cards
                ]
                game_player.send_animation(json_to_send)
        elif category == "colour":
            for game_player in self.game.players:
                removed_cards = game_player.hand.remove_colour(to_ban)
                json_to_send["banned"] = to_ban.capitalize()
                json_to_send["cards"] = [
                    {
                        "id": card.get_id(),
                        "url": card.get_url(),
                        "name": card.get_name()
                    } for card in removed_cards
                ]
                game_player.send_animation(json_to_send)

        self.game.update_players()


class Jesus(AbstractCard):
    NAME = "Jesus"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'jesus.png'
    CARD_FREQUENCY = CardFrequency(1.2, 1, 0.5, 0.7, max_cards=4, starting=0)
    CARD_TYPE = "Jesus"
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Choose any person (including yourself) to reset their entire hand " \
                         "back to a value of 15 cards."

    def play_card(self, player):
        options = {}
        for other_player in self.game.players:
            if other_player != player:
                options[other_player.get_id()] = other_player.get_name() + \
                    "(" + str(len(other_player.hand)) + ")"
            else:
                options[other_player.get_id()] = other_player.get_name() + "(You)"
        other_player_id = player.ask(
            "Select player to reset their hand:",
            options,
            allow_cancel=False,
            image=self.get_url()
        )
        other_player = self.game.get_player(other_player_id)

        if other_player is None:
            return

        self.game.animate_card_transfer(
            other_player.hand, cards_from=other_player)

        other_player.hand.clear()
        other_player.pickup(settings.jesus_card_number)


class Odin(AbstractCard):
    NAME = "Odin"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'back.png'
    CARD_FREQUENCY = CardFrequency(1, max_cards=1, starting=0, elevator=0)
    CARD_TYPE = "Odin"
    MULTI_COLOURED = False
    COMPATIBILITY_DESCRIPTION = "Can only be played as your last card. When it becomes your last card, " \
                                "regular black card rules apply, such that it can be played on red, green, " \
                                "yellow blue and black cards."

    def can_be_played_on(self, player, card):
        if super().can_be_played_on(player, card) is False:
            return False

        for your_card in player.hand:
            if not isinstance(your_card, Odin):
                return False
        return True


class Thanos(AbstractCard):
    NAME = "Thanos"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'thanos.png'
    CARD_FREQUENCY = CardFrequency(0, 0.5, 1.2, 1.2, max_cards=4, starting=0)
    CARD_TYPE = "Thanos"
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Upon play, half of the cards in your hand will randomly disappear."

    def play_card(self, player):
        """
        removes half the players cards at random
        """
        total = len(player.hand)
        num_to_remove = math.floor(total / 2)

        removed = []
        for i in range(0, num_to_remove):
            index = random.randrange(0, total)
            removed.append(player.hand.cards_list[index])
            player.hand.remove_card(index=index)
            total -= 1

        if len(removed) == 0:
            return

        player.refresh_card_play_animation()

        self.game.animate_card_transfer(
            removed, cards_from=player, cards_to="deck")

        self.game.update_players()


class CopyCat(AbstractCard):
    NAME = "Copy Cat"
    CARD_IMAGE_URL = 'copy_cat.png'
    CARD_FREQUENCY = CardFrequency(
        3.4, 1, 0.6, 0.5, max_cards=4, starting=0, elevator=0)
    MULTI_COLOURED = False
    CARD_COLOUR = "rainbow"
    CARD_TYPE = "Copy Cat"
    EFFECT_DESCRIPTION = "When you play this card, it becomes whatever card " \
                         "it is placed on and all effects apply for that card."
    COMPATIBILITY_DESCRIPTION = "Can be played on any card. After play, " \
                                "the compatibility rules of the card below are copied."
    CAN_BE_ON_PICKUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.copied = None
        self.colour = "rainbow"
        self.type = "Copy Cat"

    def can_be_played_on(self, player, card):
        return player.is_turn()

    def prepare_card(self, player, allow_cancel):
        top_card = self.game.get_top_card()
        if isinstance(top_card, CopyCat):
            copy_class = top_card.copied.__class__
        else:
            copy_class = top_card.__class__
        self.copied = copy_class(self.game)  # copied card is re-initialized
        self.copied.id = self.get_id()
        return self.copied.prepare_card(player, allow_cancel)

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
        Can play with other copycats and whatever the copied card can be played with
        """
        return isinstance(card, CopyCat) or self.copied.can_play_with(player, card, is_first_card)

    def is_compatible_with(self, player, card):
        if self.copied is None:
            return True
        else:
            return self.copied.is_compatible_with(player, card)

    def get_colour(self):
        return self.colour

    def get_type(self):
        return self.type


class Elevator(AbstractCard):
    NAME = "Elevator"
    CARD_IMAGE_URL = 'elevator.png'
    CARD_COLOUR = "rainbow"
    CARD_FREQUENCY = CardFrequency(2, starting=0, elevator=0)
    CARD_TYPE = "Elevator"
    EFFECT_DESCRIPTION = "Picks up a random card from the deck and plays it on top as if it was you."
    COMPATIBILITY_DESCRIPTION = "Can be played on any card."

    def play_card(self, player):
        # play the card as if its being played by the player
        card = self.game.deck.get_next_card(
            {"card collection": None, "elevator": True})(self.game)
        card.prepare_card(player, False)
        self.game.planning_pile.add_card(card)

        player.refresh_card_play_animation()
        self.game.animate_card_transfer([card], cards_to="planning")

    def can_be_played_on(self, player, card):
        if player.is_turn() is False:
            return False
        if self.game.pickup != 0 and self.can_be_on_pickup() is False:
            return False
        return True


class SwapCard(AbstractCard):
    NAME = "Swap Card"
    CARD_IMAGE_URL = 'swap_card.png'
    CARD_COLOUR = "black"
    MULTI_COLOURED = False
    CARD_FREQUENCY = CardFrequency(2.2, starting=0)
    CARD_TYPE = "Swap Card"
    EFFECT_DESCRIPTION = "Pick a card to give to a player of your choice. " \
                         "This is swapped with a random card from their hand."

    def play_card(self, player):
        options = {}
        for other_player in self.game.players:
            if other_player != player:
                options[other_player.get_id()] = other_player.get_name() + \
                    "(" + str(len(other_player.hand)) + ")"
        if len(options) == 0:
            return
        other_player_id = player.ask(
            "Select player to give cards to:",
            options,
            allow_cancel=False,
            image=self.get_url()
        )
        if other_player_id is None:
            return
        other_player = self.game.get_player(other_player_id)

        cards_id = player.ask(
            "Select a card to give to " + other_player.get_name() + ":",
            player.hand,
            options_type="cards",
            allow_cancel=False,
            image=self.get_url()
        )
        if cards_id is None:
            return
        if cards_id == []:
            return

        card = player.hand.find_card(cards_id)
        player.hand.remove_card(card)
        other_player.hand.add_card(card)

        self.game.animate_card_transfer(
            [card], cards_to=other_player, cards_from=player)

        card = random.choice(other_player.hand.get_cards())
        other_player.hand.remove_card(card)
        player.hand.add_card(card)

        self.game.animate_card_transfer(
            [card], cards_to=player, cards_from=other_player)


class Possess(AbstractCard):
    NAME = "Possess"
    CARD_IMAGE_URL = 'possess.png'
    CARD_COLOUR = "black"
    CARD_FREQUENCY = CardFrequency(1.5, 1, 0.5, 0.3, max_cards=4, starting=0)
    CARD_TYPE = "Possess"
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Choose a player. On their next turn you get to decide what card(s) they must play from their hand, or force them to pick up."

    def play_card(self, player):
        options = {}

        for other_player in self.game.players:
            if other_player != player:
                options[other_player.get_id()] = other_player.get_name() + \
                    "(" + str(len(other_player.hand)) + ")"

        if len(options) == 0:
            return

        player_id = player.ask(
            "Pick a player to possess:",
            options,
            allow_cancel=False,
            image=self.get_url()
        )
        chosen_player = self.game.get_player(player_id)

        json_to_send = {
            "type": "possess",
            "possessor": player.get_id(),
            "possessed": chosen_player.get_id()
        }

        for other_player in self.game.players:
            other_player.send_animation(json_to_send)

        chosen_player.possessions.append(player)
        self.game.update_players()


class Steal(AbstractCard):
    NAME = "Steal"
    CARD_IMAGE_URL = 'steal.png'
    CARD_COLOUR = "black"
    CARD_FREQUENCY = CardFrequency(1.7, 1.5, 1, 0.8, starting=0)
    CARD_TYPE = "Steal"
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Choose a card to steal from a player of your choice's hand."

    def play_card(self, player):
        options = {}
        for other_player in self.game.players:
            if other_player != player:
                options[other_player.get_id()] = other_player.get_name() + \
                    "(" + str(len(other_player.hand)) + ")"
        if len(options) == 0:
            return
        other_player_id = player.ask(
            "Select player to take cards from:",
            options,
            allow_cancel=False,
            image=self.get_url()
        )
        if other_player_id is None:
            return
        other_player = self.game.get_player(other_player_id)

        cards_id = player.ask(
            "Select a card to take from " + other_player.get_name() + ":",
            other_player.hand,
            options_type="cards",
            allow_cancel=False,
            image=self.get_url()
        )
        if cards_id is None:
            return
        if cards_id == []:
            return

        card = other_player.hand.find_card(cards_id)
        other_player.hand.remove_card(card)
        player.hand.add_card(card)

        self.game.animate_card_transfer(
            [card], cards_to=player, cards_from=other_player)


class Fire(AbstractCard):
    NAME = "Fire"
    CARD_IMAGE_URL = 'fire.png'
    CARD_COLOUR = "black"
    CARD_FREQUENCY = CardFrequency(3, 1, starting=0)
    CARD_TYPE = "Fire"
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Choose a player to set on fire for 3 turns. While on fire, they will be forced to pick up 3 cards at the beginning of their turn."

    def play_card(self, player):
        options = {}

        for other_player in self.game.players:
            if other_player != player:
                options[other_player.get_id()] = other_player.get_name() + \
                    "(" + str(len(other_player.hand)) + ")"

        if len(options) == 0:
            return

        player_id = player.ask(
            "Pick a player to set on fire:",
            options,
            allow_cancel=False,
            image=self.get_url()
        )
        chosen_player = self.game.get_player(player_id)

        effect = chosen_player.get_effect("Fire")

        if effect is None:
            effect = FireEffect(chosen_player, 3, 3)
            chosen_player.add_effect(effect)
        else:
            effect.n_turns += 3
