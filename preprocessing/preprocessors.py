import numpy as np
import pandas as pd

from preprocessing.utils import get_data


def load_dataset(pairs, years):
    # many pairs eheh
    pass


def aggregate_df(df, tf='5min'):
    conversion = {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}
    df = df.resample(tf).aggregate(conversion)
    return df

