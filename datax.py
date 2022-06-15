from datetime import datetime, timedelta

import talib
import asyncio
import pandas as pd
import numpy as np

from binance.client import AsyncClient

import config



class PatternDetect:

#=====================================================================================================================

    async def main(self):
        global timeframe

        try:
            timeframe = "1h"
            deltaSMA = 800
            pair = "BTCUSDT"
            client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
            last_hour_date_time = datetime.now() - timedelta(hours = deltaSMA)
            get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
            msg = await client.futures_historical_klines(symbol=pair, interval=timeframe, start_str=get_startDate, end_str=None)
            data = self.get_data_frame(symbol=pair, msg=msg) 
            self.Pattern_Detect()                 
            await client.close_connection()

        except: await client.close_connection()    

    def get_data_frame(self, symbol, msg):
        global rows_count, df, volume, high, close, prev_side

        df = pd.DataFrame(msg)
        df.columns = ['Time','Open', 'High', 'Low', 'Close', 'Volume','CloseTime', 'qav','num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
        df = df.loc[:, ['Time','Open', 'High', 'Low', 'Close', 'Volume']]
        df["Time"] = pd.to_datetime(df["Time"], unit='ms')

        df["Open"] = df["Open"].astype(float)
        df["High"] = df["High"].astype(float)
        df["Low"] = df["Low"].astype(float)
        df["Close"] = df["Close"].astype(float)
        df["Volume"] = df["Volume"].astype(float)

        RSI = talib.RSI(df['Close'], timeperiod=14)
        BOP = talib.BOP(df['Open'], df['High'], df['Low'], df['Close'])
        CDLSS = talib.CDLSHOOTINGSTAR(df['Open'], df['High'], df['Low'], df['Close']) ####        
        EMA = talib.EMA(df['Close'], timeperiod=30)
        WMA = talib.WMA(df['Close'], timeperiod=30)

        macd, macdsignal, macdhist = talib.MACD(df['Close'], fastperiod=3, slowperiod=10, signalperiod=16) #HIGH TF
        fastk, fastd = talib.STOCHRSI(df['Close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

        df['CDLSS'] = round(CDLSS)
        df['EMA'] = round(EMA)        
        df['WMA'] = round(WMA)        
        df['BOP'] = round(BOP, 2)
        df['RSI'] = round(RSI)
        df['fastd'] = round(fastd)
        df['fastk'] = round(fastk)
        # df['MACD'] = round(macd)
        # df['Signal'] = round(macdsignal)
        # df['History'] = round(macdhist)   
        
        for i in range(2,df.shape[0]):

            current = df.iloc[i,:]
            prev = df.iloc[i-1,:]
            prev_2 = df.iloc[i-2,:]
            realbody = abs(current['Open'] - current['Close'])
            candle_range = current['High'] - current['Low']
            sum =  prev["Close"] - current["Close"]
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

            v1 = current['High']
            v2 = current['Low']
            p1 = abs(v1 - v2)
            p2 = (v1 + v2) / 2
            p3 = p1 / p2
            p4 = round(float(p3 * 100), 3)
            p5 = p4 * 100
            df.loc[idx,'HL%'] = p5

            v1 = current['Open']
            v2 = current['Low']
            p1 = abs(v1 - v2)
            p2 = (v1 + v2) / 2
            p3 = p1 / p2
            p4 = round(float(p3 * 100), 3)
            p5 = p4 * 100
            df.loc[idx,'OL%'] = p5

            v1 = current['Open']
            v2 = current['High']
            p1 = abs(v1 - v2)
            p2 = (v1 + v2) / 2
            p3 = p1 / p2
            p4 = round(float(p3 * 100), 3)
            p5 = p4 * 100
            df.loc[idx,'OH%'] = p5

            v1 = current['Open']
            v2 = current['Close']
            p1 = abs(v1 - v2)
            p2 = (v1 + v2) / 2
            p3 = p1 / p2
            p4 = round(float(p3 * 100), 3)
            p5 = p4 * 100
            df.loc[idx,'OC%'] = p5

            v1 = current['Close']
            v2 = current['High']
            p1 =abs(v1 - v2)
            p2 = (v1 + v2) / 2
            p3 = p1 / p2
            p4 = round(float(p3 * 100), 3)
            p5 = p4 * 100
            df.loc[idx,'CH%'] = p5

            v1 = current['Close']
            v2 = current['Low']
            p1 = abs(v1 - v2)
            p2 = (v1 + v2) / 2
            p3 = p1 / p2
            p4 = round(float(p3 * 100), 3)
            p5 = p4 * 100
            df.loc[idx,'CH%'] = p5

            v1 = current['Open']
            v2 = current['Close']
            df.loc[idx,'SIDE'] = np.where(v1 < v2, 1, -1)


        # EMA--  WMA--  BOP--  BullS BullPB  BullE  BearS BearPB  BearE     IB     OB

        # dd = df.tail(4)
        # print(dd)
        # rr = len(df.index)
        
        # if df["BullishS"][rr - 2] == True:
        #     side = "BUY"
        # elif df["BullishPB"][rr - 2] == True:
        #     side = "BUY"
        # elif df["BullishE"][rr - 2] == True:
        #     side = "BUY"
        # elif df["BearishS"][rr - 2] == True:
        #     side = "SELL"            
        # elif df["BearishPB"][rr - 2] == True:
        #     side = "SELL"
        # elif df["BearishE"][rr - 2] == True:
        #     side = "SELL"
        # elif df["InsideB"][rr - 2] == True:
        #     side = "BUY"
        # elif df["OutsideB"][rr - 2] == True:
        #     side = "BUY"            
        # else:
        #     side = prev_side

        # prev_side = side

        # print(side)
        with open('output.txt', 'w') as f:
            f.write(
                df.to_string()
            )


if __name__ == '__main__':
    pattern_detect = PatternDetect()
    asyncio.get_event_loop().run_until_complete(pattern_detect.main())

# https://towardsdatascience.com/how-to-identify-japanese-candlesticks-patterns-in-python-b835d1cc72f7