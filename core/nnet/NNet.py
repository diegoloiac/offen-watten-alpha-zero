from abc import ABC, abstractmethod

import tensorflow as tf
import numpy as np
import datetime


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

    def save(self, filepath):
        filepath = filepath if filepath.endswith(self.EXTENSION_KERAS) else filepath + self.EXTENSION_KERAS
        self.model.save_weights(filepath)

    def load(self, filepath):
        filepath = filepath if filepath.endswith(self.EXTENSION_KERAS) else filepath + self.EXTENSION_KERAS
        self.model.load_weights(filepath)

    def train(self, filenames, batch_size=2048, epochs=10, verbose=1):
        print(f'Creating raw dataset from {filenames}')
        raw_dataset = tf.data.TFRecordDataset(filenames, num_parallel_reads=tf.data.AUTOTUNE)

        print('Parsing the dataset')
        parsed_dataset = raw_dataset.map(self.parse_example, num_parallel_calls=tf.data.AUTOTUNE)
        print(parsed_dataset)

        parsed_dataset.cache()
        parsed_dataset.batch(batch_size)

        log_dir = "tensorboard/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1, profile_batch='10,20')

        self.model.fit(parsed_dataset, callbacks=[tensorboard_callback], epochs=epochs)
        #dataset_empty = False

        #while not dataset_empty:
        #    batch = parsed_dataset.take(50*batch_size)
        #    batch = batch.as_numpy_iterator()
        #
        #    nnet_input, nnet_output = zip(*batch)
        #    nnet_input, nnet_output, length, batch_size = self.parse_input_output(nnet_input, nnet_output, batch_size)
        #
        #    print("Fit model with epochs %d and batch size %d" % (epochs, batch_size))
        #    model.fit(x=nnet_input, y=nnet_output, batch_size=batch_size, epochs=epochs, verbose=verbose)
        #
        #    parsed_dataset = parsed_dataset.skip(50*batch_size)
        #
        #    if length < 50*batch_size:
        #        dataset_empty = True

    def get_model(self):
        return self.model

    def set_model(self, model):
        self.model = model

    def clone(self):
        return NNet(self.observation_size_x, self.observation_size_y, self.observation_size_z, self.action_size)

    @tf.function
    def predict(self, observation):
        pi, v = self.model(observation)

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

    @abstractmethod
    def parse_example(self, example):
        """
        Should provide a method to parse a tensorflow example.
        It should have feature description and it should parse an example
        in two elements: input of the nnet and output of the nnet.
        """
        pass

    @abstractmethod
    def parse_input_output(self, inp, out, batch_size):
        """
        If needed, it provides a method to further parse inputs and outputs of the nnet
        to make them compatible with a model.fit with numpy arrays
        """
        pass
