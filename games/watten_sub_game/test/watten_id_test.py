from logging import DEBUG
from unittest import TestCase
import games.watten_sub_game.watten_sub as watten
from games.watten_sub_game.watten_sub import WorldSubWatten
from games.watten_sub_game.watten_sub import InconsistentStateError
from games.watten_sub_game.watten_sub import CardParsingError
from games.watten_sub_game.watten_sub import InvalidActionError
import numpy as np


class TestWorldCompleteGameSubWatten(TestCase):

    def test_observe(self):
        world = WorldSubWatten()
        world.first_card_deck = 32
        world.last_card_deck = 32
        world.player_A_hand = [0, 1, 2, 3, 4]
        world.player_B_hand = [31, 30, 29, 28, 27]
        world.rank = 8
        world.suit = 0
        world.played_cards = [10, 11, 12, 13, 14]
        world.current_game_player_A_score = 1
        world.current_game_player_B_score = 2

        expected_player_A = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 9
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 19
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 29
                             0, 0, 1, 0, 0, 0, 0, 0, 0, 0,  # 39
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 49
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 59
                             0, 0, 0, 0, 0, 0, 1, 1, 1, 1,  # 69
                             1, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 79
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 89
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 99
                             0, 0, 0, 0, 0, 0, 0, 1, 1, 0,  # 109
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 119
                             0, 0, 0, 0, 0, 0, 1, 0, 0, 0,  # 129
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 139
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 149
                             0, 0, 0, 0, 0, 1, 1, 1, 1, 1,  # 159
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 169
                             0, 0, 0, 0, 0, 0, 0, 0, 1, 0,  # 179
                             0, 1]  # 182

        expected_player_B = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 9
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 19
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 29
                             0, 0, 1, 0, 0, 0, 0, 0, 0, 0,  # 39
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 49
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 59
                             0, 0, 0, 0, 0, 1, 0, 0, 0, 0,  # 69
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 79
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 89
                             0, 0, 0, 1, 1, 1, 1, 1, 0, 0,  # 99
                             0, 0, 0, 0, 0, 0, 0, 1, 1, 0,  # 109
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 119
                             0, 0, 0, 0, 0, 0, 1, 0, 0, 0,  # 129
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 139
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 149
                             0, 0, 0, 0, 0, 1, 1, 1, 1, 1,  # 159
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 169
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 1,  # 179
                             1, 0]  # 182

        observation_player_A = world.observe(1)
        observation_player_B = world.observe(-1)
        np.testing.assert_array_equal(observation_player_A, np.array(expected_player_A).reshape((182, 1)))
        np.testing.assert_array_equal(observation_player_B, np.array(expected_player_B).reshape((182, 1)))
