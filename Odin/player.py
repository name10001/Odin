

class Player:
    cards = []
    name = ''

    def __init__(self, game, name, player_id):
        self.name = name
        self.game = game
        self.player_id = player_id

    def get_cards(self):
        return self.cards

    def get_name(self):
        return self.name

    def get_id(self):
        return self.player_id
