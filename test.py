from Game import Game
from Player import Player


player1 = Player(race='horde', start_gold=10, name='Grubby', number=1)
player2 = Player(race='human', start_gold=10, name='a1sok', number=2)
game = Game(player1, player2)

player2.factory.create_unit('footman', (4, 5))
player2.factory.create_unit('footman', (4, 7))

game.run()
