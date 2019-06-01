from logging import DEBUG
from unittest import TestCase
import games.watten.watten as watten
from games.watten.watten import WorldWatten
from games.watten.watten import InconsistentStateError
from games.watten.watten import CardParsingError
from games.watten.watten import InvalidActionError


class TestWorldCompleteGameWatten(TestCase):

    def test_game_no_raise_player_A_starts(self):
        world = WorldWatten()
        world.LOG.setLevel(DEBUG)

        world.init_world_to_state(1, -1, 0, 0, [14, 30, 2, 28, 11], [4, 23, 31, 7, 22], [], 0, 0, 2, False, False, None, 21, 26, None, None)

        # [40, 45, 29, 12, 28, 13, 26, 0, 33, 45,
        #  3, 25, 6, 16, 30, 14, 13, 1, 38, 43, 13, 5, 32, 3, 21, 27, 33, 42, 0,
        #  4, 30, 31, 23, 7, 29, 1, 25, 9, 33, 42, 9, 30, 14, 32, 7, 25, 34, 42,
        #  29, 7, 15, 19, 11, 17, 20, 27, 0, 2, 35, 44, 31, 4, 28, 1, 12, 3, 33,
        #  45, 24, 25, 7, 11, 14, 18, 37, 45, 2, 27, 3, 0, 8, 10, 6, 26, 33, 43,
        #  21, 22, 6, 10, 24, 14, 8, 16, 33, 42, 3, 0, 29, 17, 13, 31]
        world_copy = world.deepcopy()

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [33, 34, 35, 36, 37, 38, 39, 40, 41, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(36)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, -1)

        world_copy.rank = 3
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
        self.assertEqual(valid_moves, [14, 30, 2, 28, 11, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(30)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, -1)

        world_copy.player_A_hand = [14, 2, 28, 11]
        world_copy.played_cards = [30]
        world_copy.current_player = -1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [31, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(31)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, -1)

        world_copy.current_game_player_B_score = 1
        world_copy.player_B_hand = [4, 23, 7, 22]
        world_copy.played_cards = [30, 31]
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [4, 23, 7, 22, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(22)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, 1)

        world_copy.player_B_hand = [4, 23, 7]
        world_copy.played_cards = [30, 31, 22]
        world_copy.current_player = 1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [14, 2, 28, 11, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(2)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, -1)

        world_copy.player_A_hand = [14, 28, 11]
        world_copy.current_game_player_B_score = 2
        world_copy.played_cards = [30, 31, 22, 2]
        world_copy.current_player = -1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [4, 23, 7, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(23)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, 1)

        world_copy.player_B_hand = [4, 7]
        world_copy.played_cards = [30, 31, 22, 2, 23]
        world_copy.current_player = 1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [14, 28, 11, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(14)
        self.assertEqual(outcome, "end")
        self.assertEqual(next_player, -1)

        world.player_A_hand = [20, 21, 22, 23, 24]
        world.player_B_hand = [25, 26, 27, 28, 29]
        world.first_card_deck = 4
        world.last_card_deck = 5
        world.deck = [8, 9, 10]

        world_copy.player_A_hand = [20, 21, 22, 23, 24]
        world_copy.player_B_hand = [25, 26, 27, 28, 29]
        world_copy.first_card_deck = 4
        world_copy.last_card_deck = 5
        world_copy.deck = [8, 9, 10]
        world_copy.current_player = -1
        world_copy.distributing_cards_player = 1
        world_copy.player_B_score = 2
        world_copy.played_cards = []
        world_copy.current_game_player_A_score = 0
        world_copy.current_game_player_B_score = 0
        world_copy.rank = None
        world_copy.suit = None
        self._compare_worlds(world, world_copy)

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
