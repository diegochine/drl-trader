# PREPROCESSING
HEADERS = ['Timestamp', 'open', 'high', 'low', 'close', 'volume']

# ENV
INITIAL_BALANCE = 1000
SPREAD_BROKER = -1
N_PAIRS = 1         # number of pairs
MAX_TRADES = 5      # maximum allowed trades for each pair
TICKS_OBS = 10      # number of ticks in the state, for each pair
MAX_LOTS = 1       # maximum lots that can be opened in a single trade (divide by 100)

# Shape = 181: [Current Balance] + [prices 1-PAIRS_DIM]
# + [open trades 1-PAIRS_DIM * MAX_TRADES
#   and each trade is pair of two numbers representing volume(real) and pips(int)]

SPACE_SHAPE = (1 + N_PAIRS + MAX_TRADES*N_PAIRS*2,)
ACTION_SHAPE = (MAX_TRADES*N_PAIRS,)
