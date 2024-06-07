from collections import deque
import numpy as np
import random
from Tools import Model
import tensorflow as tf

VERBOSETRAIN = 1

class DQNAgent:
    def __init__(
        self,
        state_size,
        action_size,
        alpha=0.01,
        episodes=100,
        batch_size=32,
        log_dir = ""
    ):
        self.ModelClass = Model()

        self.SaveToTensorboard = False
        self.logDir = log_dir
    
        self.episodes = episodes
        self.batch_size = batch_size
        self.state_size = state_size
        self.action_size = action_size
        self.alpha = alpha
        self.memory = deque(maxlen=2000)  # Aquí se define la memoria de repetición
        self.gamma = 0.95  # factor de descuento para las recompensas futuras
        self.epsilon = 0.9  # tasa de exploración inicial
        self.epsilon_min = 0.01  # tasa de exploración mínima
        self.epsilon_decay = 0.995  # factor de decaimiento de la tasa de exploración
        self.model = self.ModelClass._build_model(
            self.state_size, self.action_size
        )  # construcción del modelo DQN

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(
                    self.model.predict(next_state, verbose=VERBOSETRAIN)[0]
                )
            target_f = self.model.predict(state, verbose=VERBOSETRAIN)
            target_f[0][action] = target

            if self.SaveToTensorboard:
                callbacks = tf.keras.callbacks.TensorBoard(
                    log_dir=self.logDir, histogram_freq=0, write_graph=True
                )
                self.model.fit(state, target_f, epochs=1, verbose=VERBOSETRAIN, callbacks=callbacks)
            else:
                self.model.fit(state, target_f, epochs=1, verbose=VERBOSETRAIN)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def train(self, env, STT):
        self.SaveToTensorboard = STT

        done = False
        env.reset()

        while not done:
            obs = env.get_obs()
            action = self.ModelClass.act(
                obs, self.epsilon, self.action_size, self.model
            )
            state, action, reward, next_state, doneEnv = env.step(action)

            if doneEnv == 1:
                done = True
                self.ModelClass.remember(
                    state, action, reward, next_state, True, self.memory
                )

        if len(self.memory) > self.batch_size:
            self.replay(self.batch_size)
