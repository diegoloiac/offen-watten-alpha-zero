import argparse
import shutil
import time
import logging
from tqdm import tqdm
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import sys
import glob
import tensorflow as tf


from core.EnvironmentSelector import EnvironmentSelector
from core.utils.utils import serialize, deserialize, execute_command_sync


OPERATION_SUCCESSFUL = 0


def train(agent_profile, memory_path, cur_agent_path, new_agent_path, epochs=1):
    # call trainer script
    command = "python trainer.py"
    command += " --agent %s" % agent_profile
    command += " --memory_path %s" % memory_path
    command += " --out_agent_path %s" % new_agent_path
    command += " --epochs %s" % epochs
    if cur_agent_path is not None:
        command += " --agent_path %s" % cur_agent_path

    code = execute_command_sync(command)

    print("training finished, exit code: ", code)

    if code != OPERATION_SUCCESSFUL:
        throw_error("Could not perform agent training!")


def generate_self_play(agent_profile, agent_path, temp_dir, iteration_memory_path,
                       games_num, verbose, debug, max_steps, exploration_decay_steps, add_randomness):
    # call trainer script
    # use temp dir to save all temp models and fuse them into iteration memory path
    if temp_dir is not None:
        clean_dir(temp_dir)

    if os.path.isfile(iteration_memory_path):
        os.remove(iteration_memory_path)

    command = "python self_play_generator.py"
    command += " --agent %s" % agent_profile
    command += " --agent_path %s" % agent_path
    command += " --out_experience_path %s" % iteration_memory_path
    command += " --games_num %d" % games_num
    if max_steps:
        command += " --max_steps %d" % max_steps
    if exploration_decay_steps:
        command += " --exploration_decay_steps %d" % exploration_decay_steps
    if verbose:
        command += " --verbose"
    if debug:
        command += " --debug"
    if add_randomness:
        command += " --add_randomness"

    code = execute_command_sync(command)

    print("self-play generation finished, exit code: ", code)

    if code != OPERATION_SUCCESSFUL:
        throw_error("Could not perform self-play generation!")


def clean_dir(dir_path):
    if os.path.isdir(dir_path):
        files = glob.glob(dir_path + '/*')
        for f in files:
            os.remove(f)


def throw_error(message):
    print(message)
    sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--agent", dest="agent_profile",
                        help="Agent profile from EnvironmentSelector. Required.")
    parser.add_argument("--workspace", dest="workspace",
                        help="Workspace of the training session. Required.")

    parser.add_argument("--memory_path", dest="memory_path",
                        help="Path to the game experience.")
    parser.add_argument("--agent_path", dest="agent_path",
                        help="Path to the agent's model.")

    parser.add_argument("--iterations", dest="iterations", default=100, type=int,
                        help="Number of iterations of Alpha Zero")
    parser.add_argument("--epochs", dest="epochs", default=1, type=int,
                        help="Number of epochs for training neural network")

    parser.add_argument("--start_idx", dest="start_idx", default=0, type=int,
                        help="Index of iteration to start")

    parser.add_argument("--games_num", dest="games_num", default=100, type=int,
                        help="Number of games to play. ")

    parser.add_argument('--verbose', dest='verbose', action='store_true', help="Show games outcome")
    parser.set_defaults(verbose=False)

    parser.add_argument('--debug', dest='debug', action='store_true', help="Show games per turn")
    parser.set_defaults(debug=False)

    parser.add_argument('--add_randomness', dest='add_randomness', action='store_true', help="Add randomness in card choice")
    parser.set_defaults(add_randomness=False)

    parser.add_argument("--max_steps", dest="max_steps", type=int,
                        default=None,
                        help="Max steps in each game")

    parser.add_argument("--exploration_decay_steps", dest="exploration_decay_steps", type=int,
                        default=None,
                        help="Exploration decay in turns.")

    log = logging.getLogger("TrainLogger")
    start_time = time.time()

    options = parser.parse_args()

    if not options.agent_profile:
        parser.error('Agent profile must be selected')

    if not options.workspace:
        parser.error('Workspace path must be selected')

    # use CPU
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

    # define and create a workspace
    temp_dir = options.workspace + '/temp'
    temp_games_memory_dir = temp_dir + '/cluster_memory'

    self_play_temp_memory_path = temp_dir + '/self_play_memory.pkl'
    test_play_temp_memory_path = options.workspace + '/test_memory.pkl'

    os.makedirs(options.workspace, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(temp_games_memory_dir, exist_ok=True)

    # define primary agent model and primary memory model
    cur_agent_path = options.agent_path
    if not cur_agent_path:
        cur_agent_path = options.workspace + '/best'

    memory_folder = options.workspace + '/memory'
    os.makedirs(memory_folder, exist_ok=True)
    if options.memory_path is not None:
        print("Synchronize memory in the target directory...")
        shutil.copy(options.memory_path, memory_folder)

    # get Agent and Game instances by the profile
    env_selector = EnvironmentSelector()

    print("Agent profile %s" % options.agent_profile)
    agent = env_selector.get_agent(options.agent_profile)
    agent_profile = env_selector.get_profile(options.agent_profile)
    game = env_selector.get_game(agent_profile.game)

    # perform an initial training if agent's model was not specified
    if not options.agent_path:
        if options.memory_path:
            print("Agent model was not detected. Perform initial training...")
            train(options.agent_profile, memory_folder, None, cur_agent_path, epochs=options.epochs)
        else:
            agent.save(cur_agent_path)
    else:
        agent.load(cur_agent_path)

    # main Alpha Zero loop

    loop_range = range(options.start_idx, options.iterations)

    if options.verbose:
        loop_range = tqdm(loop_range)

    for idx in loop_range:

        path_to_self_play_agent = cur_agent_path

        self_play_memory = memory_folder + f'/memory_{idx}.tfrecord'

        generate_self_play(options.agent_profile, path_to_self_play_agent,
                           temp_games_memory_dir, self_play_memory,
                           options.games_num, options.verbose,
                           options.debug, options.max_steps, options.exploration_decay_steps, options.add_randomness)

        contestant_agent_path = temp_dir + '/temp_contestant.h5'

        train(options.agent_profile, memory_folder, cur_agent_path, contestant_agent_path, epochs=options.epochs)

        agent.load(contestant_agent_path)
        agent.save(cur_agent_path)
        agent.save(options.workspace + '/model_updated_%d' % idx)

    end_time = time.time()
    log.warning(f'Start time: {start_time}')
    log.warning(f'End time: {end_time}')
    log.warning(f'Elapsed time: {end_time-start_time}')


