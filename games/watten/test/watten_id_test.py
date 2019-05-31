from logging import DEBUG
from unittest import TestCase
import games.watten.watten as watten
from games.watten.watten import WorldWatten
from games.watten.watten import InconsistentStateError
from games.watten.watten import CardParsingError
from games.watten.watten import InvalidActionError
import numpy as np


class TestWorldCompleteGameWatten(TestCase):

    def test_observe(self):
        world = WorldWatten()
        world.first_card_deck = 32
        world.last_card_deck = 32
        world.player_A_hand = [0, 1, 2, 3, 4]
        world.player_B_hand = [31, 30, 29, 28, 27]
        world.rank = 8
        world.suit = 0
        world.played_cards = [10, 11, 12, 13, 14]
        world.current_game_player_A_score = 1
        world.current_game_player_B_score = 2
        world.player_A_score = 14
        world.player_B_score = 1
        world.is_last_move_raise = True
        world.is_last_move_accepted_raise = True
        world.is_last_hand_raise_valid = False
        world.current_game_prize = 15

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
                             0, 1, 0, 0, 0, 0, 0, 0, 0, 0,  # 189
                             0, 0, 0, 0, 0, 1, 1, 0, 0, 0,  # 199
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 209
                             1, 1, 1, 0, 0, 0, 0, 0, 0, 0,  # 219
                             0, 0, 0, 0, 0, 1]  # 225

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
                             1, 0, 1, 0, 0, 0, 0, 0, 0, 0,  # 189
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 199
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 1,  # 209
                             1, 1, 1, 0, 0, 0, 0, 0, 0, 0,  # 219
                             0, 0, 0, 0, 0, 1]  # 225

        observation_player_A = world.observe(1)
        observation_player_B = world.observe(-1)
        np.testing.assert_array_equal(observation_player_A, np.array(expected_player_A).reshape((226, 1)))
        np.testing.assert_array_equal(observation_player_B, np.array(expected_player_B).reshape((226, 1)))
