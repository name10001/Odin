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

# max players
min_max_players = 2
default_max_players = 6
max_max_players = 16

# Dynamic Deck default card distribution
default_dynamic_deck = [
    {'name': 'Blue Zero', 'small': 1.0, 'elevator': 0.1},
    {'name': 'Green Zero', 'small': 1.0, 'elevator': 0.1},
    {'name': 'Red Zero', 'small': 1.0, 'elevator': 0.1},
    {'name': 'Yellow Zero', 'small': 1.0, 'elevator': 0.1},
    {'name': 'Purple Zero', 'small': 0.4, 'elevator': 0.05},
    {'name': 'Orange Zero', 'small': 0.1, 'elevator': 0.025},
    
    {'name': 'Blue One', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Green One', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Red One', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Yellow One', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Purple One', 'small': 0.8, 'elevator': 0.1},
    {'name': 'Orange One', 'small': 0.2, 'elevator': 0.05},
    
    {'name': 'Blue Two', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Green Two', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Red Two', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Yellow Two', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Purple Two', 'small': 0.8, 'elevator': 0.1},
    {'name': 'Orange Two', 'small': 0.2, 'elevator': 0.05},
    
    {'name': 'Blue Three', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Green Three', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Red Three', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Yellow Three', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Purple Three', 'small': 0.8, 'elevator': 0.1},
    {'name': 'Orange Three', 'small': 0.2, 'elevator': 0.05},
    
    {'name': 'Blue Four', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Green Four', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Red Four', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Yellow Four', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Purple Four', 'small': 0.8, 'elevator': 0.1},
    {'name': 'Orange Four', 'small': 0.2, 'elevator': 0.05},
    
    {'name': 'Blue Five', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Green Five', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Red Five', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Yellow Five', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Purple Five', 'small': 0.8, 'elevator': 0.1},
    {'name': 'Orange Five', 'small': 0.2, 'elevator': 0.05},
    
    {'name': 'Blue Six', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Green Six', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Red Six', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Yellow Six', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Purple Six', 'small': 0.8, 'elevator': 0.1},
    {'name': 'Orange Six', 'small': 0.2, 'elevator': 0.05},
    
    {'name': 'Blue Seven', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Green Seven', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Red Seven', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Yellow Seven', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Purple Seven', 'small': 0.8, 'elevator': 0.1},
    {'name': 'Orange Seven', 'small': 0.2, 'elevator': 0.05},
    
    {'name': 'Blue Eight', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Green Eight', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Red Eight', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Yellow Eight', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Purple Eight', 'small': 0.8, 'elevator': 0.1},
    {'name': 'Orange Eight', 'small': 0.2, 'elevator': 0.05},
    
    {'name': 'Blue Nine', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Green Nine', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Red Nine', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Yellow Nine', 'small': 1.6, 'elevator': 0.2},
    {'name': 'Purple Nine', 'small': 0.8, 'elevator': 0.1},
    {'name': 'Orange Nine', 'small': 0.2, 'elevator': 0.05},
    
    {'name': 'Blue Sixty Nine', 'small': 1.2, 'elevator': 0.2},
    {'name': 'Green Sixty Nine', 'small': 1.2, 'elevator': 0.2},
    {'name': 'Red Sixty Nine', 'small': 1.2, 'elevator': 0.2},
    {'name': 'Yellow Sixty Nine', 'small': 1.2, 'elevator': 0.2},
    {'name': 'Purple Sixty Nine', 'small': 0.6, 'elevator': 0.1},
    {'name': 'Orange Sixty Nine', 'small': 0.15, 'elevator': 0.05},

    {'name': 'Just A Blank Bro', 'small': 4, 'medium': 4, 'large': 6, 'massive': 12},
    {'name': 'Happiness', 'small': 4, 'medium': 4, 'large': 6, 'massive': 12},
    {'name': 'Colour Chooser', 'small': 2, 'max': 4, 'starting': 0},

    {'name': 'Red/Blue Colour Swapper', 'small': 0.8, 'elevator': 0.4, 'starting': 0},
    {'name': 'Red/Yellow Colour Swapper', 'small': 0.8, 'elevator': 0.4, 'starting': 0},
    {'name': 'Red/Green Colour Swapper', 'small': 0.8, 'elevator': 0.4, 'starting': 0},
    {'name': 'Green/Blue Colour Swapper', 'small': 0.8, 'elevator': 0.4, 'starting': 0},
    {'name': 'Yellow/Blue Colour Swapper', 'small': 0.8, 'elevator': 0.4, 'starting': 0},
    {'name': 'Yellow/Green Colour Swapper', 'small': 0.8, 'elevator': 0.4, 'starting': 0},
    {'name': 'Black/White Colour Swapper', 'small': 1.2, 'elevator': 0.6, 'starting': 0},
    
    {'name': "Fuckin' Blue M8", 'small': 1.2, 'medium': 0.5},
    {'name': "Fuckin' Green M8", 'small': 1.2, 'medium': 0.5},
    {'name': "Fuckin' Red M8", 'small': 1.2, 'medium': 0.5},
    {'name': "Fuckin' Yellow M8", 'small': 1.2, 'medium': 0.5},
    {'name': "Fuckin' Black M8", 'small': 1.2, 'medium': 0.5},

    {'name': "Blue Pickup 2", 'small': 2.5, 'medium': 2.2, 'large': 1.1, 'massive': 0.5, 'elevator': 1, 'starting': 0},
    {'name': "Green Pickup 2", 'small': 2.5, 'medium': 2.2, 'large': 1.1, 'massive': 0.5,  'elevator': 1, 'starting': 0},
    {'name': "Red Pickup 2", 'small': 2.5, 'medium': 2.2, 'large': 1.1, 'massive': 0.5,  'elevator': 1, 'starting': 0},
    {'name': "Yellow Pickup 2", 'small': 2.5, 'medium': 2.2, 'large': 1.1, 'massive': 0.5,  'elevator': 1, 'starting': 0},
    {'name': "Black Pickup 2", 'small': 2.5, 'medium': 2.2, 'large': 1.1, 'massive': 0.5,  'elevator': 1, 'starting': 0},
    {'name': "White Pickup 2", 'small': 2.5, 'medium': 2.2, 'large': 1.1, 'massive': 0.5,  'elevator': 1, 'starting': 0},
    {'name': "Purple Pickup 2", 'small': 2.5, 'medium': 2.2, 'large': 1.1, 'massive': 0.5,  'elevator': 1, 'starting': 0},

    {'name': "Pickup 100", 'small': 0.05, 'medium': 0.025, 'large': 0.025, 'massive': 0.005, 'starting': 0},
    {'name': "Pickup 10", 'small': 2.5, 'medium': 1.2, 'large': 0.7, 'massive': 0.2, 'starting': 0},
    {'name': "Pickup 4", 'small': 5, 'medium': 3, 'large': 2, 'massive': 1, 'starting': 0},
    {'name': "Pickup x2", 'small': 2.5, 'medium': 1.2, 'large': 0.7, 'massive': 0.2, 'starting': 0},
    {'name': "Pickup x Squared", 'small': 0.05, 'medium': 0.025, 'large': 0.025, 'massive': 0.005, 'starting': 0},
    {'name': "Pickup Factorial", 'small': 0.01, 'medium': 0.005, 'large': 0.005, 'massive': 0.001, 'starting': 0},
    {'name': "Pawn", 'small': 0.5, 'starting': 0, 'elevator': 0, 'max': 1},
    {'name': "Atomic Bomb", 'small': 0, 'medium': 0.6, 'large': 0.4, 'elevator': 0, 'max': 1},
    {'name': "Plus", 'small': 0.75, 'medium': 0.75, 'large': 0.5, 'massive': 0.25, 'starting': 0, 'max': 5},
    {'name': "Fuck You", 'small': 2, 'medium': 1.5, 'large': 1, 'massive': 0.15, 'starting': 0, 'max': 5},

    {'name': "Blue Reverse", 'small': 2.2, 'medium': 2, 'elevator': 1, 'starting': 0},
    {'name': "Green Reverse", 'small': 2.2, 'medium': 2, 'elevator': 1, 'starting': 0},
    {'name': "Red Reverse", 'small': 2.2, 'medium': 2, 'elevator': 1, 'starting': 0},
    {'name': "Yellow Reverse", 'small': 2.2, 'medium': 2, 'elevator': 1, 'starting': 0},
    {'name': "Black Reverse", 'small': 2.2, 'medium': 2, 'elevator': 1, 'starting': 0},
    {'name': "White Reverse", 'small': 2.2, 'medium': 2, 'elevator': 1, 'starting': 0},
    {'name': "Purple Reverse", 'small': 2.2, 'medium': 2, 'elevator': 1, 'starting': 0},

    {'name': "Blue Skip", 'small': 2.2, 'medium': 2, 'elevator': 1, 'starting': 0},
    {'name': "Green Skip", 'small': 2.2, 'medium': 2, 'elevator': 1, 'starting': 0},
    {'name': "Red Skip", 'small': 2.2, 'medium': 2, 'elevator': 1, 'starting': 0},
    {'name': "Yellow Skip", 'small': 2.2, 'medium': 2, 'elevator': 1, 'starting': 0},
    {'name': "Black Skip", 'small': 2.2, 'medium': 2, 'elevator': 1, 'starting': 0},
    {'name': "White Skip", 'small': 2.2, 'medium': 2, 'elevator': 1, 'starting': 0},
    {'name': "Purple Skip", 'small': 2.2, 'medium': 2, 'elevator': 1, 'starting': 0},

    {'name': "Free Turn", 'small': 5, 'medium': 3, 'large': 1, 'massive': 0.8, 'max': 5, 'starting': 0},
    {'name': "Freeze", 'small': 1.4, 'medium': 0.9, 'large': 0.5, 'massive': 0.2, 'max': 4, 'starting': 0},
    
    {'name': "Man Of The Day", 'small': 1, 'max': 1, 'starting': 0, 'elevator': 0},
    {'name': "Lady Of The Night", 'small': 1, 'max': 1, 'starting': 0, 'elevator': 0},
    {'name': "Smurf", 'small': 1, 'max': 1, 'starting': 0, 'elevator': 0},
    {'name': "Creeper", 'small': 1, 'max': 1, 'starting': 0, 'elevator': 0},
    {'name': "Filthy Sharon", 'small': 1, 'max': 1, 'starting': 0, 'elevator': 0},
    {'name': "Black Hole", 'small': 0.02, 'max': 1, 'starting': 0, 'elevator': 0},

    {'name': "Play One", 'small': 1, 'medium': 0.5, 'large': 0.2, 'max': 6, 'starting': 0, 'elevator': 0},
    {'name': "Play Three", 'small': 0.5, 'medium': 0.25, 'large': 0.08, 'max': 6, 'starting': 0, 'elevator': 0},
    
    {'name': "EA $15", 'small': 0.7, 'medium': 1.5, 'starting': 0, 'elevator': 0},
    {'name': "EA $20", 'small': 0.5, 'medium': 0.8, 'starting': 0, 'elevator': 0},
    {'name': "EA $30", 'small': 0.25, 'medium': 0.5, 'starting': 0, 'elevator': 0},
    {'name': "EA $100", 'small': 0, 'medium': 0, 'large': 0.05, 'starting': 0, 'elevator': 0},
    
    {'name': "Blue Trash", 'small': 1.2, 'medium': 0.5, 'max': 8, 'starting': 0},
    {'name': "Green Trash", 'small': 1.2, 'medium': 0.5, 'max': 8, 'starting': 0},
    {'name': "Red Trash", 'small': 1.2, 'medium': 0.5, 'max': 8, 'starting': 0},
    {'name': "Yellow Trash", 'small': 1.2, 'medium': 0.5, 'max': 8, 'starting': 0},
    {'name': "Black Trash", 'small': 0.5, 'max': 8, 'starting': 0},
    {'name': "Do Justly -1", 'small': 1.3, 'max': 8, 'starting': 0},
    {'name': "Do Justly -3", 'small': 0.3, 'max': 8, 'starting': 0},
    {'name': "Swap Card", 'small': 2.2, 'max': 8, 'starting': 0},
    {'name': "Steal", 'small': 1.7, 'medium': 1.5, 'large': 1, 'massive': 0.8, 'max': 8, 'starting': 0},

    {'name': "Communist", 'small': 0, 'medium': 0.7, 'large': 0.4, 'massive': 0.1, 'max': 1, 'starting': 0, 'elevator': 1},
    {'name': "Capitalist", 'small': 0.7, 'medium': 0.5, 'large': 0.3, 'massive': 0, 'max': 8, 'starting': 0, 'elevator': 1},
    {'name': "Swap Hand", 'small': 0, 'medium': 0.6, 'large': 0.3, 'max': 1, 'starting': 0, 'elevator': 0.2},
    {'name': "Feeling Blue", 'small': 1.5, 'max': 10, 'elevator': 2.1},
    {'name': "Genocide", 'small': 0.7, 'max': 8, 'starting': 0, 'elevator': 1.2},
    {'name': "Jesus", 'small': 0.6, 'max': 4, 'starting': 0},
    {'name': "Odin", 'small': 1, 'max': 1, 'starting': 0},
    {'name': "Thanos", 'small': 0, 'medium': 0.4, 'large': 1.4, 'max': 5, 'starting': 0},
    {'name': "Copy Cat", 'small': 3, 'medium': 1, 'large': 0.5, 'max': 4, 'starting': 0, 'elevator': 0},
    {'name': "Elevator", 'small': 2, 'max': 20, 'starting': 0, 'elevator': 0},
    {'name': "Possess", 'small': 1.5, 'medium': 1, 'large': 0.5, 'massive': 0.3, 'max': 4, 'starting': 0},
    {'name': "Fire", 'small': 3, 'medium': 1, 'max': 20, 'starting': 0}
]



debug_enabled = False
