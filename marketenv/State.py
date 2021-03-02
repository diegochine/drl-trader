from collections import deque
import numpy as np
import config as cfg


class State:

    def __init__(self, prices, initial_balance=cfg.INITIAL_BALANCE, n_pairs=cfg.N_PAIRS, max_trades=cfg.MAX_TRADES,
                 ticks=cfg.TICKS_OBS):
        self.balance = initial_balance
        self.prices = deque(prices, maxlen=ticks)
        self.trades = np.zeros(2*max_trades)

    def to_numpy(self):
        pass
