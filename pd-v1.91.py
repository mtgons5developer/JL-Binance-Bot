from datetime import datetime, timedelta

import time
import talib
import asyncio
import pandas as pd
import numpy as np

from binance.client import AsyncClient
from binance.client import Client


from callDB import get_startDate, put_dateError, get_toggle, get_qty, get_TH_uuid, get_TH_pair, get_TH_orderID
from CO import futures_order, get_rounded_price, get_tick_size, cancel_order
import config

global timeframe, pair, th_orderID

class PatternDetect:
    
    def get_data_frame(self, symbol, msg):
        global rows_count, df, volume

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

        return df

    def d_RSI(self):
        global rsi

        rsi = talib.RSI(df["Close"])
        rw = len(df.index)
        tt = str(rsi[rw - 1])
        rsi = round(float(tt))
    
        if tt == "nan":
            print("ERROR RSI")
            put_dateError(timeframe, pair)
        # else:
            # print("RSI:", rsi)

    def d_SMA(self):
        global curPrice, sma

        sma = talib.SMA(df['Close'])
        rw = len(df.index)
        tt = str(sma[rw - 1])
        sma = round(float(tt), 6)
        curPrice = df['Close'].iloc[-1]
        
        if tt == "nan":
            print("ERROR SMA")
            put_dateError(timeframe, pair)
        # else:
            # print("SMA:", sma)
            # print("===", curPrice, "===")
            
    async def main(self):

        i = 0
        while 1 == 1:
            i += 1
            if i == 1:
                timeframe = "5m"
            elif i == 2:
                timeframe = "15m"
            elif i == 3:
                timeframe = "30m"
            elif i ==4:
                timeframe = "1h"
            else:
                timeframe = "end"
                break

            result = get_toggle(timeframe)
            num = 0
            for x in result:
                num += 1    

            ii = 0
            while ii < num:
                ii += 1
                pair = result[num - ii]["pair"]

                try:
                    client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
                    print(f'Retrieving Historical data from Binance for: {pair, timeframe}')
                    last_hour_date_time = datetime.now() - timedelta(hours = 24)
                    get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    msg = await client.futures_historical_klines(symbol=pair, interval=timeframe, start_str=get_startDate, end_str=None)
                    data = self.get_data_frame(symbol=pair, msg=msg)
                    cc = df["Close"]
                    close = cc[rows_count - 1]
                    hh = df["High"]
                    high = hh[rows_count - 1]
                                
                    self.d_RSI()
                    self.d_SMA()

                    type = "LIMIT"
                    # type = "MARKET"

                    if volume > 1:

                        #Not important on final code
                        entry_price = 37000.05 
                        entry_price = get_rounded_price(pair, entry_price)

                        qty = get_qty(timeframe, pair)
                        
                        side = "BUY"
                        # if curPrice > close and sma > curPrice and rsi > 0 and rsi < 0:
                        #     side = "BUY"
                        # else:
                        #     side = "SELL"
                        
                        futures_order(pair, qty, entry_price, side, type, close, high)
                        print("Date/Time: %(h)s Volume: %(c)s High: %(a)s Close: %(b)s RSI: %(e)s SMA: %(f)s QTY: %(g)s" % 
                            {'a': close, 'b': high, 'c': volume, 'd': curPrice, 'e': rsi, 'f': sma, 'g': qty, 'h': get_startDate})

                    await client.close_connection()
                    break

                except:
                    print("No Action(s) for " + timeframe)
                    await client.close_connection()
            
            else:
                continue

if __name__ == '__main__':

    client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
    info = client.get_server_time()
    ts = str(info["serverTime"])
    t1 = ts[:-3]
    t2 = int(t1)
    server_time = datetime.fromtimestamp(t2).strftime('%Y-%m-%d %H:%M:%S')
    datetime_object = datetime.strptime(server_time, '%Y-%m-%d %H:%M:%S')
    hour = datetime_object.strftime("%H")
    minute = int(datetime_object.strftime("%M"))
    second = int(datetime_object.strftime("%S"))  

    while 1 == 1: 
        # timer = minute + ":" + second
        print(minute, ":", second)
        second += 1

        pattern_detect = PatternDetect()
        asyncio.get_event_loop().run_until_complete(pattern_detect.main())
        # uuid = get_TH_uuid()
        # pair = get_TH_pair(uuid)
        # orderID = get_TH_orderID(uuid)
        # cancel_order(orderID, pair)
        quit()
        #ENTRY
        if int(repr(minute)[-1]) == 5 and second == 1: #5m
            print("ENTRY 5m")
            print(minute, ":", second)
            #detect toggled at 5m
            pattern_detect = PatternDetect()
            asyncio.get_event_loop().run_until_complete(pattern_detect.main())

        # if int(repr(minute)[-1]) == 0 and second == 1: #5m
        #     print("ENTRY 5m")
        #     print(minute, ":", second)

        # if minute == 15 and second == 1: #15m
        #     print("ENTRY 15m")
        #     print(minute, ":", second)

        # if minute == 30 and second == 1: #15m/30m
        #     print("ENTRY 15m/30m")
        #     print(minute, ":", second)

        # if minute == 45 and second == 1: #15m
        #     print("ENTRY 15m")
        #     print(minute, ":", second)

        # if minute == 0 and second == 1: #15m/#30m/1h
        #     print("ENTRY 15m/#30m/1h")
        #     print(minute, ":", second)

        #=================
        #EXIT Store Close price
        if int(repr(minute)[-1]) == 4 and second == 59: #5m
            print("EXIT 5m")
            print(minute, ":", second)
            pattern_detect = PatternDetect()
            asyncio.get_event_loop().run_until_complete(pattern_detect.main())            
            orderID = get_TH_orderID()


        # if int(repr(minute)[-1]) == 9 and second == 59: #5m
        #     print("EXIT 5m")
        #     print(minute, ":", second)

        # if minute == 14 and second == 59: #15m
        #     print("EXIT 15m")
        #     print(minute, ":", second)

        # if minute == 29 and second == 59: #15m/30m
        #     print("EXIT 15m/30m")
        #     print(minute, ":", second)

        # if minute == 44 and second == 59: #15m
        #     print("EXIT 15m")
        #     print(minute, ":", second)

        # if minute == 59 and second == 59: #15m/#30m/1h
        #     print("EXIT 15m/#30m/1h")
        #     print(minute, ":", second)

        if second == 60:
            second = 0
            minute += 1
        
        if minute == 60:
            minute = 0

        time.sleep(1)
