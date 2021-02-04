from abc import ABC, abstractmethod

import tensorflow as tf
import numpy as np


class NNet(ABC):
    EXTENSION_KERAS = ".h5"

    def __init__(self, observation_size_x, observation_size_y, observation_size_z, action_size):
        self.observation_size_x = observation_size_x
        self.observation_size_y = observation_size_y
        self.observation_size_z = observation_size_z
        self.action_size = action_size

        devices = tf.config.list_physical_devices('GPU')
        print(devices)

        if len(devices) > 0:
            tf.config.set_soft_device_placement(True)
            tf.debugging.set_log_device_placement(True)

        self.model = self.build_model()
        self.graph_model = tf.function(self.model)


    def save(self, filepath):
        filepath = filepath if filepath.endswith(self.EXTENSION_KERAS) else filepath + self.EXTENSION_KERAS
        self.model.save_weights(filepath)

    def load(self, filepath):
        filepath = filepath if filepath.endswith(self.EXTENSION_KERAS) else filepath + self.EXTENSION_KERAS
        self.model.load_weights(filepath)

    def train(self, input_boards, target_pis, target_vs, batch_size=2048, epochs=10, verbose=1):
        model = self.get_model()

        print("Fit model with epochs %d and batch size %d" % (epochs, batch_size))
        model.fit(x=input_boards, y=[target_pis, target_vs], batch_size=batch_size, epochs=epochs, verbose=verbose)

    def get_model(self):
        return self.model

    def set_model(self, model):
        self.model = model

    def clone(self):
        return NNet(self.observation_size_x, self.observation_size_y, self.observation_size_z, self.action_size)

    def predict(self, observation):
        pi, v = self.graph_model(observation, training=False)

        if np.isscalar(v[0]):
            return pi[0], v[0]
        else:
            return pi[0], v[0][0]

    def _save_model(self, filepath):
        filepath = filepath if filepath.endswith(self.EXTENSION_KERAS) else filepath + self.EXTENSION_KERAS
        self.model.save(filepath)

    @abstractmethod
    def build_model(self):
        pass
