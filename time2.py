from datetime import datetime, timedelta, timezone
# from date time import timedelta
import time
import asyncio
import numpy as np
import schedule
from binance.client import Client
from binance import AsyncClient, BinanceSocketManager
from binance.exceptions import BinanceAPIException, BinanceOrderException

import config
# import schedule
# import callDB

# db = callDB.call()

client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)

ts = int('1655751600')
tz = timezone(-timedelta(hours=-9))
print(datetime.fromtimestamp(ts, tz).strftime('%Y-%m-%d %H:%M:%S'))

quit()
import matplotlib.pyplot as plt
import numpy as np
import urllib.request

external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

if external_ip == "209.35.172.250":
    print(external_ip)
quit()
def write_error(error_info):
    
    with open('debug.txt', 'a') as f:
        f.write(error_info)

e1 = "e.status_code"
e2 = "e.message"
e3 = "Error: BinanceAPIException futures_order"
datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
write_error(error_info)


quit()
xpoints = np.array([1, 8])
ypoints = np.array([3, 10])

plt.plot(xpoints, ypoints)
plt.show()

quit()
async def main():    

    client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
    bsm = BinanceSocketManager(client)
    symbol = 'BTCUSDT'
    s_socket = bsm.kline_futures_socket(symbol=symbol, interval='1m')
    async with s_socket as symbol_socket:
        while True:
            res = await symbol_socket.recv()
            price = res['k']['c']
            print(price)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

# print(datetime.today().strftime('%Y-%m-%d'))
quit()

def exit():
    global passed

    passed = 1
    print("exit")

def entry():
    print("entry")

client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
info = client.get_server_time()
ts = str(info["serverTime"])
t1 = ts[:-3]
t2 = int(t1)
server_time = datetime.fromtimestamp(t2).strftime('%Y-%m-%d %H:%M:%S')
datetime_object = datetime.strptime(server_time, '%Y-%m-%d %H:%M:%S')
second = int(datetime_object.strftime("%S"))  
sec = abs(second - 60)

passed = 0
print(sec)
schedule.every(sec).seconds.do(exit)
if passed == 1: 
    print("entry")
    schedule.every(sec).seconds.do(entry)
    passed = 0

while True:
    print(second, passed)
    second += 1
    schedule.run_pending()
    
    if second == 60:
        second = 0

    time.sleep(1)

v1 = 31065.4
v2 = 31064.5
p1 = v1 - v2
p2 = (v1 + v2) / 2
p3 = p1 / p2
p4 = round(float(p3 * 100), 3)
p5 = p4 * 100
print(p5)
quit()


# a = [23427.4, 23389.6, 22495.6, 21106.7, 22734.5, 22358.2, 22114.1, 22106.8, 22160.6, 22216.4, 21548.8, 20681.0, 21258.2]
a = [31087.8, 30625.0, 29257.6, 29487.7, 31616.6, 29631.1, 30102.0]
print(np.diff(a))
quit()

# 55  2022-05-15 22:00:00  31065.4  31462.0  31064.5  31087.8   21418.975   -100  30128.0  30206.0  0.06    True   True   True   True
# 90  2022-05-17 09:00:00  30560.0  30717.3  30550.0  30625.0   10653.588   -100  30153.0  30106.0  0.39    True   True   True  False
# 124 2022-05-18 19:00:00  29186.6  29534.4  29160.1  29257.6   23308.456   -100  29706.0  29640.0  0.19    True  False  False  False
# 202 2022-05-22 01:00:00  29455.4  29537.5  29455.4  29487.7    3399.539   -100  29429.0  29383.0  0.39    True   True   True   True
# 425 2022-05-31 08:00:00  31570.5  31720.0  31562.7  31616.6   10660.162   -100  31012.0  31292.0  0.29    True   True   True  False
# 593 2022-06-07 08:00:00  29569.1  29720.0  29540.5  29631.1   14950.566   -100  30385.0  30490.0  0.35    True  False  False  False
# 660 2022-06-10 03:00:00  30009.0  30374.1  30007.6  30102.0   20828.940   -100  30174.0  30145.0  0.25    True  False  False  False

# orders = round(float(client.futures_account()['totalWalletBalance']), 3)
# print(orders)

# for x in orders:
#     pnl = float(x['unrealizedProfit'])
#     symbol = x['symbol']
#     margin = float(x['initialMargin'])

#     if pnl != 0 and symbol == 'ETHUSDT': 
#         print("PNL:", round(pnl, 2), symbol, round(margin, 1), "USDT")
#     if pnl != 0 and symbol == 'BTCUSDT': 
#         print("PNL:", round(pnl, 2), symbol, round(margin, 1), "USDT")


# print(client.futures_position_information())
quit() 

# import multiprocessing as mp
# print("Number of processors: ", mp.cpu_count())

# quit()


# num = -10
# print(format(num).replace("-",""))
# quit()

client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
pair = "ETHUSDT"
# pair = "BTCUSDT"
# orderID = '8389765524647079298'
orderID = 56385351240


try:			
    order = client.futures_create_order(
        symbol=pair,
        side='BUY',
        type="MARKET",
        quantity='0.02',
        recvWindow=5000)

    print('============================')	
    print("Binance Futures order cancelled. ", 'OrderId:', orderID)
    print('============================')	
except BinanceAPIException as e:
    print(e)
    print("cancel1")
    quit()
except BinanceOrderException as e:
    print(e)
    print("cancel2")
quit()

try:
    result = client.futures_get_order(
        symbol=pair,
        orderId=orderID)

    status = result['status']
    print(status)
    print(result)

except BinanceAPIException as e:
    print(e)
    print("cancel1")
    quit()
except BinanceOrderException as e:
    print(e)
    print("cancel2")

quit()

def get_quantity_precision(currency_symbol):    
    info = client.futures_exchange_info() 
    info = info['symbols']
    for x in range(len(info)):
        if info[x]['symbol'] == currency_symbol:
            return info[x]['pricePrecision']
    return None

print(get_quantity_precision("XRPUSDT"))
quit()

client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)

pos = client.futures_get_all_orders(symbol="BTCUSDT")
# pos2 = client.futures_get_all_orders(orderId="")
# print(pos)
for pos2 in pos:
    if pos2["symbol"] == "BTCUSDT":
        orderId = pos2["status"]
        print(orderId)
        # print(round(float(usdt_balance), 4))
quit()

# [{'orderId': 55640823848, 'symbol': 'BTCUSDT', 'status': 'FILLED', 'clientOrderId': 'web_yZhjXYLyPHgsEMOchLwh', 'price': '0', 
# 'avgPrice': '28463.40000', 'origQty': '0.063', 'executedQty': '0.063', 'cumQuote': '1793.19420', 'timeInForce': 'GTC', 
# 'type': 'MARKET', 'reduceOnly': False, 'closePosition': False, 'side': 'BUY', 'positionSide': 'BOTH', 'stopPrice': '0', 
# 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'MARKET', 'time': 1653678033406, 'updateTime': 1653678033406}, 
# {'orderId': 55640956865, 'symbol': 'BTCUSDT', 'status': 'CANCELED', 'clientOrderId': 'web_T7dZijGDPJPQrauy4m5D', 'price': '0', 
# 'avgPrice': '0.00000', 'origQty': '0', 'executedQty': '0', 'cumQuote': '0', 'timeInForce': 'GTE_GTC', 'type': 'TAKE_PROFIT_MARKET', 
# 'reduceOnly': True, 'closePosition': True, 'side': 'SELL', 'positionSide': 'BOTH', 'stopPrice': '28700', 'workingType': 'MARK_PRICE', 
# 'priceProtect': False, 'origType': 'TAKE_PROFIT_MARKET', 'time': 1653678093156, 'updateTime': 1653678409818}, {'orderId': 55641522022, 
# 'symbol': 'BTCUSDT', 'status': 'EXPIRED', 'clientOrderId': 'web_7YRnPCg7q4I70EtchC5w', 'price': '0', 'avgPrice': '0.00000', 'origQty': '0', 
# 'executedQty': '0', 'cumQuote': '0', 'timeInForce': 'GTE_GTC', 'type': 'TAKE_PROFIT_MARKET', 'reduceOnly': True, 
# 'closePosition': True, 'side': 'SELL', 'positionSide': 'BOTH', 'stopPrice': '29650', 'workingType': 'MARK_PRICE', 
# 'priceProtect': False, 'origType': 'TAKE_PROFIT_MARKET', 'time': 1653678420309, 'updateTime': 1653681739876}, {'orderId': 55647255839, 
# 'symbol': 'BTCUSDT', 'status': 'FILLED', 'clientOrderId': 'web_6cInnUOiAhvSh2gL6GeU', 'price': '0', 'avgPrice': '28803.80000', 
# 'origQty': '0.063', 'executedQty': '0.063', 'cumQuote': '1814.63940', 'timeInForce': 'GTC', 'type': 'MARKET', 'reduceOnly': True, 
# 'closePosition': False, 'side': 'SELL', 'positionSide': 'BOTH', 'stopPrice': '0', 'workingType': 'CONTRACT_PRICE', 
# 'priceProtect': False, 'origType': 'MARKET', 'time': 1653681739876, 'updateTime': 1653681739876}]

# {'symbol': 'BTCUSDT', 'initialMargin': '23.94797654', 
# 'maintMargin': '7.18438937', 'unrealizedProfit': '2.90314293', 'positionInitialMargin': '23.94797654', 'openOrderInitialMargin': '0', 
# 'leverage': '75', 'isolated': True, 'entryPrice': '28463.4', 'maxNotional': '250000', 'positionSide': 'BOTH', 'positionAmt': '0.063', 
# 'notional': '1796.09734293', 'isolatedWallet': '24.06641386', 'updateTime': 1653678033406, 'bidNotional': '0', 'askNotional': '0'},


for check_balance in pos:
    if check_balance["positions"] == "BTCUSDT":
        usdt_balance = check_balance["balance"]
        print(round(float(usdt_balance), 4))


quit()
# Get current time in local timezone
current_time = datetime.now()
n = 2
# Add 2 hours to datetime object containing current time
future_time = current_time + timedelta(hours=n)

def entry():
    print('1')
    return

def entry2():
    print('2')
    return

# schedule.every(1).minutes.do(entry)
# schedule.every(1).minutes.do(entry2)

# while True:
#     schedule.run_pending()
#     time.sleep(1)



acc_balance = client.futures_account_balance()

for check_balance in acc_balance:
    if check_balance["asset"] == "USDT":
        usdt_balance = check_balance["balance"]
        print(round(float(usdt_balance), 4))

dd = round(float(usdt_balance), 4)
# print(round(((dd / 29900.01) * 0.25), 6))
print((dd * 125) / 42000)
# (amount*leverage)/price

if 0 < -0.3:
    print('1')
else:
    print('2')

quit()

def get_liquidation_price(self):
        # this method ignores the hedge mode

        # wallet balance
        wb = self.get_wallet_balance()

        # @TODO this needs to use other position maintenance margin
        # maintenance margin of all other contracts, excluding current contract.
        # if it is an isolated margin mode, then TMM=0
        tmm = 0

        # @TODO this needs to use other position upnl
        # unrealized pnl of all other contracts, excluding current contract
        # if it is an isolated margin mode, then UPNL=0
        upnl = 0

        # maintenance amount of both position (one-way mode)
        # unsure what this number is, but its not maintenance margin before liquidation.
        # perhaps this is the number after liquidation.
        cumb = 0

        # direction of BOTH position, 1 as long position, -1 as short position
        side1both = 1 if self.__current_trade_side == OrderSide.BUY else -1

        # absolute value of BOTH position size (one-way mode)
        position1both = self.get_current_futures_position_amount()

        # entry price of BOTH position (one-way mode)
        ep1both = self.__get_current_futures_position_entry_price()

        # Maintenance margin rate of BOTH position (one-way mode)
        mmb = self.__get_maintenance_margin_rate()

        return (wb - tmm + upnl + cumb - side1both * position1both * ep1both) /\
               (position1both * mmb - side1both * position1both)

info = client.get_server_time()
print(type(info["serverTime"]))
ts = str(info["serverTime"])
t1 = ts[:-3]
t2 = int(t1)
print(type(t2))
timestamp = datetime.utcfromtimestamp(t2).strftime('%Y-%m-%d %H:%M:%S')
print(timestamp)
