

class Player:
    def __init__(self, race, start_money, name='Rexar', factory=None):
        self.race = race
        self.name = name
        self.money = start_money
        self.factory = None