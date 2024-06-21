import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from threading import Thread, Lock
import numpy as np
import tensorflow as tf
import platform

from lib.Game.Environment import BJEnvironment
from lib.Model.Tools import ModelA3C

VERBOSETRAIN = 1
LOGSPATH = "./models/v{VERSION}/logs"

GAMMA = 0.99
LR_Actor = 0.01
LR_Critic = 0.01
UPDATE_INTERVAL = 5

NUM_WORKERS = 8

EPISODE = 0

class Actor:
    def __init__(self, state_size, action_size):
        self.ModelClass = ModelA3C(state_size, action_size)
        self.entropy_beta = 0.01

        self.ModelClass._build_modelActor()
        if platform.system() == "Darwin" and platform.processor() == "arm":
            self.opt = tf.keras.optimizers.legacy.Adam(learning_rate=LR_Actor)
        else:
            self.opt = tf.keras.optimizers.Adam(learning_rate=LR_Actor)

    def compute_loss(self, actions, logits, advantages):
        ce_loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        entropy_loss = tf.keras.losses.CategoricalCrossentropy(from_logits=True)
        actions = tf.cast(actions, tf.int32)
        policy_loss = ce_loss(actions, logits, sample_weight=tf.stop_gradient(advantages))
        entropy = entropy_loss(logits, logits)
        return policy_loss - self.entropy_beta * entropy

    def train(self,states, actions, advantages):
        with tf.GradientTape() as tape:
            logits = self.ModelClass.model(states, training = True)
            loss = self.compute_loss(
                actions, logits, advantages
            )
        grads = tape.gradient(loss, self.ModelClass.model.trainable_variables)
        self.opt.apply_gradients(zip(grads, self.ModelClass.model.trainable_variables))
        return loss

class Critic:
    def __init__(self, state_size, action_size):
        self.ModelClass = ModelA3C(state_size, action_size)
        self.entropy_beta = 0.01

        self.ModelClass._build_modelCritic()
        if platform.system() == "Darwin" and platform.processor() == "arm":
            self.opt = tf.keras.optimizers.legacy.Adam(learning_rate=LR_Critic)
        else:
            self.opt = tf.keras.optimizers.Adam(learning_rate=LR_Critic)

    def compute_loss(self, v_pred, td_targets):
        mse = tf.keras.losses.MeanSquaredError()
        return mse(td_targets, v_pred)
    
    def train(self,states, td_targets):
        with tf.GradientTape() as tape:
            v_pred = self.ModelClass.model(states, training = True)
            assert v_pred.shape == td_targets.shape
            loss = self.compute_loss(v_pred, tf.stop_gradient(td_targets))
        grads = tape.gradient(loss, self.ModelClass.model.trainable_variables)
        return loss

class Worker(Thread):
    def __init__(self,env, global_actor, global_critic, max_episodes):
        Thread.__init__(self)
        self.lock = Lock()
        self.env = env
        self.state_dim = self.env.state_size
        self.action_dim = self.env.action_size

        self.max_episodes = max_episodes
        self.global_actor = global_actor
        self.global_critic = global_critic
        self.actor = Actor(self.state_dim, self.action_dim)
        self.critic = Critic(self.state_dim, self.action_dim)

        self.actor.ModelClass.model.set_weights(
            self.global_actor.ModelClass.model.get_weights()
        )
        self.critic.ModelClass.model.set_weights(
            self.global_critic.ModelClass.model.get_weights()
        )

    def n_step_td_target(self, rewards, next_v_value, done):
        td_targets = np.zeros_like(rewards)
        cumulative = 0
        if not done:
            cumulative = next_v_value

        for k in reversed(range(0, len(rewards))):
            cumulative = GAMMA * cumulative + rewards[k]
            td_targets[k] = cumulative
        return td_targets

    def advantage(self, td_targets, baselines):
        return td_targets - baselines

    def list_to_batch(self, list):
        batch = list[0]
        for elem in list[1:]:
            batch = np.append(batch, elem, axis = 0)
        return batch

    def train(self):
        global EPISODE

        while self.max_episodes >= EPISODE:
            state_batch = []
            action_batch = []
            reward_batch = []
            episode_reward, done = 0, False

            self.env.reset(5)
            state = self.env.get_obs()

            while not done:
                probs = self.actor.ModelClass.model.predict(np.reshape(state, [1,self.state_dim]))
                action = np.random.choice(self.action_dim, p=probs[0])

                state, action, reward, next_state, done = self.env.step(action)

                state = np.reshape(state, [1, self.state_dim])
                action = np.reshape(action, [1,1])
                next_state = np.reshape(next_state, [1, self.state_dim])
                reward = np.reshape(reward, [1,1])

                state_batch.append(state)
                action_batch.append(action)
                reward_batch.append(reward)

                if len(state_batch) >= UPDATE_INTERVAL or done:
                    states = self.list_to_batch(state_batch)
                    actions = self.list_to_batch(action_batch)
                    rewards = self.list_to_batch(reward_batch)

                    next_v_value = self.critic.ModelClass.model.predict(next_state)
                    td_targets = self.n_step_td_target(rewards, next_v_value, done)
                    advantages = td_targets - self.critic.ModelClass.model.predict(states)

                    with self.lock:
                        actor_loss = self.global_actor.train(
                            states, actions, advantages
                        )
                        critic_loss = self.global_critic.train(
                            states, td_targets
                        )

                        self.actor.ModelClass.model.set_weights(
                            self.global_actor.get_weights()
                        )

                        self.critic.ModelClass.model.set_weights(
                            self.global_critic.get_weights()
                        )

                    state_batch = []
                    action_batch = []
                    reward_batch = []
                    td_target_batch = []
                    advatange_batch = []

                episode_reward += reward[0][0]
                state = next_state[0]

            print(f'Episode {EPISODE} Episode Reward={episode_reward}')
            EPISODE += 1

    def run(self):
        self.train()

class Agent:
    def __init__(self):
        env = BJEnvironment()
        self.state_dim = env.state_size
        self.action_dim = env.action_size
        
        self.global_actor = Actor(self.state_dim, self.action_dim)
        self.global_critic = Critic(self.state_dim, self.action_dim)
        
        self.num_workers = NUM_WORKERS
        
    def train(self, max_episodes = 1000):
        workers = []

        for i in range(self.num_workers):
            env = BJEnvironment()
            workers.append(Worker(env, self.global_actor, self.global_critic, max_episodes))
            
        for worker in workers:
            worker.start()
            
        for worker in workers:
            worker.join()
