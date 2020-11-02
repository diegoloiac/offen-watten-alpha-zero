from logging import DEBUG
from unittest import TestCase

from games.total_watten.total_watten import WorldTotalWatten


class TestWorldCompleteGameWatten(TestCase):

    def test_game_no_raise_player_A_starts(self):
        world = WorldTotalWatten()
        world.LOG.setLevel(DEBUG)

        world.init_world_to_state(-1, 1, 0, 0, [28, 29, 3, 15, 22], [19, 14, 7, 0, 11], [], 0, 0, 2, False, False, None, 18, 21, None, None)

        # [39, 44, 0, 46, 48, 3, 29, 46, 48, 14, 11, 15]
        world_copy = world.deepcopy()

        ######## MOVE ########
        valid_moves = world.get_valid_moves()

        outcome, next_player = world.act(39)
        outcome, next_player = world.act(44)
        outcome, next_player = world.act(0)
        outcome, next_player = world.act(46)
        outcome, next_player = world.act(48)
        outcome, next_player = world.act(3)
        outcome, next_player = world.act(29)
        outcome, next_player = world.act(46)
        outcome, next_player = world.act(48)
        outcome, next_player = world.act(14)
        outcome, next_player = world.act(11)
        outcome, next_player = world.act(15)
        world.get_valid_moves()
        # outcome, next_player = world.act(19)
