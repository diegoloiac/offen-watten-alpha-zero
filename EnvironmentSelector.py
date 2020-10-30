# from games.checkers.CheckersGame import CheckersGame
# from games.checkers.nnet.CheckersResNNet import CheckersResNNet
# from games.checkers.agent.AgentAlphaBeta import CheckersAgentAlphaBeta
# from games.checkers.agent.CheckersHumanAgent import CheckersHumanAgent

from games.tictactoe.TicTacToeGame import TicTacToeGame
from games.tictactoe.nnet.TicTacToeNNet import TicTacToeNNet
from games.tictactoe.agent.TicTacToeHumanAgent import TicTacToeHumanAgent

from games.durak.DurakGame import DurakGame
from games.durak.nnet.DurakNNet import DurakNNet
from games.durak.agent.DurakHumanAgent import DurakHumanAgent

from games.watten.WattenGame import WattenGame
from games.watten.agent.WattenHumanAgent import WattenHumanAgent
from games.watten.nnet.WattenNNet import WattenNNet
from games.watten.nnet.WattenNNet4x512 import WattenNNet4x512
from games.watten.nnet.WattenNNetFirstLayerBig import WattenNNetFirstLayerBig
# from games.watten.agent.DurakHumanAgent import DurakHumanAgent

from games.watten_sub_game.WattenSubGame import WattenSubGame
from games.watten_sub_game.nnet.SubWattenNNet import SubWattenNNet
from games.watten_sub_game.agent.SubWattenHumanAgent import SubWattenHumanAgent

from core.nnet.NNet import NNet

from core.agents.AgentNNet import AgentNNet
from core.agents.AgentMCTS import AgentMCTS
from core.agents.AgentRandom import AgentRandom

import os

import GPUtil


class EnvironmentSelector():
    # GAME_CHECKERS_DEFAULT = "checkers_environment_default"

    GAME_TICTACTOE_DEFAULT = "tictactoe_environment_default"

    GAME_DURAK_DEFAULT = "durak_environment_default"

    GAME_WATTEN_DEFAULT = "watten_environment_default"

    GAME_SUB_WATTEN_DEFAULT = "sub_watten_environment_default"

    class AgentProfile():
        def __init__(self, game, agent_profile):
            self.game = game
            self.agent_profile = agent_profile

    # agent profiles

    # CHECKERS_AGENT_ALPHA_BETA = AgentProfile(GAME_CHECKERS_DEFAULT,
    #                                          "checkers_agent_alpha_beta")
    # CHECKERS_AGENT_RANDOM = AgentProfile(GAME_CHECKERS_DEFAULT,
    #                                      "checkers_agent_random")
    # CHECKERS_AGENT_HUMAN = AgentProfile(GAME_CHECKERS_DEFAULT,
    #                                     "checkers_agent_human")
    #
    # CHECKERS_AGENT_TRAIN_RCNN_DEFAULT = AgentProfile(GAME_CHECKERS_DEFAULT,
    #                                                  "checkers_agent_train_rcnn_default")
    # CHECKERS_AGENT_TEST_AGENT_RCNN_DEFAULT = AgentProfile(GAME_CHECKERS_DEFAULT,
    #                                                       "checkers_agent_test_agent_rcnn_default")
    #
    # CHECKERS_AGENT_TRAIN_RCNN_TPU = AgentProfile(GAME_CHECKERS_DEFAULT,
    #                                              "checkers_agent_train_rcnn_tpu")
    #
    # CHECKERS_AGENT_TRAIN_RCNN_DISTRIBUTED = AgentProfile(GAME_CHECKERS_DEFAULT,
    #                                                      "checkers_agent_train_rcnn_distributed")
    # CHECKERS_AGENT_TEST_AGENT_RCNN_DISTRIBUTED = AgentProfile(GAME_CHECKERS_DEFAULT,
    #                                                           "checkers_agent_test_agent_rcnn_distributed")

    TICTACTOE_AGENT_TRAIN = AgentProfile(GAME_TICTACTOE_DEFAULT, "tictactoe_agent_train_default")
    TICTACTOE_AGENT_RANDOM = AgentProfile(GAME_TICTACTOE_DEFAULT, "tictactoe_agent_random")
    TICTACTOE_AGENT_HUMAN = AgentProfile(GAME_TICTACTOE_DEFAULT, "tictactoe_agent_human")

    DURAK_AGENT_TRAIN = AgentProfile(GAME_DURAK_DEFAULT, "durak_agent_train_default")
    DURAK_AGENT_RANDOM = AgentProfile(GAME_DURAK_DEFAULT, "durak_agent_random")
    DURAK_AGENT_HUMAN = AgentProfile(GAME_DURAK_DEFAULT, "durak_agent_human")

    WATTEN_AGENT_TRAIN = AgentProfile(GAME_WATTEN_DEFAULT, "watten_agent_train_default")
    WATTEN_AGENT_BIG_TRAIN = AgentProfile(GAME_WATTEN_DEFAULT, "watten_agent_train_big")
    WATTEN_AGENT_4_512_TRAIN = AgentProfile(GAME_WATTEN_DEFAULT, "watten_agent_train_4_512")

    WATTEN_AGENT_EVALUATE = AgentProfile(GAME_WATTEN_DEFAULT, "watten_agent_evaluate_default")
    WATTEN_AGENT_BIG_EVALUATE = AgentProfile(GAME_WATTEN_DEFAULT, "watten_agent_evaluate_big")
    WATTEN_AGENT_4_512_EVALUATE = AgentProfile(GAME_WATTEN_DEFAULT, "watten_agent_evaluate_4_512")

    WATTEN_AGENT_RANDOM = AgentProfile(GAME_WATTEN_DEFAULT, "watten_agent_random")
    WATTEN_AGENT_HUMAN = AgentProfile(GAME_WATTEN_DEFAULT, "watten_agent_human")
    WATTEN_AGENT_NNET = AgentProfile(GAME_WATTEN_DEFAULT, "watten_agent_nnet")

    SUB_WATTEN_AGENT_TRAIN = AgentProfile(GAME_SUB_WATTEN_DEFAULT, "sub_watten_agent_train_default")
    SUB_WATTEN_AGENT_RANDOM = AgentProfile(GAME_SUB_WATTEN_DEFAULT, "sub_watten_agent_random")
    SUB_WATTEN_AGENT_HUMAN = AgentProfile(GAME_SUB_WATTEN_DEFAULT, "sub_watten_agent_human")

    def __init__(self):
        super().__init__()

        self.game_mapping = {
            # EnvironmentSelector.GAME_CHECKERS_DEFAULT: CheckersGame(8, history_n=7),
            EnvironmentSelector.GAME_TICTACTOE_DEFAULT: TicTacToeGame(),
            EnvironmentSelector.GAME_DURAK_DEFAULT: DurakGame(),
            EnvironmentSelector.GAME_WATTEN_DEFAULT: WattenGame(),
            EnvironmentSelector.GAME_SUB_WATTEN_DEFAULT: WattenSubGame(),
        }

        self.agent_builder_mapping = {
            # EnvironmentSelector.CHECKERS_AGENT_ALPHA_BETA: self.build_basic_checkers_agent,
            # EnvironmentSelector.CHECKERS_AGENT_RANDOM: self.build_basic_checkers_agent,
            # EnvironmentSelector.CHECKERS_AGENT_HUMAN: self.build_basic_checkers_agent,
            #
            # EnvironmentSelector.CHECKERS_AGENT_TRAIN_RCNN_DEFAULT: self.build_native_checkers_rcnn_agent,
            # EnvironmentSelector.CHECKERS_AGENT_TEST_AGENT_RCNN_DEFAULT: self.build_native_checkers_rcnn_agent,
            #
            # EnvironmentSelector.CHECKERS_AGENT_TRAIN_RCNN_TPU: self.build_tpu_checkers_agent,
            #
            # EnvironmentSelector.CHECKERS_AGENT_TRAIN_RCNN_DISTRIBUTED: self.build_horovod_checkers_agent,
            # EnvironmentSelector.CHECKERS_AGENT_TEST_AGENT_RCNN_DISTRIBUTED: self.build_horovod_checkers_agent,

            EnvironmentSelector.TICTACTOE_AGENT_TRAIN: self.build_tictactoe_train_agent,
            EnvironmentSelector.TICTACTOE_AGENT_RANDOM: self.build_tictactoe_agent,
            EnvironmentSelector.TICTACTOE_AGENT_HUMAN: self.build_tictactoe_agent,

            EnvironmentSelector.DURAK_AGENT_TRAIN: self.build_durak_train_agent,
            EnvironmentSelector.DURAK_AGENT_RANDOM: self.build_durak_agent,
            EnvironmentSelector.DURAK_AGENT_HUMAN: self.build_durak_agent,

            EnvironmentSelector.WATTEN_AGENT_TRAIN: self.build_watten_train_agent,
            EnvironmentSelector.WATTEN_AGENT_BIG_TRAIN: self.build_watten_train_big_agent,
            EnvironmentSelector.WATTEN_AGENT_4_512_TRAIN: self.build_watten_train_4_512_agent,

            EnvironmentSelector.WATTEN_AGENT_EVALUATE: self.build_watten_train_agent,
            EnvironmentSelector.WATTEN_AGENT_BIG_EVALUATE: self.build_watten_train_big_agent,
            EnvironmentSelector.WATTEN_AGENT_4_512_EVALUATE: self.build_watten_train_4_512_agent,

            EnvironmentSelector.WATTEN_AGENT_RANDOM: self.build_watten_agent,
            EnvironmentSelector.WATTEN_AGENT_HUMAN: self.build_watten_agent,
            EnvironmentSelector.WATTEN_AGENT_NNET: self.build_watten_train_4_512_agent,

            EnvironmentSelector.SUB_WATTEN_AGENT_TRAIN: self.build_sub_watten_train_agent,
            EnvironmentSelector.SUB_WATTEN_AGENT_RANDOM: self.build_sub_watten_agent,
            EnvironmentSelector.SUB_WATTEN_AGENT_HUMAN: self.build_sub_watten_agent,
        }

        self.agent_profiles = [
            # EnvironmentSelector.CHECKERS_AGENT_ALPHA_BETA,
            # EnvironmentSelector.CHECKERS_AGENT_RANDOM,
            # EnvironmentSelector.CHECKERS_AGENT_HUMAN,
            #
            # EnvironmentSelector.CHECKERS_AGENT_TRAIN_RCNN_DEFAULT,
            # EnvironmentSelector.CHECKERS_AGENT_TEST_AGENT_RCNN_DEFAULT,
            #
            # EnvironmentSelector.CHECKERS_AGENT_TRAIN_RCNN_TPU,
            #
            # EnvironmentSelector.CHECKERS_AGENT_TRAIN_RCNN_DISTRIBUTED,
            # EnvironmentSelector.CHECKERS_AGENT_TEST_AGENT_RCNN_DISTRIBUTED,

            EnvironmentSelector.TICTACTOE_AGENT_TRAIN,
            EnvironmentSelector.TICTACTOE_AGENT_RANDOM,
            EnvironmentSelector.TICTACTOE_AGENT_HUMAN,

            EnvironmentSelector.DURAK_AGENT_TRAIN,
            EnvironmentSelector.DURAK_AGENT_RANDOM,
            EnvironmentSelector.DURAK_AGENT_HUMAN,

            EnvironmentSelector.WATTEN_AGENT_TRAIN,
            EnvironmentSelector.WATTEN_AGENT_BIG_TRAIN,
            EnvironmentSelector.WATTEN_AGENT_4_512_TRAIN,

            EnvironmentSelector.WATTEN_AGENT_EVALUATE,

            EnvironmentSelector.WATTEN_AGENT_BIG_EVALUATE,
            EnvironmentSelector.WATTEN_AGENT_4_512_EVALUATE,

            EnvironmentSelector.WATTEN_AGENT_RANDOM,
            EnvironmentSelector.WATTEN_AGENT_HUMAN,
            EnvironmentSelector.WATTEN_AGENT_NNET,

            EnvironmentSelector.SUB_WATTEN_AGENT_TRAIN,
            EnvironmentSelector.SUB_WATTEN_AGENT_RANDOM,
            EnvironmentSelector.SUB_WATTEN_AGENT_HUMAN,
        ]

    def get_profile(self, agent_profile_str):
        for profile in self.agent_profiles:
            if profile.agent_profile == agent_profile_str:
                return profile

        print("Error: could not find an agent profile by the key: ", agent_profile_str)

        return None

    def get_agent(self, agent_profile_str, native_multi_gpu_enabled=False):
        agent_profile = self.get_profile(agent_profile_str)
        if agent_profile in self.agent_builder_mapping:
            return self.agent_builder_mapping[agent_profile](agent_profile, native_multi_gpu_enabled=native_multi_gpu_enabled)

        print("Error: could not find an agent by the key: ", agent_profile_str)

        return None

    def get_game(self, game_profile):
        if game_profile in self.game_mapping:
            return self.game_mapping[game_profile]

        print("Error: could not find a game with profile: ", game_profile)

        return None

    # def build_basic_checkers_agent(self, agent_profile, native_multi_gpu_enabled=False):
    #     game = self.game_mapping[agent_profile.game]
    #
    #     if agent_profile == EnvironmentSelector.CHECKERS_AGENT_ALPHA_BETA:
    #         return CheckersAgentAlphaBeta()
    #     elif agent_profile == EnvironmentSelector.CHECKERS_AGENT_RANDOM:
    #         return AgentRandom()
    #     elif agent_profile == EnvironmentSelector.CHECKERS_AGENT_HUMAN:
    #         return CheckersHumanAgent(game)
    #     return None

    # def build_native_checkers_rcnn_agent(self, agent_profile, native_multi_gpu_enabled=False):
    #     game = self.game_mapping[agent_profile.game]
    #
    #     if not native_multi_gpu_enabled:
    #         nnet = CheckersResNNet(game.get_observation_size()[0], game.get_observation_size()[1],
    #                                game.get_observation_size()[2], game.get_action_size())
    #     else:
    #         nnet = CheckersResNNet(game.get_observation_size()[0], game.get_observation_size()[1],
    #                                game.get_observation_size()[2], game.get_action_size(),
    #                                multi_gpu=True, multi_gpu_n=len(GPUtil.getGPUs()))
    #
    #     agent_nnet = AgentNNet(nnet)
    #
    #     if agent_profile == EnvironmentSelector.CHECKERS_AGENT_TRAIN_RCNN_DEFAULT:
    #         return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_INIT, numMCTSSims=1500,
    #                          max_predict_time=3, num_threads=1)
    #     elif agent_profile == EnvironmentSelector.CHECKERS_AGENT_TEST_AGENT_RCNN_DEFAULT:
    #         return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.NO_EXPLORATION, numMCTSSims=1500,
    #                          max_predict_time=10, num_threads=2, verbose=True)
    #     else:
    #         return None

    # def build_tpu_checkers_agent(self, agent_profile, native_multi_gpu_enabled=False):
    #     from games.checkers.nnet.CheckersResNNetTPU import CheckersResNNetTPU
    #
    #     assert not native_multi_gpu_enabled, "ERROR: TPU NNet does not support native multi-gpu mode!"
    #
    #     game = self.game_mapping[agent_profile.game]
    #
    #     nnet = CheckersResNNetTPU(game.get_observation_size()[0], game.get_observation_size()[1],
    #                               game.get_observation_size()[2], game.get_action_size())
    #
    #     agent_nnet = AgentNNet(nnet)
    #
    #     if agent_profile == EnvironmentSelector.CHECKERS_AGENT_TRAIN_RCNN_TPU:
    #         return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_INIT, numMCTSSims=200,
    #                          max_predict_time=None, verbose=False, num_threads=1)
    #     else:
    #         return None

    # def build_horovod_checkers_agent(self, agent_profile, native_multi_gpu_enabled=False):
    #     from games.checkers.nnet.CheckersResNNetDistributed import CheckersResNNetDistributed
    #
    #     assert not native_multi_gpu_enabled, "ERROR: Horovod NNet does not support native multi-gpu mode!"
    #
    #     game = self.game_mapping[agent_profile.game]
    #
    #     nnet = CheckersResNNetDistributed(game.get_observation_size()[0], game.get_observation_size()[1],
    #                                       game.get_observation_size()[2], game.get_action_size(),
    #                                       horovod_distributed=True)
    #
    #     agent_nnet = AgentNNet(nnet)
    #
    #     if agent_profile == EnvironmentSelector.CHECKERS_AGENT_TRAIN_RCNN_DISTRIBUTED:
    #         return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_INIT, numMCTSSims=1500,
    #                          max_predict_time=5)
    #     elif agent_profile == EnvironmentSelector.CHECKERS_AGENT_TEST_AGENT_RCNN_DISTRIBUTED:
    #         return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.NO_EXPLORATION, numMCTSSims=1500,
    #                          max_predict_time=10)
    #     else:
    #         return None

    def build_tictactoe_train_agent(self, agent_profile, native_multi_gpu_enabled=False):

        game = self.game_mapping[agent_profile.game]

        nnet = TicTacToeNNet(game.get_observation_size()[0], game.get_observation_size()[1],
                             game.get_observation_size()[2], game.get_action_size())

        agent_nnet = AgentNNet(nnet)

        if agent_profile == EnvironmentSelector.TICTACTOE_AGENT_TRAIN:
            return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=100,
                             max_predict_time=10)
        return None

    def build_tictactoe_agent(self, agent_profile, native_multi_gpu_enabled=False):

        game = self.game_mapping[agent_profile.game]

        if agent_profile == EnvironmentSelector.TICTACTOE_AGENT_RANDOM:
            return AgentRandom()
        elif agent_profile == EnvironmentSelector.TICTACTOE_AGENT_HUMAN:
            return TicTacToeHumanAgent(game=game)
        return None

    def build_durak_train_agent(self, agent_profile, native_multi_gpu_enabled=False):

        game = self.game_mapping[agent_profile.game]

        x, y = game.get_observation_size()
        nnet = DurakNNet(x, y, 1, game.get_action_size())

        agent_nnet = AgentNNet(nnet)

        if agent_profile == EnvironmentSelector.DURAK_AGENT_TRAIN:
            return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=100,
                             max_predict_time=10)
        return None

    ############################################################
    #  NN 1
    ############################################################

    def build_watten_train_agent(self, agent_profile, native_multi_gpu_enabled=False):

        game = self.game_mapping[agent_profile.game]

        x, y = game.get_observation_size()
        nnet = WattenNNet(x, y, 1, game.get_action_size())

        agent_nnet = AgentNNet(nnet)

        if agent_profile == EnvironmentSelector.WATTEN_AGENT_TRAIN:
            print("Configuring build_watten_train_agent...")
            return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=100,
                             max_predict_time=10, num_threads=1)
        elif agent_profile == EnvironmentSelector.WATTEN_AGENT_EVALUATE:
            print("Configuring build_watten_evaluate_agent...")
            return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=2,
                             max_predict_time=10, num_threads=16, name="build_watten_evaluate_agent")
        elif agent_profile == EnvironmentSelector.WATTEN_AGENT_HUMAN:
            return WattenHumanAgent(game)

        return None

    ############################################################
    #  NN 2
    ############################################################

    def build_watten_train_big_agent(self, agent_profile, native_multi_gpu_enabled=False):

        game = self.game_mapping[agent_profile.game]

        x, y = game.get_observation_size()
        nnet = WattenNNetFirstLayerBig(x, y, 1, game.get_action_size())

        agent_nnet = AgentNNet(nnet)

        if agent_profile == EnvironmentSelector.WATTEN_AGENT_BIG_TRAIN:
            print("Configuring build_watten_train_big_agent...")
            return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=100,
                             max_predict_time=10, num_threads=16)
        elif agent_profile == EnvironmentSelector.WATTEN_AGENT_BIG_EVALUATE:
            print("Configuring build_watten_evaluate_big_agent...")
            return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=2,
                             max_predict_time=10, num_threads=16, name="build_watten_evaluate_big_agent")
        elif agent_profile == EnvironmentSelector.WATTEN_AGENT_HUMAN:
            return WattenHumanAgent(game)

        return None

    ############################################################
    #  NN 3
    ############################################################

    def build_watten_train_4_512_agent(self, agent_profile, native_multi_gpu_enabled=False):

        game = self.game_mapping[agent_profile.game]

        x, y = game.get_observation_size()
        nnet = WattenNNet4x512(x, y, 1, game.get_action_size())

        agent_nnet = AgentNNet(nnet)

        if agent_profile == EnvironmentSelector.WATTEN_AGENT_4_512_TRAIN:
            print("Configuring build_watten_train_4_512_agent...")
            return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=100,
                             max_predict_time=10, num_threads=16)
        elif agent_profile == EnvironmentSelector.WATTEN_AGENT_4_512_EVALUATE:
            print("Configuring build_watten_evaluate_4_512_agent...")
            return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=30,
                             max_predict_time=10, num_threads=16, name="build_watten_evaluate_4_512_agent")
        elif agent_profile == EnvironmentSelector.WATTEN_AGENT_HUMAN:
            return WattenHumanAgent(game)
        elif agent_profile == EnvironmentSelector.WATTEN_AGENT_NNET:
            agent_nnet.load(os.path.abspath("../games/watten/training/best-4-512-new-4.h5"))
            return agent_nnet

        return None

    def build_durak_agent(self, agent_profile, native_multi_gpu_enabled=False):

        game = self.game_mapping[agent_profile.game]

        if agent_profile == EnvironmentSelector.DURAK_AGENT_RANDOM:
            return AgentRandom()
        elif agent_profile == EnvironmentSelector.DURAK_AGENT_HUMAN:
            return DurakHumanAgent(game=game)
        return None

    def build_watten_agent(self, agent_profile, native_multi_gpu_enabled=False):

        game = self.game_mapping[agent_profile.game]

        if agent_profile == EnvironmentSelector.WATTEN_AGENT_RANDOM:
            return AgentRandom()
        elif agent_profile == EnvironmentSelector.WATTEN_AGENT_HUMAN:
            return WattenHumanAgent(game)

        return None

    def build_sub_watten_train_agent(self, agent_profile, native_multi_gpu_enabled=False):

        game = self.game_mapping[agent_profile.game]

        x, y = game.get_observation_size()
        nnet = SubWattenNNet(x, y, 1, game.get_action_size())

        agent_nnet = AgentNNet(nnet)

        if agent_profile == EnvironmentSelector.SUB_WATTEN_AGENT_TRAIN:
            print("Configuring build_sub_watten_train_agent...")
            return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=100,
                             max_predict_time=10, num_threads=1)

        return None

    def build_sub_watten_agent(self, agent_profile, native_multi_gpu_enabled=False):

        game = self.game_mapping[agent_profile.game]

        if agent_profile == EnvironmentSelector.SUB_WATTEN_AGENT_RANDOM:
            return AgentRandom()
        elif agent_profile == EnvironmentSelector.SUB_WATTEN_AGENT_HUMAN:
            return SubWattenHumanAgent(game)

        return None
