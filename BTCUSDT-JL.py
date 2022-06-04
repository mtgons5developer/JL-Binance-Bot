
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

            # BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT, SOLUSDT, LUNAUSDT, ADAUSDT, USTUSDT, BUSDUSDT, 
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

                        status = CreateOrder.futures_order(pair, qty, side, high, timeframe, low)
                        while status != 1:
                            status = CreateOrder.cancel_order2(orderIdTP, pair)
                            time.sleep(1)

                        client2 = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
                        info = client2.futures_time()
                        ts = str(info["serverTime"])
                        t1 = ts[:-3]
                        t2 = int(t1)
                        server_time = datetime.fromtimestamp(t2).strftime('%Y-%m-%d %H:%M:%S')
                        th = datetime.fromtimestamp(t2).strftime('%Y-%m-%d')
                        datetime_object = datetime.strptime(server_time, '%Y-%m-%d %H:%M:%S')
                        nextTF = datetime_object + timedelta(hours=tf)
                        
                        hour1 = int(nextTF.strftime("%H"))    

                        hour = int(datetime_object.strftime("%H"))
                        minute = int(datetime_object.strftime("%M"))
                        second = int(datetime_object.strftime("%S"))

                        if order_type != "TEST":
                            
                            while 1 == 1:
                                
                                second += 1
                                # print(second)

                                if second == 50:
                                    result = db.get_status(pair)

                                    yy = 0
                                    for y in result:
                                        yy += 1

                                    xx = 0
                                    for x in result:
                                        xx += 1
                                        orderIdTP = x['orderIdTP']
                                        orderId = x['orderId']

                                    status = CreateOrder.check_order(orderIdTP, pair)
                                    # print(orderIdTP)
                                    # print(status, orderIdTP, hour, minute, second, pair)

                                    if status != "NEW":
                                        print("EXIT FILLED", orderIdTP, pair)
                                        db.put_order_Exit(pair)
                                        break
                                    
                                    elif minute == 4 or minute == 9 or minute == 14 or minute == 19 or minute == 24 or minute == 29 or minute == 34 or minute == 39 or minute == 44 or minute == 49:
                                    # if hour == hour1 and minute == 59:

                                        print("EXIT by Time Frame", orderId, pair)                                           

                                        status = CreateOrder.cancel_order(orderId, pair, qty, side)

                                        while status != 1:
                                            
                                            status = CreateOrder.cancel_order(orderId, pair, qty, side)
                                            time.sleep(1)         
                                        
                                        print("EXIT by Time Frame", orderIdTP, pair)                               

                                        status = CreateOrder.cancel_order2(orderIdTP, pair)
                                        while status != 1:
                                            status = CreateOrder.cancel_order2(orderIdTP, pair)
                                            time.sleep(1)

                                        print("EXIT by Time Frame", orderIdTP, pair)
                                        db.put_order_Exit(pair)
                                        # insert_TH(th)                                                                             
                                        break                                         

                                if second == 60:
                                    second = 0
                                    minute += 1
                                
                                if minute == 60:
                                    minute = 0
                                    hour += 1

                                if hour == 24:
                                    hour = 0                               

                                time.sleep(1)
                        else:
                            print("EXIT")
                            break

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

    def exit(self):
        print("TEST")
        CreateOrder.cancel_order(orderId, pair)
        CreateOrder.cancel_order(orderIdTP, pair)
        print("EXIT by Time Frame")
        
        
# schedule.every(1).minutes.do(entry)
# schedule.every(1).minutes.do(exit)

client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)

# {'symbol': 'BTCUSDT', 'initialMargin': '4.95575009', 'maintMargin': '0.11893800', 'unrealizedProfit': '-0.06450000', 'positionInitialMargin': '4.95575009', 
# 'openOrderInitialMargin': '0', 'leverage': '6', 'isolated': True, 'entryPrice': '29670.0', 'maxNotional': '20000000', 'positionSide': 'BOTH', 
# 'positionAmt': '-0.001', 'notional': '-29.73450000', 'isolatedWallet': '4.93323209', 'updateTime': 1654335480477, 'bidNotional': '0', 'askNotional': '0'},

# {'feeTier': 0, 'canTrade': True, 'canDeposit': True, 'canWithdraw': True, 'updateTime': 0, 'totalInitialMargin': '4.95550579', 'totalMaintMargin': '0.11893213',
#  'totalWalletBalance': '25.45013785', 'totalUnrealizedProfit': '-0.06303420', 'totalMarginBalance': '25.38710365', 'totalPositionInitialMargin': '4.95550579', 
#  'totalOpenOrderInitialMargin': '0.00000000', 'totalCrossWalletBalance': '20.51690576', 'totalCrossUnPnl': '0.00000000', 'availableBalance': '20.51690576',
#   'maxWithdrawAmount': '20.51690576', 'assets': [{'asset': 'DOT', 'walletBalance': '0.00000000', 'unrealizedProfit': '0.00000000', 'marginBalance': '0.00000000',
#    'maintMargin': '0.00000000', 'initialMargin': '0.00000000', 'positionInitialMargin': '0.00000000', 'openOrderInitialMargin': '0.00000000', 
#    'maxWithdrawAmount': '0.00000000', 'crossWalletBalance': '0.00000000', 'crossUnPnl': '0.00000000', 'availableBalance': '0.00000000', 'marginAvailable': True, 
#    'updateTime': 0}, {'asset': 'BTC', 'walletBalance': '0.00000000', 'unrealizedProfit': '0.00000000', 'marginBalance': '0.00000000', 
#    'maintMargin': '0.00000000', 'initialMargin': '0.00000000', 'positionInitialMargin': '0.00000000', 'openOrderInitialMargin': '0.00000000', 
#    'maxWithdrawAmount': '0.00000000', 'crossWalletBalance': '0.00000000', 'crossUnPnl': '0.00000000', 'availableBalance': '0.00000000', 
#    'marginAvailable': True, 'updateTime': 1653802590669}, {'asset': 'SOL', 'walletBalance': '0.00000000', 'unrealizedProfit': '0.00000000', 
#    'marginBalance': '0.00000000', 'maintMargin': '0.00000000', 'initialMargin': '0.00000000', 'positionInitialMargin': '0.00000000',
#     'openOrderInitialMargin': '0.00000000', 'maxWithdrawAmount': '0.00000000', 'crossWalletBalance': '0.00000000', 'crossUnPnl': '0.00000000',
#      'availableBalance': '0

# while 1==1:
#     orders = client.futures_account()['positions']
#     for x in orders:
#         pnl = float(x['unrealizedProfit'])
#         symbol = x['symbol']
#         margin = float(x['initialMargin'])

#         if pnl != 0 and symbol == 'ETHUSDT': 
#             print("PNL:", round(pnl, 2), symbol, round(margin, 1), "USDT")
#         if pnl != 0 and symbol == 'BTCUSDT': 
#             print("PNL:", round(pnl, 2), symbol, round(margin, 1), "USDT")

#     time.sleep(1)

# print(client.futures_position_information())

# orders = client.futures_position_information(symbol="ETHUSDT")
# print(orders)
# quit()

if __name__ == '__main__':
    # schedule.run_pending()
    # time.sleep(1)
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    pattern_detect = PatternDetect()
    asyncio.get_event_loop().run_until_complete(pattern_detect.main())
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))




