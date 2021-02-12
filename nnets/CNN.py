from core.nnet.NNet import NNet

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPool2D, Flatten, Dense, BatchNormalization, Dropout
from tensorflow.keras.optimizers import Adam


class CNN(NNet):

    def build_model(self):
        print(f"Build model with x {self.observation_size_x}, y {self.observation_size_y}, "
              f"z {self.observation_size_z}, action size {self.action_size}")

        learning_rate = 0.001

        input_boards = Input(shape=(self.observation_size_x, self.observation_size_y, self.observation_size_z))

        print(input_boards.shape)

        cl1 = Conv2D(32, (3, 3), activation='relu')(input_boards)
        cl2 = Conv2D(32, (3, 3), activation='relu')(cl1)
        mp1 = MaxPool2D((2, 2), padding='same')(cl2)
        cl3 = Conv2D(64, (3, 3), activation='relu')(mp1)
        cl4 = Conv2D(64, (3, 3), activation='relu')(cl3)
        mp2 = MaxPool2D((2, 2), padding='same')(cl4)
        f1 = Flatten()(mp2)
        d1 = Dense(128, activation='relu')(f1)
        b1 = BatchNormalization()(d1)
        d1 = Dropout(0.5)(b1)

        pi = Dense(self.action_size, activation='softmax', name='pi')(d1)
        v = Dense(1, activation='tanh', name='v')(d1)

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
        inp = np.asarray(inp)
        inp = inp.reshape((batch_size, self.observation_size_x, self.observation_size_y, self.observation_size_z))

        pi = []
        game_result = []
        length = 0
        for o in out:
            length = length+1
            pi.append(o['pi'])
            game_result.append(o['game_result'])

        pi = np.asarray(pi)
        pi = pi.reshape(batch_size, self.action_size)

        game_result = np.asarray(game_result)

        return inp, [pi, game_result], length

    def clone(self):
        return CNN(self.observation_size_x, self.observation_size_y, self.observation_size_z, self.action_size)
