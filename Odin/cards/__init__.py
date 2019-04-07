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
    Pickup10, Pickup4, PickupTimes2, Pawn, FeelingBlue, Plus, FuckYou, AtomicBomb,
    EA15, EA20, EA30,
    BlankBro, Happiness,
    SwapHand, Communist, Capitalist, Genocide, Jesus, FreeTurn, Thanos,
    ManOfTheDay, LadyOfTheNight, Creeper, Smurf, FilthySharon, Nazi, ColourSwapper
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
        "types": ("Fuckin' M8", "Creeper", "Smurf", "Lady Of The Night", "Man Of The Day", "Thanos"),
        "index": 2
    },
    {
        "colours": (),
        "types": ('Reverse', 'Skip'),
        "index": 3
    },
    {
        "colours": (),
        "types": ('+2', '+10', '+4', 'x2'),
        "index": 4
    },
    {
        "colours": ('black'),
        "types": (),
        "index": 5
    },
    {
        "colours": ('white'),
        "types": (),
        "index": 6
    },
]


def get_card_index(card):
    """
    Finds and returns the category index of the given card.
    This is used for sorting cards by category.
    The higher the index the higher in the pile it should be
    :param card: card ti find the category of
    :return: int that represents the category that its in
    """
    for category_index in category_indexs:
        if card.get_type() in category_index["types"]:
            return category_index["index"]
        if card.get_colour() in category_index["colours"]:
            return category_index["index"]
    return miscellaneous_category_index


def get_random_card():
    """
    gets a new random card and returns it
    This does not take into account that it may be a banned type
    use a Deck class for that
    :return: an uninitiated card
    """
    place_in_deck = randint(0, size_of_deck)
    up_to = 0
    for card in all_cards:
        if place_in_deck in range(up_to, up_to + card.NUMBER_IN_DECK - 1):
            return card
        else:
            up_to += card.NUMBER_IN_DECK
    raise RuntimeError("no card found.")
