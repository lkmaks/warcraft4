import pygame
from pygame import Rect
from Constants import Colors


def dist(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def attack_is_possible(type1, type2):
    return True


class Unit():
    def __init__(self, name, hp, max_hp, damage, speed, regen, type, attack_dist, cell, owner, moves_start, cost, board):
        self.type = type
        self.hp = hp
        self.max_hp = max_hp
        self.damage = damage
        self.speed = speed
        self.attack_dist = attack_dist
        self.cell = cell
        self.board = board
        self.chosen = False
        self.owner = owner
        self.moves_left = moves_start
        self.moves_start = moves_start
        self.regen = regen
        self.cost = cost
        self.name = name

    def die(self):
        self.board.units_array[self.cell[0]][self.cell[1]] = None

    def move_to(self, cell):
        self.board.units_array[self.cell[0]][self.cell[1]] = None
        self.board.units_array[cell[0]][cell[1]] = self
        self.cell = cell

    def attack(self, unit):
        """ a """
        unit.hp -= self.damage
        if unit.hp <= 0:
            unit.die()
        return True

    def act_with_ally(self, unit):
        return False

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
    unit_cost = {'footman': 4, 'grunt': 5}
    unit_names = {'human': {'footman'},
                  'horde': {'grunt'}}
    def __init__(self, player, game):
        self.player = player
        self.game = game

    def creatable(self, name, cell):
        if self.player.money < self.unit_cost[name]:
            return False
        if not self.game.board.can_drop_unit_to(cell, self.player):
            return False
        if name not in self.unit_names[self.player.race]:
            return False
        return True

    def create_unit(self, name, cell):
        """
        creates unit owned by <player> with given name and proper characteristics, putting him in the <cell>
        assume it is possible - that means player has enough money, can drop unit on the cell and can produce this type
        """
        unit = None
        if name == 'footman':
            unit = Unit(name='footman', hp=60, max_hp=60, damage=10, speed=1,
                        regen=2, type='ground', attack_dist=1, cell=cell,
                        owner=self.player, moves_start=2, cost=4, board=self.game.board)
        elif name == 'grunt':
            unit = Unit(name='grunt', hp=100, max_hp=100, damage=12, speed=1,
                        regen=3, type='ground', attack_dist=1, cell=cell,
                        owner=self.player, moves_start=2, cost=5, board=self.game.board)

        if unit is None:
            return None
        self.game.board.units_array[cell[0]][cell[1]] = unit
        self.player.money -= unit.cost
        return self.game.board.units_array[cell[0]][cell[1]]
