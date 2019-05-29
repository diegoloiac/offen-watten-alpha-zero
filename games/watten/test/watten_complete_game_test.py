from logging import DEBUG
from unittest import TestCase
import games.watten.watten as watten
from games.watten.watten import WorldWatten
from games.watten.watten import InconsistentStateError
from games.watten.watten import CardParsingError
from games.watten.watten import InvalidActionError


class TestWorldCompleteGameWatten(TestCase):

    def test_game_no_raise_1(self):
        world = WorldWatten()
        world.LOG.setLevel(DEBUG)

        world.init_world_to_state(1, -1, 0, 0, [12, 29, 32, 24, 16], [13, 20, 31, 4, 25], [], 0, 0, 2, False, False, None, 3, 14, None, None)

        # [32, 34, 44, 23, 38, 45, 21, 41, 44, 13, 38, 44, 16, 36, 43, 4, 36,
        #  43, 7, 41, 44, 20, 36, 43, 1, 33, 43, 21, 38, 43, 11, 34, 43, 13, 33, 43, 7, 35, 43, 3]
        world_copy = world.deepcopy()

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [33, 34, 35, 36, 37, 38, 39, 40, 41, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(34)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, -1)

        world_copy.rank = 1
        world_copy.current_player = -1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [42, 43, 44, 45, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(42)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, 1)

        world_copy.suit = 0
        world_copy.current_player = 1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [12, 29, 32, 24, 16, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(32)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, -1)

        world_copy.player_A_hand = [12, 29, 24, 16]
        world_copy.played_cards = [32]
        world_copy.current_player = -1

    def test_game_no_raise_error(self):
        world = WorldWatten()
        world.LOG.setLevel(DEBUG)

        world.init_world_to_state(1, -1, 0, 0, [19, 30, 24, 23, 20], [31, 12, 7, 18, 16], [], 0, 0, 2, False, False, None, 25, 0, None, None)

        world_copy = world.deepcopy()

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [33, 34, 35, 36, 37, 38, 39, 40, 41, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(37)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, -1)

        world_copy.rank = 4
        world_copy.current_player = -1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [42, 43, 44, 45, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(45)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, 1)

        world_copy.suit = 3
        world_copy.current_player = 1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [19, 30, 24, 23, 20, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(23)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, -1)

        world_copy.player_A_hand = [19, 30, 24, 20]
        world_copy.player_B_hand = [31, 12, 7, 18, 16]
        world_copy.played_cards = [23]
        world_copy.current_player = -1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [31, 12, 7, 18, 16, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(31)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, -1)
        self.assertEqual(world.current_game_player_A_score, 0)
        self.assertEqual(world.current_game_player_B_score, 1)

        world_copy.player_A_hand = [19, 30, 24, 20]
        world_copy.player_B_hand = [12, 7, 18, 16]
        world_copy.current_game_player_B_score = 1
        world_copy.played_cards = [23, 31]
        world_copy.current_player = -1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [12, 7, 18, 16, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(18)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, 1)

        world_copy.player_B_hand = [12, 7, 16]
        world_copy.played_cards = [23, 31, 18]
        world_copy.current_player = 1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [19, 30, 24, 20, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(20)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, 1)

        world_copy.player_A_hand = [19, 30, 24]
        world_copy.current_game_player_A_score = 1
        world_copy.played_cards = [23, 31, 18, 20]
        world_copy.current_player = 1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [19, 30, 24, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(24)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, -1)

        world_copy.player_A_hand = [19, 30]
        world_copy.played_cards = [23, 31, 18, 20, 24]
        world_copy.current_player = -1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        print(world._str_cards([24, 12, 7, 16]))

        valid_moves = world.get_valid_moves()

        # ERROR, played 16

    def _compare_worlds(self, world1, world2):
        self.assertEqual(world1.current_player, world2.current_player)
        self.assertEqual(world1.distributing_cards_player, world2.distributing_cards_player)
        self.assertEqual(world1.player_A_score, world2.player_A_score)
        self.assertEqual(world1.player_B_score, world2.player_B_score)
        self.assertEqual(world1.win_threshold, world2.win_threshold)
        self.assertEqual(world1.deck, world2.deck)
        self.assertEqual(world1.player_A_hand, world2.player_A_hand)
        self.assertEqual(world1.player_B_hand, world2.player_B_hand)
        self.assertEqual(world1.played_cards, world2.played_cards)
        self.assertEqual(world1.current_game_player_A_score, world2.current_game_player_A_score)
        self.assertEqual(world1.current_game_player_B_score, world2.current_game_player_B_score)
        self.assertEqual(world1.is_last_move_raise, world2.is_last_move_raise)
        self.assertEqual(world1.is_last_move_accepted_raise, world2.is_last_move_accepted_raise)
        self.assertEqual(world1.is_last_hand_raise_valid, world2.is_last_hand_raise_valid)
        self.assertEqual(world1.first_card_deck, world2.first_card_deck)
        self.assertEqual(world1.last_card_deck, world2.last_card_deck)
        self.assertEqual(world1.rank, world2.rank)
        self.assertEqual(world1.suit, world2.suit)
        self.assertEqual(world1.moves, world2.moves)
        self.assertEqual(world1.starting_state, world2.starting_state)
        self.assertEqual(world1.current_game_prize, world2.current_game_prize)
