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
    batchSize = 32

    env = BJEnvironment()
    agent = DQNAgent(env.state_size, env.action_size, 0.01, EPISODES, batchSize, "./models/v{VERSION}/logs".format(VERSION=VERSION))
    save = SaveModel()

    for ep in range(EPISODES):
        if ep % 10 == 0:        
            print(ep)
            agent.train(env, True)
        else:
            print(ep)
            agent.train(env, False)

    save.saveModel(agent.model, VERSION, COMPLETEDVERSION)
