import pygame
from Constants import Colors
from Units import Unit
from mapgen import mapgen

class Board:
    def __init__(self, game):
        self.width = 15
        self.height = 15
        self.cell_size = 50
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

    def can_drop_unit_to(self, cell, player):
        arr = self.spawn1 if player == self.game.player1 else self.spawn2
        return self.units_array[cell[0]][cell[1]] is None and arr[cell[0]][cell[1]]
