from collections import deque
import numpy as np
import config as cfg


class State:

    def __init__(self, prices, initial_balance=cfg.INITIAL_BALANCE, n_pairs=cfg.N_PAIRS, max_trades=cfg.MAX_TRADES,
                 ticks=cfg.TICKS_OBS):
        self.balance = initial_balance
        self.prices = deque(prices, maxlen=ticks)
        self.trades = {'volumes': np.zeros(max_trades),
                       'pips': np.zeros(max_trades)}

    def _close_trade(self, trade_idx, volume):
        if 0 < self.trades['volumes'][trade_idx] <= volume:
            # update balance, TODO aggiungere commissioni
            true_volume = min(abs(volume), self.trades['volumes'][trade_idx])
            self.balance += self.trades['pips'][trade_idx] * true_volume
            self.trades['volumes'][trade_idx] -= true_volume
            if self.trades['volumes'][trade_idx] == 0:
                self.trades['pips'][trade_idx] = 0
        else:
            pass

    def _open_trade(self, trade_idx, volume):
        # index // cfg.MAX_TRADES --> l'indice della pair a cui si riferisce l'index
        # pair_index = index // cfg.MAX_TRADES
        # TODO non fare l'azione se il margine
        # perform buy action
        # available_amount = self.state[0] // self.state[index + 1]
        # print('available_amount:{}'.format(available_amount))

        if self.trades['volumes'][trade_idx] == 0:
            self.trades['volumes'][trade_idx] = volume
            # pips
            self.trades['pips'][trade_idx] = cfg.SPREAD_BROKER * volume  # TODO fare funzione in cfg
        else:
            # this trade is already open
            pass

    def compute_asset_value(self):
        return self.balance + np.sum([vol * pips * 10 for vol, pips in zip(self.trades['volumes'], self.trades['pips'])])

    def execute_actions(self, actions):
        for idx in np.argwhere(actions < 0).reshape(-1):
            self._close_trade(idx, actions[idx])

        for idx in np.argwhere(actions > 0).reshape(-1):
            self._open_trade(idx, actions[idx])

    def next_timestep(self, prices):
        self.prices.appendleft(prices)
        # TODO updates trades
        before = self.prices[1]
        after = self.prices[0]
        pips_diff = np.array(after - before) * 10000
        open_trades = np.argwhere(self.trades['volumes'] != 0)
        for idx in open_trades:
            self.trades['pips'][idx] += pips_diff

    def to_numpy(self):
        pass
