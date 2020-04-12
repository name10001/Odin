from cards.abstract_card import AbstractCard
from cards.card_frequency import CardFrequency


# ~~~~~~~~~~~~~~
# all of same colour
# ~~~~~~~~~~~~~~


class AllOfSameColour(AbstractCard):
    CARD_FREQUENCY = CardFrequency(1, max_cards=1, starting=0, elevator=0)
    MULTI_COLOURED = False
    PICK_NUMBERS = True  # False for filthy sharon cause no numbers

    def can_play_with(self, player, card, is_first_card):
        return card.get_colour() == self.get_colour()

    def prepare_card(self, player, allow_cancel):
        """
        Play all the cards in the players hand that are of the same colour as this one
        """

        options = {
            "player pick": "No, let me pick (recommended)",
            "server pick all": "Yes: Select all"
        }
        if self.PICK_NUMBERS is True:
            options["server pick numbers"] = "Yes: Only Numbers"
        option = player.ask("Would you like the game to automatically pick cards?",
                            options, allow_cancel=allow_cancel, image=self.get_url())

        if option is None:
            return False

        if option == "server pick all":
            for card in reversed(player.hand):
                if card.get_colour() == self.get_colour():
                    player.prepare_cards([card.get_id()])
        elif option == "server pick numbers":
            for card in reversed(player.hand):
                if card.get_colour() == self.get_colour() and card.get_type().isnumeric():
                    player.prepare_cards([card.get_id()])

        return True


class ManOfTheDay(AllOfSameColour):
    NAME = "Man Of The Day"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'man_of_the_day.png'
    CARD_TYPE = "Man Of The Day"
    EFFECT_DESCRIPTION = "Allows you to place as many yellow cards as you like with this card on your turn."


class LadyOfTheNight(AllOfSameColour):
    NAME = "Lady Of The Night"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'lady_of_the_night.png'
    CARD_TYPE = "Lady Of The Night"
    EFFECT_DESCRIPTION = "Allows you to place as many red cards as you like with this card on your turn."


class Smurf(AllOfSameColour):
    NAME = "Smurf"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'smurf.png'
    CARD_TYPE = "Smurf"
    EFFECT_DESCRIPTION = "Allows you to place as many blue cards as you like with this card on your turn."


class Creeper(AllOfSameColour):
    NAME = "Creeper"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'creeper.png'
    CARD_TYPE = "Creeper"
    EFFECT_DESCRIPTION = "Allows you to place as many green cards as you like with this card on your turn."


class FilthySharon(AllOfSameColour):
    NAME = "Filthy Sharon"
    CARD_COLOUR = "white"
    CARD_IMAGE_URL = 'filthy_sharon.png'
    CARD_TYPE = "Filthy Sharon"
    PICK_NUMBERS = False
    EFFECT_DESCRIPTION = "Allows you to place as many white cards as you like with this card on your turn."


class BlackHole(AbstractCard):
    CARD_FREQUENCY = CardFrequency(0.03, starting=0, elevator=0, max_cards=1)
    NAME = "Black Hole"
    CARD_TYPE = "Black Hole"
    CARD_COLOUR = "black"
    CARD_IMAGE_URL = 'black_hole.png'
    MULTI_COLOURED = False
    EFFECT_DESCRIPTION = "Allows you to place as many black cards as you like with this card on your turn."
    COMPATIBILITY_DESCRIPTION = "Before play: This card is only compatible with black cards. " \
                                "After play: Regular black card rules apply, such that it is compatible with " \
                                "any red, green, yellow, blue or black cards."

    def can_be_played_on(self, player, card):
        if player.is_turn() is False:
            return False
        if self.game.pickup != 0 and self.can_be_on_pickup() is False:
            return False
        return card.get_colour() == "black"

    def can_play_with(self, player, card, is_first_card):
        return card.get_type() == self.get_type() or card.get_colour() == "black"


class PlayOne(AbstractCard):
    NAME = "Play One"
    CARD_COLOUR = "rainbow"
    CARD_TYPE = "Play Card"
    CARD_IMAGE_URL = "play_1.png"
    MUTLI_COLOURED = False
    EFFECT_DESCRIPTION = "Allows you to play any card from your hand with this, reguardless of compatibility rules."
    CARD_FREQUENCY = CardFrequency(1, 0.5, 0.2, starting=0, max_cards=8, elevator=0)

    NUM_TO_PLAY = 1

    def can_play_with(self, player, card, is_first_card):
        """
        Any n cards can be played on top of this.
        """

        if card.get_type() == self.get_type() and is_first_card:
            return True

        # determine how many cards have been played after a Play card
        num_to_play = 0

        for card in self.game.planning_pile:
            if isinstance(card, PlayOne):
                num_to_play += card.NUM_TO_PLAY
            elif num_to_play > 0:
                num_to_play -= 1

        return num_to_play > 0


class PlayThree(PlayOne):
    NAME = "Play Three"
    CARD_IMAGE_URL = "play_3.png"
    EFFECT_DESCRIPTION = "Allows you to play any 3 cards from your hand with this, reguardless of compatibility rules."
    CARD_FREQUENCY = CardFrequency(0.7, 0.3, 0.08, starting=0, max_cards=8, elevator=0)

    NUM_TO_PLAY = 3
