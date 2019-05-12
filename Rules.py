import Units
from math import floor
from GenerateNeutralsStrategies import *
from NeutralsActStrategies import *

def limit_reduce(cnt_units, gold):
    if cnt_units > 3:
        return gold - int(floor(0.3 * gold))
    elif cnt_units > 10:
        return gold - int(floor(0.6 * gold))
    else:
        return gold


class Rules:
    MATE_MORALE = 6
    SUBORDINATE_MORALE = 10
    MORAL_DECREASE_STEP = 5
    NEUTRAL_GENERATING_STRATEGY = NormalRandomNeutralsGenerateStrategy
    NEUTRAL_ACT_STRATEGY = NormalCalmNeutralsActStrategy

    def __init__(self, game):
        self.game = game


    def gold_add(self, player):
        arr = self.game.board.units_array
        cnt_gold = 0
        cnt_units = 0
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                if isinstance(arr[i][j], Units.Unit) and arr[i][j].owner == player:
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

    @staticmethod
    def get_percentage(armor, damage_type):
        if armor == 'light':
            if damage_type == 'normal':
                return 1
            elif damage_type == 'pierce':
                return 2
            elif damage_type == 'magic':
                return 1.25
        elif armor == 'medium':
            if damage_type == 'normal':
                return 1.5
            elif damage_type == 'pierce':
                return 0.75
            elif damage_type == 'magic':
                return 0.75
        elif armor == 'heavy':
            if damage_type == 'normal':
                return 1
            elif damage_type == 'pierce':
                return 1
            elif damage_type == 'magic':
                return 2
