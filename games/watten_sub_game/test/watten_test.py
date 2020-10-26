from logging import DEBUG
from unittest import TestCase
import games.watten_sub_game.watten_sub as watten
from games.watten_sub_game.watten_sub import WorldSubWatten
from games.watten_sub_game.watten_sub import InconsistentStateError
from games.watten_sub_game.watten_sub import CardParsingError
from games.watten_sub_game.watten_sub import InvalidActionError


class TestWorldSubWatten(TestCase):

    def test_refresh(self):
        world = WorldSubWatten()

    def test_get_id(self):
        card_id = watten.get_id(8, 3)
        self.assertEqual(card_id, 32)

        card_id = watten.get_id(0, 0)
        self.assertEqual(card_id, 0)

        card_id = watten.get_id(4, 3)
        self.assertEqual(card_id, 28)

        card_id = watten.get_id(1, 2)
        self.assertEqual(card_id, 17)

        card_id = watten.get_id(7, 3)
        self.assertEqual(card_id, 31)

        card_id = watten.get_id(8, 2)
        self.assertEqual(card_id, 32)

        self.assertRaises(CardParsingError, watten.get_id, 2, 10)

        self.assertRaises(CardParsingError, watten.get_id, 14, 2)

    def test_get_rs(self):
        r, s = watten.get_rs(32)
        self.assertEqual(r, 8)
        self.assertEqual(s, 3)

        r, s = watten.get_rs(0)
        self.assertEqual(r, 0)
        self.assertEqual(s, 0)

        r, s = watten.get_rs(28)
        self.assertEqual(r, 4)
        self.assertEqual(s, 3)

        r, s = watten.get_rs(17)
        self.assertEqual(r, 1)
        self.assertEqual(s, 2)

        r, s = watten.get_rs(31)
        self.assertEqual(r, 7)
        self.assertEqual(s, 3)

        self.assertRaises(CardParsingError, watten.get_rs, 33)

    def test_get_valid_moves_declare_rank(self):
        world = WorldSubWatten()

        world.refresh()

        # opponent player declare the rank
        # valid moves: ALL RANKS
        valid_moves = world.get_valid_moves()
        self.assertEqual([33, 34, 35, 36, 37, 38, 39, 40, 41], valid_moves)

    def test_get_valid_moves_declare_suit_rank_weli(self):
        world = WorldSubWatten()

        world.refresh()

        # when the chosen rank is weli, suit is automatically
        world.rank = 8
        world.suit = 3

        # opponent player declare the rank
        valid_moves = world.get_valid_moves()

        # if picked rank is weli, then it doesn't matter to declare a suit
        self.assertEqual(len(valid_moves), 5)

    def test_get_valid_moves_declare_suit(self):
        world = WorldSubWatten()

        world.rank = 5  # rank already chosen

        # current player declare the suit
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [42, 43, 44, 45])

        world.suit = 3

        valid_moves = world.get_valid_moves()

        self.assertEqual(len(valid_moves), 5)

        # no suit played - every move is allowed
        world.played_cards.append(watten.get_id(7, 2))
        world.current_player = 1
        world.player_A_hand = [watten.get_id(3, 2), watten.get_id(6, 3), watten.get_id(3, 0),
                               watten.get_id(2, 0), watten.get_id(4, 1)]

        valid_moves = world.get_valid_moves()

        self.assertEqual(valid_moves, [19, 30, 3, 2, 12])

    def test_get_valid_moves_played_suit(self):
        world = WorldSubWatten()

        # suit has been played
        world.played_cards = []
        world.rank = 4
        world.suit = 3
        world.played_cards.append(watten.get_id(3, 3))
        world.current_player = 1
        world.player_A_hand = [watten.get_id(1, 2), watten.get_id(1, 3), watten.get_id(3, 0),
                               watten.get_id(4, 3), watten.get_id(4, 2)]

        valid_moves = world.get_valid_moves()

        self.assertEqual(valid_moves, [25, 28, 20])

    def test_get_valid_moves_played_suit_only_rechte(self):
        world = WorldSubWatten()

        # suit has been played
        world.played_cards = []
        world.rank = 4
        world.suit = 3
        world.played_cards.append(watten.get_id(3, 3))
        world.current_player = 1
        world.player_A_hand = [watten.get_id(1, 2), watten.get_id(1, 0), watten.get_id(3, 0),
                               watten.get_id(4, 3), watten.get_id(2, 2)]

        valid_moves = world.get_valid_moves()

        self.assertEqual(valid_moves, [17, 1, 3, 28, 18])

    def test_is_rechte(self):
        world = WorldSubWatten()

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
        world = WorldSubWatten()

        world.rank = 6
        world.suit = 2

        self.assertTrue(world.is_blinde(6))
        self.assertFalse(world.is_blinde(3))
        self.assertFalse(world.is_blinde(1))
        self.assertFalse(world.is_blinde(7))

    def test_is_trumpf(self):
        world = WorldSubWatten()

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
        world = WorldSubWatten()

        # if weli is rechte, then it should win
        world.rank = 8
        world.suit = 1

        card_id_one = watten.get_id(8, 3)
        card_id_two = watten.get_id(5, 1)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))
        self.assertFalse(world.compare_cards(card_id_two, card_id_one))

        world.rank = 5
        world.suit = 2

        card_id_one = watten.get_id(5, 2)
        card_id_two = watten.get_id(4, 2)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))
        self.assertFalse(world.compare_cards(card_id_two, card_id_one))

        # if weli is rechte, then it should win
        world.rank = 8
        world.suit = 1

        card_id_one = watten.get_id(4, 3)
        card_id_two = watten.get_id(8, 3)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))

    def test_compare_cards_blinde(self):
        world = WorldSubWatten()

        world.refresh()

        world.rank = 4
        world.suit = 2

        card_id_one = watten.get_id(8, 3)
        card_id_two = watten.get_id(4, 1)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))
        self.assertTrue(world.compare_cards(card_id_two, card_id_one))

        world.rank = 5
        world.suit = 1

        card_id_one = watten.get_id(5, 3)
        card_id_two = watten.get_id(5, 1)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))
        self.assertTrue(world.compare_cards(card_id_two, card_id_one))

        world.rank = 8
        world.suit = 3

        card_id_one = watten.get_id(8, 3)
        card_id_two = watten.get_id(5, 1)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))
        self.assertFalse(world.compare_cards(card_id_two, card_id_one))

        world.rank = 4
        world.suit = 0

        card_id_one = watten.get_id(3, 0)
        card_id_two = watten.get_id(4, 1)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))
        self.assertTrue(world.compare_cards(card_id_two, card_id_one))

    def test_compare_cards_first_is_trumpfe(self):
        world = WorldSubWatten()

        world.refresh()

        # only the first card is trümpfe
        world.rank = 4
        world.suit = 2

        card_id_one = watten.get_id(3, 2)
        card_id_two = watten.get_id(5, 1)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))

        world.rank = 6
        world.suit = 1

        card_id_one = watten.get_id(4, 1)
        card_id_two = watten.get_id(7, 0)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))

        # both cards are trümpfe
        world.rank = 4
        world.suit = 2

        card_id_one = watten.get_id(6, 2)
        card_id_two = watten.get_id(5, 2)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))
        self.assertFalse(world.compare_cards(card_id_two, card_id_one))

        world.rank = 7
        world.suit = 1

        card_id_one = watten.get_id(5, 1)
        card_id_two = watten.get_id(6, 1)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))
        self.assertTrue(world.compare_cards(card_id_two, card_id_one))

        world.rank = 8
        world.suit = 3

        card_id_one = watten.get_id(8, 3)
        card_id_two = watten.get_id(2, 1)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))

    def test_compare_cards_second_is_trumpfe(self):
        world = WorldSubWatten()

        world.refresh()

        world.rank = 4
        world.suit = 2

        card_id_one = watten.get_id(3, 1)
        card_id_two = watten.get_id(5, 2)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))

        world.rank = 7
        world.suit = 1

        card_id_one = watten.get_id(6, 3)
        card_id_two = watten.get_id(0, 1)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))

        world.rank = 8
        world.suit = 3

        card_id_one = watten.get_id(2, 1)
        card_id_two = watten.get_id(8, 3)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))

        world.rank = 2
        world.suit = 3

        card_id_one = watten.get_id(4, 3)
        card_id_two = watten.get_id(8, 3)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))

    def test_compare_cards_no_trumpfe(self):
        world = WorldSubWatten()

        world.refresh()

        # different suit

        world.rank = 6
        world.suit = 1

        card_id_one = watten.get_id(5, 2)
        card_id_two = watten.get_id(3, 0)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))
        self.assertTrue(world.compare_cards(card_id_two, card_id_one))

        world.rank = 4
        world.suit = 0

        card_id_one = watten.get_id(6, 1)
        card_id_two = watten.get_id(7, 2)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))
        self.assertTrue(world.compare_cards(card_id_two, card_id_one))

        # same suit

        world.rank = 7
        world.suit = 2

        card_id_one = watten.get_id(5, 1)
        card_id_two = watten.get_id(3, 1)

        self.assertTrue(world.compare_cards(card_id_one, card_id_two))
        self.assertFalse(world.compare_cards(card_id_two, card_id_one))

        world.rank = 4
        world.suit = 0

        card_id_one = watten.get_id(1, 3)
        card_id_two = watten.get_id(5, 3)

        self.assertFalse(world.compare_cards(card_id_one, card_id_two))
        self.assertTrue(world.compare_cards(card_id_two, card_id_one))

    def test_is_rank_higher(self):
        world = WorldSubWatten()

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
        world = WorldSubWatten()

        world.refresh()

        result = world.is_game_end()
        self.assertFalse(result)

        world.current_game_player_A_score = 3
        result = world.is_game_end()
        self.assertTrue(result)

        world.refresh()

        world.current_game_player_B_score = 2
        result = world.is_game_end()
        self.assertFalse(result)

        world.refresh()

        world.current_game_player_B_score = 3
        result = world.is_game_end()
        self.assertTrue(result)

    def test_is_won(self):
        world = WorldSubWatten()

        world.refresh()

        world.current_game_player_A_score = 3
        result = world.is_won(-1)
        self.assertTrue(result)

        world.refresh()

        world.current_game_player_A_score = 3
        world.current_game_player_B_score = 3
        self.assertRaises(InconsistentStateError, world.is_won, 1)

        world.refresh()

        world.current_game_player_B_score = 3
        result = world.is_won(-1)
        self.assertFalse(result)

        world.refresh()

        world.current_game_player_B_score = 3
        result = world.is_won(1)
        self.assertTrue(result)

    def test_act_unknown_move(self):
        world = WorldSubWatten()

        self.assertRaises(InvalidActionError, world.act, 46)

    def test_act_pick_suit_1(self):
        world = WorldSubWatten()

        world.current_player = 1
        world.rank = 3

        result, next_player = world.act(45)

        self.assertEqual(result, "continue")
        self.assertEqual(next_player, -1)
        self.assertEqual(world.suit, 3)

    def test_act_pick_suit_2(self):
        world = WorldSubWatten()

        world.current_player = -1
        world.rank = 3

        result, next_player = world.act(42)

        self.assertEqual(result, "continue")
        self.assertEqual(next_player, 1)
        self.assertEqual(world.suit, 0)

    def test_remove_card_from_hand(self):
        world = WorldSubWatten()

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
        world = WorldSubWatten()
        world.played_cards = [4, 3, 2]
        last_played_card = world._get_last_played_card()
        self.assertEqual(last_played_card, 2)

        world = WorldSubWatten()
        world.played_cards = []
        last_played_card = world._get_last_played_card()
        self.assertEqual(last_played_card, None)

        world = WorldSubWatten()
        world.played_cards = [123]
        last_played_card = world._get_last_played_card()
        self.assertEqual(last_played_card, 123)

        world = WorldSubWatten()
        world.played_cards = [2, 8]
        last_played_card = world._get_last_played_card()
        self.assertEqual(last_played_card, 8)

    def test_get_opponent_hand(self):
        world = WorldSubWatten()

        world.player_A_hand = [1, 2, 3]
        world.player_B_hand = [4, 5, 6]

        world.current_player = 1

        result = world._get_opponent_hand()
        self.assertEqual(result, [4, 5, 6])

        world = WorldSubWatten()

        world.player_A_hand = [1, 2, 3]
        world.player_B_hand = [4, 5, 6]

        world.current_player = -1

        result = world._get_opponent_hand()
        self.assertEqual(result, [1, 2, 3])

    def test_assign_points_single_hand_ended(self):
        # current player: 1
        world = WorldSubWatten()

        world.current_player = 1
        world.current_game_player_A_score = 1
        world.current_game_player_B_score = 2

        world._assign_points_move(True)

        self.assertEqual(world.current_game_player_A_score, 2)
        self.assertEqual(world.current_game_player_B_score, 2)

        world = WorldSubWatten()

        world.current_player = 1
        world.current_game_player_A_score = 1
        world.current_game_player_B_score = 2

        world._assign_points_move(False)

        self.assertEqual(world.current_game_player_A_score, 1)
        self.assertEqual(world.current_game_player_B_score, 3)

        # current player: 2
        world = WorldSubWatten()

        world.current_player = -1
        world.current_game_player_A_score = 1
        world.current_game_player_B_score = 2

        world._assign_points_move(True)

        self.assertEqual(world.current_game_player_A_score, 1)
        self.assertEqual(world.current_game_player_B_score, 3)

        world = WorldSubWatten()

        world.current_player = -1
        world.current_game_player_A_score = 1
        world.current_game_player_B_score = 2

        world._assign_points_move(False)

        self.assertEqual(world.current_game_player_A_score, 2)
        self.assertEqual(world.current_game_player_B_score, 2)

    def test_get_current_player_hand(self):
        world = WorldSubWatten()

        world.player_A_hand = [1, 2, 3]
        world.player_B_hand = [4, 5, 6]

        world.current_player = 1

        result = world._get_current_player_hand()
        self.assertEqual(result, [1, 2, 3])

        world = WorldSubWatten()

        world.player_A_hand = [1, 2, 3]
        world.player_B_hand = [4, 5, 6]

        world.current_player = -1

        result = world._get_current_player_hand()
        self.assertEqual(result, [4, 5, 6])

    def test_observe(self):
        world = WorldSubWatten()

        result = world.observe(1)

        print(result)

    def test_display(self):
        world = WorldSubWatten()

        world.display()
