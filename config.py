# PREPROCESSING
HEADERS = ['Timestamp', 'open', 'high', 'low', 'close', 'volume']

# ENV
INITIAL_BALANCE = 1000
PAIRS_DIM = 1
MAX_TRADES = 5
# Shape = 181: [Current Balance] + [prices 1-PAIRS_DIM]
# + [open trades 1-PAIRS_DIM * MAX_TRADES
#   and each trade is pair of two numbers representing volume(real) and pips(int)]
SPACE_SHAPE = 1 + PAIRS_DIM + MAX_TRADES*PAIRS_DIM*2
ACTION_SHAPE = MAX_TRADES*PAIRS_DIM
