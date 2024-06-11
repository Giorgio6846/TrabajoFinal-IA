import gymnasium as gym
from gymnasium import spaces
import numpy as np

from Blackjack.Blackjack import BlackjackGame

class BJEnvironment(gym.Env):
    def __init__(self):
        self.game = BlackjackGame()
        self.deck_min_len = 109

        # player_sum, dealer_sum, usable_ace, split_pos, double_pos, prob_21, game_state
        # game_state = 0 normal, 1 split, 2 double
        self.state_size = 7

        # Hit, Stand, Split, Double
        self.action_size = 4

        self.observation_space = spaces.Box(0, 100, shape=(self.state_size,), dtype=np.uint8)
        self.action_space = spaces.Discrete(self.action_size)

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
        act_string = ["hit", "stay", "double", "split"][action]
        state = self.get_obs()
        bet = self.game.bet_game
        status = self.game.player_action(act_string)

        if status[1] == "continue":
            reward = 0

            bet = self.game.return_bounty(self.bet, act_string)
            
            if self.game.badMove:
                reward = -100
            
            if status[1] == "player_blackjack":
                reward += bet
            elif status[1] == "player_bust":
                reward -= bet

            done = status[1] in ["player_blackjack", "player_bust"]

            return state, action, reward, self.get_obs(), done

        final_result = self.game.game_result()
        final_reward = (
            self.game.bet_game
            if final_result == "win"
            else (-self.game.bet_game if final_result == "loss" else 0)
        )
        print(self.game.game_result())

        return state, action, final_reward, self.get_obs(), True

    def get_obs(self):
        # player_sum, dealer_sum, usable_ace, split_pos, double_pos, prob_21, game_state
        player_sum = self.game.hand_value(self.game.player_hand)
        dealer_card = self.game.hand_value(self.game.dealer_hand)
        if self.game.firstTurn:
            dealer_card = self.game.hand_value(self.game.dealer_hand[:1])
        usable_ace = self.has_usable_ace(self.game.player_hand)
        split_possibility = (
            len(self.game.player_hand) == 2
            and self.game.player_hand[0]["number"] == self.game.player_hand[1]["number"]
        )
        double_possibility = self.game.firstTurn
        prob_21 = self.game.get_prob_of21()
        game_state = self.game.status

        state = np.array(
            [
                player_sum,
                dealer_card,
                usable_ace,
                split_possibility,
                double_possibility,
                prob_21,
                game_state,
            ]
        )
        state = state.astype(np.uint8)
        state = np.reshape(state, [1, self.state_size])
        return state

    def reset(self, bet):

        self.bet = bet

        if (len(self.game.get_deck()) <= self.deck_min_len):
            self.game.regenerate_deck()

        self.game.start_game(self.bet)

        self.status = ["act", "continue"]

        return self.get_obs(), {}