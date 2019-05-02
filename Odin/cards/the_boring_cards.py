from cards.abstract_card import AbstractCard
import cards
from cards.all_other_cards import *
from cards.card_frequency import CardFrequency
import random


class NumberCard(AbstractCard):
    CARD_FREQUENCY = CardFrequency(2)

    def prepare_card(self, player):
        if len(self.game.planning_pile) == 0:
            return
        if hasattr(self.game.planning_pile[0], 'still_needs'):
            self.game.planning_pile[0].still_needs -= int(self.get_type())

    def undo_prepare_card(self, player):
        if len(self.game.planning_pile) == 0:
            return
        if hasattr(self.game.planning_pile[0], 'still_needs'):
            self.game.planning_pile[0].still_needs += int(self.get_type())

# ~~~~~~~~~~~~~~
#     Zeros
# ~~~~~~~~~~~~~~


class BlueZero(NumberCard):
    NAME = "Blue Zero"
    CARD_FREQUENCY = CardFrequency(1)
    CARD_COLOUR = "blue"
    CARD_TYPE = "0"
    CARD_IMAGE_URL = 'cards/0_blue.png'


class GreenZero(NumberCard):
    NAME = "Green Zero"
    CARD_FREQUENCY = CardFrequency(1)
    CARD_COLOUR = "green"
    CARD_TYPE = "0"
    CARD_IMAGE_URL = 'cards/0_green.png'


class PurpleZero(NumberCard):
    NAME = "Purple Zero"
    CARD_FREQUENCY = CardFrequency(1)
    CARD_COLOUR = "purple"
    CARD_TYPE = "0"
    CARD_IMAGE_URL = 'cards/0_purple.png'


class RedZero(NumberCard):
    NAME = "Red Zero"
    CARD_FREQUENCY = CardFrequency(1)
    CARD_COLOUR = "red"
    CARD_TYPE = "0"
    CARD_IMAGE_URL = 'cards/0_red.png'


class YellowZero(NumberCard):
    NAME = "Yellow Zero"
    CARD_FREQUENCY = CardFrequency(1)
    CARD_COLOUR = "yellow"
    CARD_TYPE = "0"
    CARD_IMAGE_URL = 'cards/0_yellow.png'


# ~~~~~~~~~~~~~~
#     Ones
# ~~~~~~~~~~~~~~


class BlueOne(NumberCard):
    NAME = "Blue One"
    CARD_COLOUR = "blue"
    CARD_TYPE = "1"
    CARD_IMAGE_URL = 'cards/1_blue.png'


class GreenOne(NumberCard):
    NAME = "Green One"
    CARD_COLOUR = "green"
    CARD_TYPE = "1"
    CARD_IMAGE_URL = 'cards/1_green.png'


class PurpleOne(NumberCard):
    NAME = "Purple One"
    CARD_FREQUENCY = CardFrequency(1)
    CARD_COLOUR = "purple"
    CARD_TYPE = "1"
    CARD_IMAGE_URL = 'cards/1_purple.png'


class RedOne(NumberCard):
    NAME = "Red One"
    CARD_COLOUR = "red"
    CARD_TYPE = "1"
    CARD_IMAGE_URL = 'cards/1_red.png'


class YellowOne(NumberCard):
    NAME = "Yellow One"
    CARD_COLOUR = "yellow"
    CARD_TYPE = "1"
    CARD_IMAGE_URL = 'cards/1_yellow.png'


# ~~~~~~~~~~~~~~
#     Twos
# ~~~~~~~~~~~~~~


class BlueTwo(NumberCard):
    NAME = "Blue Two"
    CARD_COLOUR = "blue"
    CARD_TYPE = "2"
    CARD_IMAGE_URL = 'cards/2_blue.png'


class GreenTwo(NumberCard):
    NAME = "Green Two"
    CARD_COLOUR = "green"
    CARD_TYPE = "2"
    CARD_IMAGE_URL = 'cards/2_green.png'


class PurpleTwo(NumberCard):
    NAME = "Purple Two"
    CARD_FREQUENCY = CardFrequency(1)
    CARD_COLOUR = "purple"
    CARD_TYPE = "2"
    CARD_IMAGE_URL = 'cards/2_purple.png'


class RedTwo(NumberCard):
    NAME = "Red Two"
    CARD_COLOUR = "red"
    CARD_TYPE = "2"
    CARD_IMAGE_URL = 'cards/2_red.png'


class YellowTwo(NumberCard):
    NAME = "Yellow Two"
    CARD_COLOUR = "yellow"
    CARD_TYPE = "2"
    CARD_IMAGE_URL = 'cards/2_yellow.png'


# ~~~~~~~~~~~~~~
#     Threes
# ~~~~~~~~~~~~~~


class BlueThree(NumberCard):
    NAME = "Blue Three"
    CARD_COLOUR = "blue"
    CARD_TYPE = "3"
    CARD_IMAGE_URL = 'cards/3_blue.png'


class GreenThree(NumberCard):
    NAME = "Green Three"
    CARD_COLOUR = "green"
    CARD_TYPE = "3"
    CARD_IMAGE_URL = 'cards/3_green.png'


class PurpleThree(NumberCard):
    NAME = "Purple Three"
    CARD_FREQUENCY = CardFrequency(1)
    CARD_COLOUR = "purple"
    CARD_TYPE = "3"
    CARD_IMAGE_URL = 'cards/3_purple.png'


class RedThree(NumberCard):
    NAME = "Red Three"
    
    CARD_COLOUR = "red"
    CARD_TYPE = "3"
    CARD_IMAGE_URL = 'cards/3_red.png'


class YellowThree(NumberCard):
    NAME = "Yellow Three"
    CARD_COLOUR = "yellow"
    CARD_TYPE = "3"
    CARD_IMAGE_URL = 'cards/3_yellow.png'


# ~~~~~~~~~~~~~~
#     Fours
# ~~~~~~~~~~~~~~


class BlueFour(NumberCard):
    NAME = "Blue Four"
    CARD_COLOUR = "blue"
    CARD_TYPE = "4"
    CARD_IMAGE_URL = 'cards/4_blue.png'


class GreenFour(NumberCard):
    NAME = "Green Four"
    CARD_COLOUR = "green"
    CARD_TYPE = "4"
    CARD_IMAGE_URL = 'cards/4_green.png'


class PurpleFour(NumberCard):
    NAME = "Purple Four"
    CARD_FREQUENCY = CardFrequency(1)
    CARD_COLOUR = "purple"
    CARD_TYPE = "4"
    CARD_IMAGE_URL = 'cards/4_purple.png'


class RedFour(NumberCard):
    NAME = "Red Four"
    CARD_COLOUR = "red"
    CARD_TYPE = "4"
    CARD_IMAGE_URL = 'cards/4_red.png'


class YellowFour(NumberCard):
    NAME = "Yellow Four"
    CARD_COLOUR = "yellow"
    CARD_TYPE = "4"
    CARD_IMAGE_URL = 'cards/4_yellow.png'


# ~~~~~~~~~~~~~~
#     Fives
# ~~~~~~~~~~~~~~


class BlueFive(NumberCard):
    NAME = "Blue Five"
    CARD_COLOUR = "blue"
    CARD_TYPE = "5"
    CARD_IMAGE_URL = 'cards/5_blue.png'


class GreenFive(NumberCard):
    NAME = "Green Five"
    CARD_COLOUR = "green"
    CARD_TYPE = "5"
    CARD_IMAGE_URL = 'cards/5_green.png'


class PurpleFive(NumberCard):
    NAME = "Purple Five"
    CARD_FREQUENCY = CardFrequency(1)
    CARD_COLOUR = "purple"
    CARD_TYPE = "5"
    CARD_IMAGE_URL = 'cards/5_purple.png'


class RedFive(NumberCard):
    NAME = "Red Five"
    CARD_COLOUR = "red"
    CARD_TYPE = "5"
    CARD_IMAGE_URL = 'cards/5_red.png'


class YellowFive(NumberCard):
    NAME = "Yellow Five"
    CARD_COLOUR = "yellow"
    CARD_TYPE = "5"
    CARD_IMAGE_URL = 'cards/5_yellow.png'


# ~~~~~~~~~~~~~~
#     Sixs
# ~~~~~~~~~~~~~~


class BlueSix(NumberCard):
    NAME = "Blue Six"
    CARD_COLOUR = "blue"
    CARD_TYPE = "6"
    CARD_IMAGE_URL = 'cards/6_blue.png'


class GreenSix(NumberCard):
    NAME = "Green Six"
    CARD_COLOUR = "green"
    CARD_TYPE = "6"
    CARD_IMAGE_URL = 'cards/6_green.png'


class PurpleSix(NumberCard):
    NAME = "Purple Six"
    CARD_FREQUENCY = CardFrequency(1)
    CARD_COLOUR = "purple"
    CARD_TYPE = "6"
    CARD_IMAGE_URL = 'cards/6_purple.png'


class RedSix(NumberCard):
    NAME = "Red Six"
    CARD_COLOUR = "red"
    CARD_TYPE = "6"
    CARD_IMAGE_URL = 'cards/6_red.png'


class YellowSix(NumberCard):
    NAME = "Yellow Six"
    CARD_COLOUR = "yellow"
    CARD_TYPE = "6"
    CARD_IMAGE_URL = 'cards/6_yellow.png'


# ~~~~~~~~~~~~~~
#     Sevens
# ~~~~~~~~~~~~~~


class BlueSeven(NumberCard):
    NAME = "Blue Seven"
    CARD_COLOUR = "blue"
    CARD_TYPE = "7"
    CARD_IMAGE_URL = 'cards/7_blue.png'


class GreenSeven(NumberCard):
    NAME = "Green Seven"
    CARD_COLOUR = "green"
    CARD_TYPE = "7"
    CARD_IMAGE_URL = 'cards/7_green.png'


class PurpleSeven(NumberCard):
    NAME = "Purple Seven"
    CARD_FREQUENCY = CardFrequency(1)
    CARD_COLOUR = "purple"
    CARD_TYPE = "7"
    CARD_IMAGE_URL = 'cards/7_purple.png'


class RedSeven(NumberCard):
    NAME = "Red Seven"
    CARD_COLOUR = "red"
    CARD_TYPE = "7"
    CARD_IMAGE_URL = 'cards/7_red.png'


class YellowSeven(NumberCard):
    NAME = "Yellow Seven"
    CARD_COLOUR = "yellow"
    CARD_TYPE = "7"
    CARD_IMAGE_URL = 'cards/7_yellow.png'


# ~~~~~~~~~~~~~~
#     Eights
# ~~~~~~~~~~~~~~


class BlueEight(NumberCard):
    NAME = "Blue Eight"
    CARD_COLOUR = "blue"
    CARD_TYPE = "8"
    CARD_IMAGE_URL = 'cards/8_blue.png'


class GreenEight(NumberCard):
    NAME = "Green Eight"
    CARD_COLOUR = "green"
    CARD_TYPE = "8"
    CARD_IMAGE_URL = 'cards/8_green.png'


class PurpleEight(NumberCard):
    NAME = "Purple Eight"
    CARD_FREQUENCY = CardFrequency(1)
    CARD_COLOUR = "purple"
    CARD_TYPE = "8"
    CARD_IMAGE_URL = 'cards/8_purple.png'


class RedEight(NumberCard):
    NAME = "Red Eight"
    CARD_COLOUR = "red"
    CARD_TYPE = "8"
    CARD_IMAGE_URL = 'cards/8_red.png'


class YellowEight(NumberCard):
    NAME = "Yellow Eight"
    CARD_COLOUR = "yellow"
    CARD_TYPE = "8"
    CARD_IMAGE_URL = 'cards/8_yellow.png'


# ~~~~~~~~~~~~~~
#     Nines
# ~~~~~~~~~~~~~~


class BlueNine(NumberCard):
    NAME = "Blue Nine"
    CARD_COLOUR = "blue"
    CARD_TYPE = "9"
    CARD_IMAGE_URL = 'cards/9_blue.png'


class GreenNine(NumberCard):
    NAME = "Green Nine"
    CARD_COLOUR = "green"
    CARD_TYPE = "9"
    CARD_IMAGE_URL = 'cards/9_green.png'


class PurpleNine(NumberCard):
    NAME = "Purple Nine"
    CARD_FREQUENCY = CardFrequency(1)
    CARD_COLOUR = "purple"
    CARD_TYPE = "9"
    CARD_IMAGE_URL = 'cards/9_purple.png'


class RedNine(NumberCard):
    NAME = "Red Nine"
    CARD_COLOUR = "red"
    CARD_TYPE = "9"
    CARD_IMAGE_URL = 'cards/9_red.png'


class YellowNine(NumberCard):
    NAME = "Yellow Nine"
    CARD_COLOUR = "yellow"
    CARD_TYPE = "9"
    CARD_IMAGE_URL = 'cards/9_yellow.png'


# ~~~~~~~~~~~~~~
#   SixtyNines
# ~~~~~~~~~~~~~~

class SixtyNine(NumberCard):
    CARD_FREQUENCY = CardFrequency(1)
    CARD_TYPE = "69"
    EFFECT_DESCRIPTION = "A surprise ;)"

    def play_card(self, player):
        # only send "nice" sound effect if this is the bottom card in the pile
        is_bottom = True
        n_cards = 0
        for card in self.game.planning_pile:
            if not isinstance(card, SixtyNine):
                if not isinstance(card, CopyCat):
                    continue
                if not isinstance(card.copied, SixtyNine):
                    continue
            
            if card.get_id() == self.get_id() and is_bottom is True:
                n_cards += 1
            elif n_cards > 0:
                n_cards += 1
            
            is_bottom = False
        
        # play sound effect if more than 1 69 card
        if n_cards > 0:
            if n_cards < 15:
                r = random.randrange(1, 5)
                file = "/static/sounds/nice" + str(r) + ".mp3"
            else:  # fucked sound effect for >=15 69 cards played at once
                r = random.randrange(1, 4)
                file = "/static/sounds/nice_fucked" + str(r) + ".mp3"

            json_to_send = {
                "type": "sound",
                "sound": file
            }
            self.game.send_to_all_players("animate", json_to_send)
                

class BlueSixtyNine(SixtyNine):
    NAME = "Blue Sixty Nine"
    CARD_COLOUR = "blue"
    CARD_IMAGE_URL = 'cards/69_blue.png'


class GreenSixtyNine(SixtyNine):
    NAME = "Green Sixty Nine"
    CARD_COLOUR = "green"
    CARD_IMAGE_URL = 'cards/69_green.png'


class PurpleSixtyNine(SixtyNine):
    NAME = "Purple Sixty Nine"
    CARD_COLOUR = "purple"
    CARD_IMAGE_URL = 'cards/69_purple.png'


class RedSixtyNine(SixtyNine):
    NAME = "Red Sixty Nine"
    CARD_COLOUR = "red"
    CARD_IMAGE_URL = 'cards/69_red.png'


class YellowSixtyNine(SixtyNine):
    NAME = "Yellow Sixty Nine"
    CARD_COLOUR = "yellow"
    CARD_IMAGE_URL = 'cards/69_yellow.png'
