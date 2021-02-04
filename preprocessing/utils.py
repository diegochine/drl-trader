from forex_python.converter import CurrencyRates

import os
import zipfile
import pandas as pd
from histdata import download_hist_data as dl


def get_symbols(size=10):
    return open('../symbols.txt', 'r').read().split('\n')[:size]


def get_pairs(size=10):
    return open('../pairs.txt', 'r').read().split('\n')[:size]


def download_data(pair, year):
    dir = f'data/{pair}/'
    if not f'{year}.csv' in os.listdir(dir):
        dl(year, pair=pair, output_directory=dir)
        file = dir + f'DAT_ASCII_{pair}_M1_{year}.zip'
        with zipfile.ZipFile(file) as zipf:
            zipf.extractall(dir)
        os.remove(file)
        file = file[:-3] + 'csv'
        os.rename(file, dir + f'{year}.csv')
        print(f'{pair} {year} downloaded')
    else:
        print(f'{pair} {year} already present')


def get_data(pairs=['EURUSD'], years=list(range(2010, 2018))):
    header = ['Timestamp', 'Bar OPEN Bid Quote', 'Bar HIGH Bid Quote',
              'Bar LOW Bid Quote', 'Bar CLOSE Bid Quote', 'Volume']
    dfs = []
    symbols = {pair[:3] for pair in pairs} | ({pair[3:] for pair in pairs})
    for pair in pairs:
        sym1 = pair[:3]
        sym2 = pair[3:]
        dir = f'data/{pair}/'
        if not os.path.exists(dir):
            os.mkdir(dir)
        for year in years:
            try:
                download_data(pair, year)
            except AssertionError:
                print(f'{pair} {year} no data available')
                continue
            df = pd.read_csv(dir + f'{year}.csv', sep=';', names=header)
            ts = df.iloc[:, 0].apply(lambda s: f'{s[:4]}-{s[4:6]}-{s[6:8]}T{s[9:11]}:{s[11:13]}')
            ts = pd.to_datetime(ts)
            df.iloc[:, 0] = ts
            df[sym1] = True
            df[sym2] = True
            for sym in symbols:
                if (sym != sym1) and (sym != sym2):
                    df[sym] = False
            dfs.append(df)
    df = pd.concat(dfs)
    df.drop(columns='Volume', inplace=True)
    df.set_index('Timestamp', inplace=True)
    return df
