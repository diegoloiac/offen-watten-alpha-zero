import argparse
import os

import numpy as np
import tensorflow as tf
from tqdm import tqdm

from pkl_tfrec_converter import serialize_example
from versions.hand_watten.HandWattenGame import HandWattenGame


class WattenExplorer:

    def __init__(self):
        self.states = {}
        self.training_data = []

    def explore_games(self, game, path, num_games_per_iteration, iterations):

        iterations = range(iterations)
        iterations = tqdm(iterations)

        for i in iterations:
            games = range(num_games_per_iteration)
            games = tqdm(games)
            for _ in games:
                game.reset()
                self.explore_state(game, game.get_cur_player())

            n_examples = 0
            with tf.io.TFRecordWriter(f"{path}_{i}.tfrecord") as writer:
                for example_tuple in self.training_data:
                    n_examples += 1
                    writer.write(serialize_example(np.asarray(example_tuple[0], dtype=np.float64).tobytes(),
                                                   np.asarray(example_tuple[1], dtype=np.float64).tobytes(),
                                                   example_tuple[2]))

            print(f'Written {n_examples} examples to file {path}_{i}.tfrecord')

            self.states = {}
            self.training_data = []

    def explore_state(self, game, game_player):
        # The exploration is over when the game is ended
        if game.is_ended():
            return (game.get_score(game_player) + 1) / 2, 1

        complete_observation = game.get_complete_observation()
        observation = game.get_observation(game_player)
        # The exploration is over if the state has already been visited
        if complete_observation in self.states:
            return self.states[complete_observation]
        # The exploration can continue
        else:
            probabilities = np.zeros(50)
            total_expanded = 0
            total_won = 0

            valid_moves = game.get_valid_moves()
            # Masking invalid moves
            valid_moves = np.array(valid_moves)
            valid_moves[46:] = 0

            for idx, action in enumerate(valid_moves):
                if action == 1:
                    game_clone = game.clone()
                    _, next_player = game_clone.make_move(idx)

                    won, expanded = self.explore_state(game_clone, next_player)

                    if next_player != game_player:
                        won = expanded - won
                    probabilities[idx] = won / expanded

                    total_won += won
                    total_expanded += expanded

            self.states[complete_observation] = total_won, total_expanded

            self.training_data.append((observation, probabilities, (total_won/total_expanded*2) - 1))

            return total_won, total_expanded


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--workspace", dest="workspace",
                        help="Workspace of the training session. Required.")

    parser.add_argument("--iterations", dest="iterations",
                        help="Number of iterations of explorations. Required")

    parser.add_argument("--games_num", dest="games_num",
                        help="Number of games to keep in memory per iteration. Required")

    options = parser.parse_args()

    if not options.workspace:
        parser.error('Workspace path must be selected')
    if not options.iterations:
        parser.error('Number of iterations must be selected')
    if not options.games_num:
        parser.error('Number of games per iteration must be selected')

    os.makedirs(options.workspace, exist_ok=True)

    w_game = HandWattenGame()

    explorer = WattenExplorer()

    explorer.explore_games(w_game, options.workspace, int(options.games_num), iterations=int(options.iterations))


