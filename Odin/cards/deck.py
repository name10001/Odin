import cards
from random import randint


class Deck:
    def __init__(self):
        self.banded_types = []
        self.banded_colours = []

    @staticmethod
    def _get_random_card():
        """
        gets a new random card from and returns it
        This does not take into account that it may be a band type
        :return: a card
        """
        place_in_deck = randint(0, cards.size_of_deck)
        up_to = 0
        for card in cards.all_cards:
            if place_in_deck in range(up_to, up_to + card.NUMBER_IN_DECK):
                return card
            else:
                up_to += card.NUMBER_IN_DECK
        raise RuntimeError("no card found.")

    def pickup(self):
        """
        gets a new random card and returns it.
        If its a banded card, it will pick another one
        It will repeat that 100 times and if it can find an acceptable one, it will just return a random one
        :return:
        """
        random_card = Deck._get_random_card()
        i = 0
        while random_card.CARD_TYPE in self.banded_types or random_card.CARD_COLOR in self.banded_colours:
            random_card = Deck._get_random_card()
            if i > 100:
                break
            i += 1
        return random_card

    def ban_color(self, color):
        self.banded_colours.append(color)

    def ban_type(self, card_type):
        self.banded_types.append(card_type)
