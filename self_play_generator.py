import argparse
from collections import deque
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

from core.EnvironmentSelector import EnvironmentSelector
from core.utils.utils import serialize
from core.World import World
from pkl_tfrec_converter import serialize_example


def generate_self_play(opt_agent_profile, agent_path, games_num,
                       experience_path, max_steps,
                       verbose, debug, exploration_decay_steps, self_play_examples_deque=deque([]), add_randomness=False):

    # use CPU
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

    world = World(add_randomness=add_randomness)

    env_selector = EnvironmentSelector()

    agent = env_selector.get_agent(opt_agent_profile)

    agent.load(agent_path)

    agent_profile = env_selector.get_profile(opt_agent_profile)
    game = env_selector.get_game(agent_profile.game)

    self_play_examples = world.generate_self_play(agent, game, games_num,
                                                  max_game_steps_n=max_steps,
                                                  verbose=verbose,
                                                  show_every_turn=debug,
                                                  exploration_decay_steps=exploration_decay_steps)

    # Write self_play_examples as tfrecord
    self_play_examples_deque += self_play_examples
    n_examples = 0
    with tf.io.TFRecordWriter(experience_path) as writer:
        for example_tuple in self_play_examples_deque:
            n_examples += 1
            writer.write(serialize_example(np.asarray(example_tuple[0], dtype=np.float64).tobytes(),
                                           np.asarray(example_tuple[1], dtype=np.float64).tobytes(), example_tuple[2]))

    print(f'Written {n_examples} examples to file {experience_path}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--agent", dest="agent_profile",
                        help="Agent profile from EnvironmentSelector. Required.")
    parser.add_argument("--agent_path", dest="agent_path",
                        help="Path to the agent's model. Required.")
    parser.add_argument("--out_experience_path", dest="experience_path",
                        help="Path to the generated experience. Required.")
    parser.add_argument("--games_num", dest="games_num", type=int,
                        help="Number of games to play. Required.")

    parser.add_argument('--verbose', dest='verbose', action='store_true', help="Show games outcome")
    parser.set_defaults(verbose=True)

    parser.add_argument('--debug', dest='debug', action='store_true', help="Show games per turn")
    parser.set_defaults(verbose=False)

    parser.add_argument('--add_randomness', dest='add_randomness', action='store_true', help="Add randomness in card choice")
    parser.set_defaults(add_randomness=False)

    parser.add_argument("--max_steps", dest="max_steps", type=int,
                        default=None,
                        help="Max steps in each game")

    parser.add_argument("--exploration_decay_steps", dest="exploration_decay_steps", type=int,
                        default=None,
                        help="Exploration decay in turns.")

    parser.add_argument("--temp_path", dest="temp_path",
                        help="Path to the generated experience. Required.")

    options = parser.parse_args()

    if not options.agent_profile:
        parser.error('Agent profile must be selected')

    if not options.agent_path:
        parser.error('Agent path must be selected')

    if not options.experience_path:
        parser.error('Out experience path must be selected')

    if not options.games_num:
        parser.error('Number of games must be selected')

    generate_self_play(options.agent_profile, options.agent_path, options.games_num,
                       options.experience_path, options.max_steps,
                       options.verbose, options.debug, options.exploration_decay_steps, add_randomness=options.add_randomness)
