import gym

from marketenv.State import State


class TradingEnvironment(gym.Env):

    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        self.df = df

    def reset(self):
        raise NotImplementedError

    def step(self, action):
        raise NotImplementedError

    def _process_data(self):
        raise NotImplementedError

    def _calculate_reward(self, action):
        raise NotImplementedError

    def _update_profit(self, action):
        raise NotImplementedError
