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

from games.sub_watten.SubWattenGame import WattenSubGame
from games.sub_watten.nnet.SubWattenNNet import SubWattenNNet
from games.sub_watten.nnet.SubWattenSimplerNNet import SubWattenSimplerNNet
from games.sub_watten.agent.SubWattenBaggingModel import SubWattenBaggingModel
from games.sub_watten.agent.SubWattenHumanAgent import SubWattenHumanAgent

from games.asymmetric_sub_watten.AsymmetricSubWattenGame import AsymmetricSubWattenGame
from games.asymmetric_sub_watten.nnet.AsymmetricSubWattenNNet import AsymmetricSubWattenNNet

from games.total_watten.TotalWattenGame import TotalWattenGame
from games.total_watten.nnet.TotalWattenNNet import TotalWattenNNet
from games.total_watten.agent.TotalWattenHumanAgent import TotalWattenHumanAgent

from games.hand_watten.HandWattenGame import HandWattenGame
from games.hand_watten.nnet.HandWattenNNet import HandWattenNNet
from games.hand_watten.nnet.EasyEasyNNet import EasyEasyNNet
from games.hand_watten.nnet.MediumMediumNNet import MediumMediumNNet
from games.hand_watten.nnet.CNNWatten import CNNWatten
from games.hand_watten.agent.HandWattenHumanAgent import HandWattenHumanAgent

from core.agents.AgentNNet import AgentNNet
from core.agents.AgentMCTS import AgentMCTS
from core.agents.AgentRandom import AgentRandom

import os


class EnvironmentSelector():
    # GAME_CHECKERS_DEFAULT = "checkers_environment_default"

    GAME_TICTACTOE_DEFAULT = "tictactoe_environment_default"

    GAME_DURAK_DEFAULT = "durak_environment_default"

    GAME_WATTEN_DEFAULT = "watten_environment_default"

    GAME_SUB_WATTEN_DEFAULT = "sub_watten_environment_default"

    GAME_ASYMMETRIC_SUB_WATTEN_DEFAULT = "asymmetric_sub_watten_environment_default"

    GAME_ASYMMETRIC_SUB_WATTEN_EVALUATE = "asymmetric_sub_watten_environment_evaluate"

    GAME_TOTAL_WATTEN_DEFAULT = "total_watten_environment_default"

    GAME_TOTAL_WATTEN_H_VS_H = "total_watten_environment_h_vs_h"

    GAME_TOTAL_WATTEN_H_VS_NH = "total_watten_environment_h_vs_nh"

    GAME_TOTAL_WATTEN_NH_VS_H = "total_watten_environment_nh_vs_h"

    GAME_HAND_WATTEN = "hand_watten_environment_default"

    GAME_HAND_WATTEN_CNN = "hand_watten_environment_cnn"

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
    SUB_WATTEN_AGENT_TRAIN_SIMPLE = AgentProfile(GAME_SUB_WATTEN_DEFAULT, "sub_watten_agent_train_simple")
    SUB_WATTEN_AGENT_EVALUATE = AgentProfile(GAME_SUB_WATTEN_DEFAULT, "sub_watten_agent_evaluate")
    SUB_WATTEN_AGENT_EVALUATE_SIMPLE = AgentProfile(GAME_SUB_WATTEN_DEFAULT, "sub_watten_agent_evaluate_simple")
    SUB_WATTEN_AGENT_BAGGING = AgentProfile(GAME_SUB_WATTEN_DEFAULT, "sub_watten_agent_bagging")
    SUB_WATTEN_AGENT_RANDOM = AgentProfile(GAME_SUB_WATTEN_DEFAULT, "sub_watten_agent_random")
    SUB_WATTEN_AGENT_HUMAN = AgentProfile(GAME_SUB_WATTEN_DEFAULT, "sub_watten_agent_human")

    ASYMMETRIC_SUB_WATTEN_AGENT_TRAIN = AgentProfile(GAME_ASYMMETRIC_SUB_WATTEN_DEFAULT,
                                                     "asymmetric_sub_watten_agent_train_default")
    ASYMMETRIC_SUB_WATTEN_AGENT_EVALUATE = AgentProfile(GAME_ASYMMETRIC_SUB_WATTEN_EVALUATE,
                                                        "asymmetric_sub_watten_agent_evaluate")
    ASYMMETRIC_SUB_WATTEN_AGENT_RANDOM = AgentProfile(GAME_ASYMMETRIC_SUB_WATTEN_EVALUATE,
                                                      "asymmetric_sub_watten_agent_random")

    TOTAL_WATTEN_AGENT_TRAIN = AgentProfile(GAME_TOTAL_WATTEN_DEFAULT, "total_watten_agent_train_default")
    TOTAL_WATTEN_AGENT_EVALUATE = AgentProfile(GAME_TOTAL_WATTEN_DEFAULT, "total_watten_agent_evaluate")
    TOTAL_WATTEN_AGENT_RANDOM = AgentProfile(GAME_TOTAL_WATTEN_DEFAULT, "total_watten_agent_random")
    TOTAL_WATTEN_AGENT_HUMAN = AgentProfile(GAME_TOTAL_WATTEN_DEFAULT, "total_watten_agent_human")

    HAND_WATTEN_RANDOM = AgentProfile(GAME_HAND_WATTEN, "hand_watten_random")
    HAND_WATTEN_HUMAN = AgentProfile(GAME_HAND_WATTEN, "hand_watten_human")

    HAND_WATTEN_TRAIN = AgentProfile(GAME_HAND_WATTEN, "hand_watten_train_default")
    HAND_WATTEN_EVALUATE = AgentProfile(GAME_HAND_WATTEN, "hand_watten_evaluate")

    HAND_WATTEN_TRAIN_S_S = AgentProfile(GAME_HAND_WATTEN, "hand_watten_train_s_s")
    HAND_WATTEN_EVALUATE_S_S = AgentProfile(GAME_HAND_WATTEN, "hand_watten_evaluate_s_s")

    HAND_WATTEN_TRAIN_M_M = AgentProfile(GAME_HAND_WATTEN, "hand_watten_train_m_m")
    HAND_WATTEN_EVALUATE_M_M = AgentProfile(GAME_HAND_WATTEN, "hand_watten_evaluate_m_m")

    HAND_WATTEN_TRAIN_CNN = AgentProfile(GAME_HAND_WATTEN_CNN, "hand_watten_train_cnn")
    HAND_WATTEN_EVALUATE_CNN = AgentProfile(GAME_HAND_WATTEN_CNN, "hand_watten_evaluate_cnn")

    def __init__(self):
        super().__init__()

        self.game_mapping = {
            # EnvironmentSelector.GAME_CHECKERS_DEFAULT: CheckersGame(8, history_n=7),
            EnvironmentSelector.GAME_TICTACTOE_DEFAULT: TicTacToeGame(),
            EnvironmentSelector.GAME_DURAK_DEFAULT: DurakGame(),
            EnvironmentSelector.GAME_WATTEN_DEFAULT: WattenGame(),
            EnvironmentSelector.GAME_SUB_WATTEN_DEFAULT: WattenSubGame(),
            EnvironmentSelector.GAME_ASYMMETRIC_SUB_WATTEN_DEFAULT: AsymmetricSubWattenGame(),
            EnvironmentSelector.GAME_ASYMMETRIC_SUB_WATTEN_EVALUATE: WattenSubGame(),
          #  EnvironmentSelector.GAME_TOTAL_WATTEN_DEFAULT: TotalWattenGame(
          #      self.sub_watten_non_human_agent_for_total_watten(),
          #      self.sub_watten_non_human_agent_for_total_watten()
          #  ),
          #  EnvironmentSelector.GAME_TOTAL_WATTEN_H_VS_H: TotalWattenGame(
          #      self.sub_watten_human_agent_for_total_watten(),
          #      self.sub_watten_human_agent_for_total_watten()
          #  ),
          #  EnvironmentSelector.GAME_TOTAL_WATTEN_H_VS_NH: TotalWattenGame(
          #      self.sub_watten_human_agent_for_total_watten(),
          #      self.sub_watten_non_human_agent_for_total_watten()
          #  ),
          #  EnvironmentSelector.GAME_TOTAL_WATTEN_NH_VS_H: TotalWattenGame(
          #      self.sub_watten_non_human_agent_for_total_watten(),
          #      self.sub_watten_human_agent_for_total_watten()
          #  ),
            EnvironmentSelector.GAME_HAND_WATTEN: HandWattenGame(),
            EnvironmentSelector.GAME_HAND_WATTEN_CNN: HandWattenGame(cnn=True)
        }

        self.agent_builder_mapping = {

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
            EnvironmentSelector.SUB_WATTEN_AGENT_TRAIN_SIMPLE: self.build_sub_watten_train_agent,
            EnvironmentSelector.SUB_WATTEN_AGENT_EVALUATE: self.build_sub_watten_evaluate_agent,
            EnvironmentSelector.SUB_WATTEN_AGENT_EVALUATE_SIMPLE: self.build_sub_watten_evaluate_agent,
            EnvironmentSelector.SUB_WATTEN_AGENT_BAGGING: self.build_sub_watten_agent,
            EnvironmentSelector.SUB_WATTEN_AGENT_RANDOM: self.build_sub_watten_agent,
            EnvironmentSelector.SUB_WATTEN_AGENT_HUMAN: self.build_sub_watten_agent,

            EnvironmentSelector.ASYMMETRIC_SUB_WATTEN_AGENT_TRAIN: self.build_asymmetric_sub_watten_train_agent,
            EnvironmentSelector.ASYMMETRIC_SUB_WATTEN_AGENT_EVALUATE: self.build_asymmetric_sub_watten_evaluate_agent,
            EnvironmentSelector.ASYMMETRIC_SUB_WATTEN_AGENT_RANDOM: self.build_asymmetric_sub_watten_agent,

            EnvironmentSelector.TOTAL_WATTEN_AGENT_TRAIN: self.build_total_watten_train_agent,
            EnvironmentSelector.TOTAL_WATTEN_AGENT_EVALUATE: self.build_total_watten_evaluate_agent,
            EnvironmentSelector.TOTAL_WATTEN_AGENT_RANDOM: self.build_total_watten_agent,
            EnvironmentSelector.TOTAL_WATTEN_AGENT_HUMAN: self.build_total_watten_agent,

            EnvironmentSelector.HAND_WATTEN_TRAIN: self.build_hand_watten_train_agent,
            EnvironmentSelector.HAND_WATTEN_TRAIN_S_S: self.build_hand_watten_train_agent,
            EnvironmentSelector.HAND_WATTEN_TRAIN_M_M: self.build_hand_watten_train_agent,
            EnvironmentSelector.HAND_WATTEN_TRAIN_CNN: self.build_hand_watten_train_agent,
            EnvironmentSelector.HAND_WATTEN_EVALUATE: self.build_hand_watten_evaluate_agent,
            EnvironmentSelector.HAND_WATTEN_EVALUATE_S_S: self.build_hand_watten_evaluate_agent,
            EnvironmentSelector.HAND_WATTEN_EVALUATE_M_M: self.build_hand_watten_evaluate_agent,
            EnvironmentSelector.HAND_WATTEN_EVALUATE_CNN: self.build_hand_watten_evaluate_agent,
            EnvironmentSelector.HAND_WATTEN_RANDOM: self.build_hand_watten_agent,
            EnvironmentSelector.HAND_WATTEN_HUMAN: self.build_hand_watten_agent,
        }

        self.agent_profiles = [
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
            EnvironmentSelector.SUB_WATTEN_AGENT_TRAIN_SIMPLE,
            EnvironmentSelector.SUB_WATTEN_AGENT_EVALUATE,
            EnvironmentSelector.SUB_WATTEN_AGENT_EVALUATE_SIMPLE,
            EnvironmentSelector.SUB_WATTEN_AGENT_BAGGING,
            EnvironmentSelector.SUB_WATTEN_AGENT_RANDOM,
            EnvironmentSelector.SUB_WATTEN_AGENT_HUMAN,

            EnvironmentSelector.ASYMMETRIC_SUB_WATTEN_AGENT_TRAIN,
            EnvironmentSelector.ASYMMETRIC_SUB_WATTEN_AGENT_EVALUATE,
            EnvironmentSelector.ASYMMETRIC_SUB_WATTEN_AGENT_RANDOM,

            EnvironmentSelector.TOTAL_WATTEN_AGENT_TRAIN,
            EnvironmentSelector.TOTAL_WATTEN_AGENT_EVALUATE,
            EnvironmentSelector.TOTAL_WATTEN_AGENT_RANDOM,
            EnvironmentSelector.TOTAL_WATTEN_AGENT_HUMAN,

            EnvironmentSelector.HAND_WATTEN_TRAIN,
            EnvironmentSelector.HAND_WATTEN_TRAIN_S_S,
            EnvironmentSelector.HAND_WATTEN_TRAIN_M_M,
            EnvironmentSelector.HAND_WATTEN_TRAIN_CNN,
            EnvironmentSelector.HAND_WATTEN_EVALUATE,
            EnvironmentSelector.HAND_WATTEN_EVALUATE_M_M,
            EnvironmentSelector.HAND_WATTEN_EVALUATE_S_S,
            EnvironmentSelector.HAND_WATTEN_EVALUATE_CNN,
            EnvironmentSelector.HAND_WATTEN_RANDOM,
            EnvironmentSelector.HAND_WATTEN_HUMAN,
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

        if agent_profile == EnvironmentSelector.SUB_WATTEN_AGENT_TRAIN:
            nnet = SubWattenNNet(x, y, 1, game.get_action_size())
        elif agent_profile == EnvironmentSelector.SUB_WATTEN_AGENT_TRAIN_SIMPLE:
            nnet = SubWattenSimplerNNet(x, y, 1, game.get_action_size())

        agent_nnet = AgentNNet(nnet)

        if agent_profile == EnvironmentSelector.SUB_WATTEN_AGENT_TRAIN or \
                agent_profile == EnvironmentSelector.SUB_WATTEN_AGENT_TRAIN_SIMPLE:
            print("Configuring build_sub_watten_train_agent...")
            return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=100,
                             max_predict_time=10, num_threads=1)

        return None

    def build_sub_watten_evaluate_agent(self, agent_profile, native_multi_gpu_enabled=False):
        game = self.game_mapping[agent_profile.game]

        x, y = game.get_observation_size()
        if agent_profile == EnvironmentSelector.SUB_WATTEN_AGENT_EVALUATE:
            nnet = SubWattenNNet(x, y, 1, game.get_action_size())
        elif agent_profile == EnvironmentSelector.SUB_WATTEN_AGENT_EVALUATE_SIMPLE:
            nnet = SubWattenSimplerNNet(x, y, 1, game.get_action_size())

        agent_nnet = AgentNNet(nnet)

        return agent_nnet

    def build_sub_watten_agent(self, agent_profile, native_multi_gpu_enabled=False):

        game = self.game_mapping[agent_profile.game]

        if agent_profile == EnvironmentSelector.SUB_WATTEN_AGENT_RANDOM:
            return AgentRandom()
        elif agent_profile == EnvironmentSelector.SUB_WATTEN_AGENT_HUMAN:
            return SubWattenHumanAgent(game)
        elif agent_profile == EnvironmentSelector.SUB_WATTEN_AGENT_BAGGING:
            return SubWattenBaggingModel(game)

        return None

    def build_asymmetric_sub_watten_train_agent(self, agent_profile, native_multi_gpu_enabled=False):
        game = self.game_mapping[agent_profile.game]

        x, y = game.get_observation_size()
        nnet = AsymmetricSubWattenNNet(x, y, 1, game.get_action_size())

        agent_nnet = AgentNNet(nnet)

        if agent_profile == EnvironmentSelector.ASYMMETRIC_SUB_WATTEN_AGENT_TRAIN:
            print("Configuring build_asymmetric_sub_watten_train_agent...")
            return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=100,
                             max_predict_time=10, num_threads=1)

        return None

    def build_asymmetric_sub_watten_evaluate_agent(self, agent_profile, native_multi_gpu_enabled=False):
        game = self.game_mapping[agent_profile.game]

        x, y = game.get_observation_size()
        nnet = AsymmetricSubWattenNNet(x, y, 1, game.get_action_size())

        agent_nnet = AgentNNet(nnet)

        return agent_nnet

    def build_asymmetric_sub_watten_agent(self, agent_profile, native_multi_gpu_enabled=False):

        if agent_profile == EnvironmentSelector.ASYMMETRIC_SUB_WATTEN_AGENT_RANDOM:
            return AgentRandom()

        return None

    def build_total_watten_train_agent(self, agent_profile, native_multi_gpu_enabled=False):
        game = self.game_mapping[agent_profile.game]

        x, y = game.get_observation_size()
        nnet = TotalWattenNNet(x, y, 1, game.get_action_size())

        agent_nnet = AgentNNet(nnet)

        if agent_profile == EnvironmentSelector.TOTAL_WATTEN_AGENT_TRAIN:
            print("Configuring build_total_watten_train_agent...")
            return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=50,
                             max_predict_time=10, num_threads=1)

        return None

    def build_total_watten_evaluate_agent(self, agent_profile, native_multi_gpu_enabled=False):
        game = self.game_mapping[agent_profile.game]

        x, y = game.get_observation_size()
        nnet = TotalWattenNNet(x, y, 1, game.get_action_size())

        agent_nnet = AgentNNet(nnet)

        return agent_nnet

    def build_total_watten_agent(self, agent_profile, native_multi_gpu_enabled=False):

        game = self.game_mapping[agent_profile.game]

        if agent_profile == EnvironmentSelector.TOTAL_WATTEN_AGENT_RANDOM:
            return AgentRandom()
        elif agent_profile == EnvironmentSelector.TOTAL_WATTEN_AGENT_HUMAN:
            return TotalWattenHumanAgent(game)

    def sub_watten_non_human_agent_for_total_watten(self):

        game = WattenSubGame()

        x, y = game.get_observation_size()
        nnet = SubWattenNNet(x, y, 1, game.get_action_size())

        agent_nnet = AgentNNet(nnet)

        print('Building sub_watten non human agent for total_watten')

        # load here best sub_watten model
        try:
            agent_nnet.load("games/sub_watten/training/default_nn/best.h5")
        except OSError:
            print("File not found with games/sub_watten/training/best.h5")
            print("Maybe you are creating an agent for test purposes. I'll try to load the model from a different path")
            agent_nnet.load("../../sub_watten/training/default_nn/best.h5")

        return agent_nnet

    def sub_watten_human_agent_for_total_watten(self):

        game = WattenSubGame()

        return SubWattenHumanAgent(game)

    def build_hand_watten_train_agent(self, agent_profile, native_multi_gpu_enabled=False):
        game = self.game_mapping[agent_profile.game]

        if agent_profile == EnvironmentSelector.HAND_WATTEN_TRAIN:
            x, y = game.get_observation_size()
            nnet = HandWattenNNet(x, y, 1, game.get_action_size())
            agent_nnet = AgentNNet(nnet)

            print("Configuring build_hand_watten_train_agent...")
            return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=30,
                             max_predict_time=10, num_threads=1)
        elif agent_profile == EnvironmentSelector.HAND_WATTEN_TRAIN_S_S:
            x, y = game.get_observation_size()
            nnet = EasyEasyNNet(x, y, 1, game.get_action_size())
            agent_nnet = AgentNNet(nnet)
            print("Configuring build_hand_watten_s_s...")
            return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=30,
                             max_predict_time=10, num_threads=1)
        elif agent_profile == EnvironmentSelector.HAND_WATTEN_TRAIN_M_M:
            x, y = game.get_observation_size()
            nnet = MediumMediumNNet(x, y, 1, game.get_action_size())
            agent_nnet = AgentNNet(nnet)
            print("Configuring build_hand_watten_m_m...")
            return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=30,
                             max_predict_time=10, num_threads=1)
        elif agent_profile == EnvironmentSelector.HAND_WATTEN_TRAIN_CNN:
            x, y, z = game.get_observation_size()
            nnet = CNNWatten(x, y, z, game.get_action_size())
            agent_nnet = AgentNNet(nnet)
            print("Configuring build hand watten CNN....")
            return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=30,
                             max_predict_time=10, num_threads=1)

        return None

    def build_hand_watten_evaluate_agent(self, agent_profile, native_multi_gpu_enabled=False):
        game = self.game_mapping[agent_profile.game]

        agent_nnet = None

        if agent_profile == EnvironmentSelector.HAND_WATTEN_EVALUATE:
            x, y = game.get_observation_size()
            nnet = HandWattenNNet(x, y, 1, game.get_action_size())
            agent_nnet = AgentNNet(nnet)
        elif agent_profile == EnvironmentSelector.HAND_WATTEN_EVALUATE_M_M:
            x, y = game.get_observation_size()
            nnet = MediumMediumNNet(x, y, 1, game.get_action_size())
            agent_nnet = AgentNNet(nnet)
        elif agent_profile == EnvironmentSelector.HAND_WATTEN_EVALUATE_S_S:
            x, y = game.get_observation_size()
            nnet = EasyEasyNNet(x, y, 1, game.get_action_size())
            agent_nnet = AgentNNet(nnet)
        elif agent_profile == EnvironmentSelector.HAND_WATTEN_EVALUATE_CNN:
            x, y, z = game.get_observation_size()
            nnet = CNNWatten(x, y, z, game.get_action_size())
            agent_nnet = AgentNNet(nnet)

        return agent_nnet

    def build_hand_watten_agent(self, agent_profile, native_multi_gpu_enabled=False):

        if agent_profile == EnvironmentSelector.HAND_WATTEN_RANDOM:
            return AgentRandom()
        if agent_profile == EnvironmentSelector.HAND_WATTEN_HUMAN:
            return HandWattenHumanAgent(self.game_mapping[agent_profile.game])
