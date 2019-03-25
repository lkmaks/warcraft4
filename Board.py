import pygame
from Constants import Colors
from Units import Unit


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

        self.units_array[1][1] = Unit(100, 10, 2, 'footman', 1, (1, 1), self.game.player1, 1, self)
        self.units_array[4][4] = Unit(60, 20, 2, 'grunt', 1, (4, 4), self.game.player2, 1, self)

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