import numpy as np
import pandas as pd
from gym.utils import seeding
import gym
from gym import spaces
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pickle
import config as cfg


class ForexEnvironment(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, df, time_step=0):
        super(ForexEnvironment, self).__init__()

        self.df = df
        self.time_step = time_step

        # action_space normalization and shape is STOCK_DIM
        self.action_space = spaces.Box(low=-1, high=1, shape=(cfg.PAIRS_DIM,))

        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(cfg.SPACE_SHAPE,))
        # load data from a pandas dataframe
        self.data = self.df.loc[self.time_step, :]
        self.terminal = False
        # initalize state
        self.state = [cfg.INITIAL_BALANCE] + \
                     self.data.close.values.tolist() + \
                     [0] * (cfg.MAX_TRADES * cfg.PAIRS_DIM * 2)
                     #self.data.macd.values.tolist() + \
                     #self.data.rsi.values.tolist() + \
                     #self.data.cci.values.tolist() + \
                     #self.data.adx.values.tolist()
        # initialize reward
        self.reward = 0
        self.cost = 0
        # memorize all the total balance change
        self.asset_memory = [cfg.INITIAL_BALANCE]
        self.rewards_memory = []
        self.trades = 0
        # self.reset()
        self._seed()

    def step(self, actions):
        print(self.time_step)
        self.terminal = self.time_step >= len(self.df.index.unique()) - 1
        print(actions)

        if not self.terminal:
            # actions = actions * HMAX_NORMALIZE
            # TODO modificare secondo discorso pips
            begin_total_asset = self.state[0] + \
                                sum(np.array(self.state[1:(cfg.PAIRS_DIM + 1)]) * np.array(
                                    self.state[(cfg.PAIRS_DIM + 1):(cfg.PAIRS_DIM * 2 + 1)]))
            print("begin_total_asset:{}".format(begin_total_asset))
        else:
            pass

    def reset(self):
        self.asset_memory = [cfg.INITIAL_BALANCE]
        self.time_step = 0
        self.data = self.df.loc[self.time_step, :]
        self.cost = 0
        self.trades = 0
        self.terminal = False
        self.rewards_memory = []
        # initiate state
        self.state = [cfg.INITIAL_BALANCE] + \
                     self.data.close.values.tolist() + \
                     [0] * (cfg.MAX_TRADES * cfg.PAIRS_DIM * 2)
                     # self.data.macd.values.tolist() + \
                     # self.data.rsi.values.tolist() + \
                     # self.data.cci.values.tolist() + \
                     # self.data.adx.values.tolist()
        # iteration += 1
        return self.state

    def render(self, mode='human'):
        return self.state

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
