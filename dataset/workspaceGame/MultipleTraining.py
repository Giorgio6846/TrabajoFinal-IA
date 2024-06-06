import os
import gymnasium as gym
from gymnasium.vector import AsyncVectorEnv

from Agent import DQNAgent
from Environment import BJEnvironment
from Tools import SaveModel

VERSION = 1
EPOCH = 1
COMPLETEDVERSION = 1

class MultiEnvironments: 
    def __init__(self, num_envs):
        self.envs = AsyncVectorEnv([lambda: BJEnvironment() for _ in range(num_envs)])

    def make_env(self):
        return BJEnvironment()

class Network:
    def __init__(self):
        

if __name__ == "__main__":
    EPISODES = 100
    state_size = 3  # player_sum, dealer_card, usable_ace
    action_size = 3  # hit, stay, double
    batch_size = 32

    agent = DQNAgent(state_size, action_size, 0.01, EPISODES, batch_size)
    save = SaveModel()
    environments = MultiEnvironments(8)

    print(environments.envs.reset())

    #for ep in range(EPISODES):
    #    print(ep)
    #    agent.train(env)
    
    save.saveModel(agent.model, VERSION, COMPLETEDVERSION)