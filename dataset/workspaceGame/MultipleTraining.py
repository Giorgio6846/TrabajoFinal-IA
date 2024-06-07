import os
import gymnasium as gym
from gymnasium.vector import AsyncVectorEnv
import tensorflow as tf

from Agent import DQNAgent
from Environment import BJEnvironment
from Tools import SaveModel, _build_model

VERSION = 1
EPOCH = 1
COMPLETEDVERSION = 1

class MultiEnvironments: 
    def __init__(self, num_envs):
        self.envs = AsyncVectorEnv([lambda: BJEnvironment() for _ in range(num_envs)])

    def make_env(self):
        return BJEnvironment()

"""
Makes the instances for the model to train
Recives the model from the coordinator to train
Sets the ports for the computer to work on
"""
class WorkerPC:
    def __init__(self):
        self.Agent = DQNAgent()
        self.env = BJEnvironment()

"""
Merges the models that receives from the other instances
Has a dictionary to know which workers are on the network
Has a queue if it receives more than one model at the time
"""
class Coordinator:
    def __init__(self, state_size, action_size, episodes, batch_size):
        self.episodes = episodes
        self.batch_size = batch_size

        self.model = _build_model(state_size, action_size)

    def merge_networks(self, newModel):
        # Assuming net1 and net2 have the same architecture
        new_net = tf.keras.models.clone_model(self.model)
        new_net.build(
            self.model.input_shape
        )  # Build the model with the correct input shape

        weights1 = self.model.get_weights()
        weights2 = newModel.get_weights()

        new_weights = [(w1 + w2) / 2.0 for w1, w2 in zip(weights1, weights2)]
        new_net.set_weights(new_weights)

        self.model = new_net

if __name__ == "__main__":
    EPISODES = 2500
    state_size = 3  # player_sum, dealer_card, usable_ace
    action_size = 3  # hit, stay, double
    batch_size = 32

    agent = DQNAgent(state_size, action_size, 0.01, EPISODES, batch_size, "./models/v{VERSION}/logs".format(VERSION=VERSION))
    save = SaveModel(state_size, action_size, EPISODES, batch_size)

    env = BJEnvironment()

    for ep in range(EPISODES):
        if ep % 10 == 0:        
            print(ep)
            agent.train(env, True)
        else:
            print(ep)
            agent.train(env, False)

    save.saveModel(agent.model, VERSION, COMPLETEDVERSION)
