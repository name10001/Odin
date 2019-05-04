import cards


class CardFrequency:
    SMALL_HAND = 10  # Hand size between 0 - SMALL_HAND has frequency small_hand
    MEDIUM_HAND = 40  # Hand size between SMALL_HAND+1 - MEDIUM_HAND has frequency medium_hand
    LARGE_HAND = 120  # Hand size between MEDIUM_HAND+1 - LARGE_HAND has frequency large_hand
    # Hand size of at least LARGE_HAND+1 has frequency massive_hand

    # Frequency is automatically set to zero if you have at least max_cards of this card in your hand

    def __init__(self, small_hand, medium_hand=None, large_hand=None, massive_hand=None, starting=None, elevator=None, max_cards=None):
        """
        Card Frequency.
        If you call CardFrequency(n), then all frequencies will be set n,
        otherwise you can specify individual frequencies for all the hand sizes
        You can also specify a max_cards, where you will no longer be able to
        randomly draw this card if you have at least the max number of cards of that type.
        Set to None if you are allowed to draw as many cards as you like
        """
        self.small_hand = small_hand

        if medium_hand is None:
            self.medium_hand = self.small_hand
        else:
            self.medium_hand = medium_hand
        
        if large_hand is None:
            self.large_hand = self.medium_hand
        else:
            self.large_hand = large_hand
        
        if massive_hand is None:
            self.massive_hand = self.large_hand
        else:
            self.massive_hand = massive_hand
        
        if starting is None:
            self.starting = self.small_hand
        else:
            self.starting = starting
        
        if elevator is None:
            self.elevator = self.medium_hand
        else:
            self.elevator = elevator
        
        self.max_cards = max_cards
    
    def get_weight(self, n_cards, n_this_type, ignore_limit=False):
        """
        Get the weight of this card in the deck, given you have n_cards in your hand
        and n_this_type of this type of card
        """
        if ignore_limit is False and self.max_cards is not None and n_this_type >= self.max_cards:
            return 0

        if n_cards <= CardFrequency.SMALL_HAND:
            return self.small_hand
        elif n_cards <= CardFrequency.MEDIUM_HAND:
            return self.medium_hand
        elif n_cards <= CardFrequency.LARGE_HAND:
            return self.large_hand
        else:
            return self.massive_hand

    def get_starting_weight(self):
        """
        Gets the frequency of the card for the starting card
        Cards that require a player to play it should have a weight of 0
        """
        return self.starting
    
    def get_elevator_weight(self):
        """
        Gets the frequency of the card to be randomly drawn during an elevator card
        Some cards like EA or other elevator cards should have a weight of 0
        """
        return self.elevator

