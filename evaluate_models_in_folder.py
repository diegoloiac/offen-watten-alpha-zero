import argparse
from os import listdir
from os.path import isfile, join
import csv

from EnvironmentSelector import EnvironmentSelector
from core.World import World


# Print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--folder", dest="folder",
                        help="Folder where the models at each iteration are saved. Required.")

    parser.add_argument("--agent", dest="agent",
                        help="Agent to evaluate. Required.")

    parser.add_argument("--random_agent", dest="random_agent",
                        help="Random agent to play with. Required.")

    parser.add_argument("--games_num", dest="games_num", default=100, type=int,
                        help="Number of games to play. ")

    options = parser.parse_args()

    if not options.folder:
        parser.error('Folder must be selected')

    if not options.agent:
        parser.error('Agent profile must be selected')

    if not options.random_agent:
        parser.error('Random agent profile must be selected')

    env_selector = EnvironmentSelector()
    agent = env_selector.get_agent(options.agent)
    print("Pit with agent ", agent.name)
    agent.set_exploration_enabled(False)

    random_agent = env_selector.get_agent(options.random_agent)
    print("Pit with agent ", random_agent.name)
    random_agent.set_exploration_enabled(False)

    agent_profile = env_selector.get_profile(options.agent)
    game = env_selector.get_game(agent_profile.game)

    world = World()

    agents = [agent, random_agent]

    model_files = [f for f in listdir(options.folder) if isfile(join(options.folder, f)) and f.endswith('h5')]

    row_list = []

    print_progress_bar(0, len(model_files), prefix='Progress:', suffix='Complete')
    for idx, model in enumerate(model_files):
        model_path = str(options.folder) + "/" + model
        print(model_path)
        agent.load(model_path)

        result = 0
        games_won = 0

        for i in range(options.games_num):
            _, game_result = world.execute_game(agents, game)
            result += game_result[0]
            if game_result[0] > 0:
                games_won += 1

        row = [model, options.games_num, result, games_won]
        row_list.append(row)

        print_progress_bar(idx + 1, len(model_files), prefix='Progress:', suffix='Complete')

    csv_path = options.folder + '/' + 'eval_results.csv'

    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_list)
