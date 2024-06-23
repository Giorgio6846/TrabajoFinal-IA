from collections import deque
import numpy as np
import random
from pytz import VERSION
from sympy import dict_merge
import tensorflow as tf

from .Tools import ModelDQN

VERBOSETRAIN = 1

BATCH_SIZE = 32
ALPHA = 0.2

class DQNAgent:
    def __init__(
        self,
        state_size,
        action_size,
        learning_rate = 0.01,
        VERSION = 1
    ):

        # Model Parameters
        self.state_size = state_size
        self.action_size = action_size
        self.stepsAmount = 10

        # HyperParameters
        self.batch_size = BATCH_SIZE
        self.gamma = 0.95  # factor de descuento para las recompensas futuras
        self.epsilon = 0.9  # tasa de exploración inicial
        self.epsilon_min = 0.05  # tasa de exploración mínima
        self.annelingSteps = 10000
        self.learningRate = learning_rate

        # DQN Config
        self.memory = deque(maxlen=10000)  # Aquí se define la memoria de repetición
        self.ModelClass = ModelDQN(self.state_size, self.action_size, self.learning_rate)

        # Save Config
        self.version = VERSION

        # Debug Config
        self.SaveToTensorboard = False

        self.calcStepDrop()

    def calcStepDrop(self):
        self.epsilonDecay = (self.epsilon - self.epsilon_min) / self.annelingSteps      

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def getHyperparameters(self):
        return dict(
            {
                "batchSize": self.batch_size,
                "gamma": self.gamma,
                "epsilon": self.epsilon,
                "epsilonMin": self.epsilon_min,
                "annelingSteps": self.annelingSteps,
                "learningRate": self.learning_rate,
            }
        )

    def setHyperparameters(self, dictHyper):
        self.batch_size = dictHyper["batchSize"]
        self.gamma = dictHyper["gamma"]
        self.epsilon = dictHyper["epsilon"]
        self.epsilon_min = dictHyper["epsilonMin"]
        self.annelingSteps = dictHyper["annelingSteps"]
        self.learningRate = dictHyper["learningRate"]

        # Sets a new model with the diferent learning_rate
        self.ModelClass = ModelDQN(
            self.state_size, self.action_size, self.learning_rate
        )
        self.calcStepDrop()

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

            self.ModelClass.modelFit(state, target_f, VERBOSETRAIN, self.SaveToTensorboard, self.version)

        if self.epsilon > self.epsilon_min:
            self.epsilon -= self.epsilonDecay

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

            self.remember(
                state, action, reward, next_state, done
            )

            if done or env.get_badmove():
                break

        if len(self.memory) > self.batch_size:
            self.replay(self.batch_size)
