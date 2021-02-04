from logging import DEBUG
from unittest import TestCase
from games.total_watten.total_watten import WorldTotalWatten

import EnvironmentSelector as es

import numpy as np


class TestIdTotalWatten(TestCase):

    @classmethod
    def setUpClass(self):
        print('setting up test fixture')
        env = es.EnvironmentSelector()
        self.agent = env.sub_watten_non_human_agent_for_total_watten()

    def test_observe(self):
        world = WorldTotalWatten()
        world.current_game_player_A_score = 1
        world.current_game_player_B_score = 2
        world.player_A_score = 14
        world.player_B_score = 1
        world.is_last_move_raise = True
        world.is_last_move_accepted_raise = True
        world.is_last_hand_raise_valid = False
        world.current_game_prize = 15

        expected_player_A = [1, 0, 0, 1, 0, 0, 0, 0, 0, 0,  # 110
                             0, 0, 0, 0, 0, 0, 0, 1, 1, 0,  # 120
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 130
                             0, 0, 1, 1, 1, 0, 0, 0, 0, 0,  # 140
                             0, 0, 0, 0, 0, 0, 0, 1, 0, 0]  # 150

        expected_player_B = [0, 1, 1, 0, 1, 0, 0, 0, 0, 0,  # 110
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 120
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 130
                             0, 1, 1, 1, 1, 0, 0, 0, 0, 0,  # 140
                             0, 0, 0, 0, 0, 0, 0, 1, 0, 0]  # 150

        observation_player_A = world.observe(1, self.agent)
        observation_player_B = world.observe(-1, self.agent)
        #testing last part of observation is correct
        np.testing.assert_array_equal(observation_player_A[32:82], np.array(expected_player_A).reshape((50, 1)))
        np.testing.assert_array_equal(observation_player_B[32:82], np.array(expected_player_B).reshape((50, 1)))
