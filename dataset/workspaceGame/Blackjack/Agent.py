from collections import deque
import numpy as np
import random
from Blackjack.Tools import Model
import tensorflow as tf

VERBOSETRAIN = 1
LOGSPATH = "./models/v{VERSION}/logs"

class DQNAgent:
    def __init__(
        self,
        state_size,
        action_size,
        alpha=0.01,
        batch_size=32,
        VERSION = 1
    ):

        # Model Parameters
        self.state_size = state_size
        self.action_size = action_size

        # HyperParameters
        self.batch_size = batch_size
        self.alpha = alpha
        self.gamma = 0.95  # factor de descuento para las recompensas futuras
        self.epsilon = 0.9  # tasa de exploración inicial
        self.epsilon_min = 0.01  # tasa de exploración mínima
        self.epsilon_decay = 0.995  # factor de decaimiento de la tasa de exploración

        # DQN Config
        self.memory = deque(maxlen=2000)  # Aquí se define la memoria de repetición
        self.ModelClass = Model(self.state_size, self.action_size)

        # Save Config
        self.version = VERSION

        # Debug Config
        self.SaveToTensorboard = False       

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(
                    self.ModelClass.model.predict(next_state, verbose=VERBOSETRAIN, use_multiprocessing=True)[0]
                )
            target_f = self.ModelClass.model.predict(
                state, verbose=VERBOSETRAIN, use_multiprocessing=True
            )
            target_f[0][action] = target

            if self.SaveToTensorboard:
                callbacks = tf.keras.callbacks.TensorBoard(
                    log_dir=LOGSPATH.format(VERSION=self.version),
                    histogram_freq=0,
                    write_graph=True,
                )
                self.ModelClass.model.fit(
                    state,
                    target_f,
                    epochs=1,
                    verbose=VERBOSETRAIN,
                    callbacks=callbacks,
                    use_multiprocessing=True,
                )
            else:
                self.ModelClass.model.fit(
                    state,
                    target_f,
                    epochs=1,
                    verbose=VERBOSETRAIN,
                    use_multiprocessing=True,
                )

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def train(self, env, STT):
        self.SaveToTensorboard = STT

        done = False
        env.reset(5)

        while not done:
            obs = env.get_obs()
            action = self.ModelClass.act(
                obs, self.epsilon, self.action_size
            )
            state, action, reward, next_state, doneEnv = env.step(action)

            if doneEnv == 1:
                done = True
                self.ModelClass.remember(
                    state, action, reward, next_state, True, self.memory
                )

        if len(self.memory) > self.batch_size:
            self.replay(self.batch_size)
