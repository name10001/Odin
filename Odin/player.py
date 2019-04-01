

class Player:
    cards = []
    name = ''

    def __init__(self, game, name):
        self.name = name
        self.game = game
        self.player_id = self._make_id()

    def get_cards(self):
        return self.cards

    def get_name(self):
        return self.name

    def _make_id(self):
        """
        makes and ID that is unique to itself and is human readable
        """
        the_id = self.name.replace(" ", "_") + "_player"

        # remove all HTML unsafe characters
        id_safe = ""
        for character in the_id:
            # if character is a-z, A-Z, 1-9 or is _
            if ord(character) in range(ord("a"), ord("z") + 1)\
                    or ord(character) in range(ord("A"), ord("Z") + 1)\
                    or ord(character) in range(ord("1"), ord("9") + 1)\
                    or character in ("_",):
                id_safe += character

        # if its ID is already in use, add a number to it
        if self.game.get_player(id_safe) is not None:
            num = 2
            while self.game.get_card(id_safe + "_" + str(num)) is not None:
                num += 1
            id_safe += "_" + str(num)

        return id_safe

    def get_id(self):
        return self.player_id
