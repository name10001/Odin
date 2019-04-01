from random import randint
from cards.the_boring_cards import *

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

_size_of_deck = 0
for card in all_cards:
    _size_of_deck += card.NUMBER_IN_DECK


def pickup_from_deck():
    """
    gets a new random card from the deck and returns it
    :return: a card
    """
    place_in_deck = randint(0, _size_of_deck)
    up_to = 0
    for card in all_cards:
        if place_in_deck in range(up_to, up_to + card.NUMBER_IN_DECK):
            return card
        else:
            up_to += card.NUMBER_IN_DECK
    raise RuntimeError("no card found.")
