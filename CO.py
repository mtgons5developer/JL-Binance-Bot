import time
from binance.client import Client
import config
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
import callDB
db = callDB.call()
client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
# print("Logged in")

class call:
# =============================FUTURES=============================

    def futures_order_main(self, pair, qty, side, timeframe, high, low):

        try:
            order = client.futures_create_order(
                symbol=pair,
                side=side,
                type="MARKET",
                quantity=qty,
                recvWindow=15000)          

            time.sleep(2)            
            orderId = order["orderId"]
            side = order["side"]
            market_price = self.check_avgPrice(orderId, pair)
            market_price = float(market_price)

            tp_buy = float(high) - market_price
            tp_buy = float(format(tp_buy).replace("-",""))

            tp_sell = market_price - float(low)
            tp_sell = float(format(tp_sell).replace("-",""))

            profit = 0.65
            fee_range = 0.0025

            if side == "BUY":

                side2 = "SELL"
                tp_buy
                tp_buy = (tp_buy * profit)

                # take_profit = tp_buy + market_price
                take_profit = abs(tp_buy - market_price)
                fee = market_price * fee_range

                if take_profit <= fee: # Resistance
                    take_profit = fee

                deci = self.get_quantity_precision(pair)
                take_profit = round(take_profit, deci)
                print("TP:", take_profit, pair)

            elif side == "SELL":

                side2 = "BUY"
                tp_sell = (tp_sell * profit)

                # take_profit = market_price - tp_sell
                take_profit = market_price + tp_sell
                fee = market_price * fee_range

                if take_profit <= fee:
                    take_profit = fee

                deci = self.get_quantity_precision(pair)
                take_profit = round(take_profit, deci)
                print("TP:", take_profit, pair)

            order2 = client.futures_create_order(

                symbol=pair,
                side=side2,
                positionSide='BOTH',
                type="STOP_MARKET",
                timeInForce='GTC',
                stopPrice=take_profit,
                quantity=1,
                closePosition=True,
                recvWindow=15000,
                workingType= 'MARK_PRICE')

            orderIdTP = order2["orderId"]
            time.sleep(1)

            username = db.get_user()["name"]
            balance = round(float(client.futures_account()['totalWalletBalance']), 3)

            print("\nOrderID: %(n)s \nOrderIdTP: %(b)s \nMarket Price: %(c)s \nStop Loss: %(e)s \nQuantity: %(f)s \nTime Frame: %(g)s \nBlance: %(h)s \nUsername: %(i)s" % 
                {'n': orderId, 'b': orderIdTP, 'c': market_price, 'e': take_profit, 'f': qty, 'g': timeframe, 'h': balance, 'i': username})
               
            db.put_orderID(pair, orderId, side, market_price, qty, take_profit, orderIdTP, timeframe, balance)               
            db.put_homemsg(pair, timeframe, side, username)


        except BinanceAPIException as e:

            e1 = e.status_code
            e2 = e.message
            e3 = "Error: BinanceAPIException futures_order_main"
            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
            print(error_info)
            db.write_error(error_info)         

        except BinanceOrderException as e:

            e1 = e.status_code
            e2 = e.message
            e3 = "Error: BinanceOrderException futures_order_main"
            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
            print(error_info)
            db.write_error(error_info)     


    def futures_order(self, pair, qty, side, timeframe):
        
        try:
            order = client.futures_create_order(
                symbol=pair,
                side=side,
                type="MARKET",
                quantity=qty,
                recvWindow=15000)          

            time.sleep(5)
            orderId = order["orderId"]
            market_price = self.check_avgPrice(orderId, pair)
            market_price = float(market_price)

            username = db.get_user()["name"]
            balance = round(float(client.futures_account()['totalWalletBalance']), 3)

            print("\nOrderID: %(n)s \nMarket Price: %(c)s \nQuantity: %(f)s \nTime Frame: %(g)s \nBlance: %(h)s \nUsername: %(i)s" % 
                {'n': orderId, 'c': market_price, 'f': qty, 'g': timeframe, 'h': balance, 'i': username})

            db.put_orderID(pair, orderId, side, market_price, qty, timeframe, balance)            
            db.put_homemsg(pair, timeframe, side, username)

            return orderId

        except BinanceAPIException as e:
            e1 = e.status_code
            e2 = e.message
            e3 = "Error: BinanceAPIException futures_order"
            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
            print(error_info)
            db.write_error(error_info)     

        except BinanceOrderException as e:
            e1 = e.status_code
            e2 = e.message
            e3 = "Error: BinanceOrderException futures_order"
            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
            print(error_info)
            db.write_error(error_info)    

    def get_quantity_precision(self, pair):    

        try:

            info = client.futures_exchange_info() 
            info = info['symbols']
            for x in range(len(info)):
                if info[x]['symbol'] == pair:
                    return info[x]['pricePrecision']

        except BinanceAPIException as e:
            e1 = e.status_code
            e2 = e.message
            e3 = "Error: BinanceAPIException get_quantity_precision"
            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
            print(error_info)
            db.write_error(error_info)    
  
        except BinanceOrderException as e:
            e1 = e.status_code
            e2 = e.message
            e3 = "Error: BinanceOrderException get_quantity_precision"
            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
            print(error_info)
            db.write_error(error_info)   

    def check_order(self, orderIdTP, pair):

        try:
            result = client.futures_get_order(
                symbol=pair,
                orderId=orderIdTP)

            status = result['status']
            return status
            
        except BinanceAPIException as e:
            e1 = e.status_code
            e2 = e.message
            e3 = "Error: BinanceAPIException check_order"
            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
            print(error_info)
            db.write_error(error_info)  
  
        except BinanceOrderException as e:
            e1 = e.status_code
            e2 = e.message
            e3 = "Error: BinanceOrderException check_order"
            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
            print(error_info)
            db.write_error(error_info)  

        # ===========================================================================================

    def cancel_order(self, orderId, pair, qty, side):

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
            print("Binance Futures order cancelled. ", 'OrderId:', orderId)
            print('============================')	

        except BinanceAPIException as e:
            e1 = e.status_code
            e2 = e.message
            e3 = "Error: BinanceAPIException cancel_order"
            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
            print(error_info)
            db.write_error(error_info)  
  
        except BinanceOrderException as e:
            e1 = e.status_code
            e2 = e.message
            e3 = "Error: BinanceOrderException cancel_order"
            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
            print(error_info)
            db.write_error(error_info)  

        # ===========================================================================================
        
    def cancel_order2(self, orderIdTP, pair):

        try:			
            result = client.futures_cancel_order(
                symbol=pair,
                orderId=orderIdTP)
            print('============================')	
            print("Binance Futures order cancelled. ", 'OrderId:', orderIdTP)
            print('============================')	

        except BinanceAPIException as e:
            e1 = e.status_code
            e2 = e.message
            e3 = "Error: BinanceAPIException cancel_order2"
            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
            print(error_info)
            db.write_error(error_info)  
  
        except BinanceOrderException as e:
            e1 = e.status_code
            e2 = e.message
            e3 = "Error: BinanceOrderException cancel_order2"
            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
            print(error_info)
            db.write_error(error_info)  

    def check_avgPrice(self, orderIdTP, pair):

        try:
            result = client.futures_get_order(
                symbol=pair,
                orderId=orderIdTP)

            avgPrice = result['avgPrice']
            return avgPrice

        except BinanceAPIException as e:
            e1 = e.status_code
            e2 = e.message
            e3 = "Error: BinanceAPIException check_avgPrice"
            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
            print(error_info)
            db.write_error(error_info)  

        except BinanceOrderException as e:
            e1 = e.status_code
            e2 = e.message
            e3 = "Error: BinanceOrderException check_avgPrice"
            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_info = "\n" + datetime + "\n" + e1 + "\n" + e2 + "\n" + e3 + "\n"
            print(error_info)
            db.write_error(error_info)  


# [
#     {
#         "clientOrderId": "testOrder",
#         "cumQty": "0",
#         "cumQuote": "0",
#         "executedQty": "0",
#         "orderId": 22542179,
#         "avgPrice": "0.00000",
#         "origQty": "10",
#         "price": "0",
#         "reduceOnly": false,
#         "side": "BUY",
#         "positionSide": "SHORT",
#         "status": "NEW",
#         "stopPrice": "9300",        // please ignore when order type is TRAILING_STOP_MARKET
#         "symbol": "BTCUSDT",
#         "timeInForce": "GTC",
#         "type": "TRAILING_STOP_MARKET",
#         "origType": "TRAILING_STOP_MARKET",
#         "activatePrice": "9020",    // activation price, only return with TRAILING_STOP_MARKET order
#         "priceRate": "0.3",         // callback rate, only return with TRAILING_STOP_MARKET order
#         "updateTime": 1566818724722,
#         "workingType": "CONTRACT_PRICE",
#         "priceProtect": false            // if conditional order trigger is protected   
#     },
#     {
#         "code": -2022, 
#         "msg": "ReduceOnly Order is rejected."
#     }
# ]