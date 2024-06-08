from Blackjack.Agent import DQNAgent
from Blackjack.Environment import BJEnvironment
from Blackjack.Tools import SaveModel

VERSION = 2
COMPLETEDVERSION = 1

if __name__ == "__main__":
    EPISODES = 2500

    batch_size = 32

    env = BJEnvironment()
    agent = DQNAgent(env.state_size, env.action_size, 0.01, EPISODES, batch_size, "./models/v{VERSION}/logs".format(VERSION=VERSION))
    save = SaveModel()

    for ep in range(EPISODES):
        if ep % 10 == 0:        
            print(ep)
            agent.train(env, True)
        else:
            print(ep)
            agent.train(env, False)

    save.saveModel(agent.model, VERSION, COMPLETEDVERSION)
