from preprocessing.utils import get_data
from marketenv.ForexEnvironment import ForexEnvironment
from marketenv.State import State

if __name__ == "__main__":
    df = get_data('EURUSD', [2010])
    env = ForexEnvironment(df)
    act = env.action_space.sample()
    print(act)
