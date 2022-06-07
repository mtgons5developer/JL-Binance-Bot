
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
        global pair, timeframe, error_set, deltaSMA, order_type, orderId, orderIdTP
        
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

            # BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT, SOLUSDT, ADAUSDT, USTUSDT, BUSDUSDT, 
            # DOGEUSDT, AVAXUSDT, DOTUSDT, SHIBUSDT, WBTCUSDT, DAIUSDT, MATICUSDT

            rr = db.get_order_EntryStatus(pair)
            if rr != "2" or rr != "1": status = 2
            yy = 0
            for y in rr:
                yy += 1
            xx = 0
            for x in rr:
                xx += 1
                status = x['status']
            
            if pair == "BTCUSDT" and status == 2:

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

                    last_hour_date_time = datetime.now() - timedelta(hours = deltaSMA)
                    get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    msg = await client.futures_historical_klines(symbol=pair, interval=timeframe, start_str=get_startDate, end_str=None)
                    data = self.get_data_frame(symbol=pair, msg=msg)
                    self.Pattern_Detect()
                    print(f'\nRetrieving Historical data from Binance for: {pair, timeframe} \n')
                    
                    if side != "NONE":             

                        CreateOrder.futures_order(pair, qty, side, high, timeframe, low)
                        # db.put_orderID(pair, "1234", side, '1234', qty, '1234', '1234', timeframe)
                        # print('-------Order Executed-------')

                        client2 = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
                        info = client2.futures_time()
                        ts = str(info["serverTime"])
                        t1 = ts[:-3]
                        t2 = int(t1)
                        server_time = datetime.fromtimestamp(t2).strftime('%Y-%m-%d %H:%M:%S')
                        th = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
                        datetime_object = datetime.strptime(server_time, '%Y-%m-%d %H:%M:%S')
                        nextTF = datetime_object + timedelta(hours=tf)
                        
                        hour1 = int(nextTF.strftime("%H"))    

                        hour = int(datetime_object.strftime("%H"))
                        minute = int(datetime_object.strftime("%M"))
                        second = int(datetime_object.strftime("%S"))
                            
                        while 1 == 1:
                            second += 1
                            if second == 55:

                                print(minute, second, pair)

                                order = db.get_order_EntryStatus("BTCUSDT")

                                for x in order: 
                                    if x['status'] == 1:
                                        break

                                status = x['status']
                                print(x['status'])
                                print("Order Status:", status, "BTCUSDT") #Check Order Entry Status of a Pair

                                if status == 1:
                                    result = db.get_status(pair)
                                    yy = 0
                                    for y in result:
                                        yy += 1
                                    xx = 0
                                    for x in result:
                                        xx += 1
                                        orderIdTP = x['orderIdTP']
                                        orderId = x['orderId']
                                    
                                    status = CreateOrder.check_order(orderIdTP, pair) #Check OrderID Status of a Pair
                                    print(status, orderIdTP, pair)
                                    
                                    if status == "FILLED":

                                        db.put_order_Exit(pair)
                                        insert_TH(th) 
                                        print("Order FILLED", orderIdTP, pair)
                                        quit()

                                    # elif minute == 4 or minute == 9 or minute == 14 or minute == 19 or minute == 24 or minute == 29 or minute == 34 or minute == 39 or minute == 44 or minute == 49 or minute == 54 or minute == 59:
                                    if status != "FILLED":
                                        if minute == 30 or minute == 0:
                                            
                                            CreateOrder.cancel_order(orderId, pair, qty, side)
                                            CreateOrder.cancel_order2(orderIdTP, pair)
                                            db.put_order_Exit(pair)
                                            insert_TH(th) 
                                            print("EXIT by Time Frame.")
                                            quit()
                                else: 
                                    continue                             

                            if second >= 60:
                                second = 0
                                minute += 1
                            
                            if minute >= 60:
                                minute = 0
                                hour += 1   
                                if hour >= 24:
                                    hour = 0

                            time.sleep(1)

                    await client.close_connection()

                except: 
                    await client.close_connection()

            else:
                continue

                           
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

#=====================================================================================================================

# client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
# orders = client.futures_position_information(symbol="ETHUSDT")
# print(orders)
# insert_TH("2022-06-05")
# status = CreateOrder.check_order("56667156337", "BTCUSDT")
# print(status)
# print(datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d'))

# quit()

if __name__ == '__main__':
    pattern_detect = PatternDetect()
    asyncio.get_event_loop().run_until_complete(pattern_detect.main())





