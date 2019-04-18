from cards.abstract_card import AbstractCard
import cards

# ~~~~~~~~~~~~~~
#     Zeros
# ~~~~~~~~~~~~~~


class BlueZero(AbstractCard):
    NAME = "Blue Zero"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "blue"
    CARD_TYPE = "0"
    CARD_TYPE_ID = 0
    CARD_IMAGE_URL = 'cards/0_blue.png'

    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class GreenZero(AbstractCard):
    NAME = "Green Zero"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "green"
    CARD_TYPE = "0"
    CARD_TYPE_ID = 0
    CARD_IMAGE_URL = 'cards/0_green.png'

    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class PurpleZero(AbstractCard):
    NAME = "Purple Zero"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "purple"
    CARD_TYPE = "0"
    CARD_TYPE_ID = 0
    CARD_IMAGE_URL = 'cards/0_purple.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class RedZero(AbstractCard):
    NAME = "Red Zero"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "red"
    CARD_TYPE = "0"
    CARD_TYPE_ID = 0
    CARD_IMAGE_URL = 'cards/0_red.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class YellowZero(AbstractCard):
    NAME = "Yellow Zero"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "yellow"
    CARD_TYPE = "0"
    CARD_TYPE_ID = 0
    CARD_IMAGE_URL = 'cards/0_yellow.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


# ~~~~~~~~~~~~~~
#     Ones
# ~~~~~~~~~~~~~~


class BlueOne(AbstractCard):
    NAME = "Blue One"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "blue"
    CARD_TYPE = "1"
    CARD_TYPE_ID = 1
    CARD_IMAGE_URL = 'cards/1_blue.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class GreenOne(AbstractCard):
    NAME = "Green One"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "green"
    CARD_TYPE = "1"
    CARD_TYPE_ID = 1
    CARD_IMAGE_URL = 'cards/1_green.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class PurpleOne(AbstractCard):
    NAME = "Purple One"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "purple"
    CARD_TYPE = "1"
    CARD_TYPE_ID = 1
    CARD_IMAGE_URL = 'cards/1_purple.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class RedOne(AbstractCard):
    NAME = "Red One"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "red"
    CARD_TYPE = "1"
    CARD_TYPE_ID = 1
    CARD_IMAGE_URL = 'cards/1_red.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class YellowOne(AbstractCard):
    NAME = "Yellow One"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "yellow"
    CARD_TYPE = "1"
    CARD_TYPE_ID = 1
    CARD_IMAGE_URL = 'cards/1_yellow.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


# ~~~~~~~~~~~~~~
#     Twos
# ~~~~~~~~~~~~~~


class BlueTwo(AbstractCard):
    NAME = "Blue Two"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "blue"
    CARD_TYPE = "2"
    CARD_TYPE_ID = 2
    CARD_IMAGE_URL = 'cards/2_blue.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class GreenTwo(AbstractCard):
    NAME = "Green Two"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "green"
    CARD_TYPE = "2"
    CARD_TYPE_ID = 2
    CARD_IMAGE_URL = 'cards/2_green.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class PurpleTwo(AbstractCard):
    NAME = "Purple Two"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "purple"
    CARD_TYPE = "2"
    CARD_TYPE_ID = 2
    CARD_IMAGE_URL = 'cards/2_purple.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class RedTwo(AbstractCard):
    NAME = "Red Two"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "red"
    CARD_TYPE = "2"
    CARD_TYPE_ID = 2
    CARD_IMAGE_URL = 'cards/2_red.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class YellowTwo(AbstractCard):
    NAME = "Yellow Two"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "yellow"
    CARD_TYPE = "2"
    CARD_TYPE_ID = 2
    CARD_IMAGE_URL = 'cards/2_yellow.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


# ~~~~~~~~~~~~~~
#     Threes
# ~~~~~~~~~~~~~~


class BlueThree(AbstractCard):
    NAME = "Blue Three"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "blue"
    CARD_TYPE = "3"
    CARD_TYPE_ID = 3
    CARD_IMAGE_URL = 'cards/3_blue.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class GreenThree(AbstractCard):
    NAME = "Green Three"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "green"
    CARD_TYPE = "3"
    CARD_TYPE_ID = 3
    CARD_IMAGE_URL = 'cards/3_green.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class PurpleThree(AbstractCard):
    NAME = "Purple Three"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "purple"
    CARD_TYPE = "3"
    CARD_TYPE_ID = 3
    CARD_IMAGE_URL = 'cards/3_purple.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class RedThree(AbstractCard):
    NAME = "Red Three"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "red"
    CARD_TYPE = "3"
    CARD_TYPE_ID = 3
    CARD_IMAGE_URL = 'cards/3_red.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class YellowThree(AbstractCard):
    NAME = "Yellow Three"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "yellow"
    CARD_TYPE = "3"
    CARD_TYPE_ID = 3
    CARD_IMAGE_URL = 'cards/3_yellow.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


# ~~~~~~~~~~~~~~
#     Fours
# ~~~~~~~~~~~~~~


class BlueFour(AbstractCard):
    NAME = "Blue Four"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "blue"
    CARD_TYPE = "4"
    CARD_TYPE_ID = 4
    CARD_IMAGE_URL = 'cards/4_blue.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class GreenFour(AbstractCard):
    NAME = "Green Four"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "green"
    CARD_TYPE = "4"
    CARD_TYPE_ID = 4
    CARD_IMAGE_URL = 'cards/4_green.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class PurpleFour(AbstractCard):
    NAME = "Purple Four"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "purple"
    CARD_TYPE = "4"
    CARD_TYPE_ID = 4
    CARD_IMAGE_URL = 'cards/4_purple.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class RedFour(AbstractCard):
    NAME = "Red Four"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "red"
    CARD_TYPE = "4"
    CARD_TYPE_ID = 4
    CARD_IMAGE_URL = 'cards/4_red.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class YellowFour(AbstractCard):
    NAME = "Yellow Four"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "yellow"
    CARD_TYPE = "4"
    CARD_TYPE_ID = 4
    CARD_IMAGE_URL = 'cards/4_yellow.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


# ~~~~~~~~~~~~~~
#     Fives
# ~~~~~~~~~~~~~~


class BlueFive(AbstractCard):
    NAME = "Blue Five"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "blue"
    CARD_TYPE = "5"
    CARD_TYPE_ID = 5
    CARD_IMAGE_URL = 'cards/5_blue.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class GreenFive(AbstractCard):
    NAME = "Green Five"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "green"
    CARD_TYPE = "5"
    CARD_TYPE_ID = 5
    CARD_IMAGE_URL = 'cards/5_green.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class PurpleFive(AbstractCard):
    NAME = "Purple Five"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "purple"
    CARD_TYPE = "5"
    CARD_TYPE_ID = 5
    CARD_IMAGE_URL = 'cards/5_purple.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class RedFive(AbstractCard):
    NAME = "Red Five"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "red"
    CARD_TYPE = "5"
    CARD_TYPE_ID = 5
    CARD_IMAGE_URL = 'cards/5_red.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class YellowFive(AbstractCard):
    NAME = "Yellow Five"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "yellow"
    CARD_TYPE = "5"
    CARD_TYPE_ID = 5
    CARD_IMAGE_URL = 'cards/5_yellow.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


# ~~~~~~~~~~~~~~
#     Sixs
# ~~~~~~~~~~~~~~


class BlueSix(AbstractCard):
    NAME = "Blue Six"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "blue"
    CARD_TYPE = "6"
    CARD_TYPE_ID = 6
    CARD_IMAGE_URL = 'cards/6_blue.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class GreenSix(AbstractCard):
    NAME = "Green Six"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "green"
    CARD_TYPE = "6"
    CARD_TYPE_ID = 6
    CARD_IMAGE_URL = 'cards/6_green.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class PurpleSix(AbstractCard):
    NAME = "Purple Six"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "purple"
    CARD_TYPE = "6"
    CARD_TYPE_ID = 6
    CARD_IMAGE_URL = 'cards/6_purple.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class RedSix(AbstractCard):
    NAME = "Red Six"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "red"
    CARD_TYPE = "6"
    CARD_TYPE_ID = 6
    CARD_IMAGE_URL = 'cards/6_red.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class YellowSix(AbstractCard):
    NAME = "Yellow Six"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "yellow"
    CARD_TYPE = "6"
    CARD_TYPE_ID = 6
    CARD_IMAGE_URL = 'cards/6_yellow.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


# ~~~~~~~~~~~~~~
#     Sevens
# ~~~~~~~~~~~~~~


class BlueSeven(AbstractCard):
    NAME = "Blue Seven"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "blue"
    CARD_TYPE = "7"
    CARD_TYPE_ID = 7
    CARD_IMAGE_URL = 'cards/7_blue.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class GreenSeven(AbstractCard):
    NAME = "Green Seven"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "green"
    CARD_TYPE = "7"
    CARD_TYPE_ID = 7
    CARD_IMAGE_URL = 'cards/7_green.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class PurpleSeven(AbstractCard):
    NAME = "Purple Seven"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "purple"
    CARD_TYPE = "7"
    CARD_TYPE_ID = 7
    CARD_IMAGE_URL = 'cards/7_purple.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class RedSeven(AbstractCard):
    NAME = "Red Seven"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "red"
    CARD_TYPE = "7"
    CARD_TYPE_ID = 7
    CARD_IMAGE_URL = 'cards/7_red.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class YellowSeven(AbstractCard):
    NAME = "Yellow Seven"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "yellow"
    CARD_TYPE = "7"
    CARD_TYPE_ID = 7
    CARD_IMAGE_URL = 'cards/7_yellow.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


# ~~~~~~~~~~~~~~
#     Eights
# ~~~~~~~~~~~~~~


class BlueEight(AbstractCard):
    NAME = "Blue Eight"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "blue"
    CARD_TYPE = "8"
    CARD_TYPE_ID = 8
    CARD_IMAGE_URL = 'cards/8_blue.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class GreenEight(AbstractCard):
    NAME = "Green Eight"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "green"
    CARD_TYPE = "8"
    CARD_TYPE_ID = 8
    CARD_IMAGE_URL = 'cards/8_green.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class PurpleEight(AbstractCard):
    NAME = "Purple Eight"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "purple"
    CARD_TYPE = "8"
    CARD_TYPE_ID = 8
    CARD_IMAGE_URL = 'cards/8_purple.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class RedEight(AbstractCard):
    NAME = "Red Eight"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "red"
    CARD_TYPE = "8"
    CARD_TYPE_ID = 8
    CARD_IMAGE_URL = 'cards/8_red.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class YellowEight(AbstractCard):
    NAME = "Yellow Eight"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "yellow"
    CARD_TYPE = "8"
    CARD_TYPE_ID = 8
    CARD_IMAGE_URL = 'cards/8_yellow.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


# ~~~~~~~~~~~~~~
#     Nines
# ~~~~~~~~~~~~~~


class BlueNine(AbstractCard):
    NAME = "Blue Nine"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "blue"
    CARD_TYPE = "9"
    CARD_TYPE_ID = 9
    CARD_IMAGE_URL = 'cards/9_blue.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class GreenNine(AbstractCard):
    NAME = "Green Nine"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "green"
    CARD_TYPE = "9"
    CARD_TYPE_ID = 9
    CARD_IMAGE_URL = 'cards/9_green.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class PurpleNine(AbstractCard):
    NAME = "Purple Nine"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "purple"
    CARD_TYPE = "9"
    CARD_TYPE_ID = 9
    CARD_IMAGE_URL = 'cards/9_purple.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class RedNine(AbstractCard):
    NAME = "Red Nine"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "red"
    CARD_TYPE = "9"
    CARD_TYPE_ID = 9
    CARD_IMAGE_URL = 'cards/9_red.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class YellowNine(AbstractCard):
    NAME = "Yellow Nine"
    NUMBER_IN_DECK = 2
    CARD_COLOUR = "yellow"
    CARD_TYPE = "9"
    CARD_TYPE_ID = 9
    CARD_IMAGE_URL = 'cards/9_yellow.png'
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


# ~~~~~~~~~~~~~~
#   SixtyNines
# ~~~~~~~~~~~~~~


class BlueSixtyNine(AbstractCard):
    NAME = "Blue Sixty Nine"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "blue"
    CARD_TYPE = "69"
    CARD_TYPE_ID = 10
    CARD_IMAGE_URL = 'cards/69_blue.png'
    EFFECT_DESCRIPTION = "A surprise ;)"
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class GreenSixtyNine(AbstractCard):
    NAME = "Green Sixty Nine"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "green"
    CARD_TYPE = "69"
    CARD_TYPE_ID = 10
    CARD_IMAGE_URL = 'cards/69_green.png'
    EFFECT_DESCRIPTION = "A surprise ;)"
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class PurpleSixtyNine(AbstractCard):
    NAME = "Purple Sixty Nine"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "purple"
    CARD_TYPE = "69"
    CARD_TYPE_ID = 10
    CARD_IMAGE_URL = 'cards/69_purple.png'
    EFFECT_DESCRIPTION = "A surprise ;)"
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class RedSixtyNine(AbstractCard):
    NAME = "Red Sixty Nine"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "red"
    CARD_TYPE = "69"
    CARD_TYPE_ID = 10
    CARD_IMAGE_URL = 'cards/69_red.png'
    EFFECT_DESCRIPTION = "A surprise ;)"
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)


class YellowSixtyNine(AbstractCard):
    NAME = "Yellow Sixty Nine"
    NUMBER_IN_DECK = 1
    CARD_COLOUR = "yellow"
    CARD_TYPE = "69"
    CARD_TYPE_ID = 10
    CARD_IMAGE_URL = 'cards/69_yellow.png'
    EFFECT_DESCRIPTION = "A surprise ;)"
    COMPATIBILITY_DESCRIPTION = cards.default_card_compatibility_description(CARD_COLOUR,CARD_TYPE)
