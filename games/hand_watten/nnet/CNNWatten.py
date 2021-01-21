from core.nnet.NNet import NNet

from keras.models import *
from keras.layers import *
from keras.optimizers import *


class CNNWatten(NNet):

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

        _multi_gpu_model = None

        model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(learning_rate))

        return model, _multi_gpu_model

    def clone(self):
        return CNNWatten(self.observation_size_x, self.observation_size_y, 1, self.action_size, self.multi_gpu)
