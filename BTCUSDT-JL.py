from datetime import datetime, timedelta
from glob import glob

import talib
import asyncio
import pandas as pd
import numpy as np

from binance.client import AsyncClient

import config
import callDB
import CO

db = callDB.call()
CreateOrder = CO.call()

class PatternDetect:

#=====================================================================================================================

    async def main(self):
        global pair, timeframe, error_set, deltaSMA
        
        result = db.get_toggle()

        yy = 0
        for y in result:
            yy += 1

        xx = 0
        for x in result:
            xx += 1
            pair = x['pair']
            timeframe = x['timeframe']
            qty = x['qty']
            volume_set = x['vol']
            order_type = x['order_type']

            # BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT, SOLUSDT, LUNAUSDT, ADAUSDT, USTUSDT, BUSDUSDT, 
            # DOGEUSDT, AVAXUSDT, DOTUSDT, SHIBUSDT, WBTCUSDT, DAIUSDT, MATICUSDT

            if pair == "BTCUSDT":# and error_set2 == 0:
                try:                    
                    client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)

                    if timeframe == "1h":
                        deltaSMA = 40
                    if timeframe == "2h":
                        deltaSMA = 80
                    if timeframe == "4h":
                        deltaSMA = 140
                    if timeframe == "6h":
                        deltaSMA = 200
                    if timeframe == "8h":
                        deltaSMA = 300
                    if timeframe == "12h":
                        deltaSMA = 500
                    if timeframe == "1d":
                        deltaSMA = 1000

                    # last_hour_date_time = datetime.now() - timedelta(hours = 1000)
                    # get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    # msg = await client.futures_historical_klines(symbol=pair, interval="1d", start_str=get_startDate, end_str=None)
                    # data = self.get_data_frame(symbol=pair, msg=msg) 
                    # self.Pattern_Detect()                 
                    # print(f'\nRetrieving Historical data from Binance for: {pair, "1 Day"} \n')          
#======= JL ========
                    # last_hour_date_time = datetime.now() - timedelta(hours = 140)
                    # get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    # msg = await client.futures_historical_klines(symbol=pair, interval='4h', start_str=get_startDate, end_str=None)
                    # data = self.get_data_frame(symbol=pair, msg=msg) 
                    # self.Pattern_Detect()                 
                    # print(f'\nRetrieving Historical data from Binance for: {pair, "4 Hours"} \n')     

                    # last_hour_date_time = datetime.now() - timedelta(hours = 80)
                    # get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    # msg = await client.futures_historical_klines(symbol=pair, interval='2h', start_str=get_startDate, end_str=None)
                    # data = self.get_data_frame(symbol=pair, msg=msg) 
                    # self.Pattern_Detect()                 
                    # print(f'\nRetrieving Historical data from Binance for: {pair, "2 Hours"} \n')  
#======= JL ========
                    # last_hour_date_time = datetime.now() - timedelta(hours = 40)
                    # get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    # msg = await client.futures_historical_klines(symbol=pair, interval='1h', start_str=get_startDate, end_str=None)
                    # data = self.get_data_frame(symbol=pair, msg=msg) 
                    # self.Pattern_Detect()                 
                    # print(f'\nRetrieving Historical data from Binance for: {pair, "1 Hour"} \n')     

                    # last_hour_date_time = datetime.now() - timedelta(hours = 40)
                    # get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    # msg = await client.futures_historical_klines(symbol=pair, interval='30m', start_str=get_startDate, end_str=None)
                    # data = self.get_data_frame(symbol=pair, msg=msg) 
                    # self.Pattern_Detect()                 
                    # print(f'\nRetrieving Historical data from Binance for: {pair, "30 min"} \n')     

                    last_hour_date_time = datetime.now() - timedelta(hours = 200)
                    get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    msg = await client.futures_historical_klines(symbol=pair, interval='6h', start_str=get_startDate, end_str=None)
                    data = self.get_data_frame(symbol=pair, msg=msg) 
                    self.Pattern_Detect()                 
                    print(f'\nRetrieving Historical data from Binance for: {pair, timeframe} \n')   

                    # print("\nVolume: %(c)s \nHigh: %(a)s Close: %(b)s Current Price: %(d)s \nRSI: %(e)s SMA: %(f)s \nQTY: %(g)s \nSIDE: %(i)s \nEntry Price: %(k)s \nTake Profit: %(j)s \n" % 
                    #     {'a': close, 'b': high, 'c': volume, 'd': curPrice, 'e': rsi, 'f': sma, 'g': qty, 'i':side, 
                    #     'j':take_profit, 'k':entry_price})

                    # CreateOrder.futures_order(pair, qty, entry_price, side, order_type, take_profit, timeframe)
                    # print('------------futures_order------------')
                    
                    await client.close_connection()

                except: await client.close_connection()      
#=====================================================================================================================
                
    def get_data_frame(self, symbol, msg):
        global rows_count, df, volume, high, close

        df = pd.DataFrame(msg)
        df.columns = ['Time','Open', 'High', 'Low', 'Close', 'Volume','CloseTime', 'qav','num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
        df = df.loc[:, ['Time','Open', 'High', 'Low', 'Close', 'Volume']]
        df["Time"] = pd.to_datetime(df["Time"], unit='ms')
        df["Open"] = df["Open"].astype(float)
        df["High"] = df["High"].astype(float)
        df["Low"] = df["Low"].astype(float)
        df["Close"] = df["Close"].astype(float)
        df["Volume"] = df["Volume"].astype(float)

        return df

#=====================================================================================================================

    def Pattern_Detect(self):
        global side
    
        RSI = talib.RSI(df['Close'], timeperiod=14)
        BOP = talib.BOP(df['Open'], df['High'], df['Low'], df['Close'])
        macd, macdsignal, macdhist = talib.MACD(df['Close'], fastperiod=3, slowperiod=10, signalperiod=16) #HIGH TF
        fastk, fastd = talib.STOCHRSI(df['Close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

        df['BOP'] = round(BOP, 2)
        df['RSI'] = round(RSI)
        df['fastd'] = round(fastd)
        df['fastk'] = round(fastk)

        rr = len(df.index)

        pp = df.tail(3)

        dd = pd.DataFrame(pp)
        dd = dd.loc[:, ['Time', 'Open', 'High', 'Low', 'Close', 'BOP', 'RSI', 'fastd', 'fastk']]
        
        BOP2 = dd["BOP"][rr - 2]
        BOP3 = dd["BOP"][rr - 3]

        RSI2 = dd["RSI"][rr - 2]
        RSI3 = dd["RSI"][rr - 3]

        fastd2 = dd["fastd"][rr - 2]
        fastd3 = dd["fastd"][rr - 3]

        fastk2 = dd["fastk"][rr - 2]
        fastk3 = dd["fastk"][rr - 3]

        # print(dd)

        # 42 2022-05-16 04:00:00  30314.9  30436.9  30105.0  30313.9 -0.00  50.0    0.0    0.0
        # 43 2022-05-16 05:00:00  30313.4  30461.3  30233.0  30280.0 -0.15  49.0    0.0    0.0 

        # BOP3 = 0.40  
        # RSI3 = 59.0   
        # fastd3 = 67.0   
        # fastk3 = 100.0
        # BOP2 = 0.39
        # RSI2 = 60.0   
        # fastd2 = 67.0  
        # fastk2 = 100

                        #   Time     Open     High      Low    Close   BOP   RSI  fastd  fastk
        # 67 2022-05-17 05:00:00  30365.1  30519.3  30260.2  30445.6  0.31  58.0  100.0  100.0
        # 68 2022-05-17 06:00:00  30445.6  30539.0  30335.0  30514.5  0.34  59.0  100.0  100.0
        # 69 2022-05-17 07:00:00  30514.5  30576.4  30335.0  30394.3 -0.50  56.0   67.0    0.0 SHORT

        if BOP2 > BOP3 and RSI2 == RSI3 and RSI2 > 55 and fastd2 == fastd3 and fastd2 == 100 and fastk2 == fastk3 and fastk2 == 100:
            side = "SELL"
            print("1")
        elif BOP2 > BOP3 and RSI2 > RSI3 and RSI2 > 55 and fastd2 == fastd3 and fastd2 == 100 and fastk2 == fastk3 and fastk2 == 100:
            side = "SELL"   
            print("2")
                        #   Time     Open     High      Low    Close   BOP   RSI  fastd  fastk            
        # 70 2022-05-17 08:00:00  30394.2  30794.0  30375.0  30559.9  0.40  59.0   67.0  100.0
        # 71 2022-05-17 09:00:00  30560.0  30717.3  30550.0  30625.0  0.39  60.0   67.0  100.0
        # 72 2022-05-17 10:00:00  30625.0  30641.6  30429.7  30440.0 -0.87  56.0   67.0    0.0 SHORT
        #                  
        elif BOP2 < BOP3 and RSI2 == RSI3 and RSI2 > 55 and fastd2 == fastd3 and fastd2 > 60 and fastk2 == fastk3 and fastk2 == 100:
            side = "SELL"   
            print("3")     
        elif BOP2 < BOP3 and RSI2 > RSI3 and RSI2 > 55 and fastd2 == fastd3 and fastd2 > 60 and fastk2 == fastk3 and fastk2 == 100:
            side = "SELL"        
            print("4")
                        #   Time     Open     High      Low    Close   BOP   RSI  fastd  fastk            
        # 42 2022-05-16 04:00:00  30314.9  30436.9  30105.0  30313.9 -0.00  50.0    0.0    0.0
        # 43 2022-05-16 05:00:00  30313.4  30461.3  30233.0  30280.0 -0.15  49.0    0.0    0.0 
        # 44 2022-05-16 06:00:00  30279.9  30280.0  29361.1  29557.4 -0.79  38.0    0.0    0.0 SHORT

        elif BOP2 < BOP3 and RSI2 == RSI3 and RSI2 < 50 and fastd2 == fastd3 and fastd2 < 10 and fastk2 == fastk3 and fastk2 < 10:
            side = "SELL" 
            print("5")       
        elif BOP2 < BOP3 and RSI2 < RSI3 and RSI2 < 50 and fastd2 == fastd3 and fastd2 < 10 and fastk2 == fastk3 and fastk2 < 10:
            side = "SELL"   
            print("6")
                        #   Time     Open     High      Low    Close   BOP   RSI  fastd  fastk            
        # 38 2022-05-15 23:00:00  31087.7  31422.6  31035.9  31324.4  0.61  72.0  100.0  100.0
        # 39 2022-05-16 00:00:00  31324.3  31327.4  31040.0  31105.0 -0.76  66.0   67.0    0.0
        # 40 2022-05-16 01:00:00  31105.0  31152.0  30678.1  30768.6 -0.71  58.0   33.0    0.0 SHORT

        elif BOP2 < 0 and BOP2 < BOP3 and RSI2 < RSI3 and RSI2 < 70 and fastd2 < fastd3 and fastk2 < fastk3 and fastd3 == 100 and fastk2 == 100:
            side = "SELL"
            print("7-1")

                        #   Time     Open     High      Low    Close   BOP   RSI  fastd  fastk
        # 26  2022-05-11 10:00:00  31742.2  32197.6  31555.0  31835.0  0.14  55.0  100.0  100.0
        # 27  2022-05-11 11:00:00  31835.1  31895.8  31452.0  31517.1 -0.72  51.0   91.0   73.0
        # 28  2022-05-11 12:00:00  31517.1  31776.0  29000.0  29298.7 -0.80  34.0   58.0    0.0 SHORT =======
        elif BOP3 > 0 and BOP2 < 0 and BOP2 < BOP3 and RSI2 < RSI3 and RSI2 < 55 and fastd2 < fastd3 and fastk2 < fastk3 and fastd3 == 100 and fastk3 == 100:
            side = "SELL"
            print("7-2")        
                        #   Time     Open     High      Low    Close   BOP   RSI  fastd  fastk            
        # 89 2022-05-18 03:00:00  30204.8  30205.4  29700.0  29815.2 -0.77  42.0    8.0    0.0
        # 90 2022-05-18 04:00:00  29815.3  29913.0  29740.0  29809.5 -0.03  42.0    8.0    0.0
        # 91 2022-05-18 05:00:00  29809.5  30021.0  29779.7  30002.2  0.80  47.0   20.0   61.0 LONG  
 
        elif BOP2 > BOP3 and RSI2 == RSI3 and RSI2 < 50 and fastd2 == fastd3 and fastd2 < 10 and fastk2 == fastk3 and fastk2 < 10:
            side = "BUY"
            print("8")
                        #   Time     Open     High      Low    Close   BOP   RSI  fastd  fastk
        # 44 2022-05-16 08:00:00  29572.7  29900.0  29554.4  29782.0  0.61  43.0   14.0   38.0
        # 45 2022-05-16 09:00:00  29782.0  29782.1  29449.3  29595.7 -0.56  40.0   19.0   17.0

        # 46 2022-05-16 10:00:00  29595.7  30196.1  29417.3  30161.8  0.73  51.0   52.0  100.0 LONG
        elif BOP2 < BOP3 and RSI2 < RSI3 and RSI2 < 45 and fastd2 > fastd3 and fastk2 < fastk3 and fastd2 < 20 and fastk2 < 20:
            side = "BUY"
            print("9")
                        #   Time     Open     High      Low    Close   BOP   RSI  fastd  fastk
        # 27  2022-05-11 11:00:00  31835.1  31895.8  31452.0  31517.1 -0.72  51.0   91.0   73.0
        # 28  2022-05-11 12:00:00  31517.1  31776.0  29000.0  29298.7 -0.80  34.0   58.0    0.0 
        # 29  2022-05-11 13:00:00  29294.6  31889.6  29118.2  31223.0  0.70  50.0   50.0   76.0 LONG =======
        elif BOP3 < 0 and BOP2 < -0.7 and BOP3 < -0.7 and BOP2 < BOP3 and RSI2 < RSI3 and RSI2 < 35 and fastd2 < fastd3 and fastk2 < fastk3 and fastd3 <= 100 and fastk2 == 0:
            side = "BUY"
            print("10")

        else:
            side = "NONE"

        if side == "BUY" or side == "SELL":
            print(dd)
            print(side)
        else:
            print(dd) 
            print(side)

        # with open('output.txt', 'w') as f:
        #     f.write(
        #         dd.to_string()
        #     )
            
#=====================================================================================================================

if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    pattern_detect = PatternDetect()
    asyncio.get_event_loop().run_until_complete(pattern_detect.main())
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))