import datetime
import time
from binance.client import Client
import config

from binance.enums import *
from binance import AsyncClient, DepthCacheManager, BinanceSocketManager
from binance.exceptions import BinanceAPIException, BinanceOrderException

from binance.helpers import round_step_size

client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
print("Logged in")

# =============================FUTURES=============================

def futures_order():
    try:
        order = client.futures_create_order(
            symbol=pair,
            side=side,
            type='LIMIT',
            timeInForce='GTC',
            # quoteQty=qty,    
            quantity=qty,            
            recvWindow=5000,
            price=entry_price)
            # buy_order = client.create_test_order(symbol="ETHUSDT, side='BUY', type='MARKET', quoteOrderQty=10)

    except BinanceAPIException as e:
        print(e)
        print("order1")
        quit()

    except BinanceOrderException as e:
        print(e)
        print("order2")
        quit()


    if order['status'] == "NEW":
        time.sleep(5)
        try:                    
            result = client.futures_get_order(
                symbol=pair,
                orderId=order['orderId'])
            # ff = fire.post('/OrderID', order['orderId'], {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})                    
            # print(ff)
            # fire.getInstance().goOffline()
        # print('===========================')
        # print('\nSymbol:', result['symbol'], '\nOrderID:', result['orderId'], '\nPrice:', result['price'], '\nQuantity:', result['origQty'], '\nStatus:', result['status'], '\nTimeInForce:', result['timeInForce'], '\nType:', result['type'], '\nSide:', result['side'], '\nStopPrice:', result['stopPrice'], '\nUnix Timestamp:', result['time'])
        # print("\nBinance Futures order created!")
            
        except BinanceAPIException as e:
            print(e)
            print("check order1")
            quit()
        except BinanceOrderException as e:
            print(e)
            print("check order2")
            quit()            
    
    # ===========================================================================================    

    # LONG 30% TP 
    try:
        CLOSE = 42500
        HIGH = 41150
        TP1 = CLOSE - HIGH
        TP2 = TP1 * 0.30
        TP3 = CLOSE + TP2
        print(TP3)
        
        order = client.futures_create_order(
            symbol=pair,
            side=side,
            type='LIMIT',
            timeInForce='GTC',
            quantity=qty,
            recvWindow=5000,
            price=entry_price)

    except BinanceAPIException as e:
        print(e)
        print("order1")
        quit()

    except BinanceOrderException as e:
        print(e)
        print("order2")
        quit()

    # ===========================================================================================
    try:			
        result = client.futures_cancel_order(
            symbol=pair,
            orderId=order['orderId'])	
        print('============================')	
        print("Binance Futures order cancelled. ", 'OrderId:', order['orderId'])
        print('============================')	
    except BinanceAPIException as e:
        print(e)
        print("cancel1")
        quit()
    except BinanceOrderException as e:
        print(e)
        print("cancel2")
        quit()

def get_tick_size(symbol: str) -> float:
    info = client.futures_exchange_info()

    for symbol_info in info['symbols']:
        if symbol_info['symbol'] == symbol:
            for symbol_filter in symbol_info['filters']:
                if symbol_filter['filterType'] == 'PRICE_FILTER':
                    return float(symbol_filter['tickSize'])


def get_rounded_price(symbol: str, price: float) -> float:
    return round_step_size(price, get_tick_size(symbol))


# dt = '22/03/2022'
# day, month, year = (int(x) for x in dt.split('/'))    
# ans = datetime.date(year, month, day)
# print (ans.strftime("%A"))
# quit()

pair = 'BTCUSDT'
entry_price = 40500.05
entry_price = get_rounded_price(pair, entry_price)

# 3,645.1
# 4,226.4
qty = 0.099
side = 'BUY'

futures_order()
# order()
# cancel()
quit()
