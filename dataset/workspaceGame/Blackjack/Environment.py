import gymnasium as gym
from gymnasium import spaces
import numpy as np

from Blackjack.Blackjack import BlackjackGame

class BJEnvironment(gym.Env):
    def __init__(self):
        super(BJEnvironment, self).__init__()
        self.game = BlackjackGame()
        self.bet = 5
        self.deck_min_len = 109
        self.state_size = 3
        self.action_size = 3        
        self.observation_space = spaces.Box(0, 50, shape=(3,), dtype=np.int8)
        self.action_space = spaces.Discrete(3)

    @staticmethod
    def has_usable_ace(hand):
        """Check if the hand has a usable ace."""
        value, ace = 0, False
        for card in hand:
            card_number = card["number"]
            value += min(
                10, int(card_number) if card_number not in ["J", "Q", "K", "A"] else 11
            )
            ace |= card_number == "A"
        return int(ace and value + 10 <= 21)

    def step(self, action):
        act_string = ["hit", "stay", "double"][action]
        state = self.get_obs()
        bet = self.game.bet_game
        status = self.game.player_action(act_string)

        if status[1] == "continue":
            reward = 0
    
            bet = self.game.return_bounty(self.bet, act_string)

            if status[1] == "player_blackjack":
                reward += self.bet
            elif status[1] == "player_bust":
                reward -= self.bet

            done = status[1] in ["player_blackjack", "player_bust"]

            return state, action, reward, self.get_obs(), done

        final_result = self.game.game_result()
        final_reward = (
            bet if final_result == "win" else (-bet if final_result == "loss" else 0)
        )

        return state, action, final_reward, self.get_obs(), True

    def get_obs(self):
        dealer_card = (
            int(self.game.dealer_hand[0]["number"])
            if self.game.dealer_hand[0]["number"] not in ["J", "Q", "K", "A"]
            else (10 if self.game.dealer_hand[0]["number"] != "A" else 11)
        )

        player_sum = self.game.hand_value(self.game.player_hand)
        usable_ace = self.has_usable_ace(self.game.player_hand)
        state = np.array([player_sum, dealer_card, usable_ace])
        state = state.astype(np.int8)
        state = np.reshape(state, [1, self.state_size])
        return state

    def reset(self):
        
        if (len(self.game.get_deck()) <= self.deck_min_len):
            self.game.regenerate_deck()
        
        self.game.start_game(self.bet)
         
        self.status = ["act", "continue"]

        return self.get_obs(), {}