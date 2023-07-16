
from datetime import datetime, timedelta
import schedule
import time

import talib
import asyncio
import pandas as pd
import numpy as np

from binance.client import AsyncClient
from binance.exceptions import BinanceAPIException, BinanceOrderException

from Monitor import mainn

import config
import callDB
import CO

db = callDB.call()
CreateOrder = CO.call()

class PatternDetect:

#=====================================================================================================================

    async def main(self):
        global pair, timeframe, orderId, qty, tf

        result = db.get_toggle()
        found = 0
        xx = 0
        for x in result:
            xx += 1
            pair = x['pair']
            timeframe = x['timeframe']
            qty = x['qty']
            tf = int(timeframe[:-1])
            tf = tf * 60
            tf = tf - 1

            # BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT, SOLUSDT, ADAUSDT, LTCUSDT, TRXUSDT
            # DOGEUSDT, AVAXUSDT, DOTUSDT, MATICUSDT, BCHUSDT, EOSUSDT
        
            if pair == "BTCUSDT":
                found = 1
                break  

        if found == 1:
            timeframe = "1m"
            deltaSMA = 20
            try:
                client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)

                if timeframe == "1h": deltaSMA = 800
                if timeframe == "2h": deltaSMA = 80
                if timeframe == "4h": deltaSMA = 140
                if timeframe == "6h": deltaSMA = 200                        
                if timeframe == "8h": deltaSMA = 300                        
                if timeframe == "12h": deltaSMA = 500
                if timeframe == "1d": deltaSMA = 1000

                # last_hour_date_time = datetime.now() - timedelta(hours = deltaSMA)
                # get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')

                # msg = await client.futures_historical_klines(symbol=pair, interval=timeframe, start_str=get_startDate, end_str=None)
                # data = self.get_data_frame(symbol=pair, msg=msg) 
                # self.Pattern_Detect()                 
                # print(f'\nRetrieving Historical data from Binance for: {pair, timeframe} \n')                       
                date_1m = datetime.today().strftime('%Y-%m-%d')
                # print(date_1m)
                entry = 0
                take_profit = 19200
                while True:

                    mainn()

                    # try:
                    #     msg = await client.futures_historical_klines(symbol=pair, interval=timeframe, start_str=date_1m, end_str=None)
                    #     data = self.get_data_frame_1m(symbol=pair, msg=msg) 
                    #     entry = self.entry()
                    #     if entry == 1: break
                    #     time.sleep(1)

                    # except:
                    #     print("Error: Automatic Entry Initiated.")
                    #     break

                    # except BinanceAPIException as e:
                    #     e1 = e.status_code
                    #     e2 = e.message
                    #     e3 = "Error: BinanceAPIException while True"
                    #     datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    #     error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
                    #     print(error_info)
                    #     db.write_error(error_info)  
                    #     break

                    # except BinanceOrderException as e:
                    #     e1 = e.status_code
                    #     e2 = e.message
                    #     e3 = "Error: BinanceOrderException while True"
                    #     datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    #     error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
                    #     print(error_info)
                    #     db.write_error(error_info)  
                    #     break

                print("DONE")
                quit()
                orderId = CreateOrder.futures_order_main(pair, qty, side, timeframe, high, low)

                # CreateOrder.futures_order_main(pair, qty, side, timeframe, high, low)
                await client.close_connection()

            except: await client.close_connection()
#=====================================================================================================================

    def entry(self):

        rr = len(dd.index)
        RSI = dd['RSI'][rr - 1]
        BOP = dd['RSI'][rr - 1] # BOP get 30 frames Average or negative and positive
        STOCHRSI_1 = dd['fastd'][rr - 1]
        STOCHRSI_2 = dd['fastk'][rr - 1]

        print(RSI, BOP, STOCHRSI_1, STOCHRSI_2, side)

        if RSI >= 60 and side == "SELL":
            print(RSI, BOP, STOCHRSI_1, STOCHRSI_2, side, "1")
            entry = 1
            return entry

        if STOCHRSI_1 >= 85 and RSI >= 60 and side == "SELL":
            print(RSI, BOP, STOCHRSI_1, STOCHRSI_2, side, "2")
            entry = 1
            return entry
        if STOCHRSI_2 >= 85 and RSI >= 60 and side == "SELL":
            print(RSI, BOP, STOCHRSI_1, STOCHRSI_2, side, "3")
            entry = 1
            return entry

        if RSI <= 20 and RSI >= 0 and side == "BUY":
            print(RSI, BOP, STOCHRSI_1, STOCHRSI_2, side, "4")
            entry = 1
            return entry
        if STOCHRSI_1 <= 20 and side == "BUY":
            print(RSI, BOP, STOCHRSI_1, STOCHRSI_2, side, "5")
            entry = 1
            return entry
        if STOCHRSI_2 <= 20 and side == "BUY":
            print(RSI, BOP, STOCHRSI_1, STOCHRSI_2, side, "6")
            entry = 1
            return entry

    def get_data_frame_1m(self, symbol, msg):
        global dd

        dd = pd.DataFrame(msg)
        dd.columns = ['Time','Open', 'High', 'Low', 'Close', 'Volume','CloseTime', 'qav','num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
        dd = dd.loc[:, ['Close', "Time"]]
        dd["Time"] = pd.to_datetime(dd["Time"], unit='ms')

        RSI = talib.RSI(dd['Close'], timeperiod=14)
        BOP = talib.BOP(df['Open'], df['High'], df['Low'], df['Close'])
        fastk, fastd = talib.STOCHRSI(dd['Close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

        dd['RSI'] = round(RSI)
        df['BOP'] = round(BOP, 2)
        dd['fastd'] = round(fastd) # red
        dd['fastk'] = round(fastk) # white
        print(dd)
        d30 = df.tail(30)
        for i in range(2,d30.shape[0]):
            
            current = df.iloc[i,:]
            idx = df.index[i]

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

        return df

#=====================================================================================================================

    def Pattern_Detect(self):
        global high, close, low, side       

        RSI = talib.RSI(df['Close'], timeperiod=14)
        BOP = talib.BOP(df['Open'], df['High'], df['Low'], df['Close'])
        CDLSS = talib.CDLSHOOTINGSTAR(df['Open'], df['High'], df['Low'], df['Close']) ####        
        EMA = talib.EMA(df['Close'], timeperiod=30)
        WMA = talib.WMA(df['Close'], timeperiod=30)

        fastk, fastd = talib.STOCHRSI(df['Close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

        df['CDLSS'] = round(CDLSS)
        df['EMA'] = round(EMA)        
        df['WMA'] = round(WMA)        
        df['BOP'] = round(BOP, 2)
        df['RSI'] = round(RSI)
        df['fastd'] = round(fastd)
        df['fastk'] = round(fastk)

        for i in range(2,df.shape[0]):
            
            current = df.iloc[i,:]
            prev = df.iloc[i-1,:]
            prev_2 = df.iloc[i-2,:]
            realbody = abs(current['Open'] - current['Close'])
            candle_range = current['High'] - current['Low']
            idx = df.index[i]

            df.loc[idx,'EMA--'] = current["EMA"] >= prev["EMA"]
            df.loc[idx,'WMA--'] = current["WMA"] >= prev["WMA"]
            df.loc[idx,'BOP--'] = current["BOP"] >= prev["BOP"]

            df.loc[idx,'BullS'] = current['Low'] > prev['Low'] and prev['Low'] < prev_2['Low'] #Bullish Swing
            df.loc[idx,'BullPB'] = realbody <= candle_range/3 and  min(current['Open'], current['Close']) > (current['High'] + current['Low'])/2 and current['Low'] < prev['Low'] # Bullish pin bar
            df.loc[idx,'BullE'] = current['High'] > prev['High'] and current['Low'] < prev['Low'] and realbody >= 0.8 * candle_range and current['Close'] > current['Open'] #Bullish engulfing            
            
            df.loc[idx,'BearS'] = current['High'] < prev['High'] and prev['High'] > prev_2['High'] #Bearish Swing
            df.loc[idx,'BearPB'] = realbody <= candle_range/3 and max(current['Open'] , current['Close']) < (current['High'] + current['Low'])/2 and current['High'] > prev['High'] # Bearish pin bar
            
            df.loc[idx,'BearE'] = current['High'] > prev['High'] and current['Low'] < prev['Low'] and realbody >= 0.8 * candle_range and current['Close'] < current['Open'] # Bearish engulfing
            # If current candle shows position exit or stay next position.

            # Still needs historical data
            df.loc[idx,'IB'] = current['High'] < prev['High'] and current['Low'] > prev['Low'] # Inside bar
            df.loc[idx,'OB'] = current['High'] > prev['High'] and current['Low'] < prev['Low'] # Outside bar

            df.loc[idx,'SUM'] = abs(prev["Close"] - current["Close"])

            v1 = current['Open']
            v2 = current['Close']
            df.loc[idx,'SIDE'] = np.where(v1 < v2, 1, -1)

        print(df.tail(4))
        rr = len(df.index)
        high = df["High"][rr - 2]
        low = df["Low"][rr - 2]
        close = df["Close"][rr - 2]

        EMA_ANND = df["EMA--"][rr - 2]
        WMA_ANND = df["WMA--"][rr - 2]
        BOP_ANND = df["BOP--"][rr - 2]
        BullS_ANND = df["BullS"][rr - 2]
        BullPB_ANND = df["BullPB"][rr - 2]
        BullE_ANND = df["BullE"][rr - 2]
        BearS_ANND = df["BearS"][rr - 2]
        BearPB_ANND = df["BearPB"][rr - 2]
        BearE_ANND = df["BearE"][rr - 2]
        IB_ANND = df["IB"][rr - 2]
        OB_ANND = df["OB"][rr - 2]
        VOLUME_ANND = df["Volume"][rr - 2]

        plus = 0
        minus = 0
        for i in range(2,df.shape[0]):

            current = df.iloc[i,:]
            future = df.iloc[i+1,:]
            idx = df.index[i]

            if current['EMA--'] == EMA_ANND and current['WMA--'] == WMA_ANND and current['BOP--'] == BOP_ANND and current['BullS'] == BullS_ANND and current['BullPB'] == BullPB_ANND and current['BullE'] == BullE_ANND and current['BearS'] == BearS_ANND and current['BearPB'] == BearPB_ANND and current['BearE'] == BearE_ANND and current['IB'] == IB_ANND and current['OB'] == OB_ANND:# and SIDE_ANND == current['SIDE']:
                # print(current['Volume'], future['SIDE'])
                if current['Volume'] != VOLUME_ANND:
                    if future['SIDE'] > 0:
                        plus += 1
                    elif future['SIDE'] < 0:
                        minus += 1
                else:
                    break

        if plus > minus:
            side = "BUY"                        
        elif minus > plus:
            side = "SELL"                  
            print(side, plus, minus)
        else:
            if df["BullS"][rr - 2] == True:
                side = "BUY"
            elif df["BullPB"][rr - 2] == True:
                side = "BUY"
            elif df["BullE"][rr - 2] == True:
                side = "BUY"
            elif df["BearS"][rr - 2] == True:
                side = "SELL"            
            elif df["BearPB"][rr - 2] == True:
                side = "SELL"
            elif df["BearE"][rr - 2] == True:
                side = "SELL"
            elif df["IB"][rr - 2] == True:
                side = "BUY"
            elif df["OB"][rr - 2] == True:
                side = "BUY"   


        
def exit():

    result = db.get_status(pair)
    xx = 0
    for x in result:
        xx += 1
        orderIdTP = x['orderIdTP']
        orderId = x['orderId']

    status = CreateOrder.check_order(orderIdTP, pair)             

    if status == "FILLED" or status == "CANCELED":

        db.put_order_Exit(pair)
        print("Order FILLED", orderIdTP, pair)
        quit()

    if status == "NEW":
        CreateOrder.cancel_order(orderId, pair, qty, side)
        CreateOrder.cancel_order2(orderIdTP, pair)
        db.put_order_Exit(pair)
        print("EXIT by Time Frame.")
        quit()

#=====================================================================================================================

pattern_detect = PatternDetect()
asyncio.get_event_loop().run_until_complete(pattern_detect.main())

schedule.every(tf).minutes.do(exit)

while True:
    schedule.run_pending()
    time.sleep(1)