import time
from binance.client import Client
import config

from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from callDB import put_orderID

from binance.helpers import round_step_size

client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
# print("Logged in")

# =============================FUTURES=============================

def futures_order(pair, qty, entry_price, side, type, high, close):

#     "clientOrderId": "testOrder",
#     "cumQty": "0",
#     "cumQuote": "0",
#     "executedQty": "0",
#     "orderId": 22542179,
#     "avgPrice": "0.00000",
#     "origQty": "10",
#     "price": "0",
#     "reduceOnly": false,
#     "side": "BUY",
#     "positionSide": "SHORT",
#     "status": "NEW",
#     "stopPrice": "9300",        // please ignore when order type is TRAILING_STOP_MARKET
#     "closePosition": false,   // if Close-All
#     "symbol": "BTCUSDT",
#     "timeInForce": "GTC",
#     "type": "TRAILING_STOP_MARKET",
#     "origType": "TRAILING_STOP_MARKET",
#     "activatePrice": "9020",    // activation price, only return with TRAILING_STOP_MARKET order
#     "priceRate": "0.3",         // callback rate, only return with TRAILING_STOP_MARKET order
#     "updateTime": 1566818724722,
#     "workingType": "CONTRACT_PRICE",
#     "priceProtect": false            // if conditional order trigger is protected   

    try:
        if type == "MARKET":
            order = client.futures_create_order(
                symbol=pair,
                side=side,
                type=type,
                timeInForce='GTC',
                quantity=qty,            
                recvWindow=2000)
                
        else:
            order = client.futures_create_order(
                symbol=pair,
                side=side,
                type=type,
                timeInForce='GTC',
                quantity=qty,            
                recvWindow=2000,
                price=entry_price)

        orderId = order["orderId"]

        tp1 = high - close
        tp2 = tp1 * 0.30
        take_profit = round(close + tp2, 6)

        if side == "BUY":
            side = "SELL"
        else:
            side = "BUY"

        order2 = client.futures_create_order(
            symbol=pair,
            side=side,
            positionSide='BOTH',
            type="TAKE_PROFIT_MARKET",
            timeInForce='GTC',
            stopPrice=take_profit,
            quantity=1,    
            reduceOnly=True,
            workingType= 'MARK_PRICE')

        orderId2 = order2["orderId"]
        # put_orderID(orderId)
        print("Order#1: %(n)s Order#2: %(b)s" % {'n': orderId, 'b': orderId2})

    except BinanceAPIException as e:
        print(e)
        print("order1")

    except BinanceOrderException as e:
        print(e)
        print("order2")

# {'orderId': 51740849852, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'yBzqOwb4TCJcacDBVXmASM', 'price': '37000.10', 
# 'avgPrice': '0.00000', 'origQty': '0.002', 'executedQty': '0', 'cumQty': '0', 'cumQuote': '0', 'timeInForce': 'GTC', 'type': 'LIMIT', 
# 'reduceOnly': False, 'closePosition': False, 'side': 'BUY', 'positionSide': 'BOTH', 'stopPrice': '0', 'workingType': 'CONTRACT_PRICE', 
# 'priceProtect': False, 'origType': 'LIMIT', 'updateTime': 1651089447160}      
    # if order['status'] == "NEW":
    #     time.sleep(5)#   
        # try:                    
        #     result = client.futures_get_order(
        #         symbol=pair,
        #         orderId=order['orderId'],
        #         qq=order['origQty'],
        #         pp=order['price'])
            
        #     print("orderId:" + order['orderId'], "origQty:" + order['origQty'], "Price:" + order['price'])
        #     quit()
        #     # Insert to DB
            
        # except BinanceAPIException as e:
        #     print(e)
        #     print("check order1")

        # except BinanceOrderException as e:
        #     print(e)
        #     print("check order2")

    # ===========================================================================================

def cancel_order(orderID, pair):
    try:			
        result = client.futures_cancel_order(
            symbol=pair,
            orderId=orderID)	
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

# pair = 'BTCUSDT'
# entry_price = 37000.05
# entry_price = get_rounded_price(pair, entry_price)

# 3,645.1
# 4,226.4
# qty = 0.099
# qty = 0.002
# side = 'BUY'

# futures_order()
# order()
# cancel()
# quit()
