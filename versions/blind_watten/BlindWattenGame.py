import versions.blind_watten.blind_watten as blind_watten
import numpy as np

from core.interfaces.Game import Game


class BlindWattenGame(Game):

    def __init__(self):
        super().__init__()
        self.trueboard = blind_watten.WorldBlindWatten()


    def reset(self):
        self.trueboard = blind_watten.WorldBlindWatten()

    def get_cur_player(self):
        return self.trueboard.get_player()

    def get_players_num(self):
        return 4

    def get_action_size(self):
        return 49

    def get_observation_size(self):
        return 198, 1

    def make_move(self, action):
        current_player = self.trueboard.get_player()
        game_status, next_player = self.trueboard.act(action)
        if game_status == "end" and self.trueboard.is_game_end():
            if self.trueboard.winning_team is None:
                raise Exception("Winning team cannot be None if game is ended")
            if self.trueboard.winning_team == current_player % 2:
                return 1, next_player
            else:
                return -1, next_player
        else:
            return 0.0, next_player

    def get_valid_moves(self, player=None):
        return self.trueboard.get_valid_moves_zeros()

    def is_ended(self):
        return self.trueboard.is_game_end()

    def is_draw(self):
        # in Watten a game can never end with a draw
        return False

    def get_score(self, player):
        if self.trueboard.winning_team is None:
            return 0.0

        if self.trueboard.is_game_end():
            if self.trueboard.winning_team == player % 2:
                return 1
            else:
                return -1

        raise Exception("Inconsistent score")

    def get_observation(self, player):
        if not 0 <= player < 4:
            print("WARNING: %d not in [0, 1, 3, 4]" % player)
        observation = self.trueboard.observe(player)
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
        cloned_game = BlindWattenGame()
        cloned_game.trueboard = self.trueboard.deepcopy()
        return cloned_game

    def reset_unknown_states(self, player):
        pass

    def get_number_of_tricks_played(self):
        return self.trueboard.score_team_0 + self.trueboard.score_team_1

    # c_v ranges from -1 to 1, while the trick played range from 0 to 4
    @staticmethod
    def decide_about_raising(continuous_value, tricks_played, lower_range=0.1, upper_range=0.8):
        # normalize continuous value in range 0 - 1
        norm_cv = (continuous_value+1) / 2

        # normalize tricks in range 0.2 - 1
        norm_tricks = 0.2 + 0.8*tricks_played/4

        probability = norm_tricks*norm_cv

        # normalize probability in range lower-range - upper-range
        norm_probability = lower_range + (upper_range-lower_range)*probability

        coin = np.random.choice(2, p=[1-norm_probability, norm_probability])

        return coin == 1

    # returns true if player should accept raise, false otherwise
    @staticmethod
    def decide_about_accepting_raise(continuous_value, tricks_played):
        return not BlindWattenGame.decide_about_raising(-continuous_value, tricks_played, 0.02, 0.6)
