from datetime import datetime, timedelta

import time
import talib
import asyncio
import pandas as pd
import numpy as np

from binance.client import AsyncClient
from binance.client import Client


from callDB import get_startDate, put_dateError, get_toggle, get_TH_uuid, get_TH_pair, get_TH_orderID
from CO import futures_order, get_rounded_price, get_tick_size, cancel_order, check_order

import config

class PatternDetect:
    
    def get_data_frame(self, symbol, msg):
        global rows_count, df, volume, high, close

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

        return df

#=====================================================================================================================

    def d_RSI(self):
        global rsi, error_set

        rsi = talib.RSI(df["Close"])
        rw = len(df.index)
        tt = str(rsi[rw - 1])
        rsi = round(float(tt))
    
        if tt == "nan":
            print("\n ERROR deltatime adjust to a higher value\n")
            put_dateError(timeframe, pair)
            error_set = 1

#=====================================================================================================================

    def d_SMA(self):
        global curPrice, sma, error_set

        sma = talib.SMA(df['Close'])
        rw = len(df.index)
        tt = str(sma[rw - 1])
        sma = round(float(tt), 6)
        curPrice = df['Close'].iloc[-1]
        
        if tt == "nan":
            print("\nERROR deltatime adjust to a higher value\n")
            put_dateError(timeframe, pair)
            error_set = 1

#=====================================================================================================================

    async def main(self):
        global pair, timeframe, error_set
        
        error_set = 0
        result = get_toggle()

        yy = 0
        for y in result:
            yy += 1   

        xx = 0
        for x in result:
            xx += 1   
            pair = x['pair']
            timeframe = x['timeframe']
            qty = x['qty']
            deltatime = x['deltatime']
            volume_set = x['volume']
            
            if pair == "TRXUSDT":

                try:

                    client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
                    print(f'Retrieving Historical data from Binance for: {pair, timeframe}')
                    last_hour_date_time = datetime.now() - timedelta(hours = deltatime) #Change Settings Web
                    get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    msg = await client.futures_historical_klines(symbol=pair, interval=timeframe, start_str=get_startDate, end_str=None)
                    data = self.get_data_frame(symbol=pair, msg=msg) 

                    if volume > volume_set and error_set == 0:

                        self.d_RSI()
                        self.d_SMA()   

                        type = "LIMIT"
                        # type = "MARKET"

                        #Not important on final code
                        if pair == "TRXUSDT":
                            entry_price = 0.00365
                            entry_price = get_rounded_price(pair, entry_price)

                        side = "BUY"
                        # if curPrice > close and sma > curPrice and rsi > 0 and rsi < 0:
                        #     side = "BUY"
                        # else:
                        #     side = "SELL"
                        
                        print("%(h)s \nVolume: %(c)s \nHigh: %(a)s Close: %(b)s Current Price: %(d)s \nRSI: %(e)s SMA: %(f)s \nQTY: %(g)s \nSIDE: %(i)s \n" % 
                            {'a': close, 'b': high, 'c': volume, 'd': curPrice, 'e': rsi, 'f': sma, 'g': qty, 'h': get_startDate, 'i':side})
                        futures_order(pair, qty, entry_price, side, type, close, high)
                        
                    await client.clos_econnection()

                except: await client.close_connection()

            
#=====================================================================================================================

if __name__ == '__main__':

    pattern_detect = PatternDetect()
    asyncio.get_event_loop().run_until_complete(pattern_detect.main())
 