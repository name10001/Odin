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


class BoolSetting:

    def __init__(self, name, default_value):
        self.name = name
        self.default_value = default_value

    def to_json(self, index):
        return {'index': index, 'name': self.name, 'type': 'bool', 'default': self.default_value}


class OptionSetting:

    def __init__(self, name, default_value, values):
        self.name = name
        self.default_value = default_value
        self.values = values

    def to_json(self, index):
        return {'index': index, 'name': self.name, 'type': 'option', 'default': self.default_value, 'values': self.values}


def get_theme():
    if 'theme' in session:
        return session['theme']

    session['theme'] = '/static/themes/blue_theme.css'

    return session['theme']  # default theme


# starting cards
min_starting_cards = 1
default_starting_cards = 25

# card limit
min_card_limit = 25
max_card_limit = 999
default_card_limit = 500

# card settings
jesus_card_number = 25

# discard pile
played_cards_to_show = 5

# kick players if they close the tab
session_inactivity_kick = 10

# how long until a vote kick expires
kick_request_expire = 60

# kick players if they take too long
default_turn_timer = 90
max_turn_timer = 3600
min_turn_timer = 30

# max number of chat messages
max_chat_message = 50


debug_enabled = False
