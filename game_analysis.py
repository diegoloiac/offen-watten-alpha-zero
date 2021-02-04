from core.agents.AgentNNet import AgentNNet
from versions.sub_watten.SubWattenGame import SubWattenGame
from nnets.DefaultFFNN import DefaultFFNN

if __name__ == "__main__":
    game = SubWattenGame()

    x, y = game.get_observation_size()

    nnet = DefaultFFNN(x, y, 1, game.get_action_size())

    agent = AgentNNet(nnet)

    agent.load('versions/sub_watten/training/best.h5')

    game.trueboard.init_world_to_state(1, 1, [2, 8, 11, 21, 23], [0, 14, 22, 6, 30], [], 0, 0, 29, 28, 1, None)

    game.trueboard.display()

    pi, v = agent.predict(game, game.get_cur_player())

    print(pi)

    print(v)
