# BacktestingBTC.py

## Overview

BacktestingBTC.py is a Python script designed to backtest trading strategies on Bitcoin (BTC) historical data. It uses the `backtesting` library to simulate trades and evaluate the performance of a simple moving average (SMA) crossover strategy.

## Features

- **SMA Crossover Strategy**: Implements a basic trading strategy based on the crossover of two simple moving averages.
- **Optimization**: Optimizes the parameters of the SMA crossover strategy to maximize final equity.
- **Data Handling**: Reads historical BTC price data from a CSV file.
- **Visualization**: Plots the backtest results, including price, trades, and equity curve.

## Requirements

- Python 3.x
- pandas
- backtesting
- matplotlib

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/backtestingbtc.git
    cd backtestingbtc
    ```

2. Install the required packages:
    ```sh
    pip install pandas backtesting matplotlib
    ```

## Usage

2. Run the script:
    ```sh
    python backtestingbtc.py
    ```

3. The script will print the optimization results and display the backtest plot.

## Code Explanation

### SMA Function

```python
def SMA(values, n):
    return pd.Series(values).rolling(n).mean()
```

Calculates the simple moving average of the given values over a window of `n` periods.

### SmaCross Strategy

```python
class SmaCross(Strategy):
    n1 = 10
    n2 = 20
    
    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)
    
    def next(self):
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()
```

Defines a trading strategy based on the crossover of two SMAs. When the shorter SMA (`sma1`) crosses above the longer SMA (`sma2`), it buys the asset. When `sma1` crosses below `sma2`, it sells the asset.

### Running the Backtest

```python
bt = Backtest(prices, SmaCross, cash=10_000, commission=.002)
stats = bt.run()
```

Runs the backtest on the historical price data with an initial cash amount of $10,000 and a commission of 0.2% per trade.

### Optimization

```python
stats = bt.optimize(n1=range(5, 100, 1),
                    n2=range(6, 200, 1),
                    constraint=lambda param: param.n1 < param.n2,
                    maximize='Equity Final [$]')
```

Optimizes the SMA parameters (`n1` and `n2`) to maximize the final equity.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Backtesting.py](https://kernc.github.io/backtesting.py/) library for backtesting trading strategies.
- [pandas](https://pandas.pydata.org/) library for data manipulation.
- [matplotlib](https://matplotlib.org/) library for plotting.
