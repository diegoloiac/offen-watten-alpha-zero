from core.agents.AgentNNet import AgentNNet
from versions.hand_watten.HandWattenGame import HandWattenGame
from nnets.DefaultFFNN import DefaultFFNN
from nnets.CNN import CNN

if __name__ == "__main__":
    game = HandWattenGame()

    x, y = game.get_observation_size()

    nnet = DefaultFFNN(x, y, 1, game.get_action_size())

    agent = AgentNNet(nnet)

    agent.load('versions/hand_watten/training/ffnn/raise/model_updated_199.h5')

    game.trueboard.init_world_to_state(1, -1, [0, 8, 16, 12, 27], [3, 14, 22, 6, 30], [], 0, 0, 2, False, False, None, 1, 23, 0, 0, None)


    game.trueboard.display()

    pi_sub, v_sub = agent.predict(game, game.get_cur_player())

    pi_sub = pi_sub.numpy()*game.get_valid_moves(game.get_cur_player())
    print('SUB WATTEN')
    print(pi_sub)
    print(v_sub.numpy())

