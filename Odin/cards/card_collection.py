import bisect


class CardCollection:
    """
    This is meant to be a fast way to store cards.
    It uses a binary search tree and multiple kinds of data types in order to get maximum performance.
    It is not memory efferent however is fast.
    """
    def __init__(self, cards=None, sort=False):
        self.cards_list = []
        self.cards_dict = {}
        if cards is not None:
            self.add_cards(cards)
        self.should_sort = sort

    def sort(self):
        """
        Sorts the cards
        :return:
        """
        if self.should_sort:
            self.cards_list.sort()

    def add_cards(self, cards):
        """
        Adds multiple cards to the collection
        :param cards: cards to add
        :return: None
        """
        for card in cards:
            self.add_card(card)

    def add_card(self, card):
        """
        Adds a single cards to the collection
        :param card: card to add
        :return: None
        """
        if self.should_sort:
            bisect.insort(self.cards_list, card)
        else:
            self.cards_list.append(card)
        self.cards_dict[card.get_id()] = card

    def set_cards(self, cards):
        """
        Removes all the cards currently in this collection and adds the new ones given
        :param cards: collection of cards to add
        :return:
        """
        self.cards_list = []
        self.cards_dict.clear()
        self.add_cards(cards)

    def remove_card(self, card):
        """
        Removes the given card from the collection
        :param card:
        :return:
        """
        index = self.index(card)
        self.cards_list.pop(index)
        del self.cards_dict[card.get_id()]

    def find_card(self, card_id):
        """
        Finds a card by its id
        :param card_id:
        :return: Card if a card is found, None if not found
        """
        if card_id in self.cards_dict:
            return self.cards_dict[card_id]

    def clear(self):
        """
        Removes all the cards
        :return:
        """
        self.cards_list.clear()
        self.cards_dict.clear()

    def index(self, card):
        """
        Gets the index of the given card
        :param card:
        :return:
        """
        if self.should_sort:
            card_index = bisect.bisect_right(self.cards_list, card)
            if self.cards_list[card_index] is card:
                return card_index
            else:
                raise ValueError("the given card is not in this collection")
        else:
            return self.cards_list.index(card)

    def card_below(self, card):
        index = self.index(card)
        if index != 0:
            return self[index-1]
        else:
            return None

    def get_cards(self):
        return self.cards_list

    def get_top_card(self):
        return self.cards_list[-1]

    def __len__(self):
        return len(self.cards_list)

    def __iter__(self):
        return self.cards_list.__iter__()

    def __getitem__(self, key):
        return self.cards_list[key]
