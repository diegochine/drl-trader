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
        self.action_space = spaces.Box(low=-1, high=1, shape=(cfg.ACTION_SHAPE,))

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

    def _open_trade(self, index, volume, trade_type='buy'):
        # index // cfg.MAX_TRADES --> l'indice della pair a cui si riferisce l'index
        # pair_index = index // cfg.MAX_TRADES
        # TODO non fare l'azione se il margine
        # perform buy action
        # available_amount = self.state[0] // self.state[index + 1]
        # print('available_amount:{}'.format(available_amount))

        h_index = index + cfg.PAIRS_DIM + 1
        if self.state[h_index] == 0:
            self.state[h_index] = volume
            # pips
            self.state[h_index + 1] = cfg.SPREAD_BROKER * volume  # TODO fare funzione in cfg
            self.trades += 1
        else:
            pass

    def _close_trade(self, index, volume, trade_type='buy'):
        h_index = index + cfg.PAIRS_DIM + 1
        pair_index = index // cfg.MAX_TRADES
        # perform sell action
        if 0 < self.state[h_index] <= volume:
            # update balance, TODO aggiungere commissioni
            true_volume = min(abs(volume), self.state[h_index])
            self.state[0] += \
                self.state[pair_index + 1] * true_volume

            self.state[h_index] -= true_volume
            if self.state[h_index] == 0:
                self.state[h_index + 1] = 0
            self.trades += 1
        else:
            pass

    def step(self, actions):
        print(self.time_step)
        self.terminal = self.time_step >= len(self.df.index.unique()) - 1
        print(actions)

        if not self.terminal:
            # actions = actions * HMAX_NORMALIZE

            trades = self.state[(cfg.PAIRS_DIM + 1):]
            begin_total_asset = self.state[0] + \
                                np.sum([vol * pips * 10 for vol, pips in zip(trades[::2], trades[1::2])])
            print("begin_total_asset:{}".format(begin_total_asset))

            # exec action
            for idx in np.argwhere(actions < 0).reshape(-1):
                self._close_trade(idx, actions[idx])

            for idx in np.argwhere(actions > 0).reshape(-1):
                self._open_trade(idx, actions[idx])

            # next timestep, update pips and state
            self.time_step += 1
            self.data = self.df.loc[self.time_step, :]
            # load next state
            self.state = [self.state[0]] + \
                         self.data.close.values.tolist() + \
                         list(self.state[(cfg.PAIRS_DIM + 1):])
            self._update_pips_variance()

            # end_total_asset
            trades = self.state[cfg.PAIRS_DIM + 1:]
            end_total_asset = self.state[0] + \
                                np.sum([vol * pips * 10 for vol, pips in zip(trades[::2], trades[1::2])])

            self.asset_memory.append(end_total_asset)
            print("end_total_asset:{}".format(end_total_asset))
            self.reward = end_total_asset - begin_total_asset
            print("step_reward:{}".format(self.reward))
            self.rewards_memory.append(self.reward)

            # self.reward = self.reward * REWARD_SCALING(1e-4)

        else:
            # TODO implementare step se state è terminal
            pass

        return self.state, self.reward, self.terminal, {}

    def _update_pips_variance(self):
        before = self.df.loc[self.time_step - 1, :]
        after = self.df.loc[self.time_step, :]
        pips_diff = np.array(after.close - before.close) * 10000
        trades = self.state[cfg.PAIRS_DIM + 1:]
        open_trades = np.argwhere(trades[::2] != 0)
        for idx in open_trades:
            self.state[cfg.PAIRS_DIM + 1 + idx + 1] += pips_diff[idx//cfg.MAX_TRADES*2]

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
