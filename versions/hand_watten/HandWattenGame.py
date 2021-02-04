from __future__ import print_function
import versions.hand_watten.hand_watten as hand_watten
import versions.hand_watten.cnn_hand_watten as cnnwatten
import numpy as np
import math

from core.interfaces.Game import Game


class HandWattenGame(Game):
    def __init__(self, cnn=False):
        super(HandWattenGame, self).__init__()
        self.cnn = cnn
        if not cnn:
            self.trueboard = hand_watten.WorldHandWatten()
        else:
            self.trueboard = cnnwatten.CNNHandWatten()

        self.players = {1: 0, -1: 1}  # player NUMBER 1 is [0] and player NUMBER -1 is [1]
        self.players_inv = {0: 1, 1: -1}

    def reset(self):
        if not self.cnn:
            self.trueboard = hand_watten.WorldHandWatten()
        else:
            self.trueboard = cnnwatten.CNNHandWatten()

    def get_cur_player(self):
        player = self.trueboard.get_player()
        return self.players[player]

    def get_players_num(self):
        return 2

    def get_action_size(self):
        return 50

    def get_observation_size(self):
        if self.cnn:
            return 17, 17, 19
        else:
            return 198, 1

    def make_move(self, action):
        current_player = self.trueboard.current_player
        game_status, next_player = self.trueboard.act(action)
        if game_status == "end" and self.trueboard.is_game_end():
            if self.trueboard.winning_player is None:
                raise Exception("Winning player cannot be None if game is ended")

            x = self.trueboard.current_game_prize*1.0/4

            if self.trueboard.winning_player == current_player:
                return x/(math.sqrt(1+x**2)), self.players[next_player]
            else:
                return -x/(math.sqrt(1+x**2)), self.players[next_player]
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

        x = self.trueboard.current_game_prize*1.0/4

        if self.trueboard.is_game_end():
            if self.trueboard.winning_player == player_curr:
                return x/(math.sqrt(1+x**2))
            else:
                return -x/(math.sqrt(1+x**2))

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
        cloned_game = HandWattenGame(self.cnn)
        cloned_game.trueboard = self.trueboard.deepcopy()
        return cloned_game

    def reset_unknown_states(self, player):
        pass

    def get_player_visible_state(self, player):
        player_in = self.players_inv[player]

        player_hand = self.trueboard.player_A_hand if player_in == 1 else self.trueboard.player_B_hand
        opponent_hand = self.trueboard.player_B_hand if player_in == 1 else self.trueboard.player_A_hand

        first_card_deck = self.trueboard.first_card_deck
        last_card_deck = self.trueboard.last_card_deck if player_in == self.trueboard.distributing_cards_player else None

        current_game_player_A_score = self.trueboard.current_game_player_A_score
        current_game_player_B_score = self.trueboard.current_game_player_B_score

        played_cards = self.trueboard.played_cards

        current_game_prize = self.trueboard.current_game_prize

        suit = self.trueboard.suit
        rank = self.trueboard.rank

        return {
            'player_hand': player_hand,
            'opponent_hand': opponent_hand,
            'first_card_deck': first_card_deck,
            'last_card_deck': last_card_deck,
            'current_game_player_A_score': current_game_player_A_score,
            'current_game_player_B_score': current_game_player_B_score,
            'played_cards': played_cards,
            'current_game_prize': current_game_prize,
            'suit': suit,
            'rank': rank
        }
