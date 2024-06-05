import os

from Agent import DQNAgent
from Environment import BJEnvironment

if __name__ == "__main__":
    EPISODES = 1000
    state_size = 3  # player_sum, dealer_card, usable_ace
    action_size = 3  # hit, stay, double
    batch_size = 32

    agent = DQNAgent(state_size, action_size, 0.01, EPISODES, batch_size)
    env = BJEnvironment()

    agent.train(env)

    checkpoint_path = "models/v{ver}/training_{trainVer}/cp-{epoch:04d}.weights.h5"
    checkpoint_dir = os.path.dirname(checkpoint_path)

    agent.model.save_weights(checkpoint_path.format(ver=1, trainVer=1, epoch=1))

    print(checkpoint_path)
    print(checkpoint_dir)
