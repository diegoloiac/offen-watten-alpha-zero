from logging import DEBUG
from unittest import TestCase
import games.watten_sub_game.watten_sub as watten_sub
from games.watten_sub_game.watten_sub import WorldSubWatten
from games.watten_sub_game.watten_sub import InconsistentStateError
from games.watten_sub_game.watten_sub import CardParsingError
from games.watten_sub_game.watten_sub import InvalidActionError


class TestWorldCompleteGameSubWatten(TestCase):

    def test_game_no_raise_player_A_starts(self):
        world = WorldSubWatten()
        world.LOG.setLevel(DEBUG)

        world.init_world_to_state(-1, 1, [28, 29, 3, 15, 22], [19, 14, 7, 0, 11], [], 0, 0, 18, 21, None, None)

        # [39, 44, 0, 46, 48, 3, 29, 46, 48, 14, 11, 15]
        world_copy = world.deepcopy()

        ######## MOVE ########
        valid_moves = world.get_valid_moves()

        outcome, next_player = world.act(39)
        outcome, next_player = world.act(44)
        outcome, next_player = world.act(0)
        outcome, next_player = world.act(3)
        outcome, next_player = world.act(29)
        outcome, next_player = world.act(14)
        outcome, next_player = world.act(11)
        outcome, next_player = world.act(15)
        world.get_valid_moves()
        # outcome, next_player = world.act(19)
