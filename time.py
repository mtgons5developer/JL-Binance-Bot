from datetime import datetime

from binance.client import Client
import config

client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)

acc_balance = client.futures_account_balance()

for check_balance in acc_balance:
    if check_balance["asset"] == "USDT":
        usdt_balance = check_balance["balance"]
        print(round(float(usdt_balance), 4))

dd = round(float(usdt_balance), 4)
print(round(((dd / 33500.01) * 0.25), 6))

quit()

info = client.get_server_time()
print(type(info["serverTime"]))
ts = str(info["serverTime"])
t1 = ts[:-3]
t2 = int(t1)
print(type(t2))
timestamp = datetime.utcfromtimestamp(t2).strftime('%Y-%m-%d %H:%M:%S')
print(timestamp)