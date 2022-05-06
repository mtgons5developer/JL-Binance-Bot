from datetime import datetime, timedelta

import time
import talib
import asyncio
import pandas as pd
import subprocess


from binance.client import AsyncClient
from binance.client import Client


from callDB import get_startDate, put_dateError, get_toggle, get_TH_uuid, get_TH_pair, get_TH_orderID
from CO import futures_order, get_rounded_price, get_tick_size, cancel_order, check_order

import config

def main():

    subprocess.run("python3 ETHUSDT.py & python3 BTCUSDT.py & python3 BNBUSDT.py & " + 
        "python3 BCHUSDT.py & python3 XRPUSDT.py & python3 EOSUSDT.py & python3 LTCUSDT.py & python3 TRXUSDT.py", shell=True)
            
#=====================================================================================================================

if __name__ == '__main__':

    client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
    info = client.get_server_time()
    ts = str(info["serverTime"])
    t1 = ts[:-3]
    t2 = int(t1)
    server_time = datetime.fromtimestamp(t2).strftime('%Y-%m-%d %H:%M:%S')
    datetime_object = datetime.strptime(server_time, '%Y-%m-%d %H:%M:%S')
    print(datetime_object)
    hour = datetime_object.strftime("%H")
    minute = int(datetime_object.strftime("%M"))
    second = int(datetime_object.strftime("%S"))  

    while 1 == 1: 
        # timer = minute + ":" + second
        # print(minute, ":", second)
        second += 1

        main()

        #ENTRY
        if int(repr(minute)[-1]) == 5 and second == 1: #5m
            print("ENTRY 5m")
            print(minute, ":", second)
            #detect toggled at 5m

        # if int(repr(minute)[-1]) == 0 and second == 1: #5m
        #     print("ENTRY 5m")
        #     print(minute, ":", second)

        # if minute == 15 and second == 1: #15m
        #     print("ENTRY 15m")
        #     print(minute, ":", second)

        # if minute == 30 and second == 1: #15m/30m
        #     print("ENTRY 15m/30m")
        #     print(minute, ":", second)

        # if minute == 45 and second == 1: #15m
        #     print("ENTRY 15m")
        #     print(minute, ":", second)

        # if minute == 0 and second == 1: #15m/#30m/1h
        #     print("ENTRY 15m/#30m/1h")
        #     print(minute, ":", second)

        #=================
        #EXIT Store Close price
        if int(repr(minute)[-1]) == 4 and second == 59: #5m
            print("EXIT 5m")
            print(minute, ":", second)

        # if int(repr(minute)[-1]) == 9 and second == 59: #5m
        #     print("EXIT 5m")
        #     print(minute, ":", second)

        # if minute == 14 and second == 59: #15m
        #     print("EXIT 15m")
        #     print(minute, ":", second)

        # if minute == 29 and second == 59: #15m/30m
        #     print("EXIT 15m/30m")
        #     print(minute, ":", second)

        # if minute == 44 and second == 59: #15m
        #     print("EXIT 15m")
        #     print(minute, ":", second)

        # if minute == 59 and second == 59: #15m/#30m/1h
        #     print("EXIT 15m/#30m/1h")
        #     print(minute, ":", second)

        if second == 60:
            second = 0
            minute += 1
        
        if minute == 60:
            minute = 0

        info = client.get_server_time()
        ts = str(info["serverTime"])
        t1 = ts[:-3]
        t2 = int(t1)
        server_time = datetime.fromtimestamp(t2).strftime('%Y-%m-%d %H:%M:%S')
        datetime_object = datetime.strptime(server_time, '%Y-%m-%d %H:%M:%S')
        print(datetime_object)
        quit()
        
        time.sleep(1)