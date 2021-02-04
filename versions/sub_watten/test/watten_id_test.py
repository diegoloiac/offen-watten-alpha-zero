from logging import DEBUG
from unittest import TestCase
import games.sub_watten.sub_watten as watten
from games.sub_watten.sub_watten import WorldSubWatten
from games.sub_watten.sub_watten import InconsistentStateError
from games.sub_watten.sub_watten import CardParsingError
from games.sub_watten.sub_watten import InvalidActionError
import numpy as np


class TestWorldCompleteGameSubWatten(TestCase):

    def test_observe(self):
        world = WorldSubWatten()
        world.current_player = 1
        world.distributing_cards_player = -1
        world.first_card_deck = 32
        world.last_card_deck = 26
        world.player_A_hand = [0, 1, 2, 3, 4]
        world.player_B_hand = [31, 30, 29, 28, 27]
        world.deck = list(range(33))
        world.deck = world.deck[5:26]
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
                             0, 1, 0, 0, 0, 0, 0, 1, 1, 1,  # 189
                             1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  # 199
                             1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  # 209
                             1, 1, 1, 1, 0, 0, 0, 0, 0, 1,  # 219
                             1]

        expected_player_B = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 9
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 19
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 29
                             0, 0, 1, 0, 0, 0, 0, 0, 0, 0,  # 39
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 49
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 1,  # 59
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 69
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
                             1, 0, 1, 1, 1, 1, 1, 1, 1, 1,  # 189
                             1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  # 199
                             1, 1, 1, 1, 1, 1, 1, 1, 0, 0,  # 209
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 1,  # 219
                             1]

        observation_player_A = world.observe(1)
        observation_player_B = world.observe(-1)
        np.testing.assert_array_equal(observation_player_A, np.array(expected_player_A).reshape((221, 1)))
        np.testing.assert_array_equal(observation_player_B, np.array(expected_player_B).reshape((221, 1)))
