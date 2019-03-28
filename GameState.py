from Units import Unit

class GameState:
    def __init__(self, player, game):
        self.player = player
        self.state = 0
        self.chosen_unit = None
        self.game = game

    def switch_player(self):
        if self.player == self.game.player1:
            self.player = self.game.player2
        else:
            self.player = self.game.player1

    def default(self):
        self.state = 0
        if isinstance(self.chosen_unit, Unit):
            self.chosen_unit.chosen = False
        self.chosen_unit = None