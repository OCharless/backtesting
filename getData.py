from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from binance import Client
import pandas as pd


def print_file(pair, name, initial_date, final_date):
    client = Client("", "")

    # request historical candle (or klines) data
    bars = client.get_historical_klines(pair, Client.KLINE_INTERVAL_1DAY, initial_date, final_date)
    
    # delete unwanted data - just keep date, open, high, low, close
    for line in bars:
        del line[6:]
    
    # save as CSV file 
    df = pd.DataFrame(bars, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    #df.set_index('Date', inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], unit='ms', origin='unix')
    df.to_csv(name) 
