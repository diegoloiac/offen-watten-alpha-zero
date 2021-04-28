from core.nnet.NNet import NNet

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, BatchNormalization, Activation, Dropout, Flatten, Reshape, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam


class DefaultFFNN(NNet):

    def __init__(self, observation_size_x, observation_size_y, observation_size_z, action_size):
        super().__init__(observation_size_x, observation_size_y, observation_size_z, action_size)

    def build_model(self):
        print(f"Build model with x {self.observation_size_x}, y {self.observation_size_y}, "
              f"z {self.observation_size_z}, action size {self.action_size}")

        learning_rate = 0.0001

        input_boards = Input(shape=(self.observation_size_x, self.observation_size_y))

        x_image = Reshape((self.observation_size_x, self.observation_size_y, 1))(input_boards)

        print(x_image.shape)

        h_input = Flatten()(x_image)

        h_fc1 = Dropout(0.2)(Activation('relu')(BatchNormalization(axis=1)(Dense(1024)(h_input))))
        h_fc2 = Dropout(0.2)(Activation('relu')(BatchNormalization(axis=1)(Dense(1024)(h_fc1))))
        h_fc3 = Dropout(0.2)(Activation('relu')(BatchNormalization(axis=1)(Dense(1024)(h_fc2))))
        h_fc4 = Dropout(0.2)(Activation('relu')(BatchNormalization(axis=1)(Dense(1024)(h_fc3))))
        h_fc5 = Dropout(0.2)(Activation('relu')(BatchNormalization(axis=1)(Dense(512)(h_fc4))))
        h_fc6 = Dropout(0.2)(Activation('relu')(BatchNormalization(axis=1)(Dense(512)(h_fc5))))
        h_fc7 = Dropout(0.2)(Activation('relu')(BatchNormalization(axis=1)(Dense(512)(h_fc6))))

        pi = Dense(self.action_size, activation='softmax', name='pi')(h_fc7)
        v = Dense(1, activation='tanh', name='v')(h_fc7)

        model = Model(inputs=input_boards, outputs=[pi, v])

        model.summary()

        model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(learning_rate))

        return model

    def parse_example(self, example):
        feature_description = {
            'observation': tf.io.FixedLenFeature([1, ], tf.string, default_value=''),
            'pi': tf.io.FixedLenFeature([1, ], tf.string, default_value=''),
            'game_result': tf.io.FixedLenFeature([1, ], tf.float32, default_value=0.0)
        }

        parsed_example = tf.io.parse_single_example(example, feature_description)

        observation = tf.io.decode_raw(parsed_example['observation'], tf.float64, name='observation')
        outputs = {'pi': tf.io.decode_raw(parsed_example['pi'], tf.float64), 'game_result': parsed_example['game_result']}

        return observation, outputs

    def parse_input_output(self, inp, out, batch_size):
        pi = []
        game_result = []
        length = 0
        for o in out:
            length = length+1
            pi.append(o['pi'])
            game_result.append(o['game_result'])

        if length < batch_size:
            batch_size = length

        pi = np.asarray(pi)
        pi = pi.reshape(length, self.action_size)

        game_result = np.asarray(game_result)

        inp = np.asarray(inp)
        inp = inp.reshape((length, self.observation_size_x, self.observation_size_y, self.observation_size_z))

        return inp, [pi, game_result], length, batch_size

    def clone(self):
        return DefaultFFNN(self.observation_size_x, self.observation_size_y, 1, self.action_size)
