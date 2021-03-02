import numpy as np
import pandas as pd
import gym
from gym.utils import seeding
from gym import spaces
import matplotlib

from marketenv.TradingEnvironment import TradingEnvironment
from marketenv.State import State

matplotlib.use('Agg')  # boh, verificare
import matplotlib.pyplot as plt
import pickle
import config as cfg


class ForexEnvironment(TradingEnvironment):
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super().__init__(df)

        self.trade_fee = 0.0003  # unit

        # action_space normalization and shape is STOCK_DIM
        self.action_space = spaces.Box(low=-cfg.MAX_LOTS, high=cfg.MAX_LOTS, shape=cfg.ACTION_SHAPE, dtype=np.int)

        self.observation_space = spaces.Box(low=0, high=np.inf, shape=cfg.SPACE_SHAPE)

        # load data from a pandas dataframe
        self.time_step = cfg.TICKS_OBS
        self.prices = self.df.iloc[:self.time_step, :]
        self.terminal = False

        # initalize state
        self.state = State(self.prices.close.values.tolist())

        # memorize all the total balance change
        self.asset_memory = [cfg.INITIAL_BALANCE]
        self.rewards_memory = []
        # self.reset()
        self._seed()

    def step(self, actions):
        print(self.time_step)
        self.terminal = self.time_step >= len(self.df.index.unique()) - 1
        print(actions)

        if not self.terminal:
            # actions = actions * HMAX_NORMALIZE

            begin_total_asset = self.state.compute_asset_value()
            print("begin_total_asset:{}".format(begin_total_asset))

            self.state.execute_actions(actions)

            # next timestep, update pips and state
            self.time_step += 1
            self.prices = self.df.iloc[self.time_step, :]
            # load next state
            self.state.next_timestep(self.prices.close.tolist())

            end_total_asset = self.state.compute_asset_value()

            self.asset_memory.append(end_total_asset)
            print("end_total_asset:{}".format(end_total_asset))
            reward = end_total_asset - begin_total_asset
            print("step_reward:{}".format(reward))
            self.rewards_memory.append(reward)

            # self.reward = self.reward * REWARD_SCALING(1e-4)

        else:
            # TODO implementare step se state è terminal
            reward = 0

        return self.state.to_numpy(), reward, self.terminal, {}

    def reset(self):
        self.asset_memory = [cfg.INITIAL_BALANCE]
        self.time_step = cfg.TICKS_OBS
        self.prices = self.df.iloc[:self.time_step, :]
        self.terminal = False
        self.rewards_memory = []
        self.state = State(self.prices.close.values.tolist())
        return self.state.to_numpy()

    def render(self, mode='human'):
        return self.state

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
