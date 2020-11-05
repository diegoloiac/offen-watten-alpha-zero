from unittest import TestCase
from games.total_watten.TotalWattenGame import TotalWattenGame


class TestWorldWatten(TestCase):

    def test_get_cur_player(self):
        watten_game = TotalWattenGame()
        watten_game.trueboard.current_player = 1
        self.assertEqual(watten_game.get_cur_player(), 0)

        watten_game.trueboard.current_player = -1
        self.assertEqual(watten_game.get_cur_player(), 1)

    def test_get_player_num(self):
        watten_game = TotalWattenGame()
        self.assertEqual(watten_game.get_players_num(), 2)

    def test_get_action_size(self):
        watten_game = TotalWattenGame()
        self.assertEqual(watten_game.get_action_size(), 5)

    def test_get_observation_size(self):
        watten_game = TotalWattenGame()
        self.assertEqual(watten_game.get_observation_size(), (149, 1))

    def test_make_move(self):
        watten_game = TotalWattenGame()
        watten_game.trueboard.current_player = 1
        self.assertEqual(watten_game.make_move(0), (0.0, 1))

        watten_game = TotalWattenGame()
        watten_game.trueboard.distributing_cards_player = -1
        watten_game.trueboard.suit = 1
        watten_game.trueboard.rank = 3
        watten_game.trueboard.current_player = 1
        watten_game.trueboard.current_game_player_A_score = 2
        watten_game.trueboard.player_A_score = 15
        watten_game.trueboard.played_cards = [0]
        watten_game.trueboard.player_A_hand = [1]
        self.assertEqual(watten_game.make_move(0), (1.0, 1))

        watten_game = TotalWattenGame()
        watten_game.trueboard.distributing_cards_player = 1
        watten_game.trueboard.suit = 1
        watten_game.trueboard.rank = 3
        watten_game.trueboard.current_player = 1
        watten_game.trueboard.current_game_player_A_score = 2
        watten_game.trueboard.player_A_score = 15
        watten_game.trueboard.played_cards = [0]
        watten_game.trueboard.player_A_hand = [1]
        self.assertEqual(watten_game.make_move(0), (1.0, 0))

    def test_get_score(self):
        watten_game = TotalWattenGame()
        watten_game.trueboard.current_player = 1
        self.assertEqual(watten_game.get_score(1), 0.0)
        self.assertEqual(watten_game.get_score(0), 0.0)

        watten_game.trueboard.winning_player = 1
        watten_game.trueboard.player_A_score = 15
        self.assertEqual(watten_game.get_score(1), -1.0)
        self.assertEqual(watten_game.get_score(0), 1.0)

        watten_game = TotalWattenGame()
        watten_game.trueboard.current_player = -1
        self.assertEqual(watten_game.get_score(1), 0.0)
        self.assertEqual(watten_game.get_score(0), 0.0)

        watten_game.trueboard.winning_player = -1
        watten_game.trueboard.player_B_score = 15
        self.assertEqual(watten_game.get_score(1), 1.0)
        self.assertEqual(watten_game.get_score(0), -1.0)


