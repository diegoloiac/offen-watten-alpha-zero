from versions.blind_watten.BlindWattenGame import BlindWattenGame
from versions.sub_watten.SubWattenGame import SubWattenGame
from versions.asymmetric_sub_watten.AsymmetricSubWattenGame import AsymmetricSubWattenGame
# from versions.total_watten.TotalWattenGame import TotalWattenGame
from versions.hand_watten.HandWattenGame import HandWattenGame

from core.agents.AgentNNet import AgentNNet
from core.agents.AgentMCTS import AgentMCTS
from core.agents.AgentRandom import AgentRandom
from core.agents.HumanAgent import HumanAgent

from nnets.DefaultFFNN import DefaultFFNN
from nnets.CNN import CNN


class EnvironmentSelector:
    GAME_SUB_WATTEN_DEFAULT = "sub_watten_environment_default"

    GAME_ASYMMETRIC_SUB_WATTEN_DEFAULT = "asymmetric_sub_watten_environment_default"

    GAME_ASYMMETRIC_SUB_WATTEN_EVALUATE = "asymmetric_sub_watten_environment_evaluate"

    GAME_TOTAL_WATTEN_DEFAULT = "total_watten_environment_default"

    GAME_TOTAL_WATTEN_H_VS_H = "total_watten_environment_h_vs_h"

    GAME_TOTAL_WATTEN_H_VS_NH = "total_watten_environment_h_vs_nh"

    GAME_TOTAL_WATTEN_NH_VS_H = "total_watten_environment_nh_vs_h"

    GAME_HAND_WATTEN = "hand_watten_environment_default"

    GAME_HAND_WATTEN_CNN = "hand_watten_environment_cnn"

    GAME_BLIND_WATTEN = "blind_watten_environment_default"

    class AgentProfile:
        def __init__(self, game, agent_profile):
            self.game = game
            self.agent_profile = agent_profile

    # agent profiles
    AGENT_RANDOM = AgentProfile(None, "agent_random")

    SUB_WATTEN_AGENT_TRAIN = AgentProfile(GAME_SUB_WATTEN_DEFAULT, "sub_watten_train")
    SUB_WATTEN_AGENT_EVALUATE = AgentProfile(GAME_SUB_WATTEN_DEFAULT, "sub_watten_evaluate")
    SUB_WATTEN_AGENT_HUMAN = AgentProfile(GAME_SUB_WATTEN_DEFAULT, "sub_watten_human")

    ASYMMETRIC_SUB_WATTEN_AGENT_TRAIN = AgentProfile(GAME_ASYMMETRIC_SUB_WATTEN_DEFAULT, "asymmetric_sub_watten_train")
    ASYMMETRIC_SUB_WATTEN_AGENT_EVALUATE = AgentProfile(GAME_SUB_WATTEN_DEFAULT, "asymmetric_sub_watten_evaluate")

    TOTAL_WATTEN_AGENT_TRAIN = AgentProfile(GAME_TOTAL_WATTEN_DEFAULT, "total_watten_train")
    TOTAL_WATTEN_AGENT_EVALUATE = AgentProfile(GAME_TOTAL_WATTEN_DEFAULT, "total_watten_evaluate")
    TOTAL_WATTEN_AGENT_HUMAN = AgentProfile(GAME_TOTAL_WATTEN_DEFAULT, "total_watten_human")

    HAND_WATTEN_HUMAN = AgentProfile(GAME_HAND_WATTEN, "hand_watten_human")
    HAND_WATTEN_TRAIN = AgentProfile(GAME_HAND_WATTEN, "hand_watten_train")
    HAND_WATTEN_EVALUATE = AgentProfile(GAME_HAND_WATTEN, "hand_watten_evaluate")

    HAND_WATTEN_TRAIN_CNN = AgentProfile(GAME_HAND_WATTEN_CNN, "hand_watten_train_cnn")
    HAND_WATTEN_EVALUATE_CNN = AgentProfile(GAME_HAND_WATTEN_CNN, "hand_watten_evaluate_cnn")

    BLIND_WATTEN_HUMAN = AgentProfile(GAME_BLIND_WATTEN, "blind_watten_human")
    BLIND_WATTEN_TRAIN = AgentProfile(GAME_BLIND_WATTEN, "blind_watten_train")
    BLIND_WATTEN_EVALUATE = AgentProfile(GAME_BLIND_WATTEN, "blind_watten_evaluate")

    def __init__(self):
        super().__init__()

        self.game_mapping = {
            EnvironmentSelector.GAME_SUB_WATTEN_DEFAULT: SubWattenGame(),
            EnvironmentSelector.GAME_ASYMMETRIC_SUB_WATTEN_DEFAULT: AsymmetricSubWattenGame(),

            #  EnvironmentSelector.GAME_TOTAL_WATTEN_DEFAULT: TotalWattenGame(
            #      self.build_evaluate_agent_ffnn(EnvironmentSelector.SUB_WATTEN_AGENT_EVALUATE),
            #      self.build_evaluate_agent_ffnn(EnvironmentSelector.SUB_WATTEN_AGENT_EVALUATE)
            #  ),
            #  EnvironmentSelector.GAME_TOTAL_WATTEN_H_VS_H: TotalWattenGame(
            #      self.build_human_agent(EnvironmentSelector.SUB_WATTEN_AGENT_HUMAN),
            #      self.build_human_agent(EnvironmentSelector.SUB_WATTEN_AGENT_HUMAN),
            #  ),
            #  EnvironmentSelector.GAME_TOTAL_WATTEN_H_VS_NH: TotalWattenGame(
            #      self.build_human_agent(EnvironmentSelector.SUB_WATTEN_AGENT_HUMAN),
            #      self.build_evaluate_agent_ffnn(EnvironmentSelector.SUB_WATTEN_AGENT_EVALUATE)
            #  ),
            #  EnvironmentSelector.GAME_TOTAL_WATTEN_NH_VS_H: TotalWattenGame(
            #      self.build_evaluate_agent_ffnn(EnvironmentSelector.SUB_WATTEN_AGENT_EVALUATE),
            #      self.build_human_agent(EnvironmentSelector.SUB_WATTEN_AGENT_HUMAN),
            #  ),
            EnvironmentSelector.GAME_HAND_WATTEN: HandWattenGame(),
            EnvironmentSelector.GAME_HAND_WATTEN_CNN: HandWattenGame(cnn=True),
            EnvironmentSelector.GAME_BLIND_WATTEN: BlindWattenGame(),
        }

        self.agent_builder_mapping = {
            EnvironmentSelector.AGENT_RANDOM: self.build_random_agent,

            EnvironmentSelector.SUB_WATTEN_AGENT_TRAIN: self.build_train_agent_ffnn,
            EnvironmentSelector.SUB_WATTEN_AGENT_EVALUATE: self.build_evaluate_agent_ffnn,
            EnvironmentSelector.SUB_WATTEN_AGENT_HUMAN: self.build_human_agent,

            EnvironmentSelector.ASYMMETRIC_SUB_WATTEN_AGENT_TRAIN: self.build_train_agent_ffnn,
            EnvironmentSelector.ASYMMETRIC_SUB_WATTEN_AGENT_EVALUATE: self.build_evaluate_agent_ffnn,

            EnvironmentSelector.TOTAL_WATTEN_AGENT_TRAIN: self.build_train_agent_ffnn,
            EnvironmentSelector.TOTAL_WATTEN_AGENT_EVALUATE: self.build_evaluate_agent_ffnn,
            EnvironmentSelector.TOTAL_WATTEN_AGENT_HUMAN: self.build_human_agent,

            EnvironmentSelector.HAND_WATTEN_TRAIN: self.build_train_agent_ffnn,
            EnvironmentSelector.HAND_WATTEN_TRAIN_CNN: self.build_train_agent_cnn,
            EnvironmentSelector.HAND_WATTEN_EVALUATE: self.build_evaluate_agent_ffnn,
            EnvironmentSelector.HAND_WATTEN_EVALUATE_CNN: self.build_evaluate_agent_cnn,
            EnvironmentSelector.HAND_WATTEN_HUMAN: self.build_human_agent,

            EnvironmentSelector.BLIND_WATTEN_TRAIN: self.build_train_agent_ffnn,
            EnvironmentSelector.BLIND_WATTEN_EVALUATE: self.build_evaluate_agent_ffnn,
            EnvironmentSelector.BLIND_WATTEN_HUMAN: self.build_human_agent,
        }

        self.agent_profiles = [
            EnvironmentSelector.AGENT_RANDOM,

            EnvironmentSelector.SUB_WATTEN_AGENT_TRAIN,
            EnvironmentSelector.SUB_WATTEN_AGENT_EVALUATE,
            EnvironmentSelector.SUB_WATTEN_AGENT_HUMAN,

            EnvironmentSelector.ASYMMETRIC_SUB_WATTEN_AGENT_TRAIN,
            EnvironmentSelector.ASYMMETRIC_SUB_WATTEN_AGENT_EVALUATE,

            EnvironmentSelector.TOTAL_WATTEN_AGENT_TRAIN,
            EnvironmentSelector.TOTAL_WATTEN_AGENT_EVALUATE,
            EnvironmentSelector.TOTAL_WATTEN_AGENT_HUMAN,

            EnvironmentSelector.HAND_WATTEN_TRAIN,
            EnvironmentSelector.HAND_WATTEN_TRAIN_CNN,
            EnvironmentSelector.HAND_WATTEN_EVALUATE,
            EnvironmentSelector.HAND_WATTEN_EVALUATE_CNN,
            EnvironmentSelector.HAND_WATTEN_HUMAN,

            EnvironmentSelector.BLIND_WATTEN_TRAIN,
            EnvironmentSelector.BLIND_WATTEN_EVALUATE,
            EnvironmentSelector.BLIND_WATTEN_HUMAN,
        ]

    def get_profile(self, agent_profile_str):
        for profile in self.agent_profiles:
            if profile.agent_profile == agent_profile_str:
                return profile

        print("Error: could not find an agent profile by the key: ", agent_profile_str)

        return None

    def get_agent(self, agent_profile_str):
        agent_profile = self.get_profile(agent_profile_str)
        if agent_profile in self.agent_builder_mapping:
            return self.agent_builder_mapping[agent_profile](agent_profile)

        print("Error: could not find an agent by the key: ", agent_profile_str)

        return None

    def get_game(self, game_profile):
        if game_profile in self.game_mapping:
            return self.game_mapping[game_profile]

        print("Error: could not find a game with profile: ", game_profile)

        return None

    @staticmethod
    def build_random_agent(agent_profile):
        print('Building random agent')
        if agent_profile == EnvironmentSelector.AGENT_RANDOM:
            return AgentRandom()

    def build_human_agent(self, agent_profile):
        game = self.game_mapping[agent_profile.game]

        return HumanAgent(game)

    def build_evaluate_agent_ffnn(self, agent_profile):
        game = self.game_mapping[agent_profile.game]
        print(f'Building ffnn evaluate agent for {game.__class__}')

        x, y = game.get_observation_size()

        nnet = DefaultFFNN(x, y, 1, game.get_action_size())

        agent = AgentNNet(nnet)

        return agent

    def build_train_agent_ffnn(self):
        game = self.game_mapping[EnvironmentSelector.GAME_HAND_WATTEN: HandWattenGame()]
        print(f'Building ffnn train agent for {game.__class__}')

        x, y = game.get_observation_size()

        nnet = DefaultFFNN(x, y, 1, game.get_action_size())

        agent_nnet = AgentNNet(nnet)

        return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=100,
                         max_predict_time=10, num_threads=1)

    def build_evaluate_agent_cnn(self, agent_profile):
        game = self.game_mapping[agent_profile.game]
        print(f'Building cnn evaluate agent for {game.__class__}')

        x, y, z = game.get_observation_size()

        nnet = CNN(x, y, z, game.get_action_size())

        agent = AgentNNet(nnet)
        agent.name = 'evaluate_cnn'

        return agent

    def build_train_agent_cnn(self, agent_profile):
        game = self.game_mapping[agent_profile.game]
        print(f'Building cnn train agent for {game.__class__}')

        x, y, z = game.get_observation_size()

        nnet = CNN(x, y, z, game.get_action_size())

        agent_nnet = AgentNNet(nnet)

        return AgentMCTS(agent_nnet, exp_rate=AgentMCTS.EXPLORATION_RATE_MEDIUM, numMCTSSims=100,
                         max_predict_time=10, num_threads=1)
