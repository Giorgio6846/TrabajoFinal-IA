from Agent import DQNAgent
from Environment import BJEnvironment
from Tools import SaveModel


VERSION = 1
EPOCH = 1
COMPLETEDVERSION = 1



if __name__ == "__main__":
    EPISODES = 2500
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
