from Game import Game
from Player import Player


player1 = Player(race='horde', name='Grubby')
player2 = Player(race='humans', name='a1sok')
game = Game(player1, player2)
game.run()
