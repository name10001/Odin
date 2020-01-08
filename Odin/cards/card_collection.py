import bisect
from BTrees import OOBTree


class CardCollection:
    """
    This is meant to be a fast way to store cards.
    It uses a binary search tree and multiple kinds of data types in order to get maximum performance.
    It is not memory efferent however it is fast.
    Cards should not change color or type while in this collection.
    If this is sorted, it cant change its soring method ether
    """

    def __init__(self, sort=False):
        self.cards_list = []
        self.cards_dict = {}
        self.card_types = {}
        self.card_colours = {}
        self.should_sort = sort
        self.cards_removed = []
        self.cards_added = []

    def add_cards(self, cards):
        """
        Adds multiple cards to the collection
        :param cards: cards to add
        :return: None
        """
        # O(m * log n)
        # n = number of cards already in deck
        # m = number of cards to add

        for card in cards:
            self.add_card(card)

    def add_card(self, card):
        """
        Adds a single cards to the collection
        :param card: card to add
        :return: None
        """
        # if sorted: O(n * log n)
        # if not sorted: O(1)
        # n = number of cards already in deck

        if self.should_sort:
            bisect.insort(self.cards_list, card)
        else:
            self.cards_list.append(card)
        self.cards_dict[card.get_id()] = card
        self.cards_added.append(card)

        if card.get_type() not in self.card_types:
            self.card_types[card.get_type()] = set()
        self.card_types[card.get_type()].add(card)

        if card.get_colour() not in self.card_colours:
            self.card_colours[card.get_colour()] = set()
        self.card_colours[card.get_colour()].add(card)

    def add_cards_from_deck(self, game, number):
        added_cards = []

        flags = {
            "card collection": self,
            "elevator": False
        }

        picked_up = 0
        while picked_up < number:
            card_class = game.deck.get_next_card(flags)

            if card_class is None:  # nothing left in the deck
                return added_cards
            
            card = card_class(game)
            self.add_card(card)
            added_cards.append(card)

            picked_up += 1

        return added_cards


    def index(self, card):
        """
        Gets the index of the given card
        :param card: the card to find the index of
        :return: index of the given card
        """
        # if sorted: O(log n)
        # if not sorted: O(n)
        # n = number of cards already in deck

        if self.should_sort:
            card_index = bisect.bisect_right(self.cards_list, card)
            if self.cards_list[card_index] is card:
                return card_index
            else:
                if card in self.cards_list:
                    print("WARNING! card changed its location while in the card collection")
                    return self.cards_list.index(card)
                else:
                    raise RuntimeError("Can't find the given card")
        return self.cards_list.index(card)

    def remove_card(self, card=None, remove_type=True, remove_colour=True, index=None):
        """
        Removes the given card from the collection
        :param card: card to remove. If this is None, index must be specified
        :param remove_type: Only for internal use! Should the card be removed from card_types
        :param remove_colour: Only for internal use! Should the card be removed from card_colours
        :param index: The index of the card to remove
        :return: None
        """
        # if sorted: O(log n)
        # if not sorted: O(n)
        # if removing from index: O(1)
        # n = number of cards already in deck

        if card is None and index is None:
            raise RuntimeError("If Card is None, index must be specified and vice versa")

        if index is None:
            index = self.index(card)
        if card is None:
            card = self.cards_list[index]

        self.cards_list.pop(index)
        del self.cards_dict[card.get_id()]
        self.cards_removed.append(card)
        try:
            if remove_type:
                self.card_types[card.get_type()].remove(card)
            if remove_colour:
                self.card_colours[card.get_colour()].remove(card)
        except KeyError:
            raise RuntimeError("Cant remove from type/color set, has it changed since it was added to this collection?")

    def get_changed(self):
        """
        Returns a list of cards added and a list of cards removed since the last time get_changed was called
        or since this collection was initiated.
        :return: (cards_added, cards_removed)
        """
        cards_added = self.cards_added
        cards_removed = self.cards_removed
        self.cards_removed = []
        self.cards_added = []

        return cards_added, cards_removed

    def remove_type(self, card_type):
        """
        Remove all the cards of a particular type
        :param card_type: Type to ban
        :return: A list of all the cards removed
        """
        # O(m log n)
        # n = number of cards already in the collection
        # m = number of cards to ban

        removed_cards = []

        if card_type in self.card_types:
            for card in self.card_types[card_type]:
                removed_cards.append(card)
                self.remove_card(card, remove_type=False)
            self.card_types[card_type].clear()

        return removed_cards
    
    def remove_colour(self, card_colour):
        """
        Remove all the cards of a particular colour
        :param card_colour: Colour to ban
        :return: A kust of all the cards removed
        """
        # O(m log n)
        # n = number of cards already in the collection
        # m = number of cards to ban

        removed_cards = []

        if card_colour in self.card_colours:
            for card in self.card_colours[card_colour]:
                removed_cards.append(card)
                self.remove_card(card, remove_colour=False)
            self.card_colours[card_colour].clear()
        
        return removed_cards

    def number_of_type(self, card_type):
        """
        Number of cards of a particular type in a collection
        :param card_type: Type to count
        :return: The number of that type
        """
        if card_type in self.card_types:
            return len(self.card_types[card_type])
        else:
            return 0
    
    def number_of_colour(self, card_colour):
        """
        Number of cards of a particular colour in a collection
        :param card_colour: Colour to count
        :return: The number of that colour
        """
        if card_colour in self.card_colours:
            return len(self.card_colours[card_colour])
        else:
            return 0

    def set_cards(self, cards):
        """
        Removes all the cards currently in this collection and adds the new ones given
        :param cards: collection of cards to add
        :return:
        """
        # if sorted: O(n log n)
        # if not sorted: O(n)
        # n = number of cards already in deck

        self.clear()
        self.add_cards(cards)

    def find_card(self, card_id):
        """
        Finds a card by its id
        :param card_id: id of the card to find in string form
        :return: Card if a card is found, None if not found
        """
        # O(1)

        if card_id in self.cards_dict:
            return self.cards_dict[card_id]

    def contains(self, card_id):
        """
        Is the given card in this card collection
        :param card_id: card id to check
        :return: True or False
        """
        return card_id in self.cards_dict

    def clear(self):
        """
        Removes all the cards
        :return: None
        """
        self.cards_list.clear()
        self.cards_dict.clear()
        self.card_types.clear()
        self.card_colours.clear()

    def card_below(self, card):
        """
        gets the card below the given card.
        :param card:
        :return: card below the given card
        """
        # if sorted: O(log n)
        # if not sorted: O(n)
        # n = number of cards already in deck

        index = self.index(card)
        if index != 0:
            return self[index-1]
        else:
            return None

    def get_cards(self):
        """
        Gets a list of all the cards.
        If this is a sorted collection they will be in order
        :return: List of cards
        """
        return self.cards_list

    def get_top_card(self):
        return self.cards_list[-1]

    def __len__(self):
        return len(self.cards_list)

    def __iter__(self):
        return self.cards_list.__iter__()

    def __getitem__(self, key):
        return self.cards_list[key]
