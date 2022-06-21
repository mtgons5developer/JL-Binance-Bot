from datetime import datetime, timedelta
import time
import subprocess

from binance.client import Client
import urllib.request

from TH import insert_TH
import callDB
db = callDB.call()

import config

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
    BCHUSDT = ""
    EOSUSDT = ""    
    XRPUSDT = ""
    SOLUSDT = ""
    LTCUSDT = ""
    TRXUSDT = ""
    DOGEUSDT = ""
    AVAXUSDT = ""
    DOTUSDT = ""
    MATICUSDT = ""
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
        elif pair == "LTCUSDT":
            LTCUSDT = "& python3 LTCUSDT.py"
        elif pair == "TRXUSDT":
            TRXUSDT = "& python3 TRXUSDT.py"
        elif pair == "DOGEUSDT":
            DOGEUSDT = "& python3 DOGEUSDT.py"
        elif pair == "AVAXUSDT":
            AVAXUSDT = "& python3 AVAXUSDT.py"
        elif pair == "DOTUSDT":
            DOTUSDT = "& python3 DOTUSDT.py"
        elif pair == "MATICUSDT":
            MATICUSDT = "& python3 MATICUSDT.py"
        elif pair == "BCHUSDT":
            BCHUSDT = "& python3 BCHUSDT.py"
        elif pair == "EOSUSDT":
            EOSUSDT = "& python3 EOSUSDT.py"

    subprocess.run(BTCUSDT + ETHUSDT + BNBUSDT + XRPUSDT + SOLUSDT + ADAUSDT + LTCUSDT + TRXUSDT + DOGEUSDT + AVAXUSDT + DOTUSDT + MATICUSDT + BCHUSDT + EOSUSDT, shell=True)

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

# result = db.get_order_EntryStatus("BTCUSDT")
# for x in result: print(x['status'])
# quit()
timer()
external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

# if external_ip == "209.35.171.236": 
#     print("Connected")
# else:
#     print(external_ip)
#     quit()
passed = 0
while True:

    second += 1
    
    if minute == 0 and second <= 10:
        print("Main:", minute, second)

        # external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        # if external_ip == "209.35.171.236": # Add new IP Address here.

        print("Entry", minute)
        entry()
        th = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
        insert_TH(th) 
        timer()
        print("Exit", minute, second)
        
        # else:
        #     print("Error: Your new IP Address is:", external_ip)
        #     print("Please register the new IP Address to your Binance API Management.")
        #     quit()

    if second >= 60:
        second = 0
        minute += 1

    if minute >= 60:
        minute = 0
    
    time.sleep(1)

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