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

                    # last_hour_date_time = datetime.now() - timedelta(hours = 1000)
                    # get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    # msg = await client.futures_historical_klines(symbol=pair, interval="1d", start_str=get_startDate, end_str=None)
                    # data = self.get_data_frame(symbol=pair, msg=msg) 
                    # self.Pattern_Detect()                 
                    # print(f'\nRetrieving Historical data from Binance for: {pair, "1 Day"} \n')          
#======= JL ========
                    # last_hour_date_time = datetime.now() - timedelta(hours = 140)
                    # get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    # msg = await client.futures_historical_klines(symbol=pair, interval='4h', start_str=get_startDate, end_str=None)
                    # data = self.get_data_frame(symbol=pair, msg=msg) 
                    # self.Pattern_Detect()                 
                    # print(f'\nRetrieving Historical data from Binance for: {pair, "4 Hours"} \n')     

                    # last_hour_date_time = datetime.now() - timedelta(hours = 80)
                    # get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    # msg = await client.futures_historical_klines(symbol=pair, interval='2h', start_str=get_startDate, end_str=None)
                    # data = self.get_data_frame(symbol=pair, msg=msg) 
                    # self.Pattern_Detect()                 
                    # print(f'\nRetrieving Historical data from Binance for: {pair, "2 Hours"} \n')  
#======= JL ========
                    # last_hour_date_time = datetime.now() - timedelta(hours = 40)
                    # get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    # msg = await client.futures_historical_klines(symbol=pair, interval='1h', start_str=get_startDate, end_str=None)
                    # data = self.get_data_frame(symbol=pair, msg=msg) 
                    # self.Pattern_Detect()                 
                    # print(f'\nRetrieving Historical data from Binance for: {pair, "1 Hour"} \n')     

                    # last_hour_date_time = datetime.now() - timedelta(hours = 40)
                    # get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    # msg = await client.futures_historical_klines(symbol=pair, interval='30m', start_str=get_startDate, end_str=None)
                    # data = self.get_data_frame(symbol=pair, msg=msg) 
                    # self.Pattern_Detect()                 
                    # print(f'\nRetrieving Historical data from Binance for: {pair, "30 min"} \n')     

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

        df['BOP'] = round(BOP, 2)
        # df['RSI'] = round(RSI)
        df['fastd'] = round(fastd)
        df['fastk'] = round(fastk)

        # df['MACD'] = round(macd )
        # df['Signal'] = round(macdsignal)
        # df['History'] = round(macdhist)                 
        rr = len(df.index)

        pp = df.tail(3)
        dd = pd.DataFrame(pp)
        dd = dd.loc[:, ['Time', 'BOP', 'fastd', 'fastk']]
        # dd = dd.loc[:, ['Time', 'BOP', 'RSI', 'fastd', 'MACD', 'Signal', 'History']]
        BOPS = np.where(df["BOP"][rr - 3] > df['BOP'][rr -2], -1, 1)
        # RSIS = np.where(df["RSI"][rr - 3] > df['RSI'][rr -2], -1, 1)
        fastdS = np.where(df["fastd"][rr - 3] > df['fastd'][rr -2], -1, 1)
        fastkS = np.where(df["fastk"][rr - 3] > df['fastk'][rr -2], -1, 1)
        # MACDS = np.where(df["MACD"][rr - 3] > df['MACD'][rr -2], -1, 1)
        # SignalS = np.where(df["Signal"][rr - 3] > df['Signal'][rr -2], -1, 1)
        # HistoryS = np.where(df["History"][rr - 3] > df['History'][rr -2], -1, 1)                                

        dd['BOPT'] = BOPS
        # dd['RSIT'] = RSIS
        dd['fastdT'] = fastdS
        dd['fastkT'] = fastkS
        # dd['MACDT'] = MACDS
        # dd['SignalT'] = SignalS
        # dd['HistoryT'] = HistoryS
        
        Position = BOPS + fastdS

        signal1 = 0
        signal2 = 0

        if Position == 2: 
            signal1 = 1
        elif Position < 0:
            signal1 = -1
        else: 
            signal1 = 0

        BOP2 = float(df['BOP'][rr - 2])

        if BOP2 < 0.5 and BOP2 >= 0: 
            signal2 = 1
        elif BOP2 < -0.6 and BOP2 >= -0.9:
            signal2 = 1
        elif BOP2 > 0.5 and BOP2 <= 0.9: 
            signal2 = -1
        elif BOP2 > -0.6 and BOP2 >= -0.1:
            signal2 = -1
        else:
            signal2 = 0

        signalT = signal1 + signal2

        if signalT == 2:
            side = "BUY"
        elif signalT < 0:
            side = "SELL"
        else:
            side = "NONE"

        dd['Position'] = side

        print(dd)
        print(signal1)
        print(signal2)
        print(signalT)

        with open('output.txt', 'w') as f:
            f.write(
                dd.to_string()
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