import gym


class TradingEnvironment(gym.Env):

    metadata = {'render.modes': ['human']}

    def __init__(self, df, window_size):
        self.df = df
        self.window_size = window_size
        self.prices, self.signal_features = self._process_data()

    def _process_data(self):
        raise NotImplementedError

    def _calculate_reward(self, action):
        raise NotImplementedError

    def _update_profit(self, action):
        raise NotImplementedError
