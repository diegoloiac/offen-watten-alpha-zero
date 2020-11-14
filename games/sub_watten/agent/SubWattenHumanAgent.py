import sys

sys.path.append('..')

from core.interfaces.Agent import Agent
from core.interfaces.Game import Game


class SubWattenHumanAgent(Agent):
    def __init__(self, game):
        super().__init__(name="HUMAN WATTEN PLAYER")
        self.game = game

    def predict(self, game: Game, game_player):

        valid = game.get_valid_moves(game_player)
        all_moves = game.get_valid_moves(game_player)

        game.get_display_str()
        print("\nPossible moves are: {0}\n".format([x for x in range(46) if all_moves[x]]))

        print("Please, input the index of the move.")
        while True:
            idx = int(input())

            if valid[idx]:
                break
            else:
                print('Invalid move index.')

        actions = [0] * len(valid)
        actions[idx] = 1

        return actions, -1
