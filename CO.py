from datetime import datetime, timedelta
from glob import glob

from binance.client import Client
import config

from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
import callDB

db = callDB.call()
from TH import insert_TH

from binance.helpers import round_step_size

client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
# print("Logged in")
    
class call:
# =============================FUTURES=============================
                      
    def futures_order(self, pair, qty, side, high, timeframe, low):
        
        passed = 0

        try:
            order = client.futures_create_order(
                symbol=pair,
                side=side,
                type="MARKET",
                quantity=qty,
                recvWindow=5000)
            
            passed = 1

        except BinanceAPIException as e:
            print(e.status_code)
            print(e.message)
            print("order1")
            error = e.status_code
            return error

        except BinanceOrderException as e:
            print(e.status_code)
            print(e.message)
            print("order2")
            error = e.status_code
            return error

        if passed == 1:
            
            orderId = order["orderId"]
            side = order["side"]

            market_price = self.check_avgPrice(orderId, pair)
            market_price = float(market_price)

            tp_buy = float(high) - market_price
            tp_buy = float(format(tp_buy).replace("-",""))

            tp_sell = market_price - float(low)
            tp_sell = float(format(tp_sell).replace("-",""))
            # 1809.92  1813.31  1790.00  1797.35
            # print(orderId)
            # print(side)
            # print(market_price)
            # print(high)
            # print(low)
            # print(tp_buy)
            # print(tp_sell)

            profit = 0.30

            if side == "BUY":

                side2 = "SELL"
                tp_buy
                tp_buy = (tp_buy * profit)

                # if pair == "BTCUSDT": 
                #     tp_sell = 200
                # else: tp_sell = 50

                take_profit = tp_buy + market_price
                deci = self.get_quantity_precision(pair)
                take_profit = round(take_profit, deci)
                print("TP:", take_profit, pair)
                                    
            elif side == "SELL":

                side2 = "BUY"
                tp_sell = (tp_sell * profit)

                # if pair == "BTCUSDT": 
                #     tp_sell = 200
                # else: tp_sell = 50

                take_profit = market_price - tp_sell
                deci = self.get_quantity_precision(pair)
                take_profit = round(take_profit, deci)
                print("TP:", take_profit, pair)

            try:
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

            except BinanceAPIException as e:
                print(e.status_code)
                print(e.message)
                print("BinanceAPIException")

            except BinanceOrderException as e:
                print(e.status_code)
                print(e.message)
                print("BinanceOrderException")

            orderIdTP = order2["orderId"]
            status = 1
            # print(orderIdTP)

            print("\nOrderID: %(n)s \nOrderIdTP: %(b)s \nMarket Price: %(c)s \nStatus: %(d)s \nTake Profit: %(e)s \nQuantity: %(f)s \nTime Frame: %(g)s" % 
                {'n': orderId, 'b': orderIdTP, 'c': market_price, 'd': status, 'e': take_profit, 'f': qty, 'g': timeframe})

            # print(pair)
            # print(orderId)
            # print(side)
            # print(market_price)
            # print(take_profit)
            # print(orderIdTP)
            # print(timeframe)
            # print(order_type)
            error = 1
            return error

            db.put_orderID(pair, orderId, side, market_price, qty, take_profit, orderIdTP, timeframe)
            print('-------Order Executed-------')

    def get_quantity_precision(self, pair):    
        info = client.futures_exchange_info() 
        info = info['symbols']
        for x in range(len(info)):
            if info[x]['symbol'] == pair:
                return info[x]['pricePrecision']
        return None

    def check_order(self, pair):

        try:
            result = client.futures_get_open_orders(
                symbol=pair)
                # orderId=orderIdTP)

            # status = result['status']
            print(result)
            # return status
            
        except BinanceAPIException as e:
            print(e.status_code)
            print(e.message)
            print("No order(s) found.")

        except BinanceOrderException as e:
            print(e.status_code)
            print(e.message)
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
            print(e.status_code)
            print(e.message)
            print("No order(s) found.")

        except BinanceOrderException as e:
            print(e.status_code)
            print(e.message)
            print("check order2")

    def cancel_order(self, orderID, pair, qty, side):

        if side == "BUY":
            side = "SELL"
        else:
            side = "BUY"

        try:			
            result = client.futures_create_order(
                symbol=pair,
                side=side,
                type="MARKET",
                quantity=qty,
                recvWindow=5000)
            print('============================')	
            print("Binance Futures order cancelled. ", 'OrderId:', orderID)
            print('============================')	
            status = 1
            return status
        except BinanceAPIException as e:
            print(e.status_code)
            print(e.message)
            print("cancel1 cancel_order")
            status = e
            # status = 2
            return status
        except BinanceOrderException as e:
            print(e.status_code)
            print(e.message)
            print("cancel2 cancel_order")
            status = 3
            return status
    def cancel_order2(self, orderId, pair):

        try:			
            result = client.futures_cancel_order(
                symbol=pair,
                orderId=orderId)
            print('============================')	
            print("Binance Futures order cancelled. ", 'OrderId:', orderId)
            print('============================')	
            status = 1
            return status
        except BinanceAPIException as e:
            print(e.status_code)
            print(e.message)
            print("cancel1 cancel_order2")
            status = 2
            return status            
        except BinanceOrderException as e:
            print(e.status_code)
            print(e.message)
            print("cancel2 cancel_order2")
            status = 3
            return status
    def get_tick_size(self, symbol: str) -> float:
        info = client.futures_exchange_info()

        for symbol_info in info['symbols']:
            if symbol_info['symbol'] == symbol:
                for symbol_filter in symbol_info['filters']:
                    if symbol_filter['filterType'] == 'PRICE_FILTER':
                        return float(symbol_filter['tickSize'])


    def get_rounded_price(self, symbol: str, price: float) -> float:
        return round_step_size(price, self.get_tick_size(symbol))

