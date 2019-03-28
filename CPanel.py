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



        self.player1_train_buttons = []
        i = 0
        for name in self.game.player1.factory.unit_names:
            r = Rect(self.left, self.top + 180 + i * 40, 180, 30)
            self.player1_train_buttons.append(Button('train_{}'.format(name), r, name.capitalize(), Colors.GREENLOW, 10, 4))
            i += 1

        self.player2_train_buttons = []
        i = 0
        for name in self.game.player2.factory.unit_names:
            r = Rect(self.left, self.top + 180 + i * 40, 180, 30)
            self.player2_train_buttons.append(Button('train_{}'.format(name), r, name.capitalize(), Colors.GREENLOW, 10, 4))
            i += 1


        self.buttons['player1'] = self.player1_button
        self.buttons['player2'] = self.player2_button
        self.buttons['endmove'] = self.endmove_button
        self.buttons['player1_move'] = self.player1_move_button
        for but in self.player1_train_buttons:
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

            but_color = but.color
            if but.id.startswith('train_'):
                name = but.id[6:]
                if name == self.game.gamestate.chosen_unit:
                    but_color = Colors.PINKPINKRED

            pygame.draw.rect(self.game.screen, but_color, but.rect)
            if but.text_surface:
                self.game.screen.blit(but.text_surface, (but.rect.left + but.left, but.rect.top + but.top))


    def get_button(self, pos):
        for e in self.buttons:
            if self.buttons[e].rect.collidepoint(pos):
                return e

    def endmove(self):
        for key in list(self.buttons.keys()):
            if key.startswith('train'):
                del self.buttons[key]
        if 'player1_move' in self.buttons.keys():
            del self.buttons['player1_move']
            self.buttons['player2_move'] = self.player2_move_button
            for but in self.player2_train_buttons:
                self.buttons[but.id] = but
        elif 'player2_move' in self.buttons.keys():
            del self.buttons['player2_move']
            self.buttons['player1_move'] = self.player1_move_button
            for but in self.player1_train_buttons:
                self.buttons[but.id] = but