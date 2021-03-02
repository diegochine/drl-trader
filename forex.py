from preprocessing.utils import get_data
from marketenv.ForexEnvironment import ForexEnvironment
from marketenv.State import State

if __name__ == "__main__":
    df = get_data('EURUSD', [2010])
    env = ForexEnvironment(df)

    for i_episode in range(20):
        observation = env.reset()
        for t in range(100):
            env.render()
            print(observation)
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)

