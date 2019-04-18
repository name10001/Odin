def default_card_compatibility_description(colour, type):
    if colour == "black":
        return "This is a regular black card. Black cards are compatible with everything except white cards and purple cards. Always compatible and can be played with other " + type + " cards."
    elif colour == "white":
        return "This is a regular white card. White cards are compatible with everything except black cards. Always compatible and can be played with other " + type + " cards."
    elif colour == "purple":
        return "This is a regular purple card. Purple cards are compatible with all purple cards and white cards. Always compatible and can be played with other " + type + " cards."
    else:
        return "This is a regular " + colour + " card. " + colour.capitalize() + " cards are compatible with all other " + colour + " cards and can be played with any white or black card too. Always compatible and can be played with other " + type + " cards."


from random import choices
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
    ManOfTheDay, LadyOfTheNight, Creeper, Smurf, FilthySharon, Nazi, 
    ColourChooser, RedBlueSwapper, RedGreenSwapper, RedYellowSwapper, GreenBlueSwapper,
    BlueYellowSwapper, YellowGreenSwapper, BlackWhiteSwapper
]


card_weights = [card.NUMBER_IN_DECK for card in all_cards]

# find information about all cards
all_types = []
all_colours = []
size_of_deck = 0
# all_urls = []
for card in all_cards:
    size_of_deck += card.NUMBER_IN_DECK
    # all_urls.append(card.CARD_IMAGE_URL)
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
        "types": ("Fuckin' M8"),
        "index": 3
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
        "types": ('+2', '+10', '+4', 'x2'),
        "index": 6
    },
    {
        "colours": ('black'),
        "types": (),
        "index": 7
    },
    {
        "colours": ('white'),
        "types": (),
        "index": 8
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


def get_random_cards(number):
    """
    gets a new random card and returns it
    This does not take into account that it may be a banned type
    use a Deck class for that
    :param number: the number of cards to return
    :return: an uninitiated card array
    """
    return choices(all_cards, weights=card_weights, k=number)


def get_random_card():
    """
    gets a new random card and returns it
    This does not take into account that it may be a banned type
    use a Deck class for that
    :return:
    """
    return get_random_cards(1)[0]


def colours_are_compatible(colour1, colour2):
    if colour1 == colour2:
        return True
    elif colour1 == "white":
        return colour2 != "black"
    elif colour1 == "black":
        return colour2 != "white" and colour2 != "purple"
    elif colour1 == "purple":
        return colour2 == "white"
    else:
        return colour2 == "white" or colour2 == "black"