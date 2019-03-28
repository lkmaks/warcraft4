from Units import Unit
from math import floor

def limit_reduce(cnt_units, gold):
    if cnt_units > 3:
        return gold - int(floor(0.3 * gold))
    elif cnt_units > 10:
        return gold - int(floor(0.6 * gold))
    else:
        return gold


class Rules:
    def __init__(self, game):
        self.game = game


    def gold_add(self, player):
        arr = self.game.board.units_array
        cnt_gold = 0
        cnt_units = 0
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                if isinstance(arr[i][j], Unit) and arr[i][j].owner == player:
                    if self.game.board.is_gold[i][j]:
                        cnt_gold += 1
                    cnt_units += 1

        return 3 + limit_reduce(cnt_units, cnt_gold * 2)

    def game_result(self):
        g1 = self.game.player1.gold
        g2 = self.game.player2.gold
        if g1 >= 200 and g2 < 200:
            return 1
        elif g2 >= 200 and g1 < 200:
            return 2
        elif g1 >= 200 and g2 >= 200:
            if g1 - g2 >= 5:
                return 1
            elif g2 - g1 >= 5:
                return 2
            else:
                return 0
        else:
            return 0
