from datetime import datetime
from datetime import timedelta

import time
import subprocess

from binance.client import Client

import callDB
db = callDB.call()

import config

# https://stackoverflow.com/questions/22715086/scheduling-python-script-to-run-every-hour-accurately
# https://schedule.readthedocs.io/en/stable/

def entry():

 # subprocess.run("python3 ETHUSDT.py & python3 BTCUSDT.py & python3 BNBUSDT.py & " + 
    #     "python3 BCHUSDT.py & python3 XRPUSDT.py & python3 EOSUSDT.py & python3 LTCUSDT.py & python3 TRXUSDT.py", shell=True)

    # subprocess.run("python3 BTCUSDT-JL.py", shell=True)
    subprocess.run("python3 BTCUSDT-JL.py & python3 ETHUSDT.py", shell=True)
    return

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

result = db.get_toggle()
yy = 0
for y in result:
    yy += 1

xx = 0
for x in result:
    xx += 1
    pair = x['pair']
    print("Active Pairs:", pair)

timer()

while True:

    #if coin is activated then read order entry at X time.
    second += 1
    # print(minute, second)

    if second == 60:
        second = 0
        minute += 1
    
    if second == 1:
        if minute == 5 or minute == 10 or minute == 15 or minute == 20 or minute == 25 or minute == 30 or minute == 35 or minute == 40 or minute == 45 or minute == 50 or minute == 55 or minute == 0:
        # if minute == 26 and second == 1:
            print("Entry", minute)
            entry()
            timer()
            print("Exit")

    # if minute == 26 and second == 1:
        # print("Entry")
        # entry()
        # timer()
        # print("Exit")

    if minute == 60:
        minute = 0
    
    time.sleep(1)



