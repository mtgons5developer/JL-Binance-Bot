from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.client import Client
import config
import time

client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)

pair = 'BTCUSDT'
qty = 0.012 #QTY for Futures

# ===========================================SHORT==============================================================

async def futures_short(): #https://binance-docs.github.io/apidocs/futures/en/#new-order-trade
    global orderId
    try: #dmdm        
        order = client.futures_create_order(
            symbol=pair,
            side="SELL",
            type='MARKET',
            # timeInForce='GTC',
            quantity=qty)
            # price=entry_price)
    except BinanceAPIException as e:
        print(e)
        print("order1")
        quit()

    except BinanceOrderException as e:
        print(e)
        print("order2")
        quit()

    orderId = order['orderId']

    if order['status'] == "NEW":
        try:                
            result = client.futures_get_order(
                symbol=pair,
                orderId=orderId)

            print('===========================')
            print('Binance Futures order created SHORT! ', 
                # "Time: ", st_string, 
                "Price: ", current_price, 
                "Order: ", orderId,                 
                "Position: ", entry_pos)
            print('===========================')

        except BinanceAPIException as e:
            print(e)
            print("check order1")
            quit()
        except BinanceOrderException as e:
            print(e)
            print("check order2")
            quit()

    try:        
        order = client.futures_create_order(
            symbol=pair,
            side="BUY",
            type='MARKET',
            timeInForce='GTC',
            quantity=qty,
            price=entry_price)
    except BinanceAPIException as e:
        print(e)
        print("order1")
        quit()

    except BinanceOrderException as e:
        print(e)
        print("order2")
        quit()

# ===========================================LONG==============================================================

def futures_long():
    global orderId
    try: #dmdm        
        order = client.futures_create_order(
            symbol=pair,
            side="BUY",
            type='MARKET',
            # timeInForce='GTC',
            quantity=qty)
            # price=entry_price)
    except BinanceAPIException as e:
        print(e)
        print("order1")
        quit()

    except BinanceOrderException as e:
        print(e)
        print("order2")
        quit()

    orderId = order['orderId']

    if order['status'] == "NEW":
        try:                
            result = client.futures_get_order(
                symbol=pair,
                orderId=orderId)

            print('===========================')
            print('Binance Futures order created LONG! ', 
                # "Time: ", st_string, 
                "Price: ", current_price, 
                "Order: ", orderId,                 
                "Position: ", entry_pos)
            print('===========================')

        except BinanceAPIException as e:
            print(e)
            print("check order1")
            quit()
        except BinanceOrderException as e:
            print(e)
            print("check order2")
            quit()

    try:        
        order = client.futures_create_order(
            symbol=pair,
            side="SELL",
            type='MARKET',
            timeInForce='GTC',
            quantity=qty,
            price=entry_price)
    except BinanceAPIException as e:
        print(e)
        print("order1")
        quit()

    except BinanceOrderException as e:
        print(e)
        print("order2")
        quit()

# =========================================================================================================

async def order_history():

    file = open('Trade_History2.txt')  
    content = file.readlines()

    for i in range(3):
        try:            
            result = client.futures_get_order(
                symbol=pair,
                orderId=int(content[i]))
            print(result)
        except BinanceAPIException as e:
            print(e)
            print("check order1")
            quit()
        except BinanceOrderException as e:
            print(e)
            print("check order2")
            quit()

# =========================================================================================================

async def sync_time():

    gt = client.get_server_time()
    aa = str(gt)
    bb = aa.replace("{'serverTime': ","")
    aa = bb.replace("}","")
    gg=int(aa)
    ff=gg-10799260
    uu=ff/1000
    yy=int(uu)
    tt=time.localtime(yy)
    win32api.SetSystemTime(tt[0],tt[1],0,tt[2],tt[3],tt[4],tt[5],0)

async def futures_coin_ping(client):
    futures_coin_ping = await client.futures_coin_ping()
    print(futures_coin_ping)  

# ===========================================TEST ORDER==============================================================

async def test_order():    
    try:
        order = client.futures_create_order(
            symbol=pair,
            side="SELL",
            type='LIMIT',
            timeInForce='GTC',
            quantity=qty,
            price=41111) 
    except BinanceAPIException as e:
        print(e)
        print("order1")
        quit()

    except BinanceOrderException as e:
        print(e)
        print("order2")
        quit()

    orderId = order['orderId']

    if order['status'] == "NEW":
        time.sleep(1)
        try:            
            result = client.futures_cancel_order(
                symbol=pair,
                orderId=order['orderId'])   
            print('============================')   
            print("Binance Futures order cancelled. ", 'OrderId:', orderId)
            print('============================')   
            f = open("Trade_History2.txt", "a")            
            f.write(str(orderId) + "\n")
            f.close()            
        except BinanceAPIException as e:
            print(e)
            print("cancel1")
            quit()
        except BinanceOrderException as e:
            print(e)
            print("cancel2")
            quit()        