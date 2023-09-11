import ccxt
import pandas as pd

# Initialize the Binance exchange object
exchange = ccxt.binance()

# Set the symbol for the trading pair (BTCUSDT) and the timeframe (15 minutes)
symbol = 'BTC/USDT'
timeframe = '15m'

# Define the number of candlesticks you want to retrieve
limit = 1000  # You can adjust this as needed

# Fetch historical OHLCV data
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

# Create a DataFrame from the data
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Drop the timestamp column
df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

# Save the DataFrame to a text file
df.to_csv('o.txt', sep='\t', index=False)
