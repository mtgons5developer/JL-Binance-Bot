
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

            # BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT, SOLUSDT, ADAUSDT, LTCUSDT
            # DOGEUSDT, AVAXUSDT, DOTUSDT, SHIBUSDT, MATICUSDT, BCHUSDT

            rr = db.get_order_EntryStatus(pair)
            if rr != "2" or rr != "1": status = 2

            for x in rr:
                xx += 1
                status = x['status']
            
            if pair == "DOGEUSDT" and status == 2:
                found = 1
                break

        if found == 1:

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
            await client.close_connection()
            CreateOrder.futures_order(pair, qty, side, high, timeframe, low)

#=====================================================================================================================

    def get_data_frame(self, symbol, msg):
        global rows_count, df, high, close

        df = pd.DataFrame(msg)
        df.columns = ['Time','Open', 'High', 'Low', 'Close', 'Volume','CloseTime', 'qav','num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
        df = df.loc[:, ['Time','Open', 'High', 'Low', 'Close']]
        df["Time"] = pd.to_datetime(df["Time"], unit='ms')
        df["Open"] = df["Open"].astype(float)
        df["High"] = df["High"].astype(float)
        df["Low"] = df["Low"].astype(float)
        df["Close"] = df["Close"].astype(float)

        return df

#=====================================================================================================================

    def Pattern_Detect(self):
        global side, take_profit, entry_price, high, low, close, open       

        dd = df.tail(4)
        rr = len(df.index)

        open = df["Open"][rr - 2] 
        high = df["High"][rr - 2] 
        low = df["Low"][rr - 2] 
        close = df['Close'][rr - 2] 
        hc = high - close
        lc = close - low
        llc = lc * 4
        
        if open > close:
            side = "BUY"
            if lc > 0: # Upper wick high but large body                
                if hc < llc:
                    side = "SELL"
        elif open < close:
            side = "SELL"
            if lc > 0: # Upper wick high but low body                
                if hc > llc:
                    side = "BUY"
        else:
            side = "NONE"  

        
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
        insert_TH(th) 
        print("Order FILLED", orderIdTP, pair)
        quit()

    if status == "NEW":
        CreateOrder.cancel_order(orderId, pair, qty, side)
        CreateOrder.cancel_order2(orderIdTP, pair)
        db.put_order_Exit(pair)
        insert_TH(th) 
        print("EXIT by Time Frame.")
        quit()

#=====================================================================================================================

pattern_detect = PatternDetect()
asyncio.get_event_loop().run_until_complete(pattern_detect.main())

schedule.every(tf).minutes.do(exit)

while True:
    schedule.run_pending()
    time.sleep(1)




