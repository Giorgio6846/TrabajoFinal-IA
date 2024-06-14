from collections import deque
import numpy as np
import random
from Blackjack.Tools import Model
import tensorflow as tf

VERBOSETRAIN = 1
LOGSPATH = "./models/v{VERSION}/logs"

BATCH_SIZE = 32
ALPHA = 0.03

class DQNAgent:
    def __init__(
        self,
        state_size,
        action_size,
        VERSION = 1
    ):

        # Model Parameters
        self.state_size = state_size
        self.action_size = action_size
        self.stepsAmount = 10

        # HyperParameters
        self.batch_size = BATCH_SIZE
        self.alpha = ALPHA
        self.gamma = 0.95  # factor de descuento para las recompensas futuras
        self.epsilon = 0.9  # tasa de exploración inicial
        self.epsilon_min = 0.05  # tasa de exploración mínima
        self.epsilon_decay = 0.995  # factor de decaimiento de la tasa de exploración

        # DQN Config
        self.memory = deque(maxlen=2000)  # Aquí se define la memoria de repetición
        self.ModelClass = Model(self.state_size, self.action_size)

        # Save Config
        self.version = VERSION

        # Debug Config
        self.SaveToTensorboard = False       

    def getHyperparameters(self):
        return dict(
            {
                "batch_size": self.batch_size,
                "alpha": self.alpha,
                "gamma": self.gamma,
                "epsilon": self.epsilon,
                "epsilon_min": self.epsilon_min,
                "epsilon_min": self.epsilon_decay
            }
        )

    def setHyperparameters(self, dictHyper):
        self.batch_size = dictHyper["batch_size"]
        self.alpha = dictHyper["alpha"]
        self.gamma = dictHyper["gamma"]
        self.epsilon = dictHyper["epsilon"]
        self.epsilon_min = dictHyper["epsilon_min"]
        self.epsilon_decay = dictHyper["epsilon_decay"]

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

        for _ in range(self.stepsAmount):
            obs = env.get_obs()
            action = self.ModelClass.act(
                obs, self.epsilon, self.action_size
            )
            state, action, reward, next_state, done = env.step(action)

            self.ModelClass.remember(
                state, action, reward, next_state, done, self.memory
            )

            if done or env.get_badmove():
                break

        if len(self.memory) > self.batch_size:
            self.replay(self.batch_size)