import numpy as np
import tensorflow as tf
from Blackjack.Environment import BJEnvironment
from Blackjack.Tools import SaveModel, Model

VERSION = 1
COMPLETEDVERSION = 1
VERBOSETRAIN = 1

class Test:
    def __init__(self, model):
        self.ModelClass = Model()
        self.env = BJEnvironment()
        self.model = model
        self.state_size = 3
        self.epsilon = 0

    def play(self, bet):
        
        self.env.reset()
        done = False
        total_reward = 0

        while not done:
            state = self.env.get_obs()
            action = self.act(state)
            state, action, bet, next_state, done = self.env.step(action)
            total_reward += bet

            if done:
                break

        final_result = "win" if total_reward > 0 else ("loss" if total_reward < 0 else "draw")
        return final_result


if __name__ == "__main__":
    save = SaveModel()
    model = save.loadModel(VERSION, COMPLETEDVERSION)

    TestClass = Test(model)

    # Evaluate the agent
    test_games = 10000
    wins, losses, draws = 0, 0, 0

    for index in range(1, test_games):
        print("-----")
        print(index)
        bet = 5
        result = TestClass.play(bet)
        print(result)
        if result == "win":
            wins += 1
        elif result == "loss":
            losses += 1
        elif result == "draw":
            draws += 1

    print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")
    print(f"Win rate: {wins / (wins + losses) * 100:.2f}%")
