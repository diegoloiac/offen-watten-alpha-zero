import argparse
from os import listdir
from os.path import isfile, join
import csv

from EnvironmentSelector import EnvironmentSelector
from core.World import World

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

    for model in model_files:
        model_path = str(options.folder) + "/" + model
        print(model_path)
        agent.load(model_path)

        sess_arena_examples, games_results = world.execute_games(agents, game, options.games_num)

        row = [model, options.games_num, games_results[0]]
        row_list.append(row)

    csv_path = options.folder + '/' + 'eval_results.csv'

    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_list)
