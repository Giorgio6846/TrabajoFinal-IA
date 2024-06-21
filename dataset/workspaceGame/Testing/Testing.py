from calendar import EPOCH
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.Game.Environment import BJEnvironment
from lib.Model.Tools import ModelDQN

VERSION = 4
COMPLETEDVERSION = 1
VERBOSETRAIN = 60
EPOCH = 33

class Test:
    def __init__(self):
        self.env = BJEnvironment()
        self.ModelClass = ModelDQN(self.env.state_size,self.env.action_size)

        self.state_size = 3

    def play(self, bet):
        self.env.reset(bet)

        done = False

        while not done:
            obs = self.env.get_obs()
            action = self.ModelClass.predict(obs)
            state, action, reward, next_state, done = self.env.step(action)

            if self.env.get_badmove():
                done = True

        final_result = self.env.get_final_result()
        return final_result

if __name__ == "__main__":
    TestClass = Test()
    TestClass.ModelClass.loadModel(VERSION, COMPLETEDVERSION)
    #TestClass.ModelClass.loadCheckpoint(VERSION, COMPLETEDVERSION, EPOCH)
        
    # Evaluate the agent
    test_games = 1000
    wins, losses, draws, nf, win_double = 0, 0, 0, 0, 0
    budget = 1000

    for index in range(1, test_games):
        print("-----")
        print(index)
        bet = 5
        result = TestClass.play(bet)
        print(result)
        if result == "win":
            wins += 1
            budget += 5
        elif result == "loss":
            losses += 1
            budget -= 5
        elif result == "draw":
            draws += 1
        elif result == "win_double":
            win_double += 1
            budget += 10
        elif result == "badmove":
            nf += 1
    total_profit = budget - 1000
    print(f"Total profit: {total_profit}")
    print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")
    print(f"Win rate: {wins / (wins + losses) * 100:.2f}%")
    print(f"Not Finished: {nf}")    
