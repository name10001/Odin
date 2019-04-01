import cards


class Player:
    cards = []
    name = ''

    def __init__(self, game, name, player_id):
        self.name = name
        self.game = game
        self.player_id = player_id
        self.pickup(game.starting_number_of_cards)

    def pickup(self, number):
        for i in range(0, number):
            self.cards.append(cards.pickup_from_deck()(self.game))

    def get_cards(self):
        return self.cards

    def get_name(self):
        return self.name

    def get_id(self):
        return self.player_id
