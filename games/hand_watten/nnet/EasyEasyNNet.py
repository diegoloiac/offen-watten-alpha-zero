from core.nnet.NNet import NNet

from keras.models import *
from keras.layers import *
from keras.optimizers import *


class EasyEasyNNet(NNet):

    def build_model(self):
        print(f"Build model with x {self.observation_size_x}, y {self.observation_size_y}, "
              f"z {self.observation_size_z}, action size {self.action_size}")

        learning_rate = 0.0001

        input_boards = Input(shape=(self.observation_size_x, self.observation_size_y))

        x_image = Reshape((self.observation_size_x, self.observation_size_y, 1))(input_boards)

        print(x_image.shape)

        h_input = Flatten()(x_image)

        h_fc1 = Dropout(0.2)(Activation('relu')(BatchNormalization(axis=1)(Dense(150)(h_input))))

        pi = Dense(self.action_size, activation='softmax', name='pi')(h_fc1)
        v = Dense(1, activation='tanh', name='v')(h_fc1)

        model = Model(inputs=input_boards, outputs=[pi, v])

        _multi_gpu_model = None

        model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(learning_rate))

        return model, _multi_gpu_model

    def clone(self):
        return EasyEasyNNet(self.observation_size_x, self.observation_size_y, 1, self.action_size, self.multi_gpu)
