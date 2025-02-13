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

        rr = len(df.index)

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

        RSI_ANND = df["RSI"][rr - 2]
        fastd_ANND = df["fastd"][rr - 2]
        fastk_ANND = df["fastk"][rr - 2]
        HL_ANND = df["HL%"][rr - 2]
        OL_ANND = df["OL%"][rr - 2]
        OH_ANND = df["OH%"][rr - 2]
        OC_ANND = df["OC%"][rr - 2]
        CH_ANND = df["CH%"][rr - 2]
        SIDE_ANND = df["SIDE"][rr - 2]
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
        else:
            if plus > minus:
                side = "BUY"                        
            elif minus > plus:
                side = "SELL"            

        print(side, plus, minus)
        with open('output.txt', 'w') as f:
            f.write(
                df.to_string()
            )

        print("-----")

if __name__ == '__main__':
    pattern_detect = PatternDetect()
    asyncio.get_event_loop().run_until_complete(pattern_detect.main())

# https://towardsdatascience.com/how-to-identify-japanese-candlesticks-patterns-in-python-b835d1cc72f7