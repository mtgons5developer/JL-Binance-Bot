import time
import asyncio
import talib
import numpy as np
from numpy import genfromtxt
from io import StringIO
from datetime import datetime

from binance.client import Client
from binance import AsyncClient, BinanceSocketManager
from binance.exceptions import BinanceAPIException, BinanceOrderException

import config
import callDB
import CO 

db = callDB.call()
CreateOrder = CO.call()

client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)

DataFrame = []
minutes_processed = {} #dictionary
minute_candlesticks = [] #list
seconds_processed = {} #dictionary
second_candlesticks = [] #list
current_tick = None
previous_tick = None
closeRSI = []
closeRSI_TP = 0
RSI_60_SUM = 0
tick = 0

async def mainn():    
    
    try:
        client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
        bsm = BinanceSocketManager(client)
        symbol = 'BTCUSDT'
        s_socket = bsm.kline_futures_socket(symbol=symbol, interval='1h')
        async with s_socket as symbol_socket:
            global price, prev_price, entry_price, take_profit
            prev_price = 0
            entry_price = 0
            take_profit = 0
            take = 0
            side = "SELL"
            # side = "BUY"
            orderSL = 0

            while True:

                try: # RSI divergence.
                    res = await symbol_socket.recv()
                    price = round(float(res['k']['c']), 2)
                    if price != prev_price: print("\nPrice: ", price, "\nTake Profit:", take_profit, "\nEntry Price:", entry_price)
                    prev_price = price

                    if take == 0 : entry_price = price

                    if entry_price != 0 and take == 0:
                        take = 1
                        m1 = round(price * 0.0015, 2)
                        if side == "SELL":
                            take_profit = round(entry_price - m1, 2)
                        else:
                            take_profit = round(entry_price + m1, 2)

                    if float(price) < float(take_profit) and side == "SELL" and take_profit != 0: 
                        if orderSL != 0: print("")
                        print("SL created.")
                        print("SL order check.")
                        print("SL adjusted.")
                        print("\nPrice: ", price, "\nTake Profit:", take_profit, "\nEntry Price:", entry_price)
                        take = 0
                        await client.close_connection()
                        break

                    #========================
                    # now = datetime.now()
                    # print(now)
                    # dt_string = now.strftime("%d/%m/%Y %H:%M")
                    # print(now)
                    # minute = now.strftime("%M")
                    # previous_tick = price

                    # DataFrame.append(price)
                    # df = len(DataFrame)

                    # if df >= 56:

                    #     data = ','.join(str(v) for v in DataFrame)
                    #     RSI60 = np.genfromtxt(StringIO(data), delimiter=",")
                    #     RSI60V = talib.RSI(RSI60, timeperiod=14)
                        # fastk, fastd = talib.STOCHRSI(RSI60, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

                        # print(fastk, fastk)
                        # print(RSI60V, fastk, fastk)
                    #     if not dt_string in minutes_processed:
                    #         print(dt_string + " ---Starting New Candlesticks---")
                    #         minutes_processed[dt_string] = True

                    #         if len(minute_candlesticks) > 0:
                    #             tick = price - minute_candlesticks[-1]["O"]

                    #         if len(minute_candlesticks) > 2:
                    #             minute_candlesticks[-1]["C"] = minute_candlesticks[-2]["O"]

                    #         minute_candlesticks[-1]["T"] = price - minute_candlesticks[-1]["O"]
                    #         # minute_candlesticks[-1]["S"] = status

                    # if len(minute_candlesticks) > 1:
                    #     current_candlestick = minute_candlesticks[-1]

                    # await asyncio.sleep(0.5)
                except:
                    print("ERROR")
                    await asyncio.sleep(0.5)
                    quit()
        
        await client.close_connection()
        quit()

    except BinanceAPIException as e:

        e1 = e.status_code
        e2 = e.message
        e3 = "Error: BinanceAPIException mainn"
        datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
        print(error_info)
        db.write_error(error_info)  

    except BinanceOrderException as e:
        
        e1 = e.status_code
        e2 = e.message
        e3 = "Error: BinanceOrderException mainn"
        datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
        print(error_info)
        db.write_error(error_info)  

    # await client.close_connection()

def orderSL(self, orderId, side2, pair, stop_loss, qty):

    order = client.futures_create_order(
        symbol=pair,
        side=side2,
        type="STOP_MARKET",
            timeInForce='GTC',
            stopPrice=stop_loss,
            closePosition=True)
    
    time.sleep(1)
    orderIdSL = order["orderId"]

def check_avgPrice(self, orderIdTP, pair):

    try:
        result = client.futures_get_order(
            symbol=pair,
            orderId=orderIdTP)

        avgPrice = result['avgPrice']
        return avgPrice

    except BinanceAPIException as e:
        e1 = e.status_code
        e2 = e.message
        e3 = "Error: BinanceAPIException check_avgPrice"
        datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
        print(error_info)
        db.write_error(error_info)     

    except BinanceOrderException as e:
        e1 = e.status_code
        e2 = e.message
        e3 = "Error: BinanceOrderException check_avgPrice"
        datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
        print(error_info)
        db.write_error(error_info)   

def get_quantity_precision(self, pair):   
    try:

        info = client.futures_exchange_info() 
        info = info['symbols']
        for x in range(len(info)):
            if info[x]['symbol'] == pair:
                return info[x]['pricePrecision']

    except BinanceAPIException as e:
        e1 = e.status_code
        e2 = e.message
        e3 = "Error: BinanceAPIException get_quantity_precision"
        datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
        print(error_info)
        db.write_error(error_info)     

    except BinanceOrderException as e:
        e1 = e.status_code
        e2 = e.message
        e3 = "Error: BinanceOrderException get_quantity_precision"
        datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
        print(error_info)
        db.write_error(error_info)   


loop = asyncio.get_event_loop()
loop.run_until_complete(mainn())
