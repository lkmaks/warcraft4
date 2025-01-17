import pygame
from pygame import Rect
from Constants import Colors
from Rules import Rules
import json
import os
from BattleActions import *


def sign(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1


def dist(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def attack_is_possible(type1, type2):
    return True


class Unit():
    def __init__(self, kwargs):
        self.cell = self.board = self.owner = self.name = None
        self.hp = self.max_hp = self.damage = self.speed = None
        self.regen = self.type = self.attack_dist = self.cell = None
        self.owner = self.moves_start = self.cost = self.board = None
        self.morale = 0
        self.parent = None
        self.children = set()

        for key in kwargs:
            self.__setattr__(key, kwargs[key])
        self.chosen = self.chosen_to_bound = False
        self.moves_left = self.moves_start

    def accept_battle_action(self, action):
        action.log()
        if type(action) == NormalUnitAttack:
            self.hp -= int(action.damage * Rules.get_percentage(self.armor, action.damage_type))
            if self.hp <= 0:
                self.die(action.source)
        elif type(action) == PriestHeal:
            self.hp += action.heal
            self.hp = min(self.hp, self.max_hp)
        elif type(action) == BomberDetonation:
            for r in range(1, self.bomb_radius + 1):
                s = set()
                x, y = self.cell
                for i in range(-r, r + 1):
                    s.add((x + r, y + i))
                    s.add((x - r, y + i))
                    s.add((x + i, y + r))
                    s.add((x + i, y - r))
                for pos in s:
                    other_unit = self.board.units_array[pos[0]][pos[1]]
                    if not other_unit is None:
                        attack = NormalUnitAttack(self.bomb_damage, self.bomb_damage_type, self, other_unit)
                        other_unit.accept_battle_action(attack)
                self.die()

    def die(self, died_from=None):
        if died_from:
            died_from.owner.get_reward(self)
        self.board.units_array[self.cell[0]][self.cell[1]] = None
        for unit in self.children:
            unit.parent = self.parent
            unit.cascade_morale_decrease_after_death(self.morale * 5, 0)

    def move_to(self, cell):
        self.board.units_array[self.cell[0]][self.cell[1]] = None
        self.board.units_array[cell[0]][cell[1]] = self
        self.cell = cell

    def act_with_enemy(self, unit):
        attack = NormalUnitAttack(max(0, self.damage + self.morale // 5), self.damage_type, self, unit)
        unit.accept_battle_action(attack)
        return True

    def act_with_ally(self, unit):
        if self.name == "priest":
            action = PriestHeal(self.heal, self, unit)
            unit.accept_battle_action(action)
        elif self.name == "bomber" and unit == self:
            action = BomberDetonation(self.bomb_damage, self.bomb_radius, self)
            self.accept_battle_action(action)
        return True

    def able(self, cell):
        if self.moves_left == 0:
            return False
        if self.board.units_array[cell[0]][cell[1]] is None:
            return dist(cell, self.cell) <= self.speed
        else:
            return dist(cell, self.cell) <= self.attack_dist

    def take_action(self, cell):
        """ assuming able() == True """
        if self.board.units_array[cell[0]][cell[1]] is None:
            self.move_to(cell)
            self.moves_left -= 1
        else:
            unit = self.board.units_array[cell[0]][cell[1]]
            if unit.owner != self.owner and attack_is_possible(self.type, unit.type):
                if self.act_with_enemy(unit):
                    self.moves_left -= 1
            else:
                if self.act_with_ally(unit):
                    self.moves_left -= 1

    def render(self):
        sx, sy = self.board.get_coords(self.cell)
        d = self.board.cell_size

        img = pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '/img/{}.png'.format(self.name))
        self.board.game.screen.blit(img, Rect((sx + 1, sy + 1, sx + d, sy + d)))

        font = pygame.font.SysFont('Comic Sans MS', 30)
        ts = font.render(str(self.hp), False, (0,  200, 0))
        self.board.game.screen.blit(ts, (sx, sy, sx + d, sy + d))

        ts = font.render(str(self.morale), False, (200, 200, 0))
        self.board.game.screen.blit(ts, (sx + d - 25, sy + d - 20, sx + d, sy + d))

        if self.chosen:
            pygame.draw.rect(self.board.game.screen, Colors.PINKRED, (sx + d - 10, sy + d - 10, 10, 10))
        if self.chosen_to_bound:
            pygame.draw.rect(self.board.game.screen, Colors.CHOSEN_TO_BOUND, (sx + d - 10, sy + d - 10, 10, 10))

    def end_of_our_move(self):
        self.moves_left = self.moves_start
        self.chosen = False
        self.hp += self.regen
        self.hp = min(self.hp, self.max_hp)

    def end_of_their_move(self):
        self.end_of_our_move()

    def set_parent(self, parent_unit):
        self.parent = parent_unit
        if not parent_unit == self:
            self.morale = len(self.parent.children) * Rules.MATE_MORALE
            self.parent.children.add(self)
            for unit in self.parent.children:
                if unit != self:
                    unit.morale += Rules.MATE_MORALE
            unit = parent_unit
            while not unit is None:
                unit.morale += Rules.SUBORDINATE_MORALE
                unit = unit.parent

    def able_to_set_parent(self, parent_unit):
        if not self.parent is None:
            return False
        if len(self.children) > 0:
            return False
        unit = parent_unit
        while not unit is None:
            if unit == self:
                return False
            unit = unit.parent
        return True

    def cascade_morale_decrease_after_death(self, value, depth):
        if value <= 0:
            return
        self.morale -= value
        for unit in self.children:
            unit.cascade_morale_decrease_after_death(value - Rules.MORAL_DECREASE_STEP, depth)

    def act(self, strategy):
        # method of acting according to the strategy {strategy}
        cell = strategy.get_action_cell(self, self.board)
        if self.able(cell):
            self.take_action(cell)


class UnitFactory:
    def __init__(self, player, game):
        self.player = player
        self.game = game
        self.unit_names = set()
        self.unit_cost = dict()
        with open(os.path.dirname(os.path.abspath(__file__)) + '/units_data.json') as file:
            data = json.loads(file.read())
            for key in data:
                if data[key]['race'] == self.player.race:
                    self.unit_names.add(key)
                    self.unit_cost[key] = data[key]['cost']

    def creatable(self, name, cell):
        if self.player.gold < self.unit_cost[name]:
            return False
        if not self.game.board.can_drop_unit_to(cell, self.player):
            return False
        if name not in self.unit_names:
            return False
        return True

    def affordable(self, name):
        """ Same as creatable, but without the context of cell """
        if name not in self.unit_names:
            return False
        if self.player.gold < self.unit_cost[name]:
            return False
        return True

    def create_unit(self, name, cell):
        """
        creates unit owned by <player> with given name and proper characteristics, putting him in the <cell>
        assume it is possible - that means player has enough gold, can drop unit on the cell and can produce this type
        """
        with open(os.path.dirname(os.path.abspath(__file__)) + '/units_data.json', 'r') as file:
            data = json.loads(file.read(), encoding='utf-8')
        unit = None
        if name in data.keys():
            dc = data[name]
            dc['name'] = name
            dc['cell'] = cell
            dc['board'] = self.game.board
            dc['owner'] = self.player
            unit = Unit(dc)

        if unit is None:
            return None
        self.game.board.units_array[cell[0]][cell[1]] = unit
        self.player.gold -= unit.cost
        return self.game.board.units_array[cell[0]][cell[1]]
