import os
import gymnasium as gym

from Agent import DQNAgent
from Environment import BJEnvironment
from Tools import SaveModel

VERSION = 1
EPOCH = 1
COMPLETEDVERSION = 1

if __name__ == "__main__":
    EPISODES = 100
    state_size = 3  # player_sum, dealer_card, usable_ace
    action_size = 3  # hit, stay, double
    batch_size = 8

    agent = DQNAgent(state_size, action_size, 0.01, EPISODES, batch_size)
    save = SaveModel()

    env = BJEnvironment()
    
    #env = gym.vector.AsyncVectorEnv([
    #    lambda: BJEnvironment()
    #])

    for ep in range(EPISODES):
        print(ep)
        agent.train(env)
    
    save.saveModel(agent.model, VERSION, COMPLETEDVERSION)