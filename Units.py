import pygame
from pygame import Rect
from Constants import Colors
import json


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

        for key in kwargs:
            self.__setattr__(key, kwargs[key])
        self.chosen = False
        self.moves_left = self.moves_start

    def die(self):
        self.board.units_array[self.cell[0]][self.cell[1]] = None

    def move_to(self, cell):
        self.board.units_array[self.cell[0]][self.cell[1]] = None
        self.board.units_array[cell[0]][cell[1]] = self
        self.cell = cell

    def attack(self, unit, damage=None):
        """ a """
        unit.hp -= (damage if damage else self.damage)
        if unit.hp <= 0:
            unit.die()
        return True

    def act_with_ally(self, unit):
        if self.name == "priest":
            unit.hp += self.heal
            unit.hp = min(unit.hp, unit.max_hp)
        if self.name == "bomber" and unit == self:
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
                        self.attack(other_unit, self.bomb_damage)
                self.die()

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
                if self.attack(unit):
                    self.moves_left -= 1
            else:
                if self.act_with_ally(unit):
                    self.moves_left -= 1

    def render(self):
        sx, sy = self.board.get_coords(self.cell)
        d = self.board.cell_size

        img = pygame.image.load('img/{}.png'.format(self.name))
        self.board.game.screen.blit(img, Rect((sx + 1, sy + 1, sx + d, sy + d)))

        font = pygame.font.SysFont('Comic Sans MS', 30)
        ts = font.render(str(self.hp), False, (0,  200, 0))
        self.board.game.screen.blit(ts, (sx, sy, sx + d, sy + d))

        if self.chosen:
            pygame.draw.rect(self.board.game.screen, Colors.PINKRED, (sx + d - 10, sy + d - 10, 10, 10))

    def end_of_our_move(self):
        self.moves_left = self.moves_start
        self.chosen = False
        self.hp += self.regen
        self.hp = min(self.hp, self.max_hp)

    def end_of_their_move(self):
        self.end_of_our_move()


class UnitFactory:
    def __init__(self, player, game):
        self.player = player
        self.game = game
        self.unit_names = set()
        self.unit_cost = dict()
        with open('units_data.json') as file:
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
        with open('units_data.json', 'r') as file:
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
