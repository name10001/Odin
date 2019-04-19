

class CardCollection:
    """
    This is meant to be a fast way to store cards.
    It uses multiple kinds of data types in order to get maximum performance.
    It is not memory efferent however is fast.
    """
    def __init__(self, cards=None, sort=False):
        self.cards_list = []
        self.cards_dict = {}
        if cards is not None:
            self.add_cards(cards)
        self.sort = sort

    def add_cards(self, cards, sort_after=True):
        """
        Adds multiple cards to the collection
        :param cards: cards to add
        :param sort_after: should the collection be sorted after the cards are added
        :return: None
        """
        for card in cards:
            self.add_card(card, sort_after=False)
        if self.sort and sort_after:
            self.cards_list.sort()

    def add_card(self, card, sort_after=True):
        """
        Adds a single cards to the collection
        :param card: card to add
        :param sort_after: should the collection be sorted after the card is added
        :return: None
        """
        self.cards_list.append(card)
        self.cards_dict[card.get_id()] = card
        if self.sort and sort_after:
            self.cards_list.sort()

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
        self.cards_list.remove(card)
        del self.cards_dict[card.get_id()]

    def find_card(self, card_id):
        """
        Finds a card by its id
        :param card_id:
        :return: Card if a card is found, None if not found
        """
        if card_id in self.cards_dict:
            return self.cards_dict[card_id]

    def get_cards(self):
        return self.cards_list

    def __len__(self):
        return len(self.cards_list)

    def __iter__(self):
        return self.cards_list.__iter__()
