from datetime import datetime, timedelta
from glob import glob

import talib
import asyncio
import pandas as pd
import numpy as np

from binance.client import AsyncClient

import config
import callDB
import CO

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

            if pair == "BTCUSDT":# and error_set2 == 0:
                try:                    
                    client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
                    if timeframe == "3m": 
                        deltaSMA = 10
                    if timeframe == "5m":
                        deltaSMA = 12
                    if timeframe == "15m":
                        deltaSMA = 16
                    if timeframe == "30m":
                        deltaSMA = 24
                    if timeframe == "1h":
                        deltaSMA = 40
                    if timeframe == "2h":
                        deltaSMA = 80
                    if timeframe == "4h":
                        deltaSMA = 140
                    if timeframe == "6h":
                        deltaSMA = 200
                    if timeframe == "8h":
                        deltaSMA = 300
                    if timeframe == "12h":
                        deltaSMA = 500
                    if timeframe == "1d":
                        deltaSMA = 1000

                    last_hour_date_time = datetime.now() - timedelta(hours = 1000)
                    get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    msg = await client.futures_historical_klines(symbol=pair, interval="1d", start_str=get_startDate, end_str=None)
                    data = self.get_data_frame(symbol=pair, msg=msg) 
                    self.Pattern_Detect()                 
                    print(f'\nRetrieving Historical data from Binance for: {pair, "1 Day"} \n')          

                    last_hour_date_time = datetime.now() - timedelta(hours = 40)
                    get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    msg = await client.futures_historical_klines(symbol=pair, interval='1h', start_str=get_startDate, end_str=None)
                    data = self.get_data_frame(symbol=pair, msg=msg) 
                    self.Pattern_Detect()                 
                    print(f'\nRetrieving Historical data from Binance for: {pair, "1 Hour"} \n')     

                    last_hour_date_time = datetime.now() - timedelta(hours = deltaSMA)
                    get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    msg = await client.futures_historical_klines(symbol=pair, interval=timeframe, start_str=get_startDate, end_str=None)
                    data = self.get_data_frame(symbol=pair, msg=msg) 
                    self.Pattern_Detect()                 
                    print(f'\nRetrieving Historical data from Binance for: {pair, timeframe} \n')     
                    # print("\nVolume: %(c)s \nHigh: %(a)s Close: %(b)s Current Price: %(d)s \nRSI: %(e)s SMA: %(f)s \nQTY: %(g)s \nSIDE: %(i)s \nEntry Price: %(k)s \nTake Profit: %(j)s \n" % 
                    #     {'a': close, 'b': high, 'c': volume, 'd': curPrice, 'e': rsi, 'f': sma, 'g': qty, 'i':side, 
                    #     'j':take_profit, 'k':entry_price})

                    # CreateOrder.futures_order(pair, qty, entry_price, side, order_type, take_profit, timeframe)
                    # print('------------futures_order------------')
                    
                    await client.close_connection()

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

        return df

#=====================================================================================================================

    def Pattern_Detect(self):
        global side

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
        df['OpenT'] = np.where(df["Open"][rr - 4] < df['Close'], -1, 1)
        df['BOPT'] = np.where(df["BOP"][rr - 4] < df['BOP'], -1, 1)
        df['RSIT'] = np.where(df["RSI"][rr - 4] < df['RSI'], -1, 1)
        df['fastdT'] = np.where(df["fastd"][rr - 4] < df['fastd'], -1, 1)
        df['MACDT'] = np.where(df["MACD"][rr - 4] < df['MACD'], -1, 1)
        df['SignalT'] = np.where(df["Signal"][rr - 4] < df['Signal'], -1, 1)
        df['HistoryT'] = np.where(df["History"][rr - 4] < df['History'], -1, 1)

        # Cross Entry test
        # Support current TF by Higher TF
        # Multiple API Code
        # Quantity Test orders
        # Leverage Changer
        # Check orders and monitor
        # Signals must read 4 3 2 1
        # PNL Calculation
        # https://stackoverflow.com/questions/67643077/how-can-i-adjust-the-leverage-with-bianance-api
        # https://dev.binance.vision/t/how-to-calculate-cumb-while-calculating-liquidation-price/883
        # https://www.binance.com/en/support/faq/b3c689c1f50a44cabb3a84e663b81d93
        # https://gist.github.com/highfestiva/b71e76f51eed84d56c1be8ebbcc286b5?permalink_comment_id=3617078
        # https://binance-docs.github.io/apidocs/futures/en/#change-log

        yy = 5
        OpenT = "NONE"
        for y in df:
            yy -= 1
            n = df['OpenT'][rr - yy]
            # if yy == 4: 
            #     n = -1
            #     df['OpenT'] = np.where(df["Open"][rr - 4] < df['Close'], -1, -1)

            if n < 0:
                OpenT = "SHORT"
            else:
                OpenT = "LONG"

            if yy == 1: break

        yy = 5
        BOPT = "NONE"
        BOP = 0
        for y in df:
            yy -= 1
            # n = df['BOP'][rr - yy]
            # print(df['BOP'][rr - yy])

            # BOP += n

            if yy == 1: break

        # print(BOP) # Error
        # print(BOPT)
        # quit()

        yy = 5
        RSIT = "NONE"
        for y in df:
            yy -= 1
            n = df['RSIT'][rr - yy]
            if n < 0:
                RSIT = "SHORT"
            else:
                RSIT = "LONG"

            if yy == 1: break

        yy = 5
        fastdT = "NONE"
        for y in df:
            yy -= 1
            n = df['fastdT'][rr - yy]
            if n < 0:
                fastdT = "SHORT"
            else:
                fastdT = "LONG"

            if yy == 1: break

        yy = 5
        MACDT = "NONE"
        for y in df:
            yy -= 1
            n = df['MACDT'][rr - yy]
            if n < 0:
                MACDT = "SHORT"
            else:
                MACDT = "LONG"

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
        HistoryT = "NONE"
        for y in df:
            yy -= 1
            n = df['HistoryT'][rr - yy]
            if n < 0:
                HistoryT = "SHORT"
            else:
                HistoryT = "LONG"

            if yy == 1: break

        # print(OpenT)
        # print(RSIT)
        # print(fastdT)
        # print(MACDT)
        # print(SignalT)        
        # print(HistoryT)

        if OpenT == "LONG" and BOPT == "LONG" and RSIT == "LONG" and fastdT == "LONG" and MACDT == "LONG" and SignalT == "LONG" and HistoryT == "LONG":
            print("======== B U Y =======")
            side = "BUY"
        elif OpenT == "SHORT" and BOPT == "SHORT" and RSIT == "SHORT" and fastdT == "SHORT" and MACDT == "SHORT" and SignalT == "SHORT" and HistoryT == "SHORT":
            print("======= S E L L =======")
            side = "SELL"
        #dldl

        pp = df.tail(4)
        print(pp)
        val = pp['OpenT'].value_counts()
        # print(val[0:1]) #- Column
        # print(val[0:2]) #+ Column

        with open('output.txt', 'w') as f:
            f.write(
                pp.to_string()
            )  

    def d_Candle(self):
        global open

        cc = df["Open"]
        rw = len(df.index)
        tt = str(cc[rw - 1])
        open = float(tt)
        # print(open)

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