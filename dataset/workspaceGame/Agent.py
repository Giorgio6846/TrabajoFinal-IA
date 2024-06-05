from tensorflow.keras import layers, models
from tensorflow.keras.optimizers import Adam
from collections import deque
import numpy as np
import random

class DQNAgent:
    def __init__(self, state_size, action_size, alpha=0.01, episodes = 100, batch_size = 32):
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
        self.model = self._build_model()  # construcción del modelo DQN

    def _build_model(self):
        model = models.Sequential()
        model.add(layers.Dense(24, input_dim=self.state_size, activation="relu"))
        model.add(layers.Dense(24, activation="relu"))
        model.add(layers.Dense(self.action_size, activation="linear"))
        custom_optimizer = Adam(learning_rate=0.01)
        model.compile(loss="mse", optimizer=custom_optimizer)
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(
                    self.model.predict(next_state)[0]
                )
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def train(self, env):
        done = False
        env.reset()
        
        while not done:
            obs = env.get_obs()
            action = self.act(obs)
            state, action, reward, next_state, doneEnv = env.step(action)
            
            if doneEnv == 1:
                done = True
                self.remember(state, action, reward, next_state, True)        
        
            if len(self.memory) > self.batch_size:
                self.replay(self.batch_size)