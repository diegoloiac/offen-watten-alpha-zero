import argparse
import os
import subprocess

from EnvironmentSelector import EnvironmentSelector
from alpha_zero_trainer import fuse_memory, train
from core.utils.utils import serialize, deserialize
from alpha_zero_trainer import generate_self_play
import tensorflow as tf


def execute_command_synch(command, show_output=True):
    print("execute command: ", command)

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)

    if show_output:
        for line in iter(process.stdout.readline, ""):
            print(line)

    process.stdout.close()
    process.wait()
    return process.returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--agent", dest="agent_profile",
                        help="Agent profile from EnvironmentSelector. Required.")

    parser.add_argument("--workspace", dest="workspace",
                        help="Workspace of the training session. Required.")

    parser.add_argument("--train_memory", dest="train_memory", default=-1,
                        help="N° of last self-play memories with which the model has to be trained at each iteration."
                             "-1 to use all, 0 to use only the just generated")

    parser.add_argument("--memory_dir", dest="memory_path",
                        help="Path to the game experience.")

    parser.add_argument("--agent_path", dest="agent_path",
                        help="Path to the agent's model.")

    parser.add_argument("--iterations", dest="iterations", default=100, type=int,
                        help="Number of iterations of Alpha Zero")

    parser.add_argument("--start_idx", dest="start_idx", default=0, type=int,
                        help="Index of iteration to start")

    parser.add_argument("--games_num", dest="games_num", default=100, type=int,
                        help="Number of games to play. ")

    parser.add_argument("--test_games_num", dest="test_games_num", type=int,
                        help="Number of games to play. ")

    parser.add_argument('--verbose', dest='verbose', action='store_true', help="Show games outcome")
    parser.set_defaults(verbose=False)

    parser.add_argument('--debug', dest='debug', action='store_true', help="Show games per turn")
    parser.set_defaults(debug=False)

    parser.add_argument("--max_steps", dest="max_steps", type=int,
                        default=None,
                        help="Max steps in each game")

    parser.add_argument("--epochs", dest="epochs", default=1, type=int,
                        help="Number of epochs for training neural network")

    parser.add_argument("--exploration_decay_steps", dest="exploration_decay_steps", type=int,
                        default=None,
                        help="Exploration decay in turns.")

    parser.add_argument("--hosts", dest="hosts",
                        default=None,
                        help="Hosts to run Alpha Zero. The folder of the repo must be shared between all of them")

    parser.add_argument('--train_distributed', dest='train_distributed', action='store_true',
                        help="Train NN in cluster specified by hosts option")
    parser.set_defaults(train_distributed=False)

    parser.add_argument('--train_distributed_native', dest='train_distributed_native', action='store_true',
                        help="Enable native distributed training on main machine")
    parser.set_defaults(train_distributed_native=False)


    options = parser.parse_args()

    loop_range = range(options.start_idx, options.iterations)

    # force agent to use CPU in the main script
    config = tf.compat.v1.ConfigProto(device_count={'CPU': 1, 'GPU': 0})
    session = tf.compat.v1.Session(config=config)
    tf.compat.v1.keras.backend.set_session(session)

    agent = options.agent_profile
    workspace = options.workspace
    memory_dir = workspace + "/memory"
    train_memory_file = workspace + "/memory.pkl"

    os.makedirs(options.workspace, exist_ok=True)
    os.makedirs(memory_dir, exist_ok=True)

    # define primary agent model and primary memory model
    cur_agent_path = options.agent_path
    if not cur_agent_path:
        cur_agent_path = options.workspace + '/best'

    env_selector = EnvironmentSelector()

    print("Agent profile %s" % options.agent_profile)
    agent = env_selector.get_agent(options.agent_profile)
    agent_profile = env_selector.get_profile(options.agent_profile)
    game = env_selector.get_game(agent_profile.game)

    if options.agent_path:
        agent.load(cur_agent_path)
    agent.save(cur_agent_path)

    memories = []

    if options.memory_path is not None:
        memories.append(options.memory_path)

    for i in loop_range:
        memory = memory_dir + '/%d.pkl' % i

        # generating self plays
        generate_self_play(options.agent_profile, cur_agent_path, None,
                           memory, options.games_num, options.verbose,
                           options.debug,
                           options.max_steps,
                           options.exploration_decay_steps)

        n_memory = int(options.train_memory)
        # fusing memory to be used in training
        if n_memory != 0:
            print('Deserializing memory from %s' % memory)
            des_mem = deserialize(memory)
            print(type(des_mem))
            # serialize(des_mem, train_memory_file)
            if n_memory == -1 or n_memory > len(memories):
                for file in memories:
                    print('Deserializing memory from %s' % file)
                    des_mem.extend(deserialize(file))
                    # fuse_memory(train_memory_file, file, train_memory_file)
            elif n_memory > 0:
                for file in memories[n_memory:]:
                    print('Deserializing memory from %s' % file)
                    des_mem.extend(deserialize(file))
                    # fuse_memory(train_memory_file, file, train_memory_file)
            serialize(des_mem, train_memory_file)
        else:
            train_memory_file = memory

        memories.append(memory)

        # train with selected memory
        new_agent_path = workspace + '/model_updated_%d.h5' % i

        train(options.agent_profile, train_memory_file, cur_agent_path, new_agent_path,
              train_distributed=options.train_distributed,
              train_distributed_native=options.train_distributed_native,
              epochs=options.epochs)

        cur_agent_path = new_agent_path

    agent.load(cur_agent_path)
    agent.save(workspace + '/best.h5')

