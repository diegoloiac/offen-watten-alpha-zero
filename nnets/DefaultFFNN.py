from core.nnet.NNet import NNet

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

    def clone(self):
        return DefaultFFNN(self.observation_size_x, self.observation_size_y, 1, self.action_size)
