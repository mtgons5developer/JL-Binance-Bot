from datetime import datetime, timedelta

import talib
import asyncio
import pandas as pd
import numpy as np

from binance.client import AsyncClient
from binance.client import Client

import config
import callDB
import CO

db = callDB.call()
CreateOrder = CO.call()

class PatternDetect:

#=====================================================================================================================

    async def main(self):
        global pair, timeframe, error_set, deltaSMA, rsiLong, rsiShort
        
        error_set = 0
        error_set2 = 0
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

            rsiLong = x['rsiLong']
            rsiShort = x['rsiShort']
            deltaSMA = x['deltaSMA']

            # BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT, SOLUSDT, LUNAUSDT, ADAUSDT, USTUSDT, BUSDUSDT, 
            # DOGEUSDT, AVAXUSDT, DOTUSDT, SHIBUSDT, WBTCUSDT, DAIUSDT, MATICUSDT

            if pair == "BTCUSDT":# and error_set2 == 0:

                try:
                    
                    client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
                    print(f'Retrieving Historical data from Binance for: {pair, timeframe} \n')          
                    last_hour_date_time = datetime.now() - timedelta(hours = deltaSMA)
                    get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    msg = await client.futures_historical_klines(symbol=pair, interval=timeframe, start_str=get_startDate, end_str=None)
                    data = self.get_data_frame(symbol=pair, msg=msg) 
                    self.d_RSI()                  
                    self.d_SMA()  

                    if error_set == 0:
                        type = "LIMIT"
                        # type = "MARKET"

                        #Not important on final code      
                        side = "NONE"

                        print("SMA >= curPrice: %(g)s >= %(a)s \nRSI+rsiLong: %(c)s <= %(d)s\nVolume >= Volume_SET: %(e)s >= %(f)s" % 
                                {'a': curPrice, 'c': rsi, 'd': rsiLong, 'e': volume, 'f': volume_set, 'g': sma})    

                        if curPrice > sma and rsi < rsiLong and volume >= volume_set:  
                            side = "BUY" 
                        elif curPrice < sma and rsi > rsiShort and volume >= volume_set:
                            side = "SELL" 
                        elif rsiShort == 0 and rsiLong == 0 and volume_set == 0:
                            side = "NONE"

                        print("passed")
                        if side == "BUY":    
                            print("passed1")
                            entry_price = round(curPrice / 2, 8)
                            entry_price = CreateOrder.get_rounded_price(pair, entry_price)
                            tp1 = high - close
                            tp2 = tp1 * 0.30
                            take_profit = round(close + tp2, 8)                                
                        elif side == "SELL":
                            print("passed2")
                            entry_price = round(curPrice * 1.5, 8)
                            entry_price = CreateOrder.get_rounded_price(pair, entry_price)
                            tp1 = high - close
                            tp2 = tp1 * 0.30
                            take_profit = round(close + tp2, 8)                                

                        print("\nVolume: %(c)s \nHigh: %(a)s Close: %(b)s Current Price: %(d)s \nRSI: %(e)s SMA: %(f)s \nQTY: %(g)s \nSIDE: %(i)s \nEntry Price: %(k)s \nTake Profit: %(j)s \n" % 
                            {'a': close, 'b': high, 'c': volume, 'd': curPrice, 'e': rsi, 'f': sma, 'g': qty, 'i':side, 
                            'j':take_profit, 'k':entry_price})
                        # CreateOrder.futures_order(pair, qty, entry_price, side, type, close, high)
                    
                    await client.clos_econnection()

                except: await client.close_connection()      
#=====================================================================================================================
                
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
        print(df)
        return df

#=====================================================================================================================

    def d_RSI(self):
        global rsi, error_set

        rsi = talib.RSI(df["Close"])
        rw = len(df.index)
        tt = str(rsi[rw - 1])
        rsi = round(float(tt))

        if tt == "nan":
            print("\n RSI: ERROR deltatime adjust to a higher value\n")
            # db.put_dateErrorRSI(timeframe, pair)
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
            print("\n SMA: ERROR deltatime adjust to a higher value\n")
            # db.put_dateErrorSMA(timeframe, pair)
            error_set = 1   
            
#=====================================================================================================================

if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    pattern_detect = PatternDetect()
    asyncio.get_event_loop().run_until_complete(pattern_detect.main())
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))