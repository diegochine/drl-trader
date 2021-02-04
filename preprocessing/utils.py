import os
import zipfile
import pandas as pd
from histdata import download_hist_data as dl
import config as cfg


def get_symbols(size=10):
    return open('../symbols.txt', 'r').read().split('\n')[:size]


def get_pairs(size=10):
    return open('../pairs.txt', 'r').read().split('\n')[:size]


def download_data(pair, year):
    path = f'data/{pair}/'
    if f'{year}.csv' not in os.listdir(path):
        dl(year, pair=pair, output_directory=path)
        file = path + f'DAT_ASCII_{pair}_M1_{year}.zip'
        with zipfile.ZipFile(file) as zipf:
            zipf.extractall(path)
        os.remove(file)
        file = file[:-3] + 'csv'
        os.rename(file, path + f'{year}.csv')
        print(f'{pair} {year} downloaded')
    else:
        print(f'{pair} {year} already present')


def get_data(pair, years):
    path = f'data/{pair}/'
    dfs = []
    if not os.path.exists(path):
        os.mkdir(path)
    for year in years:
        try:
            download_data(pair, year)
        except AssertionError:
            print(f'{pair} {year} no data available')
            continue
        df = pd.read_csv(path + f'{year}.csv', sep=';', names=cfg.HEADERS)
        ts = df.iloc[:, 0].apply(lambda s: f'{s[:4]}-{s[4:6]}-{s[6:8]}T{s[9:11]}:{s[11:13]}')
        ts = pd.to_datetime(ts)
        df.iloc[:, 0] = ts
        dfs.append(df)
    df = pd.concat(dfs)
    # df.drop(columns='Volume', inplace=True)
    df.set_index('Timestamp', inplace=True)
    return df
