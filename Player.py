

class Player:
    def __init__(self, race, start_gold, name='Rexar', factory=None):
        self.race = race
        self.name = name
        self.gold = start_gold
        self.factory = None