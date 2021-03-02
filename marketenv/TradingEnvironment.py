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
