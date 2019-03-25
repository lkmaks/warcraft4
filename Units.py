import pygame
from pygame import Rect


def dist(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def attack_is_possible(type1, type2):
    return True


class Unit():
    def __init__(self, hp, damage, speed, type, attack_dist, cell, owner, moves_left, board):
        self.type = type
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.attack_dist = attack_dist
        self.cell = cell
        self.board = board
        self.chosen = False
        self.owner = owner
        self.moves_left = moves_left

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

        img = pygame.image.load('img/{}.png'.format(self.type))
        self.board.game.screen.blit(img, Rect((sx + 1, sy + 1, sx + d, sy + d)))

        font = pygame.font.SysFont('Comic Sans MS', 30)
        ts = font.render(str(self.hp), False, (0,  200, 0))
        self.board.game.screen.blit(ts, (sx, sy, sx + d, sy + d))
