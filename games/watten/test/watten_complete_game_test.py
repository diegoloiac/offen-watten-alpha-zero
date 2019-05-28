from logging import DEBUG
from unittest import TestCase
import games.watten.watten as watten
from games.watten.watten import WorldWatten
from games.watten.watten import InconsistentStateError
from games.watten.watten import CardParsingError
from games.watten.watten import InvalidActionError


class TestWorldWatten(TestCase):

    def test_game_no_raise(self):
        world = WorldWatten()
        world.LOG.setLevel(DEBUG)

        world.init_world_to_state(1, -1, 0, 0, [12, 9, 5, 14, 8], [17, 23, 29, 20, 25], [], 0, 0, 2, False, False, None, 21, 27, None, None)

        # [39, 42, 8, 41, 23, 36, 43, 25, 40, 43, 22, 34, 43, 32, 33, 43, 2,
        #  39, 43, 14, 36, 44, 32, 38, 43, 18, 40, 43, 7, 38, 42, 1, 41, 3]
        world_copy = world.deepcopy()

        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [33, 34, 35, 36, 37, 38, 39, 40, 41, 46])
        self.assertEqual(world.current_player, 1)
        self._compare_worlds(world, world_copy)

        world.act(39)

        valid_moves = world.get_valid_moves()

        self.assertEqual(world.current_player, -1)
        self.assertEqual(valid_moves, [42, 43, 44, 45, 46])




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
        self.assertEqual(world1.moves_series, world2.moves_series)
        self.assertEqual(world1.current_game_prize, world2.current_game_prize)
