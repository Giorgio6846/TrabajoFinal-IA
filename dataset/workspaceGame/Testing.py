import numpy as np
import tensorflow as tf
from Blackjack.Environment import BJEnvironment
from Blackjack.Tools import Model

VERSION = 3
COMPLETEDVERSION = 1
VERBOSETRAIN = 1

class Test:
    def __init__(self):
        self.env = BJEnvironment()
        self.ModelClass = Model(self.env.state_size,self.env.action_size)

        self.state_size = 3

    def play(self, bet):
        self.env.reset(bet)
        done = False
        total_reward = 0

        while not done:
            state = self.env.get_obs()
            action = self.ModelClass.predict(state)
            state, action, bet, next_state, done = self.env.step(action)
            if bet == -10:
                done = True
                return "BadMove"
                
            total_reward += bet

            if done:
                break

        final_result = "win" if total_reward > 0 else ("loss" if total_reward < 0 else "draw")
        return final_result
    
if __name__ == "__main__":
    TestClass = Test()
    TestClass.ModelClass.loadModel(VERSION, COMPLETEDVERSION)
        
    # Evaluate the agent
    test_games = 10000
    wins, losses, draws, nf = 0, 0, 0, 0

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
        elif result == "BadMove":
            nf += 1

    print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")
    print(f"Win rate: {wins / (wins + losses) * 100:.2f}%")
    print(f"Not Finished: {nf}")
