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
        msg = await client.futures_historical_klines(symbol=symbol, interval="15m", start_str="2022-14-05 03:00:00", end_str=None)
        data = self.get_data_frame(symbol=symbol, msg=msg) 
        # macd, macdsignal, macdhist = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        # print(macd)
        # print(macdsignal)
        # print(macdhist)
        # quit()
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
        # print(df)
        df['Buy'] = np.where(df['Position'] == 1, df['Close'], 'NaN')
        df['Sell'] = np.where(df['Position'] == -1, df['Close'], 'NaN')

        with open('output.txt', 'w') as f:
            f.write(
                df.to_string()
            )
        

        # self.plot_graph(df)

    def get_data_frame(self, symbol, msg):
        global df

        df = pd.DataFrame(msg)
        df.columns = ['Time','Open', 'High', 'Low', 'Close', 'Volume','CloseTime', 'qav','num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
        df = df.loc[:, ['Time','Open', 'High', 'Low', 'Close', 'Volume']]
        df["Time"] = pd.to_datetime(df["Time"], unit='ms')
        df["Open"] = df["Open"].astype(float)
        df["High"] = df["High"].astype(float)
        df["Low"] = df["Low"].astype(float)
        df["Close"] = df["Close"].astype(float)
        df["Volume"] = df["Volume"].astype(float)

        rows_count = len(df.index)
        vv = df["Volume"]
        volume = round(vv[rows_count - 1])
        cc = df["Close"]
        close = cc[rows_count - 1]
        hh = df["High"]
        high = hh[rows_count - 1]  
        # print(df)

        return df

if __name__ == '__main__':
    pattern_detect = PatternDetect()
    asyncio.get_event_loop().run_until_complete(pattern_detect.main())
