from Blackjack.Environment import BJEnvironment
from Blackjack.Tools import Model

VERSION = 1
COMPLETEDVERSION = 2
VERBOSETRAIN = 1

class Test:
    def __init__(self):
        self.env = BJEnvironment()
        self.ModelClass = Model(self.env.state_size,self.env.action_size)

        self.state_size = 3

    def play(self, bet):
        self.env.reset(bet)

        done = False

        while not done:
            obs = self.env.get_obs()
            action = self.ModelClass.predict(obs)
            state, action, reward, next_state, done = self.env.step(action)

            if self.env.get_badmove:
                done = True

        final_result = "win" if reward > 0 else ("loss" if reward < 0 else "draw")
        return final_result

if __name__ == "__main__":
    TestClass = Test()
    TestClass.ModelClass.loadModel(VERSION, COMPLETEDVERSION)
        
    # Evaluate the agent
    test_games = 5000
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
        elif result == "badmove":
            nf += 1

    print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")
    print(f"Win rate: {wins / (wins + losses) * 100:.2f}%")
    print(f"Not Finished: {nf}")
