from datetime import datetime, timedelta
from glob import glob

from binance.client import Client
import config

from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
# from callDB import put_orderID
import callDB

db = callDB.call()
from TH import insert_TH

from binance.helpers import round_step_size

client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
# print("Logged in")
    
class call:
# =============================FUTURES=============================
                      
    def futures_order(self, pair, qty, side, order_type, high, timeframe, low):
        
        passed = 0

        try:
            order = client.futures_create_order(
                symbol=pair,
                side=side,
                type=order_type,
                quantity=qty,
                recvWindow=5000)
            
            passed = 1

        except BinanceAPIException as e:
            print(e)
            print("order1")

        except BinanceOrderException as e:
            print(e)
            print("order2")

        if passed == 1:
               
            orderId = order["orderId"]
            side = order["side"]

            market_price = self.check_avgPrice(orderId, pair)
            market_price = float(market_price)

            tp_buy = float(high) - market_price
            tp_buy = float(format(tp_buy).replace("-",""))

            tp_sell = market_price - float(low)
            tp_sell = float(format(tp_sell).replace("-",""))

            if side == "BUY":

                side2 = "SELL"
                tp_buy = (tp_buy * 0.30)
                # print(type(tp_buy))
                take_profit = tp_buy + market_price
                take_profit = round(take_profit, 6)
                print("TP:", take_profit, pair)
                                    
            elif side == "SELL":

                side2 = "BUY"
                tp_sell = (tp_sell * 0.30)
                # print(type(tp_sell))
                take_profit = market_price - tp_sell
                take_profit = round(take_profit, 6)
                print("TP:", take_profit, pair)

            order2 = client.futures_create_order(
                symbol=pair,
                side=side2,
                positionSide='BOTH',
                type="TAKE_PROFIT_MARKET",
                    timeInForce='GTC',
                    stopPrice=take_profit,
                    quantity=1,
                    reduceOnly=True,
                    recvWindow=5000,
                    workingType= 'MARK_PRICE')

            orderIdTP = order2["orderId"]
            status = 1

            print("\nOrderID: %(n)s \nOrderIdTP: %(b)s \nMarket Price: %(c)s \nStatus: %(d)s \nTake Profit: %(e)s \nQuantity: %(f)s \nTime Frame: %(g)s" % 
                {'n': orderId, 'b': orderIdTP, 'c': market_price, 'd': status, 'e': take_profit, 'f': qty, 'g': timeframe})

            db.put_orderID(pair, orderId, market_price, qty, status, take_profit, orderIdTP, side, timeframe, order_type)
            print('-------Order Executed-------')

            # last_hour_date_time = datetime.now() - timedelta(hours = 24)
            # get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
            # insert_TH(get_startDate)


                # if order_type == "TEST":
                                
                #     db.put_orderTest(pair, qty, market_price, take_profit, side, order_type, timeframe)
                #     # last_hour_date_time = datetime.now() - timedelta(hours = 24)
                #     # get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                #     # insert_TH(get_startDate)
                #     # print("\nOrder_Position: %(n)s \nOrderIdTP: %(b)s \nMarket Price: %(c)s \nStatus: %(d)s \nTake Profit: %(e)s \nQuantity: %(f)s" % 
                #     #     {'n': orderId, 'b': orderIdTP, 'c': market_price, 'd': status, 'e': take_profit, 'f': qty})

    # {'orderId': 51740849852, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'yBzqOwb4TCJcacDBVXmASM', 'price': '37000.10', 
    # 'avgPrice': '0.00000', 'origQty': '0.002', 'executedQty': '0', 'cumQty': '0', 'cumQuote': '0', 'timeInForce': 'GTC', 'type': 'LIMIT', 
    # 'reduceOnly': False, 'closePosition': False, 'side': 'BUY', 'positionSide': 'BOTH', 'stopPrice': '0', 'workingType': 'CONTRACT_PRICE', 
    # 'priceProtect': False, 'origType': 'LIMIT', 'updateTime': 1651089447160}

    # {'orderId': 56111597252, 'symbol': 'BTCUSDT', 'status': 'FILLED', 'clientOrderId': 'VTRxCD7wQr9ml7TsgG7Lo5', 'price': '0', 'avgPrice': '31805.50000', 
    # 'origQty': '0.002', 'executedQty': '0.002', 'cumQuote': '63.61100', 'timeInForce': 'GTC', 'type': 'MARKET', 'reduceOnly': False, 'closePosition': False, 
    # 'side': 'SELL', 'positionSide': 'BOTH', 'stopPrice': '0', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'MARKET', 'time': 1654050887076, 
    # 'updateTime': 1654050887077}

    def check_order(self, orderIdTP, pair):

        try:
            result = client.futures_get_order(
                symbol=pair,
                orderId=orderIdTP)

            status = result['status']

            return status
            
        except BinanceAPIException as e:
            print(e)
            print("No order(s) found.")

        except BinanceOrderException as e:
            print(e)
            print("check order2")

        # ===========================================================================================

    def check_avgPrice(self, orderIdTP, pair):

        try:
            result = client.futures_get_order(
                symbol=pair,
                orderId=orderIdTP)

            avgPrice = result['avgPrice']
            return avgPrice
            
        except BinanceAPIException as e:
            print(e)
            print("No order(s) found.")

        except BinanceOrderException as e:
            print(e)
            print("check order2")

    def cancel_order(self, orderID, pair):

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

    def get_tick_size(self, symbol: str) -> float:
        info = client.futures_exchange_info()

        for symbol_info in info['symbols']:
            if symbol_info['symbol'] == symbol:
                for symbol_filter in symbol_info['filters']:
                    if symbol_filter['filterType'] == 'PRICE_FILTER':
                        return float(symbol_filter['tickSize'])


    def get_rounded_price(self, symbol: str, price: float) -> float:
        return round_step_size(price, self.get_tick_size(symbol))

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