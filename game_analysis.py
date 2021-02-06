from core.agents.AgentNNet import AgentNNet
from versions.sub_watten.SubWattenGame import SubWattenGame
from nnets.DefaultFFNN import DefaultFFNN

if __name__ == "__main__":
    game = SubWattenGame()

    x, y = game.get_observation_size()

    nnet_sub = DefaultFFNN(x, y, 1, game.get_action_size())

    nnet_a_sub = DefaultFFNN(x, y, 1, game.get_action_size())

    agent_sub = AgentNNet(nnet_sub)
    agent_a_sub = AgentNNet(nnet_a_sub)

    agent_sub.load('versions/sub_watten/training/model_updated_599.h5')
    agent_a_sub.load('versions/asymmetric_sub_watten/training/model_updated_599.h5')

    game.trueboard.init_world_to_state(1, 0, [2, 9, 3, 21, 23], [0, 14, 22, 6, 30], [], 0, 0, 29, 28, 0, 0)

    game.trueboard.display()

    pi_sub, v_sub = agent_sub.predict(game, game.get_cur_player())

    pi_sub = pi_sub.numpy()*game.get_valid_moves(game.get_cur_player())
    print('SUB WATTEN')
    print(pi_sub)
    print(v_sub.numpy())

    game.trueboard.init_world_to_state(1, 0, [2, 9, 3, 21, 23], [0, 14, 22, 6, 30], [], 0, 0, 29, 28, 0, 0)

    game.trueboard.display()

    pi_a_sub, v_a_sub = agent_a_sub.predict(game, game.get_cur_player())

    pi_a_sub = pi_a_sub.numpy()*game.get_valid_moves(game.get_cur_player())
    print('ASYMMETRIC SUB WATTEN')
    print(pi_a_sub)
    print(v_a_sub.numpy())
