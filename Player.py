from Rules import Rules


class Player:
    def __init__(self, race, start_gold, number, name='Rexar', factory=None):
        self.race = race
        self.name = name
        self.gold = start_gold
        self.factory = None
        self.number = number

    def get_reward(self, unit):
        if unit.owner.name == "Neutrals":
            self.gold += unit.cost

    def act(self):
        # special method for neutral player; act when the move ends
        units_array = self.factory.game.board.units_array
        for i in range(len(units_array)):
            for j in range(len(units_array[i])):
                if not (units_array[i][j] is None) and units_array[i][j].owner.name == 'Neutrals':
                    unit = units_array[i][j]
                    cnt = unit.moves_left
                    for _ in range(cnt):
                        unit.act(Rules.NEUTRAL_ACT_STRATEGY())
