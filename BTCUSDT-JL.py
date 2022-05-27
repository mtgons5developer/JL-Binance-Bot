
from datetime import datetime, timedelta
import schedule
import time

import asyncio
import pandas as pd

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
        global pair, timeframe, error_set, deltaSMA, order_type
        
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
            order_type = x['order_type']
            tf = int(timeframe[:-1])

            # BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT, SOLUSDT, LUNAUSDT, ADAUSDT, USTUSDT, BUSDUSDT, 
            # DOGEUSDT, AVAXUSDT, DOTUSDT, SHIBUSDT, WBTCUSDT, DAIUSDT, MATICUSDT

            if pair == "BTCUSDT":

                try:                    
                    client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
                    client2 = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
                    info = client2.get_server_time()
                    ts = str(info["serverTime"])
                    t1 = ts[:-3]
                    t2 = int(t1)
                    server_time = datetime.fromtimestamp(t2).strftime('%Y-%m-%d %H:%M:%S')
                    datetime_object = datetime.strptime(server_time, '%Y-%m-%d %H:%M:%S')
                    nextTF = datetime_object + timedelta(hours=tf)

                    hour1 = nextTF.strftime("%H")
                    minute1 = int(nextTF.strftime("%M"))
                    second1 = int(nextTF.strftime("%S"))

                    hour = datetime_object.strftime("%H")
                    minute = int(datetime_object.strftime("%M"))
                    second = int(datetime_object.strftime("%S"))
                    
                    CreateOrder.check_order("55640823848", pair)
                    quit()

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

                    # print("NextTF:", nextTF, "Hour:", hour1)
                    # print(hour)
                    # quit()

                    last_hour_date_time = datetime.now() - timedelta(hours = deltaSMA)
                    get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    msg = await client.futures_historical_klines(symbol=pair, interval=timeframe, start_str=get_startDate, end_str=None)
                    data = self.get_data_frame(symbol=pair, msg=msg)
                    self.Pattern_Detect()
                    print(f'\nRetrieving Historical data from Binance for: {pair, timeframe} \n')

                    if side != "NONE":

                        CreateOrder.futures_order(pair, qty, side, order_type, take_profit, timeframe, entry_price)

                        # while 1==1:
                            


                    
                    await client.close_connection()


                except: await client.close_connection()
                  
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
        global side, take_profit, entry_price

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
            tp = high - close
            take_profit = (tp * 0.30) + close

            if lc > 0: # Upper wick high but large body
                
                if hc < llc:

                    side = "SELL"
                    tp = close - low
                    take_profit = (tp * 0.30) + close

        elif open < close:

            side = "SELL"
            tp = close - low
            take_profit = close - (tp * 0.30)

            if lc > 0: # Upper wick high but low body
                
                if hc > llc:
                    side = "BUY"
                    tp = high - close
                    take_profit = (tp * 0.30) + close

        else:
            side = "NONE"

        if order_type == "TEST": entry_price = close
        take_profit = round(take_profit, 6)
        print(dd)
        print(close)
        print(low)
        print(side)
        print(take_profit)
        # quit()    

        
#=====================================================================================================================

def entry():
    print("entry")
    # pattern_detect = PatternDetect()
    # asyncio.get_event_loop().run_until_complete(pattern_detect.main())
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def entry():
    print("exit")

schedule.every(1).minutes.do(entry)
schedule.every(1).minutes.do(exit)


if __name__ == '__main__':
    # schedule.run_pending()
    # time.sleep(1)
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    pattern_detect = PatternDetect()
    asyncio.get_event_loop().run_until_complete(pattern_detect.main())
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))