from cards.abstract_card import AbstractCard


class ColourChooser(AbstractCard):
    NAME = "Colour Chooser"
    CARD_IMAGE_URL = 'color_swapper.png'
    CARD_COLOUR = "black"
    CARD_TYPE = "Colour Chooser"
    EFFECT_DESCRIPTION = "Allows you to change the colour to any of the 4 given colours: red, green, yellow or blue."
    COMPATIBILITY_DESCRIPTION = "Before play: Regular black card, compatible with any black, red, green, blue or " \
                                "yellow cards. After play: Compatible any cards of the colour picked and black cards."
    ADDITIONAL_URLS = ['choose_yellow.png', 'choose_blue.png',
                       'choose_red.png', 'choose_green.png']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colour = "black"
        self.url = self.CARD_IMAGE_URL

    def is_compatible_with(self, player, card):
        """
        This compatibility method is used to prevent white cards from being able to be played on top
        """
        if card.get_colour() == "white" or card.get_colour() == "purple":
            return False
        else:
            return True

    def prepare_card(self, player, allow_cancel):
        option = player.ask(
            "Choose colour:",
            {
                "red": "Red",
                "green": "Green",
                "blue": "Blue",
                "yellow": "Yellow"
            },
            allow_cancel=allow_cancel,
            image=self.get_url()
        )
        if option is None:
            return False

        self.colour = option
        self.url = 'choose_' + option + '.png'
        return True

    def undo_prepare_card(self, player):
        self.url = self.CARD_IMAGE_URL
        self.colour = "black"

    def get_colour(self):
        return self.colour

    def get_url(self):
        return '/static/cards/' + self.url


class ColourSwapper(AbstractCard):
    """
    Abstract double-colour swapper card
    """
    CARD_TYPE = "Colour Swapper"
    COLOUR_1 = "black"
    COLOUR_2 = "black"
    CARD_COLOUR = "colour swapper"
    EFFECT_DESCRIPTION = "When played on one of the colours shown on the card, this card will swap to the " \
                         "opposite card. If played on a colour that is not shown on the card " \
                         "you get to choose the colour it switches to."
    COMPATIBILITY_DESCRIPTION = "Before play: Compatible with any {cls.COLOUR_1}," \
                                "{cls.COLOUR_2}, white or black cards. \n" \
                                "After play: Compatible with any cards of the chosen colour, white or black cards. " \
                                "Note: when playing multiple, the colours must be compatible too."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # gets changed to a particular colour after being played
        self.colour = "colour swapper"
        self.url = self.CARD_IMAGE_URL

    def is_compatible_with(self, player, card):
        if self.colour == "colour swapper":  # compatible if either of the card colours are compatible
            if self.colours_are_compatible(card.get_colour(), self.COLOUR_1) \
                    or self.colours_are_compatible(card.get_colour(), self.COLOUR_2):
                return True
        else:
            return super().is_compatible_with(player, card)

    def prepare_card(self, player, allow_cancel):
        played_on = self.game.get_top_card()

        # change colour to the opposite of the one you played on
        first_compatible = self.colours_are_compatible(
            played_on.get_colour(), self.COLOUR_1)
        second_compatible = self.colours_are_compatible(
            played_on.get_colour(), self.COLOUR_2)
        if first_compatible and not second_compatible:
            self.colour = self.COLOUR_2
        elif second_compatible and not first_compatible:
            self.colour = self.COLOUR_1
        else:
            colour = player.ask(
                "Select colour:",
                {
                    self.COLOUR_1: self.COLOUR_1.capitalize(),
                    self.COLOUR_2: self.COLOUR_2.capitalize()
                },
                allow_cancel=allow_cancel,
                image=self.get_url()
            )
            if colour is None:
                return False

            self.colour = colour
        self.url = 'switch_' + self.colour + '.png'
        return True

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
        return '/static/cards/' + self.url


class RedBlueSwapper(ColourSwapper):
    NAME = "Red/Blue Colour Swapper"
    CARD_IMAGE_URL = 'blue_red.png'
    COLOUR_1 = "red"
    COLOUR_2 = "blue"


class RedYellowSwapper(ColourSwapper):
    NAME = "Red/Yellow Colour Swapper"
    CARD_IMAGE_URL = 'red_yellow.png'
    COLOUR_1 = "red"
    COLOUR_2 = "yellow"


class RedGreenSwapper(ColourSwapper):
    NAME = "Red/Green Colour Swapper"
    CARD_IMAGE_URL = 'green_red.png'
    COLOUR_1 = "red"
    COLOUR_2 = "green"


class GreenBlueSwapper(ColourSwapper):
    NAME = "Green/Blue Colour Swapper"
    CARD_IMAGE_URL = 'green_blue.png'
    COLOUR_1 = "green"
    COLOUR_2 = "blue"


class BlueYellowSwapper(ColourSwapper):
    NAME = "Yellow/Blue Colour Swapper"
    CARD_IMAGE_URL = 'yellow_blue.png'
    COLOUR_1 = "yellow"
    COLOUR_2 = "blue"


class YellowGreenSwapper(ColourSwapper):
    NAME = "Yellow/Green Colour Swapper"
    CARD_IMAGE_URL = 'green_yellow.png'
    COLOUR_1 = "yellow"
    COLOUR_2 = "green"


class BlackWhiteSwapper(ColourSwapper):
    NAME = "Black/White Colour Swapper"
    CARD_IMAGE_URL = 'black_white.png'
    COLOUR_1 = "black"
    COLOUR_2 = "white"
    COMPATIBILITY_DESCRIPTION = "Before play: Compatible with all colours. " \
                                "After play: Depends on the colour you selected. Black is compatible with any red, " \
                                "blue, green, yellow and black cards. " \
                                "White is compatible with any red, blue, green, yellow, purple and white cards. "
    ADDITIONAL_URLS = ['switch_black.png', 'switch_white.png', 'switch_red.png',
                       'switch_yellow.png', 'switch_green.png', 'switch_blue.png']
