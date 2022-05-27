from datetime import datetime
from datetime import timedelta

import schedule
import time
import subprocess
import schedule

from binance.client import Client

import callDB
db = callDB.call()

import config

# https://stackoverflow.com/questions/22715086/scheduling-python-script-to-run-every-hour-accurately
# https://schedule.readthedocs.io/en/stable/

def entry():

 # subprocess.run("python3 ETHUSDT.py & python3 BTCUSDT.py & python3 BNBUSDT.py & " + 
    #     "python3 BCHUSDT.py & python3 XRPUSDT.py & python3 EOSUSDT.py & python3 LTCUSDT.py & python3 TRXUSDT.py", shell=True)

    subprocess.run("python3 BTCUSDT-JL.py", shell=True)
    return

#=====================================================================================================================

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
second += 2

while True:

    second += 1

    if minute == 60 and second == 1:
        
        entry()
        
    if second == 60:
        second = 0
        minute += 1
    
    if minute == 60:
        minute = 0
    
    time.sleep(1)
    print(second)

#=====================================================================================================================

# schedule.every(10).minutes.do(entry)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

        # result = db.get_status()
        # print(result)
        # quit()
        # yy = 0
        # for y in result:
        #     yy += 1

        # if yy > 0:

        #     xx = 0
        #     for x in result:
        #         xx += 1
        #         timeframe = x['timeframe']
        #         order_type = x['order_type']
        #         entry_date = x['entry_date']
        #         pair = x['pair']
        #         tf = int(timeframe[:-1])

            # print(timeframe, entry_date, pair, tf, datetime_object)
            # print(type(entry_date))
            # db.put_orderTest_Exit(pair, order_type, timeframe, win_lose)  
