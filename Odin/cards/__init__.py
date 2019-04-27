from random import choice
from cards.the_boring_cards import *
from cards.all_other_cards import *
from cards.card_frequency import *
from cards.deck import Deck
from flask import url_for

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
    BlueReverse, GreenReverse, PurpleReverse, RedReverse, YellowReverse, WhiteReverse, BlackReverse,
    BlueFuck, GreenFuck, RedFuck, YellowFuck, BlackFuck,
    BlueTrash, GreenTrash, RedTrash, YellowTrash,
    BluePickup2, GreenPickup2, PurplePickup2, RedPickup2, YellowPickup2, WhitePickup2, BlackPickup2,
    Pickup10, Pickup4, PickupTimes2, Pawn, FeelingBlue, Plus, FuckYou, AtomicBomb, PickupPower2, Pickup100, PickupFactorial,
    EA15, EA20, EA30, EA100,
    BlankBro, Happiness,
    SwapHand, Communist, Capitalist, Genocide, Jesus, FreeTurn, Thanos, Odin, CopyCat,
    ManOfTheDay, LadyOfTheNight, Creeper, Smurf, FilthySharon, Nazi, 
    ColourChooser, RedBlueSwapper, RedGreenSwapper, RedYellowSwapper, GreenBlueSwapper,
    BlueYellowSwapper, YellowGreenSwapper, BlackWhiteSwapper
]

# find information about all cards
all_card_info = []
all_urls = []
all_types = []
all_colours = []
for card in all_cards:
    card_info = {
        "url": '/static/' + card.CARD_IMAGE_URL,  # default url
        "name": card.NAME,
        "type": card.CARD_TYPE,
        "colour": card.CARD_COLOUR,
        "can be on pickup": card.CAN_BE_ON_PICKUP,
        "effect description": card.EFFECT_DESCRIPTION,
        "compatibility description": card.get_compatibility_description()
    }
    all_urls.append('/static/' + card.CARD_IMAGE_URL)
    for url in card.ADDITIONAL_URLS:
        all_urls.append('/static/' + url)

    all_card_info.append(card_info)
    if card.CARD_TYPE not in all_types:
        all_types.append(card.CARD_TYPE)
    if card.CARD_COLOUR not in all_colours:
        all_colours.append(card.CARD_COLOUR)

# highest one takes priority!
# don't mix "types" and "colours", only use one per index
miscellaneous_category_index = 3
category_indexes = (
    {
        "colours": (),
        "types": ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '69'),
        "index": 1
    },
    {
        "colours": (),
        "types": ("Fuckin' M8"),
        "index": 2
    },
    {
        "colours": (),
        "types": ("Creeper", "Smurf", "Lady Of The Night", "Man Of The Day"),
        "index": 4
    },
    {
        "colours": (),
        "types": ('Reverse', 'Skip'),
        "index": 5
    },
    {
        "colours": (),
        "types": ('+2', '+4', '+10', '+100', 'x2', 'x Squared', "Factorial"),
        "index": 6
    },
    {
        "colours": (),
        "types": ('Atomic Bomb', 'Fuck You', 'Plus', 'Pawn'),
        "index": 7
    },
    {
        "colours": ('black', 'white'),
        "types": (),
        "index": 8
    }
)


def get_card_index(card):
    """
    Finds and returns the category index of the given card.
    This is used for sorting cards by category.
    The higher the index the higher in the pile it should be
    :param card: card ti find the category of
    :return: int that represents the category that its in
    """
    for category_index in category_indexes:
        if card.get_type() in category_index["types"]:
            point = category_index["types"].index(card.get_type()) / len(category_index["types"])
            return category_index["index"] + point
        if card.get_colour() in category_index["colours"]:
            point = category_index["colours"].index(card.get_colour()) / len(category_index["colours"])
            return category_index["index"] + point
    return miscellaneous_category_index


def get_random_card():
    """
    gets a random card with no weights.
    This shouldn't really occur because you should win the game if you can't pick anything up
    :return:
    """
    return choice(all_cards)
