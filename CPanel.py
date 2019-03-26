import pygame
from Constants import Colors
from pygame import Rect


class Button:
    def __init__(self, id, rect, text, color, left, top, text_color=None):
        self.rect = rect
        self.color = color
        self.left = left
        self.top = top
        self.text = text
        self.id = id

        font = pygame.font.SysFont('Comic Sans MS', 30)
        self.text_surface = font.render(text, False, text_color if text_color else Colors.BLACK)

    def set_text(self, text):
        font = pygame.font.SysFont('Comic Sans MS', 30)
        self.text_surface = font.render(text, False, Colors.BLACK)


class CPanel:
    def __init__(self, game, left, top, width, height):
        self.game = game
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.buttons = dict()

        r = Rect(self.left, self.top, 220, 50)
        self.endmove_button = Button('endmove', r, 'End move', Colors.PINKRED, 55, 15, (150, 200, 205))

        r = Rect(self.left, self.top + 60, 220, 50)
        self.player1_button = Button('player1', r, 'Player 1: {}'.format(self.game.player1.name), Colors.GREENLOW, 20, 15)

        r = Rect(self.left, self.top + 120, 220, 50)
        self.player2_button = Button('player2', r, 'Player 2: {}'.format(self.game.player2.name), Colors.GREENLOW, 20, 15)

        r = Rect(self.left + 200, self.top + 80, 10, 10)
        self.player1_move_button = Button('player1_move_button', r, '', Colors.PINKRED, 0, 0)

        r = Rect(self.left + 200, self.top + 140, 10, 10)
        self.player2_move_button = Button('player2_move_button', r, '', Colors.PINKRED, 0, 0)


        r = Rect(self.left, self.top + 180, 80, 30)
        self.train_grunt_button = Button('train_grunt', r, 'Grunt', Colors.GREENLOW, 10, 4)

        self.orc_unit_train_buttons = []
        self.orc_unit_train_buttons.append(self.train_grunt_button)


        r = Rect(self.left, self.top + 180, 110, 30)
        self.train_human_button = Button('train_footman', r, 'Footman', Colors.GREENLOW, 10, 4)

        self.human_unit_train_buttons = []
        self.human_unit_train_buttons.append(self.train_human_button)

        self.buttons['player1'] = self.player1_button
        self.buttons['player2'] = self.player2_button
        self.buttons['endmove'] = self.endmove_button
        self.buttons['player1_move'] = self.player1_move_button
        if self.game.player1.race == 'horde':
            for but in self.orc_unit_train_buttons:
                self.buttons[but.id] = but
        elif self.game.player1.race == 'human':
            for but in self.human_unit_train_buttons:
                self.buttons[but.id] = but

    def render(self):
        for key in self.buttons:
            but = self.buttons[key]

            # update players money
            if but.id == 'player1' or but.id == 'player2':
                pos = but.text.find(': ')
                money = self.game.player1.money if but.id == 'player1' else self.game.player2.money
                if pos == -1:
                    but.set_text(but.text + ': ' + str(money))
                else:
                    but.set_text(but.text[:pos + 2] + str(money))


            pygame.draw.rect(self.game.screen, but.color, but.rect)
            if but.text_surface:
                self.game.screen.blit(but.text_surface, (but.rect.left + but.left, but.rect.top + but.top))


    def get_button(self, pos):
        for e in self.buttons:
            if self.buttons[e].rect.collidepoint(pos):
                return e

    def endmove(self):
        if 'player1_move' in self.buttons.keys():
            del self.buttons['player1_move']
            self.buttons['player2_move'] = self.player2_move_button
        elif 'player2_move' in self.buttons.keys():
            del self.buttons['player2_move']
            self.buttons['player1_move'] = self.player1_move_button
        for but in self.human_unit_train_buttons + self.orc_unit_train_buttons:
            if but.id in self.buttons.keys():
                del self.buttons[but.id]
        if self.game.gamestate.player.race == 'horde':
            for but in self.orc_unit_train_buttons:
                self.buttons[but.id] = but
        elif self.game.gamestate.player.race == 'human':
            for but in self.human_unit_train_buttons:
                self.buttons[but.id] = but