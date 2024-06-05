import numpy as np
import random
from collections import deque
from blackjack import BlackjackGame
from tensorflow.keras import layers, models
import tensorflow as tf
from tensorflow.keras.optimizers import Adam

class DQN:

    def __init__(self, state_size, action_size, alpha=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.alpha = alpha
        self.memory = deque(maxlen=2000)  # Aquí se define la memoria de repetición
        self.gamma = 0.95    # factor de descuento para las recompensas futuras
        self.epsilon = 0.9   # tasa de exploración inicial
        self.epsilon_min = 0.01  # tasa de exploración mínima
        self.epsilon_decay = 0.995  # factor de decaimiento de la tasa de exploración
        self.model = self._build_model()  # construcción del modelo DQN

    def _build_model(self):
        model = models.Sequential()
        model.add(layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(layers.Dense(24, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        custom_optimizer = Adam(learning_rate=0.01)
        model.compile(loss='mse', optimizer=custom_optimizer)
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
    @staticmethod
    def has_usable_ace(hand):
        """Check if the hand has a usable ace."""
        value, ace = 0, False
        for card in hand:
            card_number = card['number']
            value += min(10, int(card_number) if card_number not in ['J', 'Q', 'K', 'A'] else 11)
            ace |= (card_number == 'A')
        return int(ace and value + 10 <= 21)

    def train(self, episodes, batch_size):
        one_percent = round(episodes / 100)

        for ep in range(episodes):
            print(ep)
            game = BlackjackGame()
            bet = 5
            game.start_game(bet)

            if ep % one_percent == 0:
                progress = (ep / episodes) * 100
                print(f"Training progress: {progress:.2f}%")

            dealer_card = int(game.dealer_hand[0]['number']) if game.dealer_hand[0]['number'] not in ['J', 'Q', 'K', 'A'] else (
                10 if game.dealer_hand[0]['number'] != 'A' else 11)
            status = ["act","continue"]

            while status[1] == "continue":
                player_sum = game.hand_value(game.player_hand)
                usable_ace = self.has_usable_ace(game.player_hand)
                state = np.array([player_sum, dealer_card, usable_ace])
                state = np.reshape(state, [1, self.state_size])
                action = self.act(state)
                action_str = ["hit", "stay", "double"][action]
                bet = game.return_bounty(bet, action_str)
                status = game.player_action(action_str)
                new_player_sum = game.hand_value(game.player_hand)
                new_usable_ace = self.has_usable_ace(game.player_hand)
                next_state = np.array([new_player_sum, dealer_card, new_usable_ace])
                next_state = np.reshape(next_state, [1, self.state_size])

                reward = 0  # Intermediate reward, only final matters

                if status[1] == "player_blackjack":
                    reward += bet
                elif status[1] == "player_bust":
                    reward -= bet

                if reward != 0:
                    done = status[1] in ["player_blackjack", "player_bust"]
                    self.remember(state, action, reward, next_state, done)

                if status[0] == "stay":
                    break

            final_result = game.game_result()
            final_reward = bet if final_result == "win" else (-bet if final_result == "loss" else 0)
            self.remember(state, action, final_reward, next_state, True)

            if len(self.memory) > batch_size:
               self.replay(batch_size)

    def play(self, bet):
        game = BlackjackGame()
        game.start_game(bet)

        print("Dealer shows:", game.format_cards(game.dealer_hand[:1]))
        status = ["act", "continue"]
        print(game.format_cards(game.player_hand), game.hand_value(game.player_hand))
        while status[1] == "continue":
            player_sum = game.hand_value(game.player_hand)
            usable_ace = self.has_usable_ace(game.player_hand)
            dealer_card = int(game.dealer_hand[0]['number']) if game.dealer_hand[0]['number'] not in ['J', 'Q', 'K', 'A'] else (
                10 if game.dealer_hand[0]['number'] != 'A' else 11)
            state = np.array([player_sum, dealer_card, usable_ace])
            state = np.reshape(state, [1, self.state_size])
            action = self.act(state)
            action_str = ["hit", "stay", "double"][action]
            status = game.player_action(action_str)

            if action_str == "stay":
                break

            print(game.format_cards(game.player_hand), game.hand_value(game.player_hand))

        if status[1] == "continue":
            print("Dealer has:", game.format_cards(game.dealer_hand), game.hand_value(game.dealer_hand))
            game.dealer_action()

        final_result = game.game_result()
        return final_result


if __name__ == "__main__":
    EPISODES = 1000
    state_size = 3  # player_sum, dealer_card, usable_ace
    action_size = 3  # hit, stay, double
    agent = DQN(state_size, action_size)
    batch_size = 32

    agent.train(500000, batch_size)

    # Evaluate the agent
    test_games = 100000
    wins, losses, draws = 0, 0, 0

    for index in range(test_games):
        print("-----")
        bet = 5
        result = agent.play(bet)
        print(result)
        if result == "win":
            wins += 1
        elif result == "loss":
            losses += 1
        elif result == "draw":
            draws += 1

    print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")
    print(f"Win rate: {wins / (wins + losses) * 100:.2f}%")