import time
from binance.client import Client
import config
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
import callDB

db = callDB.call()
from binance.helpers import round_step_size

client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
# print("Logged in")
    
class call:
# =============================FUTURES=============================

    def futures_order(self, pair, qty, side, high, timeframe, low):
        
        try:
            order = client.futures_create_order(
                symbol=pair,
                side=side,
                type="MARKET",
                quantity=qty,
                recvWindow=15000)          

            time.sleep(5)
            orderId = order["orderId"]
            side = order["side"]

            market_price = self.check_avgPrice(orderId, pair)
            market_price = float(market_price)

            tp_buy = float(high) - market_price
            tp_buy = float(format(tp_buy).replace("-",""))

            tp_sell = market_price - float(low)
            tp_sell = float(format(tp_sell).replace("-",""))

            profit = 0.30

            if side == "BUY":

                side2 = "SELL"
                tp_buy
                tp_buy = (tp_buy * profit)

                take_profit = tp_buy + market_price
                deci = self.get_quantity_precision(pair)
                take_profit = round(take_profit, deci)
                print("TP:", take_profit, pair)
                                    
            elif side == "SELL":

                side2 = "BUY"
                tp_sell = (tp_sell * profit)

                take_profit = market_price - tp_sell
                deci = self.get_quantity_precision(pair)
                take_profit = round(take_profit, deci)
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
                    recvWindow=15000,
                    workingType= 'MARK_PRICE')

            orderIdTP = order2["orderId"]

            print("\nOrderID: %(n)s \nOrderIdTP: %(b)s \nMarket Price: %(c)s \nTake Profit: %(e)s \nQuantity: %(f)s \nTime Frame: %(g)s" % 
                {'n': orderId, 'b': orderIdTP, 'c': market_price, 'e': take_profit, 'f': qty, 'g': timeframe})

            db.put_orderID(pair, orderId, side, market_price, qty, take_profit, orderIdTP, timeframe)
            print('-------Order Executed-------', pair)

        except BinanceAPIException as e:
            print(e.status_code)
            print(e.message)
            print("order1")
            if e.status_code == 400:
                print(qty)
            error = e.status_code
            # return error

        except BinanceOrderException as e:
            print(e.status_code)
            print(e.message)
            print("order2")
            error = e.status_code
            # return error

    def get_quantity_precision(self, pair):    
        info = client.futures_exchange_info() 
        info = info['symbols']
        for x in range(len(info)):
            if info[x]['symbol'] == pair:
                return info[x]['pricePrecision']
        return None

    def check_order(self, orderIdTP, pair):

        try:
            result = client.futures_get_order(
                symbol=pair,
                orderId=orderIdTP)

            status = result['status']
            # print(result)
            return status
            
        except BinanceAPIException as e:
            print(e.status_code)
            print(e.message)
            print("No order(s) found.", pair)

        except BinanceOrderException as e:
            print(e.status_code)
            print(e.message)
            print("check order2", pair)

        # ===========================================================================================

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
            # status = 1
            # return status
        except BinanceAPIException as e:
            print(e.status_code)
            print(e.message)
            print("cancel1 cancel_order")
            # status = e
            # status = 2
            # return status
        except BinanceOrderException as e:
            print(e.status_code)
            print(e.message)
            print("cancel2 cancel_order")
            # status = 3
            # return status
    def cancel_order2(self, orderId, pair):

        try:			
            result = client.futures_cancel_order(
                symbol=pair,
                orderId=orderId)
            print('============================')	
            print("Binance Futures order cancelled. ", 'OrderId:', orderId)
            print('============================')	
            # status = 1
            # return status
        except BinanceAPIException as e:
            print(e.status_code)
            print(e.message)
            print("cancel1 cancel_order2")
            # status = 2
            # return status       
            #      
        except BinanceOrderException as e:
            print(e.status_code)
            print(e.message)
            print("cancel2 cancel_order2")
            # status = 3
            # return status

    def get_tick_size(self, symbol: str) -> float:
        info = client.futures_exchange_info()

        for symbol_info in info['symbols']:
            if symbol_info['symbol'] == symbol:
                for symbol_filter in symbol_info['filters']:
                    if symbol_filter['filterType'] == 'PRICE_FILTER':
                        return float(symbol_filter['tickSize'])


    def get_rounded_price(self, symbol: str, price: float) -> float:
        return round_step_size(price, self.get_tick_size(symbol))

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