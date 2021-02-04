from logging import DEBUG
from unittest import TestCase

from games.total_watten.total_watten import WorldTotalWatten
import EnvironmentSelector as es


class TestNoErrorWorldTotalWatten(TestCase):

    @classmethod
    def setUpClass(self):
        print('setting up test fixture')
        env = es.EnvironmentSelector()
        self.agent = env.sub_watten_non_human_agent_for_total_watten()

    def test_game_no_raise_player_A_starts(self):
        world = WorldTotalWatten()
        world.LOG.setLevel(DEBUG)

        world.init_world_to_state(-1, 1, 0, 0, [28, 29, 3, 15, 22], [19, 14, 7, 0, 11], [], 0, 0, 2, False, False, None, 18, 21, None, None)

        # [39, 44, 0, 46, 48, 3, 29, 46, 48, 14, 11, 15]
        world_copy = world.deepcopy()

        ######## MOVE ########
        valid_moves = world.get_valid_moves()

        outcome, next_player = world.act(0, self.agent) # rank
        outcome, next_player = world.act(0, self.agent) # suit
        outcome, next_player = world.act(0, self.agent) # card
        outcome, next_player = world.act(1, self.agent) # raise
        outcome, next_player = world.act(3, self.agent) # accepted raise
        outcome, next_player = world.act(0, self.agent) # card --
        outcome, next_player = world.act(1, self.agent) # raise
        outcome, next_player = world.act(3, self.agent) # accepted raise
        outcome, next_player = world.act(0, self.agent) # card --
        outcome, next_player = world.act(0, self.agent) # card
        outcome, next_player = world.act(0, self.agent) # card
        outcome, next_player = world.act(0, self.agent) # card
        world.get_valid_moves()
