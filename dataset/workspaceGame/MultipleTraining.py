from Blackjack.Agent import DQNAgent
from Blackjack.Environment import BJEnvironment
from dataset.workspaceGame.Blackjack.Tools import SaveModel

VERSION = 2
COMPLETEDVERSION = 1

"""
Makes the instances for the model to train
Recives the model from the coordinator to train
Sets the ports for the computer to work on
"""

"""
Merges the models that receives from the other instances
Has a dictionary to know which workers are on the network
Has a queue if it receives more than one model at the time
"""

if __name__ == "__main__":
    EPISODES = 600
    state_size = 3  # player_sum, dealer_card, usable_ace
    action_size = 3  # hit, stay, double
    batch_size = 32

    agent = DQNAgent(state_size, action_size, 0.01, EPISODES, batch_size, "./models/v{VERSION}/logs".format(VERSION=VERSION))
    save = SaveModel()

    env = BJEnvironment()

    for ep in range(EPISODES):
        if ep % 10 == 0:        
            print(ep)
            agent.train(env, True)
        else:
            print(ep)
            agent.train(env, False)

    save.saveModel(agent.model, VERSION, COMPLETEDVERSION)
