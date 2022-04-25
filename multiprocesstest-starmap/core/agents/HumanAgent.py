from core.interfaces.Agent import Agent
from core.interfaces.Game import Game


class HumanAgent(Agent):
    def __init__(self, game, name="HUMAN AGENT"):
        super().__init__(name=name)
        self.game = game

    def predict(self, game: Game, game_player):
        print(type(game))

        valid = game.get_valid_moves(game_player)

        game.get_display_str()
        print("\nPossible moves are: {0}\n".format([x for x in range(game.get_action_size()) if valid[x]]))

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
