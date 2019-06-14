from __future__ import print_function
import sys
import copy

sys.path.append('..')
sys.path.append('watten')

import games.watten.watten as watten
import numpy as np

from core.interfaces.Game import Game

from loggers import stdout_logger


class WattenGame(Game):
    def __init__(self):
        self.trueboard = watten.WorldWatten()
        self.players = {1: 0, -1: 1}  # player NUMBER 1 is [0] and player NUMBER -1 is [1]
        self.players_inv = {0: 1, 1: -1}

    def reset(self):
        self.trueboard = watten.WorldWatten()

    def get_cur_player(self):
        player = self.trueboard.get_player()
        return self.players[player]

    def get_players_num(self):
        return 2

    def get_action_size(self):
        return 50

    def get_observation_size(self):
        return 226, 1

    def make_move(self, action):
        current_player = self.trueboard.current_player
        game_status, next_player = self.trueboard.act(action)
        if game_status == "end" and self.trueboard.is_game_end():
            if self.trueboard.winning_player is None:
                raise Exception("Winning player cannot be None if game is ended")

            if self.trueboard.winning_player == current_player:
                return 1.0, self.players[next_player]
            else:
                return -1.0, self.players[next_player]
        else:
            return 0.0, self.players[next_player]

    def get_valid_moves(self, player=None):
        return self.trueboard.get_valid_moves_zeros()

    def get_valid_moves_no_zeros(self):
        return self.trueboard.get_valid_moves()

    def is_ended(self):
        return self.trueboard.is_game_end()

    def is_draw(self):
        # in Watten a game can never end with a draw
        return False

    def get_score(self, player):
        player_curr = self.players_inv[player]  # 1 if player == 0 else -1

        if self.trueboard.winning_player is None:
            return 0.0

        if self.trueboard.is_game_end():
            if self.trueboard.winning_player == player_curr:
                return 1.0
            else:
                return -1.0

        raise Exception("Inconsistent score")

    def get_observation(self, player):
        if player not in [0, 1]:
            print("WARNING: %d not in [0, 1]" % player)
        player_in = self.players_inv[player]  # 1 if player == 0 else -1
        observation = self.trueboard.observe(player_in)
        return observation

    def get_observation_str(self, observation):
        if isinstance(observation, np.ndarray):
            return observation.tostring()
        else:
            return str(observation)

    def get_display_str(self):
        self.trueboard.display()
        return ""

    def clone(self):
        cloned_game = WattenGame()
        cloned_game.trueboard = self.trueboard.deepcopy()
        return cloned_game

    def reset_unknown_states(self, player):
        pass
