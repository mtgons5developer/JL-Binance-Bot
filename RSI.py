import talib
import pandas as pd
from td.client import TDClient

ticker = 'GOOG'
data = TDSession.get_price_history(
    symbol = ticker,
    period_type = 'month',
    frequency_type = 'daily',
    frequency = 1,
    period = 1,
)

df = pd.DataFrame(data['candles'])

close = df['close']

# Gets the RSI of the ticker 
rsi = str(talib.RSI(close, timeperiod=14))

current = float(rsi[len(rsi)-40:len(rsi)-33])