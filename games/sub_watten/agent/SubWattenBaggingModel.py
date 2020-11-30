import sys

from core.agents.AgentNNet import AgentNNet
from core.interfaces.Agent import Agent
from core.interfaces.Game import Game

from games.asymmetric_sub_watten.nnet.AsymmetricSubWattenNNet import AsymmetricSubWattenNNet
from games.sub_watten.nnet.SubWattenNNet import SubWattenNNet

sys.path.append('..')


class SubWattenBaggingModel(Agent):

    def __init__(self, game):
        super().__init__(name="SUB WATTEN BAGGING AGENT")
        self.game = game

        x, y = game.get_observation_size()
        nnet1 = SubWattenNNet(x, y, 1, game.get_action_size())

        nnet2 = AsymmetricSubWattenNNet(x, y, 1, game.get_action_size())

        # Setting up the symmetric and asymmetric nnet

        self.agent_symmetric = AgentNNet(nnet1)
        self.agent_asymmetric = AgentNNet(nnet2)

        try:
            self.agent_symmetric.load("games/sub_watten/training/best.h5")
            self.agent_asymmetric.load("games/asymmetric_sub_watten/training/v2/best.h5")
        except OSError:
            print("File not found with games/sub_watten/training/best.h5")
            print("Maybe you are creating an agent for test purposes. I'll try to load the model from a different path")
            self.agent_symmetric.load("../../sub_watten/training/best.h5")
            self.agent_asymmetric.load("../../asymmetric_sub_watten/training/v2/best.h5")

    def predict(self, game: Game, game_player):

        # Prediction of both nnet
        actions_s, obs_value_s = self.agent_symmetric.predict(game, game_player)

        actions_a, obs_value_a = self.agent_asymmetric.predict(game, game_player)

        # Symmetric has 78,96% of success against random
        # Asymmetric has 73,14% of success against random
        actions = (7896 * actions_s + 7314 * actions_a) / (7896+7314)

        obs_value = (7896*obs_value_s + 7314*obs_value_a) / (7896+7314)

        return actions, obs_value
