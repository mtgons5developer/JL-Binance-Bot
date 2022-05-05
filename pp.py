# https://www.mt2trading.com/features/
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import talib
import random
import asyncio
import pyfiglet
import pandas as pd
import logging.config
from time import sleep
from pathlib import Path
from binance.enums import *
from binance import BinanceSocketManager
from binance.client import Client, AsyncClient
from datetime import timedelta, datetime, timezone


class PatternDetect:
    def __init__(self):
        self.PROJECT_ROOT = Path(os.path.abspath(os.path.dirname(__file__)))

    # Get dataframe
    def get_data_frame(self, symbol, msg):
        df = pd.DataFrame([msg['k']])
        df = df.loc[:, ['T', 'o', 'h', 'l', 'c']]
        df.columns = ['Time', 'Open', 'High', 'Low', 'Close']
        df["Time"] = pd.to_datetime(df["Time"], unit='ms')
        df["Open"] = df["Open"].astype(float)
        df["High"] = df["High"].astype(float)
        df["Low"] = df["Low"].astype(float)
        df["Close"] = df["Close"].astype(float)
        print(df)
        # quit()
        # file_path = str(self.PROJECT_ROOT / f'{symbol}.csv')
        # # if file does not exist write header
        # if not os.path.isfile(file_path):
        #     df.to_csv(file_path, index=False)
        # else:  # else if exists so append without writing the header
        #     df.to_csv(file_path, mode='a', header=False, index=False)
        return df

    def detect_pattern(self, symbol, data):
        data["Time"] = pd.to_datetime(data["Time"])
        ms = talib.CDLMORNINGSTAR(data["Open"], data["High"], data["Low"], data["Close"])
        eng = talib.CDLENGULFING(data["Open"], data["High"], data["Low"], data["Close"])
        # quit()
        data['msi'] = ms
        data['eng'] = eng
        eng_days = data[data['eng'] != 0]
        print(data['eng'])

    async def main(self):
        api_key = 'evdqA4eKyHWAGjBn4uFJtGeSCSqTxPbndlCi8mLhqcAT0iXk5IaKohpxkmkFo6tc'
        api_secret = 'i4jsUwqB2PPQOuoDms2xB3RyRCEGDM5kSaXnWPIu4HQlMnB52Q164rNxierthAEi'
        client = await AsyncClient.create(api_key=api_key, api_secret=api_secret)
        bsm = BinanceSocketManager(client)
        symbol = 'BTCUSDT'
        s_socket = bsm.kline_futures_socket(symbol=symbol, interval='1h')
        print(s_socket)
        # quit()
        print(f'Retrieving live OHLC data from Binance for: {symbol}')
        async with s_socket as symbol_socket:
            while True:
                msg = await symbol_socket.recv()
                ros = msg['k']
                current_price = float(ros['c'])

                print(current_price)
                # quit()
                # data = self.get_data_frame(symbol=symbol, msg=msg)
                # self.detect_pattern(symbol, data)



if __name__ == '__main__':
    pattern_detect = PatternDetect()
    asyncio.get_event_loop().run_until_complete(pattern_detect.main())

# https://stackoverflow.com/questions/66666134/how-to-install-homebrew-on-m1-mac
# brew install ta-lib
# export TA_INCLUDE_PATH="$(brew --prefix ta-lib)/include"
# export TA_LIBRARY_PATH="$(brew --prefix ta-lib)/lib"
# pip install ta-lib