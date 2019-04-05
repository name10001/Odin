from random import randint
from cards.the_boring_cards import *
from cards.all_other_cards import *
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
    BlueSkip, GreenSkip, PurpleSkip, RedSkip, YellowSkip, WhiteSkip, BlackSkip,
    BluePickup2, GreenPickup2, PurplePickup2, RedPickup2, YellowPickup2, WhitePickup2, BlackPickup2,
    BlueReverse, GreenReverse, PurpleReverse, RedReverse, YellowReverse, WhiteReverse, BlackReverse,
    BlueFuck, GreenFuck, RedFuck, YellowFuck, BlackFuck,
    Pickup10, Pickup4, PickupTimes2,
    BlankBro, Happiness, SwapHand, Communist, Pawn, FeelingBlue, Plus, FuckYou, Genocide, Jesus
]


# find information about all cards
all_types = []
all_colours = []
size_of_deck = 0
all_urls = []
for card in all_cards:
    size_of_deck += card.NUMBER_IN_DECK
    all_urls.append(card.CARD_IMAGE_URL)
    if card.CARD_TYPE not in all_types:
        all_types.append(card.CARD_TYPE)
    if card.CARD_COLOUR not in all_colours:
        all_colours.append(card.CARD_COLOUR)

miscellaneous_category_index = 2
# highest one takes priority!
category_indexs = [
    {
        "colours": (),
        "types": ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'),
        "index": 0
    },
    {
        "colours": (),
        "types": ('69'),
        "index": 1
    },
    {
        "colours": (),
        "types": ('pickup2', 'pickup10', 'pickup4', 'pickupTimes2'),
        "index": 5
    },
    {
        "colours": ('black'),
        "types": (),
        "index": 3
    },
    {
        "colours": ('white'),
        "types": (),
        "index": 4
    }
]


def get_card_index(card):
    for category_index in category_indexs:
        if card.CARD_TYPE in category_index["types"]:
            return category_index["index"]
        if card.CARD_COLOUR in category_index["colours"]:
            return category_index["index"]
    return miscellaneous_category_index


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
        if place_in_deck in range(up_to, up_to + card.NUMBER_IN_DECK - 1):
            return card
        else:
            up_to += card.NUMBER_IN_DECK
    raise RuntimeError("no card found.")
