from datetime import datetime, timedelta

import os
from binance.client import AsyncClient
import talib
import asyncio
import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import config

symbol = "BTCUSDT"

class PatternDetect:

    async def main(self):

        client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
        msg = await client.futures_historical_klines(symbol=symbol, interval="1h", start_str="2022-13-05 00:00:00", end_str=None)
        data = self.get_data_frame(symbol=symbol, msg=msg) 

        RSI = talib.RSI(df['Close'], timeperiod=14)
        BOP = talib.BOP(df['Open'], df['High'], df['Low'], df['Close'])
        macd, macdsignal, macdhist = talib.MACD(df['Close'], fastperiod=3, slowperiod=10, signalperiod=16) #HIGH TF
        fastk, fastd = talib.STOCHRSI(df['Close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        # Find Entry Trigger
        # Open     High      Low      Close  BOP   RSI   fastk  fastd   MACD  Signal  History
        # 29482.5  29495.0  29241.9  29313.5 -0.7  44.0    0.0   55.0 -100.0  -100.0     -0.0
        # 29313.6  29365.2  28812.4  29065.0 -0.4  40.0    0.0   22.0 -188.0  -110.0    -77.0   
        # 29065.3  29249.9  28929.0  29091.4  0.1  40.0    8.0    3.0 -198.0  -121.0    -78.0
        # 29091.4  29159.1  28752.0  28827.2 -0.6  36.0    0.0    3.0 -268.0  -138.0   -130.0 =======
        # Trigger Point
        # 28827.9  28976.9  28644.0  28930.1  0.3  39.0   34.0   14.0 -240.0  -150.0    -90.0 =======
        # 28930.1  29087.7  28751.2  28812.6 -0.3  37.0   19.0   18.0 -244.0  -161.0    -83.0 

        # Open TF 1 < Close TF 4 == Trigger
        # MACD =    "4x TF going lower or equal or TF 1 is < TF2-4" Then Long
        # BOP =     "4x TF going lower or equal or TF 1 is < TF2-4" Then Long
        # RSI =     "4x TF going lower or equal or TF 1 is < TF2-4" Then Long
        # fastd =   "4x TF going lower or equal or TF 1 is < TF2-4" Then Long
        # fastk =   "4x TF going lower or equal or TF 1 is > TF2-4" Then Long
        # History = "4x TF going lower or equal or TF 1 is < TF2-4" Then Long

        df['BOP'] = round(BOP, 1)
        df['RSI'] = round(RSI)
        df['fastk'] = round(fastk)
        df['fastd'] = round(fastd)
        df['MACD'] = round(macd )
        df['Signal'] = round(macdsignal)
        df['History'] = round(macdhist)

        df['Trigger'] = np.where(df['MACD'] > df['Signal'], 1, 0)
        df['Position'] = df['Trigger'].diff()
        df['Buy'] = np.where(df['Position'] == 1, df['Close'], 'NaN')
        df['Sell'] = np.where(df['Position'] == -1, df['Close'], 'NaN')                     
        print(df)
        with open('output.txt', 'w') as f:
            f.write(
                df.to_string()
            )        
        quit()
        # self.shortEMA()
        # self.longEMA()
        self.MACD()
        # self.plot_graph(df)        
        # shortEMA = df['Close'].ewm(span=12, adjust=False).mean()
        # longEMA = df['Close'].ewm(span=26, adjust=False).mean()
        # MACD = shortEMA - longEMA 
        # signal = MACD.ewm(span=9, adjust=False).mean()
        # df['MACD'] = MACD 
        # df['signal'] = signal
        # df['Trigger'] = np.where(df['MACD'] > df['signal'], 1, 0)
        # df['Position'] = df['Trigger'].diff()
        # print(df)
        await client.close_connection()

    def plot_graph(df):
        df=df.astype(float)
        df[['Close', 'MACD', 'signal']].plot()
        plt.xlabel('Time', fontsize=18)
        plt.ylabel('Close Price', fontsize=18)
        x_axis = df.index
        plt.show()

    def MACD(self):
        shortEMA = df['Close'].ewm(span=12, adjust=False).mean()
        longEMA = df['Close'].ewm(span=26, adjust=False).mean()
        MACD = shortEMA - longEMA 
        signal = MACD.ewm(span=9, adjust=False).mean()
        df['MACD'] = MACD 
        df['signal'] = signal
        df['Trigger'] = np.where(df['MACD'] > df['signal'], 1, 0)
        df['Position'] = df['Trigger'].diff()
        df['Buy'] = np.where(df['Position'] == 1, df['Close'], 'NaN')
        df['Sell'] = np.where(df['Position'] == -1, df['Close'], 'NaN')
        print(df)

        with open('output.txt', 'w') as f:
            f.write(
                df.to_string()
            )
        

        # self.plot_graph(df)

    def get_data_frame(self, symbol, msg):
        global df

        df = pd.DataFrame(msg)
        df.columns = ['Time','Open', 'High', 'Low', 'Close', 'Volume','CloseTime', 'qav','num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
        df = df.loc[:, ['Open', 'High', 'Low', 'Close']]
        # df["Time"] = pd.to_datetime(df["Time"], unit='ms')
        df["Open"] = df["Open"].astype(float)
        df["High"] = df["High"].astype(float)
        df["Low"] = df["Low"].astype(float)
        df["Close"] = df["Close"].astype(float)
        # df["Volume"] = df["Volume"].astype(float)

        rows_count = len(df.index)
        # vv = df["Volume"]
        # volume = round(vv[rows_count - 1])
        cc = df["Close"]
        close = cc[rows_count - 1]
        hh = df["High"]
        high = hh[rows_count - 1]  
        # print(df)

        return df

if __name__ == '__main__':
    pattern_detect = PatternDetect()
    asyncio.get_event_loop().run_until_complete(pattern_detect.main())
