import numpy as np

from core.interfaces.Agent import Agent


class AgentNNet(Agent):
    def __init__(self, nnet, name="Agent NNet"):
        super().__init__(name=name)
        self.nnet = nnet

    def prepare_to_game(self):
        pass

    def disable_training_capability(self, temp_dir=None, optimize=True):
        self.nnet.disable_training_capability(temp_dir=temp_dir, optimize=optimize)

    def enable_training_capability(self):
        self.nnet.enable_training_capability()

    def predict(self, game, game_player):
        observation = game.get_observation(game_player)
        observation = observation[np.newaxis, :, :]

        result = self.nnet.predict(observation)

        return result

    def save(self, path_to_file):
        self.nnet.save(path_to_file)

    def load(self, path_to_file):
        print("Loading model", path_to_file)
        self.nnet.load(path_to_file)

    def train(self, filenames, batch_size=2048, epochs=10, verbose=1):

        self.nnet.train(filenames, batch_size=batch_size, epochs=epochs, verbose=verbose)

    def set_exploration_enabled(self, enabled):
        pass

    def clone(self):
        return AgentNNet(self.nnet, name=self.name)
