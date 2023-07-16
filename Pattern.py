# %matplotlib inline

from datetime import datetime, timedelta, timezone
from glob import glob
import time
import talib
import asyncio

import pandas as pd
import numpy as np

from binance.client import AsyncClient

import config
import callDB
import CO

# import seaborn as sns
# import matplotlib.pyplot as plt


db = callDB.call()
CreateOrder = CO.call()

class PatternDetect:

#=====================================================================================================================

    async def main(self):
        global pair, timeframe, error_set, deltaSMA
        
        result = db.get_toggle()

        yy = 0
        for y in result:
            yy += 1

        xx = 0
        for x in result:
            xx += 1
            pair = x['pair']
            timeframe = x['timeframe']
            qty = x['qty']
            volume_set = x['vol']
            order_type = x['order_type']

            # BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT, SOLUSDT, LUNAUSDT, ADAUSDT, USTUSDT, BUSDUSDT, 
            # DOGEUSDT, AVAXUSDT, DOTUSDT, SHIBUSDT, WBTCUSDT, DAIUSDT, MATICUSDT
            # Short        4    33240    <c>+123399   </c>-<c>   +1403% </c>
            # Short        7    3425    <c>+7399   </c>-<c>   +1403% </c>
            # Long        125    20220    <c>+21723   </c>-<c>   +783% </c>
            if pair == "BTCUSDT":
                # pair = "MKRUSDT"
                # timeframe = "1d"
                try:                    
                    client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)

                    if timeframe == "1m": deltaSMA = 10
                    if timeframe == "3m": deltaSMA = 20
                    if timeframe == "5m": deltaSMA = 20
                    if timeframe == "15m": deltaSMA = 16
                    if timeframe == "30m": deltaSMA = 24
                    if timeframe == "1h": deltaSMA = 100
                    if timeframe == "2h": deltaSMA = 80
                    if timeframe == "4h": deltaSMA = 140
                    if timeframe == "6h": deltaSMA = 200                        
                    if timeframe == "8h": deltaSMA = 300                        
                    if timeframe == "12h": deltaSMA = 500
                    if timeframe == "1d": deltaSMA = 2000
                        
                    last_hour_date_time = datetime.now() - timedelta(hours = deltaSMA)
                    get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')

                    msg = await client.futures_historical_klines(symbol=pair, interval=timeframe, start_str=get_startDate, end_str=None)
                    data = self.get_data_frame(symbol=pair, msg=msg) 
                    self.Pattern_Detect()                 
                    print(f'\nRetrieving Historical data from Binance for: {pair, timeframe} \n')                       
                    
                    await client.close_connection()

                except: await client.close_connection()     

#=====================================================================================================================

    def get_data_frame(self, symbol, msg):
        global rows_count, df, volume, high, close

        df = pd.DataFrame(msg)
        df.columns = ['Time','Open', 'High', 'Low', 'Close', 'Volume','CloseTime', 'qav','num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
        df = df.loc[:, ['Time','Open', 'High', 'Low', 'Close', 'Volume']]
        times = pd.to_datetime(df["Time"], unit='ms')
        times_index = pd.Index(times)
        times_index_Singapore = times_index.tz_localize('GMT').tz_convert('Singapore')

        df["Open"] = df["Open"].astype(float)
        df["High"] = df["High"].astype(float)
        df["Low"] = df["Low"].astype(float)
        df["Close"] = df["Close"].astype(float)

        return df

#=====================================================================================================================

    def Pattern_Detect(self):
        # df['Open'], df['High'], df['Low'], df['Close']

        # https://www.investopedia.com/terms/u/upside-gap-two-crows.asp
        CDL2CROWS = talib.CDL2CROWS(df['Open'], df['High'], df['Low'], df['Close']) 
        
        # 3 Candle Bearish
        # https://www.investopedia.com/terms/t/three_black_crows.asp
        CDL3BLACKCROWS = talib.CDL3BLACKCROWS(df['Open'], df['High'], df['Low'], df['Close']) 
        # Start of a bearish downtrend.

        # https://www.investopedia.com/terms/t/three-inside-updown.asp
        CDL3INSIDE = talib.CDL3INSIDE(df['Open'], df['High'], df['Low'], df['Close']) 
        # The up version of the pattern is bullish.

        # https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp
        CDL3LINESTRIKE = talib.CDL3LINESTRIKE(df['Open'], df['High'], df['Low'], df['Close'])
        # The bullish three line strike reversal pattern carves out three black candles within a downtrend.

        # https://www.investopedia.com/terms/t/three-outside-updown.asp
        CDL3OUTSIDE = talib.CDL3OUTSIDE(df['Open'], df['High'], df['Low'], df['Close']) 
        # The market is in an uptrend.
        # The first candle is white.
        # The second candle is black with a long real body that fully contains the first candle.
        # The third candle is black with a close lower than the second candle.

        # https://www.investopedia.com/terms/t/three-stars-south.asp
        CDL3STARSINSOUTH = talib.CDL3STARSINSOUTH(df['Open'], df['High'], df['Low'], df['Close'])

        # https://www.investopedia.com/terms/t/three_white_soldiers.asp
        CDL3WHITESOLDIERS = talib.CDL3WHITESOLDIERS(df['Open'], df['High'], df['Low'], df['Close'])

        # https://www.investopedia.com/terms/b/bearish-abandoned-baby.asp
        CDLABANDONEDBABY = talib.CDLABANDONEDBABY(df['Open'], df['High'], df['Low'], df['Close'])
        #A bearish abandoned baby can be a signal for a downward reversal trend in the price of a security.

        CDLADVANCEBLOCK = talib.CDLADVANCEBLOCK(df['Open'], df['High'], df['Low'], df['Close'])




        df['2CROWS'] = CDL2CROWS
        df['3BLACKCROWS'] = CDL3BLACKCROWS
        df['3INSIDE'] = CDL3INSIDE
        df['3LINESTRIKE'] = CDL3LINESTRIKE
        df['3OUTSIDE'] = CDL3OUTSIDE
        df['3STARSINSOUTH'] = CDL3STARSINSOUTH
        df['3WHITESOLDIERS'] = CDL3WHITESOLDIERS
        df['ABANDONEDBABY'] = CDLABANDONEDBABY
        df['ADVBLOCK'] = CDLADVANCEBLOCK


        with open('output.txt', 'w') as f:
            f.write(
                df.to_string()
            )
            
#=====================================================================================================================

if __name__ == '__main__':
    pattern_detect = PatternDetect()
    asyncio.get_event_loop().run_until_complete(pattern_detect.main())
