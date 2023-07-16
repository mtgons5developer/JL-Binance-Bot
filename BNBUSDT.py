
from datetime import datetime, timedelta
import schedule
import time

import asyncio
import pandas as pd

from binance.client import AsyncClient
from binance.client import Client

from TH import insert_TH
import config
import callDB
import CO

db = callDB.call()
CreateOrder = CO.call()

class PatternDetect:

#=====================================================================================================================

    async def main(self):
        global pair, timeframe, error_set, deltaSMA, order_type, orderId, orderIdTP, qty, tf
        # client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
        
        result = db.get_toggle()
        found = 0
        xx = 0
        for x in result:
            xx += 1
            pair = x['pair']
            timeframe = x['timeframe']
            qty = x['qty']
            order_type = x['order_type']
            tf = int(timeframe[:-1])
            tf = tf * 60
            tf = tf - 1

            # BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT, SOLUSDT, ADAUSDT, LTCUSDT, TRXUSDT
            # DOGEUSDT, AVAXUSDT, DOTUSDT, MATICUSDT, BCHUSDT, EOSUSDT

            rr = db.get_order_EntryStatus(pair)
            if rr != "2" or rr != "1": status = 2

            for x in rr:
                xx += 1
                status = x['status']
            
            if pair == "BNBUSDT" and status == 2:
                found = 1
                break

        if found == 1:

            try:

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

                client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
                last_hour_date_time = datetime.now() - timedelta(hours = deltaSMA)
                get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                msg = await client.futures_historical_klines(symbol=pair, interval=timeframe, start_str=get_startDate, end_str=None)
                data = self.get_data_frame(symbol=pair, msg=msg)
                self.Pattern_Detect()
                print(f'\nRetrieving Historical data from Binance for: {pair, timeframe} \n')
                
                CreateOrder.futures_order(pair, qty, side, high, timeframe, low)

                await client.close_connection()

            except: await client.close_connection()
#=====================================================================================================================

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
        global side, high, low, close, open, volume
        
        for i in range(2,df.shape[0]):

            current = df.iloc[i,:]
            prev = df.iloc[i-1,:]
            prev_2 = df.iloc[i-2,:]
            realbody = abs(current['Open'] - current['Close'])
            candle_range = current['High'] - current['Low']
            idx = df.index[i]

            df.loc[idx,'BullishS'] = current['Low'] > prev['Low'] and prev['Low'] < prev_2['Low'] #Bullish Swing
            df.loc[idx,'BullishPB'] = realbody <= candle_range/3 and  min(current['Open'], current['Close']) > (current['High'] + current['Low'])/2 and current['Low'] < prev['Low'] # Bullish pin bar
            df.loc[idx,'BullishE'] = current['High'] > prev['High'] and current['Low'] < prev['Low'] and realbody >= 0.8 * candle_range and current['Close'] > current['Open'] #Bullish engulfing            
            
            df.loc[idx,'BearishS'] = current['High'] < prev['High'] and prev['High'] > prev_2['High'] #Bearish Swing            
            df.loc[idx,'BearishPB'] = realbody <= candle_range/3 and max(current['Open'] , current['Close']) < (current['High'] + current['Low'])/2 and current['High'] > prev['High'] # Bearish pin bar
            df.loc[idx,'BearishE'] = current['High'] > prev['High'] and current['Low'] < prev['Low'] and realbody >= 0.8 * candle_range and current['Close'] < current['Open'] # Bearish engulfing

            # Still needs historical data
            df.loc[idx,'InsideB'] = current['High'] < prev['High'] and current['Low'] > prev['Low'] # Inside bar 
            df.loc[idx,'OutsideB'] = current['High'] > prev['High'] and current['Low'] < prev['Low'] # Outside bar
            
        print(df.tail(4))
        rr = len(df.index)
        volume = df["Volume"][rr - 2]
        open = df["Open"][rr - 2]
        high = df["High"][rr - 2]
        low = df["Low"][rr - 2]
        close = df["Close"][rr - 2]
        
        if df["BullishS"][rr - 2] == True:
            side = "BUY"
        elif df["BullishPB"][rr - 2] == True:
            side = "BUY"
        elif df["BullishE"][rr - 2] == True:
            side = "BUY"
        elif df["BearishS"][rr - 2] == True:
            side = "SELL"            
        elif df["BearishPB"][rr - 2] == True:
            side = "SELL"
        elif df["BearishE"][rr - 2] == True:
            side = "SELL"
        elif df["InsideB"][rr - 2] == True:
            side = "BUY"
        elif df["OutsideB"][rr - 2] == True:
            side = "BUY"            
        else:
            side = "SELL"

        # with open('output.txt', 'w') as f:
        #     f.write(
        #         df.to_string()
        #     )
        
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