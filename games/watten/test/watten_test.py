from logging import DEBUG
from unittest import TestCase
import games.watten.watten as watten
from games.watten.watten import WorldWatten
from games.watten.watten import InconsistentStateError
from games.watten.watten import CardParsingError


class TestWorldWatten(TestCase):

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

    def test_get_valid_moves_last_move_raise(self):
        world = WorldWatten()

        world.is_last_move_raise = True

        valid_moves = world.get_valid_moves()

        # after a raise a player can only accept it or fold
        self.assertEqual([47, 48], valid_moves)

    def test_get_valid_moves_last_move_accepted_raise(self):
        world = WorldWatten()

        world.is_last_move_raise_accepted = True

        valid_moves = world.get_valid_moves()

        # after an accepted raise a player can't raise again
        self.assertNotEqual([47, 48], valid_moves)

    def test_get_valid_moves_declare_rank(self):
        world = WorldWatten()

        world.refresh()

        # opponent player declare the rank
        # valid moves: ALL RANKS + RAISE POINTS
        valid_moves = world.get_valid_moves()
        self.assertEqual([33, 34, 35, 36, 37, 38, 39, 40, 41, 46], valid_moves)

    def test_get_valid_moves_declare_suit_rank_weli(self):
        world = WorldWatten()

        world.refresh()

        # when the chosen rank is weli, suit is automatically
        world.rank = 8
        world.suit = None

        # opponent player declare the rank
        valid_moves = world.get_valid_moves()

        # if picked rank is weli, then it doesn't matter to declare a suit
        self.assertEqual(len(valid_moves), 6)

    def test_get_valid_moves_declare_suit(self):
        world = WorldWatten()

        world.rank = 5  # rank already chosen

        # current player declare the suit
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [42, 43, 44, 45, 46])

        world.suit = 3

        valid_moves = world.get_valid_moves()

        self.assertEqual(len(valid_moves), 6)

        # no suit played - every move is allowed
        world.played_cards.append(watten.get_id(7, 2))
        world.current_player = 1
        world.player_A_hand = [watten.get_id(3, 2), watten.get_id(6, 3), watten.get_id(3, 0),
                               watten.get_id(2, 0), watten.get_id(4, 1)]

        valid_moves = world.get_valid_moves()

        self.assertEqual(valid_moves, [19, 30, 3, 2, 12, 46])

    def test_get_valid_moves_played_suit(self):
        world = WorldWatten()

        # suit has been played
        world.played_cards = []
        world.rank = 4
        world.suit = 3
        world.played_cards.append(watten.get_id(3, 3))
        world.current_player = 1
        world.player_A_hand = [watten.get_id(1, 2), watten.get_id(1, 3), watten.get_id(3, 0),
                               watten.get_id(4, 3), watten.get_id(4, 2)]

        valid_moves = world.get_valid_moves()

        self.assertEqual(valid_moves, [25, 28, 20, 46])

    def test_get_valid_moves_played_suit_only_rechte(self):
        world = WorldWatten()

        # suit has been played
        world.played_cards = []
        world.rank = 4
        world.suit = 3
        world.played_cards.append(watten.get_id(3, 3))
        world.current_player = 1
        world.player_A_hand = [watten.get_id(1, 2), watten.get_id(1, 0), watten.get_id(3, 0),
                               watten.get_id(4, 3), watten.get_id(2, 2)]

        valid_moves = world.get_valid_moves()

        self.assertEqual(valid_moves, [17, 1, 3, 28, 18, 46])

    def test_is_rechte(self):
        world = WorldWatten()

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
        world = WorldWatten()

        world.refresh()

        world.rank = 6
        world.suit = 2

        self.assertTrue(world.is_blinde(6))
        self.assertFalse(world.is_blinde(3))
        self.assertFalse(world.is_blinde(1))
        self.assertFalse(world.is_blinde(7))

    def test_compare_cards_rechte(self):
        world = WorldWatten()

        world.refresh()

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
        world = WorldWatten()

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
        world = WorldWatten()

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
        world = WorldWatten()

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
        world = WorldWatten()

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
        world = WorldWatten()

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
        world = WorldWatten()

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
        world = WorldWatten()

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

    def test_act_fold(self):
        world = WorldWatten()

        world.refresh()

        world.player_A_score = 4
        world.player_B_score = 7

        world.current_game_prize = 3

        world.current_player = 1

        result, next_player = world.act(watten.moves["fold_hand"])

        self.assertEqual("end", result)
        self.assertEqual(4 + 3, world.player_A_score)

        self.assertEqual(-1, world.current_player)
        self.assertEqual(-1, next_player)

    def test_act_unknown_move(self):
        world = WorldWatten()

        self.assertRaises(InconsistentStateError, world.act, 49)

    def test_observe(self):
        world = WorldWatten()

        world.current_game_player_A_score = 3
        world.observe(1)

    def test_display(self):
        watten = WorldWatten()

        watten.display()

    def test_game_1(self):
        watten = WorldWatten()
        watten.LOG.setLevel(DEBUG)

        watten.player_A_hand = [6, 20, 12, 26, 10]
        watten.player_B_hand = [8, 22, 7, 3, 1]
        watten.display()

        watten.get_valid_moves()

        watten.act(35)

        watten.get_valid_moves()

        watten.act(42)

        watten.get_valid_moves()

        watten.act(20)

        watten.get_valid_moves()

        watten.act(46)

        watten.get_valid_moves()

        watten.act(48)

        watten.get_valid_moves()

        watten.act(22)

        watten.get_valid_moves()

        watten.act(8)

        watten.get_valid_moves()

        watten.act(12)

        watten.get_valid_moves()

        watten.act(6)

        watten.get_valid_moves()

        watten.act(7)

        watten.get_valid_moves()

        watten.act(3)

        watten.get_valid_moves()

        watten.act(26)

        watten.get_valid_moves()

        watten.act(10)

        watten.get_valid_moves()

        watten.act(1)

        watten.display()

    # TODO debug
    def test_game_2(self):
        watten = WorldWatten()
        watten.LOG.setLevel(DEBUG)
        watten.init_world_to_state(1, -1, 0, 0, [6, 19, 17, 23, 12], [9, 28, 0, 10, 29], [], 0, 0, 2, False, False, 26,
                                   16, None, None)
        watten.display()
        # 34, 44, 19, 9, 29, 46, 48, 46, 0, 10, 12, 23, 28
        watten.get_valid_moves()

        watten.act(34)

        watten.get_valid_moves()

        watten.act(44)

        watten.get_valid_moves()

        watten.act(19)

        watten.get_valid_moves()

        watten.act(9)

        watten.get_valid_moves()

        watten.act(29)

        watten.get_valid_moves()

        watten.act(46)

        watten.get_valid_moves()

        watten.act(48)

        watten.get_valid_moves()

        watten.act(46)

        watten.get_valid_moves()

        watten.act(0)

        watten.get_valid_moves()

        watten.act(10)

        watten.get_valid_moves()

        watten.act(12)

        watten.get_valid_moves()

        watten.act(23)

        watten.get_valid_moves()

        watten.act(28)

        watten.get_valid_moves()

        watten.display()
