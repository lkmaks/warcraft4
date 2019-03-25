

class CPanel:
    def __init__(self, game, left, top, width, height):
        self.game = game
        self.width = width
        self.height = height
        self.left = left
        self.top = top

    def render(self):
        