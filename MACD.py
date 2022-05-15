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
        msg = await client.futures_historical_klines(symbol=symbol, interval="3m", start_str="2022-14-05 00:00:00", end_str=None)
        data = self.get_data_frame(symbol=symbol, msg=msg) 
        self.MACD()
        await client.close_connection()
        quit()

    def MACD(self):
        RSI = talib.RSI(df['Close'], timeperiod=14)
        BOP = talib.BOP(df['Open'], df['High'], df['Low'], df['Close'])
        macd, macdsignal, macdhist = talib.MACD(df['Close'], fastperiod=3, slowperiod=10, signalperiod=16) #HIGH TF
        fastk, fastd = talib.STOCHRSI(df['Close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

        df['BOP'] = round(BOP, 1)
        df['RSI'] = round(RSI)
        df['fastd'] = round(fastd)
        df['MACD'] = round(macd )
        df['Signal'] = round(macdsignal)
        df['History'] = round(macdhist)                 
        rr = len(df.index)
        df['OpenT'] = np.where(df["Open"][rr - 4] < df['Close'], 1, -1)
        df['RSIT'] = np.where(df["RSI"][rr - 4] < df['RSI'], 1, -1)
        df['fastdT'] = np.where(df["fastd"][rr - 4] < df['fastd'], 1, -1)
        df['MACDT'] = np.where(df["MACD"][rr - 4] < df['MACD'], 1, -1)
        df['SignalT'] = np.where(df["Signal"][rr - 4] < df['Signal'], 1, -1)
        df['HistoryT'] = np.where(df["History"][rr - 4] < df['History'], 1, -1)

        yy = 5
        HistoryT = "NONE"
        for y in df:
            yy -= 1
            n = df['HistoryT'][rr - yy]
            if n < 0:
                HistoryT = "LONG"
            else:
                HistoryT = "SHORT"

            if yy == 1: break

        yy = 5
        SignalT = "NONE"
        for y in df:
            yy -= 1
            n = df['SignalT'][rr - yy]
            if n < 0:
                SignalT = "LONG"
            else:
                SignalT = "SHORT"

            if yy == 1: break
        yy = 5
        SignalT = "NONE"
        for y in df:
            yy -= 1
            n = df['SignalT'][rr - yy]
            if n < 0:
                SignalT = "LONG"
            else:
                SignalT = "SHORT"

            if yy == 1: break

        yy = 5
        MACDT = "NONE"
        for y in df:
            yy -= 1
            n = df['MACDT'][rr - yy]
            if n < 0:
                MACDT = "LONG"
            else:
                MACDT = "SHORT"

            if yy == 1: break

        yy = 5
        fastdT = "NONE"
        for y in df:
            yy -= 1
            n = df['fastdT'][rr - yy]
            if n < 0:
                fastdT = "LONG"
            else:
                fastdT = "SHORT"

            if yy == 1: break

        yy = 5
        RSIT = "NONE"
        for y in df:
            yy -= 1
            n = df['RSIT'][rr - yy]
            if n < 0:
                RSIT = "LONG"
            else:
                RSIT = "SHORT"

            if yy == 1: break

        yy = 5
        OpenT = "NONE"
        for y in df:
            yy -= 1
            n = df['OpenT'][rr - yy]
            if n < 0:
                OpenT = "LONG"
            else:
                OpenT = "SHORT"

            if yy == 1: break

        if OpenT < "LONG" and RSIT < "LONG" and fastdT < "LONG" and MACDT < "LONG" and SignalT < "LONG" and HistoryT < "LONG":
            df['Trigger'] = "LONG"
        else:
            df['Trigger'] = "SHORT"

        print(df)
        with open('output.txt', 'w') as f:
            f.write(
                df.to_string()
            )  

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
