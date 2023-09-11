import ccxt
import pandas as pd

# Initialize the Binance exchange object
# exchange = ccxt.binance()

# # Set the symbol for the trading pair (BTCUSDT) and the timeframe (15 minutes)
# symbol = 'BTC/USDT'
# timeframe = '15m'

# # Define the number of candlesticks you want to retrieve
# limit = 1000  # You can adjust this as needed

# # Fetch historical OHLCV data
# ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

# # Create a DataFrame from the data
# df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# # Drop the timestamp column
# df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

# Read data from "o.txt" into a DataFrame
data = pd.read_csv('o.txt', sep='\t')

# Create a DataFrame from the data
df = pd.DataFrame(data)

# # Calculate wick size (difference between high and low)
# df['wick_size'] = df['high'] - df['low']

# # Save the DataFrame with wick size to "o2.txt"
# df[['timestamp', 'wick_size']].to_csv('o2.txt', sep='\t', index=False)

# Calculate the wick size (difference between high and low)
data['wick_size'] = data['high'] - data['low']

# Define a threshold for a strong wick (you can adjust this threshold)
strong_wick_threshold = 10  # For example, consider wicks longer than 10 as strong

# Determine if the wick is strong based on the threshold
data['strong_wick'] = ['Strong' if wick_size > strong_wick_threshold else 'Weak' for wick_size in data['wick_size']]

# Determine if each candlestick is bullish or bearish
data['candle_type'] = ['Bullish' if row['close'] > row['open'] else 'Bearish' for index, row in data.iterrows()]

# Create a new column for open-close difference and calculate it
data['open_close_diff'] = data['close'] - data['open']

# Calculate the open-close difference (body)
data['body'] = data['close'] - data['open']

# Save the DataFrame with candle type, strong wick, wick size, open-close difference (body), and other columns to "o2.txt"
data[['timestamp', 'candle_type', 'strong_wick', 'wick_size', 'open', 'high', 'low', 'close', 'body']].to_csv('o2.txt', sep='\t', index=False)
