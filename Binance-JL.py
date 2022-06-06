from datetime import datetime, timedelta
import time
import subprocess

from binance.client import Client

import callDB
db = callDB.call()

import config

# https://stackoverflow.com/questions/22715086/scheduling-python-script-to-run-every-hour-accurately
# https://schedule.readthedocs.io/en/stable/

# BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT, SOLUSDT, LUNAUSDT, ADAUSDT, USTUSDT, BUSDUSDT, 
# DOGEUSDT, AVAXUSDT, DOTUSDT, SHIBUSDT, WBTCUSDT, DAIUSDT, MATICUSDT

#=====================================================================================================================

def timer():
    global hour, minute, second

    client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
    info = client.futures_time()
    ts = str(info["serverTime"])
    t1 = ts[:-3]
    t2 = int(t1)
    server_time = datetime.fromtimestamp(t2).strftime('%Y-%m-%d %H:%M:%S')
    datetime_object = datetime.strptime(server_time, '%Y-%m-%d %H:%M:%S')
    print(datetime_object)
    hour = datetime_object.strftime("%H")
    minute = int(datetime_object.strftime("%M"))
    second = int(datetime_object.strftime("%S"))
    second += 2

def entry():
    
    BTCUSDT = ""
    ETHUSDT = ""
    BNBUSDT = ""
    XRPUSDT = ""
    SOLUSDT = ""
    ADAUSDT = ""

    result = db.get_toggle()
    yy = 0
    for y in result:
        yy += 1

    xx = 0
    for x in result:
        xx += 1
        pair = x['pair']
        print(pair)

        if pair == "BTCUSDT":
            BTCUSDT = "python3 BTCUSDT-JL.py"
        elif pair == "ETHUSDT":
            ETHUSDT = "& python3 ETHUSDT.py"
        elif pair == "BNBUSDT":
            BNBUSDT = "& python3 BNBUSDT.py"
        elif pair == "XRPUSDT": 
            XRPUSDT = "& python3 XRPUSDT.py"
        elif pair == "SOLUSDT":
            SOLUSDT = "& python3 SOLUSDT.py"
        elif pair == "ADAUSDT":
            ADAUSDT = "& python3 ADAUSDT.py"

    subprocess.run(BTCUSDT + ETHUSDT + BNBUSDT + XRPUSDT + SOLUSDT + ADAUSDT, shell=True)

result = db.get_toggle()
yy = 0
for y in result:
    yy += 1

xx = 0
for x in result:
    xx += 1
    pair = x['pair']
    tf = x['timeframe']
    db.put_order_Exit(pair)
    print("Active Pairs:", pair, tf)

timer()

while True:

    #if coin is activated then read order entry at X time.
    second += 1
    print(minute, second)
    
    if second == 1:
        if minute == 28:# or minute == 10 or minute == 15 or minute == 20 or minute == 25 or minute == 30 or minute == 35 or minute == 40 or minute == 45 or minute == 50 or minute == 55 or minute == 0:
            print("Entry", minute)
            entry()
            timer()
            print("Exit")

    # if minute == 4 and second == 1:
    #     print("Entry")
    #     entry()
    #     timer()
    #     print("Exit")

    if second >= 60:
        second = 0
        minute += 1

    if minute >= 60:
        minute = 0
    
    time.sleep(1)


