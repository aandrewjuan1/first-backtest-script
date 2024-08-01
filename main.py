import backtrader as bt
from datetime import datetime

# Create a Cerebro instance
cerebro = bt.Cerebro()

# Define the data feeds
class MinutesCSVData(bt.feeds.GenericCSVData):
    params = (
        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', -1),
        ('separator', '\t'),
        ('dtformat', '%Y.%m.%d %H:%M:%S'),
        ('timeframe', bt.TimeFrame.Minutes)
    )

class DailyCSVData(bt.feeds.GenericCSVData):
    params = (
        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', -1),
        ('separator', '\t'),
        ('dtformat', '%Y.%m.%d'),
        ('timeframe', bt.TimeFrame.Days)
    )

# Create data feed instances
h1_data = MinutesCSVData(
    dataname='EURUSDH1.csv',
    fromdate=datetime(2023, 1, 2),
    todate=datetime(2023, 12, 29)
)

m15_data = MinutesCSVData(
    dataname='EURUSDM15.csv',
    fromdate=datetime(2023, 1, 2),
    todate=datetime(2023, 12, 29)
)

daily_data = DailyCSVData(
    dataname='EURUSDDAILY.csv',
    fromdate=datetime(2023, 1, 2),
    todate=datetime(2023, 12, 29)
)

# Add the data feeds to Cerebro
cerebro.adddata(h1_data, name='H1 Data')
cerebro.adddata(m15_data, name='M15 Data')
cerebro.adddata(daily_data, name='Daily Data')

# Define the strategy
class LondonReversalStrategy(bt.Strategy):

    """
    1. skip monday
    2. only trade london killzone onwards, 7 am UTC
    3. mark previous daily high and low
    4. when it's london killzone, go to m15 and wait for the candle to reach either of previous daily high or low
    5 if reached, wait for the reversal (apply the entry rule)

    M15 pattern, entry rule:
        two executive candle; 
            if the high is reached, 2 bearish m15 candle,
            if the low is reached, 2 bullish m15 candle

    """
    pass

# Add the strategy to Cerebro
cerebro.addstrategy(LondonReversalStrategy)

# Set the broker
cerebro.broker.set_cash(10000)  # Starting cash
cerebro.broker.setcommission(commission=0.001)  # Commission per trade (e.g., 0.1%)

# Print starting cash
print(f'Starting Portfolio Value: {cerebro.broker.getvalue()}')

# Run the strategy
cerebro.run()

# Print final cash and portfolio value
print(f'Ending Portfolio Value: {cerebro.broker.getvalue()}')

# Plot the results
cerebro.plot()
