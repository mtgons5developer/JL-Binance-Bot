from datetime import datetime, timedelta

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

    def futures_order(self, pair, qty, entry_price, take_profit, side, type, high, close):

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

        # if pair == "BTCUSDT":            
        #     take_profit = 41000.01
        #     entry_price = 32000
        # if pair == "ETHUSDT":            
        #     take_profit = 3000.01
        #     entry_price = 2000
        # if pair == "BNBUSDT":            
        #     take_profit = 400.01
        #     entry_price = 200
        # if pair == "BCHUSDT":            
        #     take_profit = 400.01
        #     entry_price = 200
        # if pair == "XRPUSDT":            
        #     take_profit = 0.7
        #     entry_price = 0.4
        # if pair == "SOLUSDT":            
        #     take_profit = 3.01
        #     entry_price = 1
        # if pair == "LUNAUSDT":            
        #     take_profit = 200.01
        #     entry_price = 50
        # if pair == "ADAUSDT":            
        #     take_profit = 0.09
        #     entry_price = 0.05
        # if pair == "USTUSDT":            
        #     take_profit = 0.7
        #     entry_price = 0.4
        # if pair == "BUSDUSDT":            
        #     take_profit = 3.01
        #     entry_price = 1          
        # if pair == "DOGEUSDT":            
        #     take_profit = 200.01
        #     entry_price = 50
        # if pair == "AVAXUSDT":            
        #     take_profit = 0.09
        #     entry_price = 0.05
        # if pair == "DOTUSDT":            
        #     take_profit = 0.7
        #     entry_price = 0.4
        # if pair == "SHIBUSDT":            
        #     take_profit = 3.01
        #     entry_price = 1
        # if pair == "WBTCUSDT":            
        #     take_profit = 200.01
        #     entry_price = 50
        # if pair == "DAIUSDT":            
        #     take_profit = 0.09
        #     entry_price = 0.05
        # if pair == "MATICUSDT":            
        #     take_profit = 0.09
        #     entry_price = 0.05

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
            market_price = order["price"]

            # tp1 = high - close
            # tp2 = tp1 * 0.30
            # take_profit = round(close + tp2, 6)
                                                                                        
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

            orderIdTP = order2["orderId"]
            status = 1
            db.put_orderID(orderId, market_price, qty, status, take_profit, orderIdTP)

            last_hour_date_time = datetime.now() - timedelta(hours = 24)
            get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
            insert_TH(get_startDate)

            print("\nOrder_Position: %(n)s \nOrderIdTP: %(b)s \nMarket Price: %(c)s \nStatus: %(d)s \nTake Profit: %(e)s \nQuantity: %(f)s" % 
                {'n': orderId, 'b': orderIdTP, 'c': market_price, 'd': status, 'e': take_profit, 'f': qty})

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

    def check_order(self, orderId):

        try:                    
            result = client.futures_get_order(
                orderId=orderId)        

            # Insert to DB
            print(result['orderId'])
            quit()
            
        except BinanceAPIException as e:
            print(e)
            print("No order(s) found.")

        except BinanceOrderException as e:
            print(e)
            print("check order2")

        # ===========================================================================================

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
