import pygame
import sys
from Constants import Colors
from Board import Board
from CPanel import CPanel
from GameState import GameState
from Units import UnitFactory
from Rules import Rules


class Game:
    def __init__(self, player1, player2):
        pygame.init()
        pygame.font.init()
        self.player1 = player1
        self.player2 = player2

        self.factory1 = UnitFactory(player1, self)
        self.factory2 = UnitFactory(player2, self)

        self.player1.factory = self.factory1
        self.player2.factory = self.factory2

        self.board = Board(self)

        bw, bh = self.board.real_size_with_offsets()

        self.cpanel = CPanel(self, bw, self.board.top_offset, 400, self.board.real_size_with_offsets()[1])
        self.screen = pygame.display.set_mode((bw + self.cpanel.width, bh))
        self.clock = pygame.time.Clock()

        self.gamestate = GameState(player1)

        self.rules = Rules(Game)

    def render(self):
        self.board.render()
        self.cpanel.render()

    def endmove(self):
        self.gamestate.chosen_unit = None
        self.gamestate.state = 0
        for i in range(len(self.board.units_array)):
            for j in range(len(self.board.units_array[i])):
                if not self.board.units_array[i][j] is None and \
                        self.board.units_array[i][j].owner == self.gamestate.player:
                    self.board.units_array[i][j].end_of_our_move()
                elif not self.board.units_array[i][j] is None and \
                        self.board.units_array[i][j].owner != self.gamestate.player:
                    self.board.units_array[i][j].end_of_their_move()
        self.gamestate.player = self.player1 if self.gamestate.player == self.player2 else self.player2
        self.cpanel.endmove()
        self.player1.money += self.rules.gold_add()
        self.player2.money += self.rules.gold_add()

    def handle_keyup(self, key):
        if key == ord('e'):
            self.endmove()
        elif key == ord('f') and self.gamestate.player.race == 'human':
            self.choose_unit_to_train('footman')
        elif key == ord('g') and self.gamestate.player.race == 'horde':
            self.choose_unit_to_train('grunt')

    def choose_unit_to_train(self, name):
        self.gamestate.state = 2
        # gamestate 2: ready to drop unit
        self.gamestate.chosen_unit = name

    def handle_mouseup(self, pos, mouse_button):
        print(self.gamestate.__dict__)
        cell = self.board.get_cell(pos)

        # if we are in state of making an action, but dont click on a cell, remove action mark from the unit
        if cell is None and self.gamestate.state == 1:
            self.gamestate.chosen_unit.chosen = False

        if not cell is None and mouse_button == 1:
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
            elif self.gamestate.state == 2:
                factory = self.gamestate.player.factory
                if factory.creatable(self.gamestate.chosen_unit, cell):
                    factory.create_unit(self.gamestate.chosen_unit, cell)

        elif not cell is None and mouse_button == 3:
            if self.gamestate.state == 1:
                self.gamestate.chosen_unit.chosen = False
                self.gamestate.state = 0
                self.gamestate.chosen_unit = False
            elif self.gamestate.state == 2:
                self.gamestate.state = 0
                self.gamestate.chosen_unit = False

        button = self.cpanel.get_button(pos)
        if not button is None:
            if button == 'endmove':
                self.endmove()
            elif button.startswith('train_'):
                name = button[6:]
                self.choose_unit_to_train(name)



    def run(self):
        while True:
            self.clock.tick(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouseup(event.pos, event.button)
                elif event.type == pygame.KEYUP:
                    self.handle_keyup(event.key)
            self.render()
            pygame.display.flip()

