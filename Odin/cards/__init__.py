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

size_of_deck = 0
for card in all_cards:
    size_of_deck += card.NUMBER_IN_DECK
