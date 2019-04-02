from random import randint
from cards.the_boring_cards import *
from cards.deck import Deck

all_cards = [
    BlueZero, GreenZero, PurpleZero, RedZero, YellowZero, 
    BlueOne, GreenOne, PurpleOne, RedOne, YellowOne, 
    BlueTwo, GreenTwo, PurpleTwo, RedTwo, YellowTwo, 
    BlueThree, GreenThree, PurpleThree, RedThree, YellowThree, 
    BlueFour, GreenFour, PurpleFour, RedFour, YellowFour, 
    BlueFive, GreenFive, PurpleFive, RedFive, YellowFive, 
    BlueSix, GreenSix, PurpleSix, RedSix, YellowSix, 
    BlueSeven, GreenSeven, PurpleSeven, RedSeven, YellowSeven, 
    BlueEight, GreenEight, PurpleEight, RedEight, YellowEight, 
    BlueNine, GreenNine, PurpleNine, RedNine, YellowNine, 
    BlueSixtyNine, GreenSixtyNine, PurpleSixtyNine, RedSixtyNine, YellowSixtyNine, 
]


# find information about all cards
all_types = []
all_colours = []
size_of_deck = 0
for card in all_cards:
    size_of_deck += card.NUMBER_IN_DECK
    if card.CARD_TYPE not in all_types:
        all_types.append(card.CARD_TYPE)
    if card.CARD_COLOUR not in all_colours:
        all_colours.append(card.CARD_COLOUR)


def get_random_card():
    """
    gets a new random card and returns it
    This does not take into account that it may be a band type
    use Deck class for that
    :return: a card
    """
    place_in_deck = randint(0, size_of_deck)
    up_to = 0
    for card in all_cards:
        if place_in_deck in range(up_to, up_to + card.NUMBER_IN_DECK):
            return card
        else:
            up_to += card.NUMBER_IN_DECK
    raise RuntimeError("no card found.")
