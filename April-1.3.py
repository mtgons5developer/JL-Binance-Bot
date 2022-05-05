# https://www.tradingview.com/script/og7JPrRA-CM-Williams-Vix-Fix-Finds-Market-Bottoms/
# https://python-binance.readthedocs.io/en/latest/websockets.html
# https://www.binance.com/en/support/faq/930bf9127f45403182c178e9a174e6fa
# https://pypi.org/project/service-identity/
# https://stackoverflow.com/questions/42637878/modulenotfounderror-no-module-named-openssl
# https://stackoverflow.com/questions/66167697/python-binance-futures-user-data-websocket

import aiohttp
import time
import numpy as np
import talib
import asyncio
from myconstants import *

from function_futures import futures_short, order_history, sync_time
from numpy import genfromtxt
from io import StringIO
from datetime import datetime 
from binance import AsyncClient, BinanceSocketManager
from binance.exceptions import BinanceAPIException, BinanceOrderException

from binance.client import Client
import config

# client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
# print("Logged in")

async def main():    
    #https://github.com/sammchardy/python-binance
    global RSI_60_SUM, prev_RSI, tick, close, prev_RSI, status, open_price, close_price
    global RSI6_SUM, RSI12_SUM, RSI24_SUM
    client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)

    bsm = BinanceSocketManager(client)
    symbol = "BTCUSDT"
    time_res = client.get_server_time()
    print(time_res)
    quit()
    # async with bsm.trade_socket(symbol) as stream:    
    async with bsm.kline_futures_socket(symbol=symbol, interval='1m') as stream:    
        while True:
            res = await stream.recv()
# {'e': 'continuous_kline', 'E': 1649521533009, 'ps': 'BTCUSDT', 'ct': 'PERPETUAL', 'k': {'t': 1649520000000,
#  'T': 1649523599999, 'i': '1h', 'f': 1375932109315, 'L': 1375992747178, 'o': '42243.90', 'c': '42381.80',
#   'h': '42392.70', 'l': '42164.00', 'v': '3971.038', 'n': 41049, 'x': False, 'q': '167888693.68421',
#    'V': '2286.230', 'Q': '96670726.37288', 'B': '0'}}
            print("======")
            ros = res['k']  
            ts = ros['t'] / 1000
            # print(ts)
            # quit()
            print(datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
            # print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
            # print(ts)
            quit()
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M")
            minute = now.strftime("%M")            
            second = now.strftime("%S")
            current_price = float(ros['c'])
            closeRSI.append(current_price)  
            closeRSI_TP = len(closeRSI)                
            # print(closeRSI_TP)

            if closeRSI_TP >= 56:

                data = ','.join(str(v) for v in closeRSI)   
                RSI60 = np.genfromtxt(StringIO(data), delimiter=",")          
                RSI60V = talib.RSI(RSI60, timeperiod=14)
                RSI6 = talib.RSI(RSI60, timeperiod=6)
                RSI12 = talib.RSI(RSI60, timeperiod=12)                
                RSI24 = talib.RSI(RSI60, timeperiod=24)                

                RSI_60_SUM = RSI_60_SUM + RSI60V[closeRSI_TP-1]
                DIV = round(RSI_60_SUM / closeRSI_TP, 2)

                RSI6_SUM = RSI6_SUM + RSI6[closeRSI_TP-1]
                DIV6 = round(RSI6_SUM / closeRSI_TP, 2)
                
                RSI12_SUM = RSI12_SUM + RSI12[closeRSI_TP-1]
                DIV12 = round(RSI12_SUM / closeRSI_TP, 2)
                
                RSI24_SUM = RSI24_SUM + RSI24[closeRSI_TP-1]
                DIV24 = round(RSI24_SUM / closeRSI_TP, 2)                               
                               
                if not dt_string in minutes_processed:
                    print(dt_string + " ---Starting New Candlesticks---")
                    minutes_processed[dt_string] = True

                    if len(minute_candlesticks) > 0:
                        tick = current_price - minute_candlesticks[-1]["O"]
                        # reset += 1
                        if tick > 0:                        
                           status = "LONG"
                        if tick < 0:                   
                            status = "SHORT"

                        if len(minute_candlesticks) > 2:
                            minute_candlesticks[-1]["C"] = minute_candlesticks[-2]["O"]                            

                        minute_candlesticks[-1]["T"] = round(current_price - minute_candlesticks[-1]["O"], 2)
                        minute_candlesticks[-1]["S"] = status                        

                    minute_candlesticks.append({
                        "m": dt_string,
                        "O": current_price,
                        "R": DIV,
                        "S": status})

                if len(minute_candlesticks) > 1:
                    current_candlestick = minute_candlesticks[-1]

                    for candlestick in minute_candlesticks:
                        # https://www.programcreek.com/python/example/92318/talib.ADX
                        print(candlestick)
            
            if len(minute_candlesticks) > 2:

                ticktock = current_price - minute_candlesticks[-1]["O"]

                if ticktock > 0:
                   status = "LONG"
                if ticktock < 0:
                    status = "SHORT"

                print("#Time:", second,
                    "RSI:", str(DIV),
                    "Price:", current_price,
                    "tick:", round(ticktock),
                    "Position:", status)
 
                print("Green:", DIV24, "Signal:", DIV12, "Red:", DIV6)


if __name__ == "__main__":
    # futures_short()
    # futures_long()
    # order_history()
    # quit()    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


# We are looking for a technical analyst which is able to help us to find technical indicators for trading futures on binance.
# You should have experience with futures trading and have a very good knowledge about technical indicators.

# The goal of this job is, you have to help us to find and configure technical indicators with the correct values.

# E.g we are looking for indicators which are based on the volume, if there is a spike of the volume then place a trade, etc. we want to skip side-ways trends and so on.

# https://github.com/sammchardy/python-binance/issues/489