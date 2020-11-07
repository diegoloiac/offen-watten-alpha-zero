from logging import DEBUG
from unittest import TestCase
from games.total_watten.TotalWattenGame import TotalWattenGame
from games.total_watten.total_watten import WorldTotalWatten
import EnvironmentSelector as es


class TestWorldCompleteGameWatten(TestCase):

    @classmethod
    def setUpClass(self):
        print('setting up test fixture')
        env = es.EnvironmentSelector()
        self.agent = env.sub_watten_non_human_agent_for_total_watten()

    # Forse non ha senso perchè non posso scegliere la mossa
    def no_test_game_no_raise_player_A_starts(self):
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

    # probabilmente non serve
    def no_test_game_no_raise_player_B_starts(self):
        world = WorldWatten()
        world.LOG.setLevel(DEBUG)

        world.init_world_to_state(-1, 1, 0, 0, [3, 31, 27, 10, 29], [0, 9, 30, 25, 26], [], 0, 0, 2, False, False, None, 15, 20, None, None)

        # [30, 29, 37, 45, 7, 10, 21, 19, 25, 24,
        # 33, 42, 8, 20, 32, 31, 24, 10, 0, 9, 36, 43, 23, 28, 12, 8, 31, 30, 34,
        #  43, 21, 23, 12, 17, 22, 24, 0, 4, 11, 25, 35, 44, 12, 1, 21, 17, 10,
        #  32, 34, 42, 19, 16, 3, 2, 20, 7, 13, 22, 11, 29, 37, 42, 8, 2, 3, 9, 5,
        #  4, 31, 16, 15, 32, 38, 44, 7, 24, 6, 22, 2, 23, 27, 9, 33, 42, 6, 16,
        #  17, 9, 13, 22, 34, 43, 19, 1, 5, 20, 10, 12, 17, 31, 22, 18, 35, 44,
        #  23, 20, 10, 25, 15, 14, 34, 43, 13, 12, 22, 10, 2, 1, 29, 18, 41, 45,
        #  5, 2, 14, 16, 27, 25]
        world_copy = world.deepcopy()

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [33, 34, 35, 36, 37, 38, 39, 40, 41, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(37)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, 1)

        world_copy.rank = 4
        world_copy.current_player = 1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [42, 43, 44, 45, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(45)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, -1)

        world_copy.suit = 3
        world_copy.current_player = -1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [0, 9, 30, 25, 26, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(0)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, 1)

        world_copy.player_B_hand = [9, 30, 25, 26]
        world_copy.played_cards = [0]
        world_copy.current_player = 1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [3, 31, 27, 10, 29, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(10)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, -1)

        world_copy.player_A_hand = [3, 31, 27, 29]
        world_copy.played_cards = [0, 10]
        world_copy.current_game_player_B_score = 1
        world_copy.current_player = -1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [9, 30, 25, 26, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(25)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, 1)

        world_copy.player_B_hand = [9, 30, 26]
        world_copy.played_cards = [0, 10, 25]
        world_copy.current_player = 1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [31, 27, 29, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(31)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, 1)

        world_copy.player_A_hand = [3, 27, 29]
        world_copy.played_cards = [0, 10, 25, 31]
        world_copy.current_player = 1
        world_copy.current_game_player_A_score = 1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [3, 27, 29, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(3)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, -1)

        world_copy.player_A_hand = [27, 29]
        world_copy.played_cards = [0, 10, 25, 31, 3]
        world_copy.current_player = -1
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [9, 30, 26, 46])
        self._compare_worlds(world, world_copy)

        outcome, next_player = world.act(26)
        self.assertEqual(outcome, "continue")
        self.assertEqual(next_player, -1)

        world_copy.player_B_hand = [9, 30]
        world_copy.played_cards = [0, 10, 25, 31, 3, 26]
        world_copy.current_game_player_B_score = 2
        self._compare_worlds(world, world_copy)

        ######## MOVE ########
        valid_moves = world.get_valid_moves()
        self.assertEqual(valid_moves, [9, 30, 46])
        self._compare_worlds(world, world_copy)

    def test_game_complete(self):
        # [36, 45, 14, 5, 25, 20, 46, 48, 1, 46, 48, 13, 35, 45, 15, 18, 7, 2,
        #  30, 46, 47, 36, 43, 27, 5, 46, 48, 6, 2, 22, 46, 47, 35, 44, 29, 8, 46,
        #  48, 18, 21, 27, 26, 14, 11, 9, 46, 48, 17, 34, 43, 10, 1, 46, 47, 41,
        #  42, 24, 17, 46, 48, 0, 14, 3, 29, 46, 48, 41, 45, 19, 8, 30, 24, 20,
        #  16, 34, 46, 47, 39, 44, 16, 30, 18, 46, 48, 21, 46, 47, 39, 43, 24,
        #  26, 14, 22, 29, 6, 5, 7]

        game = TotalWattenGame(self.agent, self.agent)
        world = WorldTotalWatten()
        world.init_world_to_state(1, -1, 0, 0, [25, 9, 1, 32, 14], [5, 13, 7, 10, 20], [], 0, 0, 2, False, False, None, 16, 28, None, None)
        game.trueboard = world

        cur_player = game.get_cur_player()
        self.assertEqual(cur_player, 0)

        moves = game.get_valid_moves_no_zeros()
        self.assertEqual(moves, [0, 1])

        self.assertEqual(game.make_move(0), (0.0, 1))

        cur_player = game.get_cur_player()
        self.assertEqual(cur_player, 1)

        moves = game.get_valid_moves_no_zeros()
        self.assertEqual(moves, [0, 1])

    def test_clone(self):
        game = TotalWattenGame(self.agent, self.agent)
        world = WorldTotalWatten()
        world.init_world_to_state(1, -1, 0, 0, [25, 9, 1, 32, 14], [5, 13, 7, 10, 20], [], 0, 0, 2, False, False, None, 16, 28, None, None)
        game.trueboard = world

        clone_game = game.clone()

        obs_game = game.get_observation(game.get_cur_player())

        obs_clone_game = clone_game.get_observation(clone_game.get_cur_player())

        obs_str = game.get_observation_str(obs_game)
        clone_obs_str = clone_game.get_observation_str(obs_clone_game)

        self.assertEqual(obs_str, clone_obs_str)


    # probabilmente non serve
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
