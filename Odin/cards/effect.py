from flask import *

class Effect:
    """
    Represents an abstract effect for a player that lasts a given amount of turns.
    """
    EFFECT_IMAGE_URL = 'generic.png'

    def __init__(self, player, n_turns):
        self.player = player
        self.n_turns = n_turns

    def begin_turn(self):
        """
        What the effect does at the beginning of a turn.
        """
        pass
    
    def end_turn(self):
        """
        What the effect does at the end of a turn.
        """
        pass

    def get_url(self):
        """
        Get the image URL of the effect
        """
        
        return '/static/effects/' + escape(self.EFFECT_IMAGE_URL)

class FreezeEffect(Effect):
    """
    The freeze effect causes the player to have their turn skipped for a certain number of turns
    """
    EFFECT_IMAGE_URL = 'freeze.png'

    def begin_turn(self):
        self.player.next_turn()

class FireEffect(Effect):
    """
    The fire effect causes the player to gain a certain amount of cards at the beginning of their turn.
    """
    EFFECT_IMAGE_URL = 'fire.png'

    def __init__(self, player, n_turns, n_cards):
        super().__init__(player, n_turns)
        self.n_cards = n_cards

    def begin_turn(self):
        self.player.refresh_card_play_animation()
        self.player.pickup(self.n_cards)