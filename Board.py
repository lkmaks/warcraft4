import pygame
from Constants import Colors
from mapgen import mapgen
from pygame.math import Vector2 as Vec
import math


def apply_vec(pos, vec):
    return (pos[0] + vec.x, pos[1] + vec.y)


def add_next_by_vector(arr, vec):
    arr.append(apply_vec(arr[len(arr) - 1], vec))


def draw_arrow(pos_from, pos_to, color, screen):
    H = 15
    alpha = 20
    W = 2

    alpha_rad = alpha * (math.pi / 180)
    v0 = Vec(pos_from[0] - pos_to[0], pos_from[1] - pos_to[1])
    dir = v0.normalize()
    arr = [pos_to]
    add_next_by_vector(arr, dir.rotate(alpha) * H / math.cos(alpha_rad))
    add_next_by_vector(arr, dir.rotate(-90) * (H * math.tan(alpha_rad) - W / 2))
    add_next_by_vector(arr, dir * (math.hypot(v0.x, v0.y) - H))
    add_next_by_vector(arr, dir.rotate(-90) * W)
    add_next_by_vector(arr, -dir * (math.hypot(v0.x, v0.y) - H))
    add_next_by_vector(arr, dir.rotate(-90) * (H * math.tan(alpha_rad) - W / 2))
    add_next_by_vector(arr, -dir.rotate(-alpha) * H / math.cos(alpha_rad))
    pygame.draw.polygon(screen, color, arr)


class Board:
    def __init__(self, game):
        self.width = 15
        self.height = 15
        self.cell_size = 60
        self.left_offset = 40
        self.right_offset = 40
        self.top_offset = 40
        self.bot_offset = 40
        self.game = game

        self.units_array = [[None] * self.height for _ in range(self.width)]
        self.is_gold = [[False] * self.height for _ in range(self.width)]
        self.spawn1 = [[False] * self.height for _ in range(self.width)]
        self.spawn2 = [[False] * self.height for _ in range(self.width)]
        mapgen(self.is_gold, self.spawn1, self.spawn2)

    def real_size(self):
        return (self.height * self.cell_size, self.width * self.cell_size)

    def real_size_with_offsets(self):
        return (self.width * self.cell_size + self.left_offset + self.right_offset,
                self.height * self.cell_size + self.top_offset + self.bot_offset)

    def render(self):
        self.game.screen.fill(Colors.WHITE)
        for i in range(0, self.height + 1):
            d = self.cell_size
            y = i * d
            pygame.draw.line(self.game.screen, Colors.BLACK, [self.top_offset + y , self.left_offset],
                             [self.top_offset + y , self.left_offset + d * self.width])

        for i in range(self.width + 1):
            d = self.cell_size
            x = i * d
            pygame.draw.line(self.game.screen, Colors.BLACK, [self.top_offset + 0, self.left_offset + x],
                             [self.top_offset + d * self.height, self.left_offset + x])

        for i in range(self.width):
            for j in range(self.height):
                x, y = self.get_coords((i, j))
                if self.is_gold[i][j]:
                    pygame.draw.rect(self.game.screen, Colors.GOLD, (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1))
                elif self.spawn1[i][j]:
                    pygame.draw.rect(self.game.screen, Colors.PLAYER_1_SPAWN,
                                     (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1))
                elif self.spawn2[i][j]:
                    pygame.draw.rect(self.game.screen, Colors.PLAYER_2_SPAWN,
                                     (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1))
                if self.units_array[i][j]:
                    self.units_array[i][j].render()

        if self.game.render_mode == 'subordination':
            for i in range(self.width):
                for j in range(self.height):
                    if not self.units_array[i][j] is None:
                        pos_from = self.get_center_coords((i, j))
                        for unit in self.units_array[i][j].children:
                            pos_to = self.get_center_coords(unit.cell)
                            color = Colors.PLAYER_1_ARROW if unit.owner.number == 1 else Colors.PLAYER_2_ARROW
                            draw_arrow(pos_from, pos_to, color, self.game.screen)

    def get_cell(self, pos):
        x, y = pos
        ix = (x - self.left_offset) // self.cell_size
        iy = (y - self.top_offset) // self.cell_size
        if ix in range(self.width) and iy in range(self.height):
            return (ix, iy)
        else:
            return None

    def get_coords(self, cell):
        """ returns coordinate on screen for left top corner of the cell """
        i, j = cell 
        return (self.left_offset + i * self.cell_size, self.top_offset + j * self.cell_size)

    def get_center_coords(self, cell):
        pos = self.get_coords(cell)
        return (pos[0] + self.cell_size // 2, pos[1] + self.cell_size // 2)

    def can_drop_unit_to(self, cell, player):
        arr = self.spawn1 if player == self.game.player1 else self.spawn2
        return self.units_array[cell[0]][cell[1]] is None and arr[cell[0]][cell[1]]

    def endmove(self):
        for i in range(len(self.units_array)):
            for j in range(len(self.units_array[i])):
                if not self.units_array[i][j] is None and \
                        self.units_array[i][j].owner == self.game.gamestate.player:
                    self.units_array[i][j].end_of_our_move()
                elif not self.units_array[i][j] is None and \
                        self.units_array[i][j].owner != self.game.gamestate.player:
                    self.units_array[i][j].end_of_their_move()

    def generate_neutrals(self, strategy):
        arr_neutrals = strategy.generate_unit_names_array(self.units_array, self.spawn1,
                                                     self.spawn2, self.game.factoryNeutral.unit_names)
        for i in range(len(arr_neutrals)):
            for j in range(len(arr_neutrals[i])):
                self.game.factoryNeutral.create_unit(arr_neutrals[i][j], (i, j))
