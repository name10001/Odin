import cards
import random


class Deck:
    def __init__(self, game):
        self.game = game
        self.set_cards(cards.all_cards.copy())
    
    def calculate_weights(self, player=None):
        card_weights = []
        if player is None:
            for card in self.cards:
                card_weights.append(card.CARD_FREQUENCY.medium_hand)  # null player just use the medium hand size by default
        else:
            n_cards = len(player.hand)
            for card in self.cards:
                n_this_type = player.hand.number_of_type(card.CARD_TYPE)
                card_weights.append(card.CARD_FREQUENCY.get_frequency(n_cards, n_this_type))
        return card_weights
    
    def calculate_remaining_cards(self):
        """
        After banning cards, calculate the remaining types and colours left
        """
        self.all_types = []
        self.all_colours = []
        for card in self.cards:
            if card.CARD_TYPE not in self.all_types:
                self.all_types.append(card.CARD_TYPE)
            if card.CARD_COLOUR not in self.all_colours:
                self.all_colours.append(card.CARD_COLOUR)

    def set_cards(self, cards):
        """
        Set the list of all cards
        Used when undoing a genocide card or initialization
        """
        self.cards = cards
        self.calculate_remaining_cards()

    def get_random_card(self, weights):
        """
        gets a new random card and returns it.
        It will not return banned card unless all cards have been banned
        :return:
        """
        # if all cards have been banned - you would never reach here anyway because the game would end?
        if len(self.cards) == 0:
            return cards.get_random_card()
        else:
            return random.choices(self.cards, weights=weights)[0]

    def ban_colour(self, card_colour):
        """
        removes a color from the deck
        :param card_color: color to remove
        :return:
        """
        for card in self.cards.copy():
            if card.CARD_COLOUR == card_colour:
                self.cards.remove(card)
        self.calculate_remaining_cards()

    def ban_type(self, card_type):
        """
        removes a type from the deck
        :param card_type: type to remove
        :return:
        """
        for card in self.cards.copy():
            if card.CARD_TYPE == card_type:
                self.cards.remove(card)
        self.calculate_remaining_cards()

