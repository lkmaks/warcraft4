from Game import Game
from Player import Player


player1 = Player(race='horde', start_money=10, name='Grubby')
player2 = Player(race='human', start_money=10, name='a1sok')
game = Game(player1, player2)
game.run()
