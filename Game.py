import pygame
import sys
from Constants import Colors
from Board import Board
from CPanel import CPanel
from GameState import GameState


class Game:
    def __init__(self, player1, player2):
        pygame.init()
        pygame.font.init()
        self.player1 = player1
        self.player2 = player2
        self.board = Board(self)

        bw, bh = self.board.real_size_with_offsets()

        self.cpanel = CPanel(self, bw, 0, 400, self.board.real_size_with_offsets()[1])
        self.screen = pygame.display.set_mode((bw + self.cpanel.width, bh))
        self.clock = pygame.time.Clock()

        self.gamestate = GameState(player1)

    def render(self):
        self.board.render()
        self.cpanel.render()

    def handle_mouseup(self, pos, button):
        cell = self.board.get_cell(pos)
        print(pos, button)
        if not cell is None and button == 1:
            if self.gamestate.state == 0:
                unit = self.board.units_array[cell[0]][cell[1]]
                if not unit is None and \
                    unit.owner == self.gamestate.player:
                    self.gamestate.state = 1
                    self.gamestate.chosen_unit = unit
                    unit.chosen = True
            elif self.gamestate.state == 1:
                unit = self.gamestate.chosen_unit
                if unit.able(cell):
                    unit.take_action(cell)
                    self.gamestate.state = 0
                    self.gamestate.chosen_unit = None
                    unit.chosen = False
        elif not cell is None and button == 3:
            if self.gamestate.state == 1 and cell == self.gamestate.chosen_unit.cell:
                self.gamestate.chosen_unit.chosen = False
                self.gamestate.state = 0
                self.gamestate.chosen_unit = False


    def run(self):
        while True:
            self.clock.tick(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouseup(event.pos, event.button)
            self.render()
            pygame.display.flip()

