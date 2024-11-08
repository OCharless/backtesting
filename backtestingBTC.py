from backtesting import Strategy,Backtest
from backtesting.lib import crossover
from backtesting.test import GOOG
import pandas as pd
from getData import print_file
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def SMA(values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    return pd.Series(values).rolling(n).mean()


class SmaCross(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 10
    n2 = 20
    
    def init(self):
        # Precompute the two moving averages
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)
    
    def next(self):
        # If sma1 crosses above sma2, close any existing
        # short trades, and buy the asset
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()

        # Else, if sma1 crosses below sma2, close any existing
        # long trades, and sell the asset
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()

# Print file
filename = "BTCUSDT.csv"

print_file("BTCUSDT", "BTCUSDT.csv", "1 Jan, 2013", "7 Nov, 2024")


# Read file
prices = pd.read_csv(filename, index_col='Date', parse_dates=True)
            
            
bt = Backtest(prices, SmaCross, cash=10_000, commission=.002)
stats = bt.run()
# print(stats)
# bt.plot()

stats = bt.optimize(n1=range(5, 100, 1),
                    n2=range(6, 200, 1),
                    constraint=lambda param: param.n1 < param.n2,
                    maximize='Equity Final [$]',
                    )
print(stats)
print(stats._strategy)
bt.plot(plot_volume=False, plot_pl=False)
print('\n')
