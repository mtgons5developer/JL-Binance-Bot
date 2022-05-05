from datetime import datetime

from binance.client import Client
import config

client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)

info = client.get_server_time()
print(type(info["serverTime"]))
ts = str(info["serverTime"])
t1 = ts[:-3]
t2 = int(t1)
print(type(t2))
timestamp = datetime.utcfromtimestamp(t2).strftime('%Y-%m-%d %H:%M:%S')
print(timestamp)