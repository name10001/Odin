from flask import session

# server info
port = 80
host = '0.0.0.0'


class IntSetting:

    def __init__(self, name, default_value, min_value, max_value):
        self.name = name
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value

    def to_json(self, index):
        return {'index': index, 'name': self.name, 'type': 'int', 'default': self.default_value, 'min': self.min_value, 'max': self.max_value}


def get_theme():
    return '/static/themes/blue_theme.css'  # default theme


# game settings
min_player_card_limit = 3
default_starting_cards = 25
min_max_player_card_limit = 25
max_player_card_limit = 999

jesus_card_number = 15
played_cards_to_show = 5
session_inactivity_kick = 5
