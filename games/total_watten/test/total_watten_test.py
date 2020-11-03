from logging import DEBUG
from unittest import TestCase
import numpy as np

import games.total_watten.total_watten as total_watten
from games.total_watten.total_watten import WorldTotalWatten
from games.total_watten.total_watten import InconsistentStateError
from games.total_watten.total_watten import CardParsingError
from games.total_watten.total_watten import InvalidActionError


class TestWorldTotalWatten(TestCase):

    def test_refresh(self):
        world = WorldTotalWatten()

    def test_get_id(self):
        card_id = total_watten.get_id(8, 3)
        self.assertEqual(card_id, 32)

        card_id = total_watten.get_id(0, 0)
        self.assertEqual(card_id, 0)

        card_id = total_watten.get_id(4, 3)
        self.assertEqual(card_id, 28)

        card_id = total_watten.get_id(1, 2)
        self.assertEqual(card_id, 17)

        card_id = total_watten.get_id(7, 3)
        self.assertEqual(card_id, 31)

        card_id = total_watten.get_id(8, 2)
        self.assertEqual(card_id, 32)

        self.assertRaises(CardParsingError, total_watten.get_id, 2, 10)

        self.assertRaises(CardParsingError, total_watten.get_id, 14, 2)

    def test_get_rs(self):
        r, s = total_watten.get_rs(32)
        self.assertEqual(r, 8)
        self.assertEqual(s, 3)

        r, s = total_watten.get_rs(0)
        self.assertEqual(r, 0)
        self.assertEqual(s, 0)

        r, s = total_watten.get_rs(28)
        self.assertEqual(r, 4)
        self.assertEqual(s, 3)

        r, s = total_watten.get_rs(17)
        self.assertEqual(r, 1)
        self.assertEqual(s, 2)

        r, s = total_watten.get_rs(31)
        self.assertEqual(r, 7)
        self.assertEqual(s, 3)

        self.assertRaises(CardParsingError, total_watten.get_rs, 33)

    def test_get_valid_moves_last_move_raise(self):
        world = WorldTotalWatten()

        world.is_last_move_raise = True

        valid_moves = world.get_valid_moves()

        # after a raise a player can only accept it or fold
        self.assertEqual([2, 3], valid_moves)

    def test_get_valid_moves_last_move_raise_last_hand(self):
        world = WorldTotalWatten()

        world.is_last_move_raise = True
        world.is_last_hand_raise_valid = True

        valid_moves = world.get_valid_moves()

        # after a raise in last hand a player can only accept, fold, or fold and verify conditions for raise in last hand
        self.assertEqual([2, 3, 4], valid_moves)

    def test_get_valid_moves_last_move_accepted_raise(self):
        world = WorldTotalWatten()

        world.is_last_move_accepted_raise = True

        valid_moves = world.get_valid_moves()

        # after an accepted raise a player can't raise again
        self.assertNotIn(1, valid_moves)
        # self.assertNotEqual([47, 48], valid_moves)

    def test_get_valid_moves_normal(self):
        world = WorldTotalWatten()

        world.refresh()

        # opponent player declare the rank
        # valid moves: MAKE_BEST_MOVE + RAISE POINTS
        valid_moves = world.get_valid_moves()
        self.assertEqual([0, 1], valid_moves)

    def test_is_rechte(self):
        world = WorldTotalWatten()

        world.rank = 6
        world.suit = 2

        self.assertTrue(world.is_rechte(6, 2))
        self.assertFalse(world.is_rechte(6, 3))
        self.assertFalse(world.is_rechte(3, 2))
        self.assertFalse(world.is_rechte(1, 0))

        world.rank = 4
        world.suit = 2

        self.assertFalse(world.is_rechte(8, -1))
        self.assertFalse(world.is_rechte(4, 3))
        self.assertFalse(world.is_rechte(2, 4))
        self.assertFalse(world.is_rechte(5, 1))
        self.assertTrue(world.is_rechte(4, 2))

    def test_is_blinde(self):
        world = WorldTotalWatten()

        world.rank = 6
        world.suit = 2

        self.assertTrue(world.is_blinde(6))
        self.assertFalse(world.is_blinde(3))
        self.assertFalse(world.is_blinde(1))
        self.assertFalse(world.is_blinde(7))

    def test_is_trumpf(self):
        world = WorldTotalWatten()

        world.rank = 6
        world.suit = 2

        self.assertTrue(world.is_trumpf(4, 2))
        self.assertFalse(world.is_trumpf(5, 1))
        self.assertFalse(world.is_trumpf(6, 2))
        self.assertTrue(world.is_trumpf(0, 2))
        self.assertTrue(world.is_trumpf(1, 2))
        self.assertTrue(world.is_trumpf(3, 2))

        world.rank = 8
        world.suit = 3

        self.assertTrue(world.is_trumpf(1, 3))
        self.assertFalse(world.is_trumpf(5, 2))

    def test_compare_cards_rechte(self):
        world = WorldTotalWatten()

        # if weli is rechte, then it should win
        world.rank = 8
        world.suit = 1

        card_id_one = total_watten.get_id(8, 3)
        card_id_two = total_watten.get_id(5, 1)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))
        self.assertFalse(world.compare_cards(card_id_two, card_id_one))

        world.rank = 5
        world.suit = 2

        card_id_one = total_watten.get_id(5, 2)
        card_id_two = total_watten.get_id(4, 2)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))
        self.assertFalse(world.compare_cards(card_id_two, card_id_one))

        # if weli is rechte, then it should win
        world.rank = 8
        world.suit = 1

        card_id_one = total_watten.get_id(4, 3)
        card_id_two = total_watten.get_id(8, 3)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))

    def test_compare_cards_blinde(self):
        world = WorldTotalWatten()

        world.refresh()

        world.rank = 4
        world.suit = 2

        card_id_one = total_watten.get_id(8, 3)
        card_id_two = total_watten.get_id(4, 1)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))
        self.assertTrue(world.compare_cards(card_id_two, card_id_one))

        world.rank = 5
        world.suit = 1

        card_id_one = total_watten.get_id(5, 3)
        card_id_two = total_watten.get_id(5, 1)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))
        self.assertTrue(world.compare_cards(card_id_two, card_id_one))

        world.rank = 8
        world.suit = 3

        card_id_one = total_watten.get_id(8, 3)
        card_id_two = total_watten.get_id(5, 1)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))
        self.assertFalse(world.compare_cards(card_id_two, card_id_one))

        world.rank = 4
        world.suit = 0

        card_id_one = total_watten.get_id(3, 0)
        card_id_two = total_watten.get_id(4, 1)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))
        self.assertTrue(world.compare_cards(card_id_two, card_id_one))

    def test_compare_cards_first_is_trumpfe(self):
        world = WorldTotalWatten()

        world.refresh()

        # only the first card is trümpfe
        world.rank = 4
        world.suit = 2

        card_id_one = total_watten.get_id(3, 2)
        card_id_two = total_watten.get_id(5, 1)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))

        world.rank = 6
        world.suit = 1

        card_id_one = total_watten.get_id(4, 1)
        card_id_two = total_watten.get_id(7, 0)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))

        # both cards are trümpfe
        world.rank = 4
        world.suit = 2

        card_id_one = total_watten.get_id(6, 2)
        card_id_two = total_watten.get_id(5, 2)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))
        self.assertFalse(world.compare_cards(card_id_two, card_id_one))

        world.rank = 7
        world.suit = 1

        card_id_one = total_watten.get_id(5, 1)
        card_id_two = total_watten.get_id(6, 1)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))
        self.assertTrue(world.compare_cards(card_id_two, card_id_one))

        world.rank = 8
        world.suit = 3

        card_id_one = total_watten.get_id(8, 3)
        card_id_two = total_watten.get_id(2, 1)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))

    def test_compare_cards_second_is_trumpfe(self):
        world = WorldTotalWatten()

        world.refresh()

        world.rank = 4
        world.suit = 2

        card_id_one = total_watten.get_id(3, 1)
        card_id_two = total_watten.get_id(5, 2)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))

        world.rank = 7
        world.suit = 1

        card_id_one = total_watten.get_id(6, 3)
        card_id_two = total_watten.get_id(0, 1)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))

        world.rank = 8
        world.suit = 3

        card_id_one = total_watten.get_id(2, 1)
        card_id_two = total_watten.get_id(8, 3)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))

        world.rank = 2
        world.suit = 3

        card_id_one = total_watten.get_id(4, 3)
        card_id_two = total_watten.get_id(8, 3)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))

    def test_compare_cards_no_trumpfe(self):
        world = WorldTotalWatten()

        world.refresh()

        # different suit

        world.rank = 6
        world.suit = 1

        card_id_one = total_watten.get_id(5, 2)
        card_id_two = total_watten.get_id(3, 0)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))
        self.assertTrue(world.compare_cards(card_id_two, card_id_one))

        world.rank = 4
        world.suit = 0

        card_id_one = total_watten.get_id(6, 1)
        card_id_two = total_watten.get_id(7, 2)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))
        self.assertTrue(world.compare_cards(card_id_two, card_id_one))

        # same suit

        world.rank = 7
        world.suit = 2

        card_id_one = total_watten.get_id(5, 1)
        card_id_two = total_watten.get_id(3, 1)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))
        self.assertFalse(world.compare_cards(card_id_two, card_id_one))

        world.rank = 4
        world.suit = 0

        card_id_one = total_watten.get_id(1, 3)
        card_id_two = total_watten.get_id(5, 3)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))
        self.assertTrue(world.compare_cards(card_id_two, card_id_one))

    def test_is_rank_higher(self):
        world = WorldTotalWatten()

        world.refresh()

        # weli played
        self.assertFalse(world.is_rank_higher(8, 0))
        self.assertFalse(world.is_rank_higher(8, 1))
        self.assertFalse(world.is_rank_higher(8, 2))
        self.assertFalse(world.is_rank_higher(8, 3))
        self.assertFalse(world.is_rank_higher(8, 4))
        self.assertFalse(world.is_rank_higher(8, 5))
        self.assertFalse(world.is_rank_higher(8, 6))
        self.assertFalse(world.is_rank_higher(8, 7))
        self.assertTrue(world.is_rank_higher(0, 8))
        self.assertTrue(world.is_rank_higher(1, 8))
        self.assertTrue(world.is_rank_higher(2, 8))
        self.assertTrue(world.is_rank_higher(3, 8))
        self.assertTrue(world.is_rank_higher(4, 8))
        self.assertTrue(world.is_rank_higher(5, 8))
        self.assertTrue(world.is_rank_higher(6, 8))
        self.assertTrue(world.is_rank_higher(7, 8))
        self.assertTrue(world.is_rank_higher(3, 8))

        # not weli
        self.assertTrue(world.is_rank_higher(6, 5))
        self.assertTrue(world.is_rank_higher(7, 1))
        self.assertFalse(world.is_rank_higher(1, 4))
        self.assertFalse(world.is_rank_higher(3, 6))
        self.assertFalse(world.is_rank_higher(4, 6))
        self.assertFalse(world.is_rank_higher(5, 6))

    def test_is_game_end(self):
        world = WorldTotalWatten()

        world.refresh()

        result = world.is_game_end()
        self.assertFalse(result)

        world.player_A_score = 15
        result = world.is_game_end()
        self.assertTrue(result)

        world.refresh()

        world.player_B_score = 13
        result = world.is_game_end()
        self.assertFalse(result)

        world.refresh()

        world.player_B_score = 18
        result = world.is_game_end()
        self.assertTrue(result)

    def test_is_won(self):
        world = WorldTotalWatten()

        world.refresh()

        world.player_A_score = 15
        result = world.is_won(-1)
        self.assertTrue(result)

        world.refresh()

        world.player_A_score = 15
        world.player_B_score = 15
        self.assertRaises(InconsistentStateError, world.is_won, 1)

        world.refresh()

        world.player_B_score = 15
        result = world.is_won(-1)
        self.assertFalse(result)

        world.refresh()

        world.player_B_score = 15
        result = world.is_won(1)
        self.assertTrue(result)

    def test_act_unknown_move(self):
        world = WorldTotalWatten()

        self.assertRaises(InvalidActionError, world.act, 5)

    def test_act_fold(self):
        world = WorldTotalWatten()

        world.player_A_score = 4
        world.player_B_score = 7

        world.current_game_prize = 3

        world.current_player = 1
        world.distributing_cards_player = -1
        world.is_last_move_raise = True

        result, next_player = world.act(total_watten.moves["fold_hand"])

        self.assertEqual("end", result)
        self.assertEqual(7 + 2, world.player_B_score)

        self.assertEqual(-1, world.current_player)
        self.assertEqual(-1, next_player)

    def test_act_fold_hand_and_show_valid_raise(self):
        world = WorldTotalWatten()

        world.player_A_score = 4
        world.player_B_score = 7

        world.current_game_prize = 3

        world.current_player = 1
        world.distributing_cards_player = -1
        world.is_last_move_raise = True
        world.is_last_hand_raise_valid = False

        result, next_player = world.act(total_watten.moves["fold_hand_and_show_valid_raise"])

        self.assertEqual("end", result)
        self.assertEqual(7, world.player_B_score)
        self.assertEqual(4 + 2, world.player_A_score)

        self.assertEqual(-1, world.current_player)
        self.assertEqual(-1, next_player)

    def test_act_raise_points(self):
        world = WorldTotalWatten()

        world.current_player = -1
        world.current_game_prize = 4
        world.is_last_move_raise = False
        world.is_last_move_accepted_raise = False

        result, next_player = world.act(1)

        self.assertEqual(result, "continue")
        self.assertEqual(next_player, 1)
        self.assertEqual(world.current_player, 1)
        self.assertEqual(world.current_game_prize, 5)
        self.assertEqual(world.is_last_move_raise, True)
        self.assertEqual(world.is_last_move_accepted_raise, False)

    def test_act_accept_raise(self):
        world = WorldTotalWatten()

        world.current_player = 1
        world.is_last_move_accepted_raise = False
        world.is_last_move_raise = True

        result, next_player = world.act(3)

        self.assertEqual(result, "continue")
        self.assertEqual(next_player, -1)
        self.assertEqual(world.is_last_move_raise, False)
        self.assertEqual(world.is_last_move_accepted_raise, True)

    def test_last_hand_raise_valid_error(self):
        world = WorldTotalWatten()

        world.played_cards = [0, 1, 2, 3, 4]
        world.rank = 3
        world.suit = 2
        world.current_player = 1
        world.player_B_hand = [total_watten.get_id(4, 1)]
        world.player_A_hand = [total_watten.get_id(5, 0)]

        self.assertRaises(InconsistentStateError, world._last_hand_raise_valid)

    def test_last_hand_raise_valid_8_cards(self):
        # player -1 raised
        world = WorldTotalWatten()

        world.played_cards = [0, 1, 2, 3, 4, 5, 6, 7]
        world.rank = 3
        world.suit = 2
        world.current_player = -1
        world.player_B_hand = [total_watten.get_id(4, 1)]
        world.player_A_hand = [total_watten.get_id(5, 0)]

        result = world._last_hand_raise_valid()
        self.assertFalse(result)

        world = WorldTotalWatten()

        world.played_cards = [0, 1, 2, 3, 4, 5, 6, 7]
        world.rank = 3
        world.suit = 2
        world.current_player = -1
        world.player_B_hand = [total_watten.get_id(4, 2)]
        world.player_A_hand = [total_watten.get_id(5, 0)]

        result = world._last_hand_raise_valid()
        self.assertTrue(result)

        # player 1 raised
        world = WorldTotalWatten()

        world.played_cards = [0, 1, 2, 3, 4, 5, 6, 7]
        world.rank = 3
        world.suit = 2
        world.current_player = 1
        world.player_B_hand = [total_watten.get_id(4, 1)]
        world.player_A_hand = [total_watten.get_id(5, 0)]

        result = world._last_hand_raise_valid()
        self.assertFalse(result)

        world = WorldTotalWatten()

        world.played_cards = [0, 1, 2, 3, 4, 5, 6, 7]
        world.rank = 3
        world.suit = 2
        world.current_player = 1
        world.player_B_hand = [total_watten.get_id(4, 2)]
        world.player_A_hand = [total_watten.get_id(5, 2)]

        result = world._last_hand_raise_valid()
        self.assertTrue(result)

    def test_last_hand_raise_valid_9_cards(self):
        # trumpf

        # player -1 raised
        world = WorldTotalWatten()

        world.played_cards = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        world.rank = 3
        world.suit = 2
        world.current_player = -1
        world.player_B_hand = [total_watten.get_id(4, 2)]
        world.player_A_hand = [total_watten.get_id(5, 0)]

        result = world._last_hand_raise_valid()
        self.assertTrue(result)

        # player 1 raised
        world = WorldTotalWatten()

        world.played_cards = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        world.rank = 3
        world.suit = 2
        world.current_player = 1
        world.player_B_hand = [total_watten.get_id(4, 2)]
        world.player_A_hand = [total_watten.get_id(5, 2)]

        result = world._last_hand_raise_valid()
        self.assertTrue(result)

        # same suit

        # player 1 raised
        world = WorldTotalWatten()

        world.played_cards = [0, 1, 2, 3, 4, 5, 6, 7, total_watten.get_id(1, 0)]
        world.rank = 3
        world.suit = 2
        world.current_player = 1
        world.player_B_hand = []
        world.player_A_hand = [total_watten.get_id(4, 0)]

        result = world._last_hand_raise_valid()
        self.assertTrue(result)

        # player -1 raised
        world = WorldTotalWatten()

        world.played_cards = [0, 1, 2, 3, 4, 5, 6, 7, total_watten.get_id(1, 0)]
        world.rank = 3
        world.suit = 2
        world.current_player = -1
        world.player_B_hand = [total_watten.get_id(4, 0)]
        world.player_A_hand = []

        result = world._last_hand_raise_valid()
        self.assertTrue(result)

        # card beats the played one

        # player 1 raised
        world = WorldTotalWatten()

        world.played_cards = [0, 1, 2, 3, 4, 5, 6, 7, total_watten.get_id(1, 0)]
        world.rank = 3
        world.suit = 2
        world.current_player = 1
        world.player_B_hand = []
        world.player_A_hand = [total_watten.get_id(3, 2)]

        result = world._last_hand_raise_valid()
        self.assertTrue(result)

        # player -1 raised
        world = WorldTotalWatten()

        world.played_cards = [0, 1, 2, 3, 4, 5, 6, 7, total_watten.get_id(1, 0)]
        world.rank = 3
        world.suit = 2
        world.current_player = -1
        world.player_B_hand = [total_watten.get_id(3, 2)]
        world.player_A_hand = []

        result = world._last_hand_raise_valid()
        self.assertTrue(result)

        # raise was not legal

        # player 1 raised
        world = WorldTotalWatten()

        world.played_cards = [0, 1, 2, 3, 4, 5, 6, 7, total_watten.get_id(6, 3)]
        world.rank = 3
        world.suit = 2
        world.current_player = 1
        world.player_B_hand = []
        world.player_A_hand = [total_watten.get_id(1, 0)]

        result = world._last_hand_raise_valid()
        self.assertFalse(result)

        # player -1 raised
        world = WorldTotalWatten()

        world.played_cards = [0, 1, 2, 3, 4, 5, 6, 7, total_watten.get_id(6, 3)]
        world.rank = 3
        world.suit = 2
        world.current_player = -1
        world.player_B_hand = [total_watten.get_id(1, 0)]
        world.player_A_hand = []

        result = world._last_hand_raise_valid()
        self.assertFalse(result)

    def test_remove_card_from_hand(self):
        world = WorldTotalWatten()

        world.player_A_hand = [0, 1, 2, 3, 4]
        world.player_B_hand = [5, 6, 7, 8, 9]

        world._remove_card_from_hand(3, 1)
        self.assertTrue(world.player_A_hand, [0, 1, 2, 4])

        world._remove_card_from_hand(5, -1)
        self.assertTrue(world.player_A_hand, [6, 7, 8, 9])

        world._remove_card_from_hand(4, 1)
        self.assertTrue(world.player_A_hand, [0, 1, 2])

        world._remove_card_from_hand(8, -1)
        self.assertTrue(world.player_A_hand, [6, 7, 9])

    def test_get_last_played_card(self):
        world = WorldTotalWatten()
        world.played_cards = [4, 3, 2]
        last_played_card = world._get_last_played_card()
        self.assertEqual(last_played_card, 2)

        world = WorldTotalWatten()
        world.played_cards = []
        last_played_card = world._get_last_played_card()
        self.assertEqual(last_played_card, None)

        world = WorldTotalWatten()
        world.played_cards = [123]
        last_played_card = world._get_last_played_card()
        self.assertEqual(last_played_card, 123)

        world = WorldTotalWatten()
        world.played_cards = [2, 8]
        last_played_card = world._get_last_played_card()
        self.assertEqual(last_played_card, 8)

    def test_get_opponent_hand(self):
        world = WorldTotalWatten()

        world.player_A_hand = [1, 2, 3]
        world.player_B_hand = [4, 5, 6]

        world.current_player = 1

        result = world._get_opponent_hand()
        self.assertEqual(result, [4, 5, 6])

        world = WorldTotalWatten()

        world.player_A_hand = [1, 2, 3]
        world.player_B_hand = [4, 5, 6]

        world.current_player = -1

        result = world._get_opponent_hand()
        self.assertEqual(result, [1, 2, 3])

    def test_assign_points_single_hand_ended(self):
        # current player: 1
        world = WorldTotalWatten()

        world.current_player = 1
        world.current_game_player_A_score = 1
        world.current_game_player_B_score = 2

        world._assign_points_move(True)

        self.assertEqual(world.current_game_player_A_score, 2)
        self.assertEqual(world.current_game_player_B_score, 2)

        world = WorldTotalWatten()

        world.current_player = 1
        world.current_game_player_A_score = 1
        world.current_game_player_B_score = 2

        world._assign_points_move(False)

        self.assertEqual(world.current_game_player_A_score, 1)
        self.assertEqual(world.current_game_player_B_score, 3)

        # current player: 2
        world = WorldTotalWatten()

        world.current_player = -1
        world.current_game_player_A_score = 1
        world.current_game_player_B_score = 2

        world._assign_points_move(True)

        self.assertEqual(world.current_game_player_A_score, 1)
        self.assertEqual(world.current_game_player_B_score, 3)

        world = WorldTotalWatten()

        world.current_player = -1
        world.current_game_player_A_score = 1
        world.current_game_player_B_score = 2

        world._assign_points_move(False)

        self.assertEqual(world.current_game_player_A_score, 2)
        self.assertEqual(world.current_game_player_B_score, 2)

    def test_assign_points_fold(self):
        # player -1 fold
        world = WorldTotalWatten()

        world.current_player = -1
        world.current_game_prize = 5
        world.player_A_score = 3
        world.player_B_score = 8
        world.is_last_hand_raise_valid = None

        world._assign_points_fold()

        self.assertEqual(world.player_A_score, 7)
        self.assertEqual(world.player_B_score, 8)

        # player 1 fold
        world = WorldTotalWatten()

        world.current_player = 1
        world.current_game_prize = 5
        world.player_A_score = 3
        world.player_B_score = 8
        world.is_last_hand_raise_valid = None

        world._assign_points_fold()

        self.assertEqual(world.player_A_score, 3)
        self.assertEqual(world.player_B_score, 12)

        # player 1 fold is last hand raise not valid
        world = WorldTotalWatten()

        world.current_player = 1
        world.current_game_prize = 5
        world.player_A_score = 3
        world.player_B_score = 8
        world.is_last_hand_raise_valid = False

        world._assign_points_fold()

        self.assertEqual(world.player_A_score, 7)
        self.assertEqual(world.player_B_score, 8)

        # player 1 fold is last hand raise valid
        world = WorldTotalWatten()

        world.current_player = 1
        world.current_game_prize = 5
        world.player_A_score = 3
        world.player_B_score = 8
        world.is_last_hand_raise_valid = True

        world._assign_points_fold()

        self.assertEqual(world.player_A_score, 3)
        self.assertEqual(world.player_B_score, 12)

        # player -1 fold is last hand raise not valid
        world = WorldTotalWatten()

        world.current_player = -1
        world.current_game_prize = 5
        world.player_A_score = 3
        world.player_B_score = 8
        world.is_last_hand_raise_valid = False

        world._assign_points_fold()

        self.assertEqual(world.player_A_score, 3)
        self.assertEqual(world.player_B_score, 12)

        # player -1 fold is last hand raise valid
        world = WorldTotalWatten()

        world.current_player = -1
        world.current_game_prize = 5
        world.player_A_score = 3
        world.player_B_score = 8
        world.is_last_hand_raise_valid = True

        world._assign_points_fold()

        self.assertEqual(world.player_A_score, 7)
        self.assertEqual(world.player_B_score, 8)

    def test_get_current_player_hand(self):
        world = WorldTotalWatten()

        world.player_A_hand = [1, 2, 3]
        world.player_B_hand = [4, 5, 6]

        world.current_player = 1

        result = world._get_current_player_hand()
        self.assertEqual(result, [1, 2, 3])

        world = WorldTotalWatten()

        world.player_A_hand = [1, 2, 3]
        world.player_B_hand = [4, 5, 6]

        world.current_player = -1

        result = world._get_current_player_hand()
        self.assertEqual(result, [4, 5, 6])

    def test_set_initial_game_prize_player_A_ahead(self):
        world = WorldTotalWatten()

        self.assertEqual(world.current_game_prize, 2)

        world = WorldTotalWatten()
        world.player_A_score = 13
        world.player_B_score = 4

        world._set_initial_game_prize()

        self.assertEqual(world.current_game_prize, 4)

        world = WorldTotalWatten()
        world.player_A_score = 13
        world.player_B_score = 10

        world._set_initial_game_prize()

        self.assertEqual(world.current_game_prize, 3)

    def test_set_initial_game_prize_player_B_ahead(self):
        world = WorldTotalWatten()

        self.assertEqual(world.current_game_prize, 2)

        world = WorldTotalWatten()
        world.player_B_score = 13
        world.player_A_score = 4

        world._set_initial_game_prize()

        self.assertEqual(world.current_game_prize, 4)

        world = WorldTotalWatten()
        world.player_B_score = 13
        world.player_A_score = 10

        world._set_initial_game_prize()

        self.assertEqual(world.current_game_prize, 3)

    def test_observe(self):
        world = WorldTotalWatten()

        world.current_game_prize = 15

        result = world.observe(1)

        print(result)

    def test_display(self):
        watten = WorldTotalWatten()

        watten.display()


    def test_agent_returns_prediction(self):
        world = WorldTotalWatten()

        p_values, v = world.agent.predict(world.sub_watten_game, world.get_player())

        print('Observation value')
        print(v)
        print('p-values')
        print(p_values)
        print(np.argmax(p_values))

        self.assertEqual(len(p_values), 46)

    def test_best_move_declares_rank_1(self):
        world = WorldTotalWatten()

        world.current_player = 1
        world.is_last_move_accepted_raise = True
        world.is_last_move_raise = False

        result, next_player = world.act(0)

        self.assertEqual(result, "continue")
        self.assertEqual(next_player, -1)
        self.assertIsNotNone(world.rank)
        self.assertEqual(world.is_last_move_raise, False)
        self.assertEqual(False, world.is_last_move_accepted_raise)

    def test_best_move_declares_rank_2(self):
        world = WorldTotalWatten()

        world.current_player = -1
        result, next_player = world.act(0)

        self.assertEqual(result, "continue")
        self.assertEqual(next_player, 1)
        self.assertIsNotNone(world.rank)
        self.assertEqual(world.is_last_move_raise, False)
        self.assertEqual(world.is_last_move_accepted_raise, False)

    def test_best_move_declares_suit_1(self):
        world = WorldTotalWatten()

        world.current_player = 1
        world.rank = 3
        world.is_last_move_accepted_raise = True
        world.is_last_move_raise = False

        result, next_player = world.act(0)

        self.assertEqual(result, "continue")
        self.assertEqual(next_player, -1)
        self.assertIsNotNone(world.suit)
        self.assertEqual(world.is_last_move_raise, False)
        self.assertEqual(world.is_last_move_accepted_raise, False)

    def test_best_move_declares_suit_2(self):
        world = WorldTotalWatten()

        world.current_player = -1
        world.rank = 3

        result, next_player = world.act(0)

        self.assertEqual(result, "continue")
        self.assertEqual(next_player, 1)
        self.assertIsNotNone(world.suit)
        self.assertEqual(world.is_last_move_raise, False)
        self.assertEqual(world.is_last_move_accepted_raise, False)

    def test_best_move_plays_card_1(self):
        world = WorldTotalWatten()

        world.current_player = 1
        world.rank = 3
        world.suit = 1

        result, next_player = world.act(0)

        self.assertEqual(result, "continue")
        self.assertEqual(next_player, -1)
        self.assertEqual(len(world.player_A_hand), 4)
        self.assertEqual(len(world.player_B_hand), 5)

    def test_best_move_move_plays_card_2(self):
        world = WorldTotalWatten()

        world.current_player = -1
        world.rank = 3
        world.suit = 1

        result, next_player = world.act(0)

        self.assertEqual(result, "continue")
        self.assertEqual(next_player, 1)
        self.assertEqual(len(world.player_A_hand), 5)
        self.assertEqual(len(world.player_B_hand), 4)
