import unittest
import EnvironmentSelector as es
from games.sub_watten.SubWattenGame import WattenSubGame
from games.sub_watten.nnet.SubWattenNNet import SubWattenNNet
from core.agents.AgentNNet import AgentNNet


class SubWattenAgentTest(unittest.TestCase):

    def test_cloned_prediction(self):
        env = es.EnvironmentSelector()
        # get agent
        agent = env.sub_watten_non_human_agent_for_total_watten()

        sub_watten_game = WattenSubGame()

        clone_sub_watten_game = sub_watten_game.clone()

        pi_values, v = agent.predict(sub_watten_game, sub_watten_game.get_cur_player())

        clone_pi_values, clone_v = agent.predict(clone_sub_watten_game, clone_sub_watten_game.get_cur_player())

        self.assertEqual(pi_values.all(), clone_pi_values.all())
        self.assertEqual(v, clone_v)

    def test_nn_agent_prediction(self):
        sub_watten_game = WattenSubGame()

        clone_sub_watten_game = sub_watten_game.clone()

        x, y = sub_watten_game.get_observation_size()
        nnet = SubWattenNNet(x, y, 1, sub_watten_game.get_action_size())

        agent_nnet = AgentNNet(nnet)

        agent_nnet.load("../../sub_watten/training/best.h5")

        pi_values, v = agent_nnet.predict(sub_watten_game, sub_watten_game.get_cur_player())

        clone_pi_values, clone_v = agent_nnet.predict(clone_sub_watten_game, clone_sub_watten_game.get_cur_player())

        self.assertEqual(pi_values.all(), clone_pi_values.all())
        self.assertEqual(v, clone_v)


if __name__ == '__main__':
    unittest.main()
