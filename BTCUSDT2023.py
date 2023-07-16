
# %matplotlib inline
import os
from datetime import datetime, timedelta
import talib
import time
import asyncio
import pandas as pd
import callDB
import CO
from binance.client import AsyncClient

# Define the Cloud SQL PostgreSQL connection details
from dotenv import load_dotenv
load_dotenv()

# import seaborn as sns
# import matplotlib.pyplot as plt

HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD')
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

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
            # Short        19    61240    <c>+123399   </c>-<c>   +14403% </c>
            # Short        7    3425    <c>+7399   </c>-<c>   +1403% </c>
            # Long        125    17650    <c>+58723   </c>-<c>   +4283% </c>
            if pair == "BTCUSDT":
                # pair = "MKRUSDT"
                # timeframe = "1d"
                try:                    
                    client = await AsyncClient.create(BINANCE_API_KEY,BINANCE_SECRET_KEY)

                    if timeframe == "1m": deltaSMA = 10
                    if timeframe == "3m": deltaSMA = 20
                    if timeframe == "5m": deltaSMA = 20
                    if timeframe == "15m": deltaSMA = 16
                    if timeframe == "30m": deltaSMA = 24
                    if timeframe == "1h": deltaSMA = 200
                    if timeframe == "2h": deltaSMA = 80
                    if timeframe == "4h": deltaSMA = 140
                    if timeframe == "6h": deltaSMA = 200                        
                    if timeframe == "8h": deltaSMA = 300                        
                    if timeframe == "12h": deltaSMA = 500
                    if timeframe == "1d": deltaSMA = 2000
                        
                    last_hour_date_time = datetime.now() - timedelta(hours = deltaSMA)
                    get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    print(f'\nRetrieving Historical data from Binance for: {pair, timeframe} \n')                       

                    msg = await client.futures_historical_klines(symbol=pair, interval=timeframe, start_str=get_startDate, end_str=None)
                    data = self.get_data_frame(symbol=pair, msg=msg) 
                    self.Pattern_Detect()              
                    print(f'\nRetrieving Historical data from Binance for: {pair, timeframe} \n') 
                             
                    print(deltaSMA)

                    await client.close_connection()
                    while 1 == 1:
                        try:
                            last_hour_date_time = datetime.now() - timedelta(hours = deltaSMA)
                            get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')

                            msg = await client.futures_historical_klines(symbol=pair, interval=timeframe, start_str=get_startDate, end_str=None)
                            data = self.get_data_frame(symbol=pair, msg=msg) 
                            print(data)

                            rr = len(dd.index)
                            RSI = dd['RSI'][rr - 1]
                            STOCHRSI_1 = dd['fastd'][rr - 1]
                            STOCHRSI_2 = dd['fastk'][rr - 1]
                            print(RSI, STOCHRSI_1, STOCHRSI_2)

                            time.sleep(1)
                        except:
                            print("Error:")
                            break

                    await client.close_connection()
                    quit()

                    # CreateOrder.futures_order(pair, qty, side, order_type, take_profit, timeframe)
                    # print('------------futures_order------------')
                    
                    # await client.close_connection()

                except: await client.close_connection()     

#=====================================================================================================================

    def get_data_frame_1m(self, symbol, msg):
        global dd

        dd = pd.DataFrame(msg)
        dd.columns = ['Time','Open', 'High', 'Low', 'Close', 'Volume','CloseTime', 'qav','num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
        dd = dd.loc[:, ['Close', "Time"]]
        dd["Time"] = pd.to_datetime(dd["Time"], unit='ms')

        RSI = talib.RSI(dd['Close'], timeperiod=14)
        fastk, fastd = talib.STOCHRSI(dd['Close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

        dd['RSI'] = round(RSI)
        dd['fastd'] = round(fastd) # red
        dd['fastk'] = round(fastk) # white

#=====================================================================================================================

    def get_data_frame(self, symbol, msg):
        global rows_count, df, volume, high, close

        df = pd.DataFrame(msg)
        df.columns = ['Time','Open', 'High', 'Low', 'Close', 'Volume','CloseTime', 'qav','num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
        df = df.loc[:, ['Time','Open', 'High', 'Low', 'Close', 'Volume']]
        times = pd.to_datetime(df["Time"], unit='ms')
        times_index = pd.Index(times)
        times_index_Singapore = times_index.tz_localize('GMT').tz_convert('Singapore')


        df["Date"] = times_index_Singapore
        df["Open"] = df["Open"].astype(float)
        df["High"] = df["High"].astype(float)
        df["Low"] = df["Low"].astype(float)
        df["Close"] = df["Close"].astype(float)
        df["Volume"] = df["Volume"].astype(float)

        df = df.set_index('Date',drop = False)
        date1 = "2022-06-25 04:00:00"
        date2 = "2022-06-26 20:00:00"

        max = df['Close'][date1:date2].max()
        min = df['Close'][date1:date2].min()
        df1 = df[date1:date2]
        diff1 = round(max - min)
        print("\n", max, min, diff1)
        d = diff1 / 2

        with open('output.txt', 'w') as f:
            f.write(
                df1.to_string()
            )

        low = df1['Low'][date1:date2].min()
        high = df1['High'][date1:date2].min()
        diff = round(float(high - low))
        print(high, low, diff)

        level1 = round(float(high - 0.236 * diff))
        level2 = round(float(high - 0.382 * diff))
        level3 = round(float(high - 0.618 * diff))

        print ("Level", " ", "PRICE")
        print ("0 ", "      " , high)
        print ("0.236", "   " ,level1)
        print ("0.382",  "   ",level2)
        print ("0.618","   ",  level3)
        print ("1 ",   "      ", low)

        # fig, ax = plt.subplots(figsize=(15,5))

        # ax.plot(df1.Date, df1.Close)

        # ax.axhspan(level1, min + d, alpha=0.4, facecolor='lightsalmon')
        # ax.axhspan(level2, level1, alpha=0.5, color='palegoldenrod')
        # ax.axhspan(level3, level2, alpha=0.5, color='palegreen')
        # ax.axhspan(max, max - d, alpha=0.5, color='powderblue')

        # plt.ylabel("Closing Price per 1 Hour")
        # plt.xlabel("2022 June")

        # plt.title('Fibonacci')
        # ax.grid()
        # plt.show()
        
        # quit()

        return df

#=====================================================================================================================

    def Pattern_Detect(self):
        global side, take_profit

        RSI = talib.RSI(df['Close'], timeperiod=14)
        BOP = talib.BOP(df['Open'], df['High'], df['Low'], df['Close'])
        # OBV = talib.OBV(df['Close'], df['Volume'])
        ADOSC = talib.ADOSC(df['High'], df['Low'], df['Close'], df['Volume'], fastperiod=3, slowperiod=10)
        CDLHAM = talib.CDLHAMMER(df['Open'], df['High'], df['Low'], df['Close'])
        CDLSS = talib.CDLSHOOTINGSTAR(df['Open'], df['High'], df['Low'], df['Close']) ####
        CDLHANGINGMAN = talib.CDLHANGINGMAN(df['Open'], df['High'], df['Low'], df['Close'])
        WMA = talib.WMA(df['Close'], timeperiod=30)
        EMA = talib.EMA(df['Close'], timeperiod=10)
        #EMA changes from previous time frame
        CDLBREAKAWAY = talib.CDLBREAKAWAY(df['Open'], df['High'], df['Low'], df['Close'])
        CDLHARAMI = talib.CDLHARAMI(df['Open'], df['High'], df['Low'], df['Close'])
        ATR = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
        CMO = talib.CMO(df['Close'], timeperiod=14)
        MFI = talib.MFI(df['High'], df['Low'], df['Close'], df['Volume'], timeperiod=14)


        CDLENGULFING = talib.CDLENGULFING(df['Open'], df['High'], df['Low'], df['Close'])
        CDLGRAVESTONEDOJI = talib.CDLGRAVESTONEDOJI(df['Open'], df['High'], df['Low'], df['Close']) #Bearish
        CDLDRAGONFLYDOJI = talib.CDLDRAGONFLYDOJI(df['Open'], df['High'], df['Low'], df['Close']) #Bullish

        # macd, macdsignal, macdhist = talib.MACD(df['Close'], fastperiod=3, slowperiod=10, signalperiod=16) #HIGH TF
        fastk, fastd = talib.STOCHRSI(df['Close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

        # df['MFI'] = round(MFI, 2)
        # df['CMO'] = round(CMO, 2) # https://www.investopedia.com/terms/c/chandemomentumoscillator.asp
        # df['ATR'] = round(ATR, 2) # https://www.investopedia.com/terms/a/atr.asp

        df['ENGULF'] = round(CDLENGULFING)
        df['STONED'] = round(CDLGRAVESTONEDOJI)
        df['DRAGON'] = round(CDLDRAGONFLYDOJI)
        # df['EMA'] = round(EMA, 2)
        # df['WMA'] = round(WMA, 2)
        df['RSI'] = round(RSI)
        df['fastd'] = round(fastd)
        df['fastk'] = round(fastk)

        # df['BOP'] = round(BOP, 2)
        # df['CDLHARAMI'] = round(CDLHARAMI) #https://www.investopedia.com/terms/h/haramicross.asp
        # df['CDLHM'] = round(CDLHANGINGMAN)
        # df['CDLSS'] = round(CDLSS)

        # df['MACD'] = round(macd)
        # df['Signal'] = round(macdsignal)
        # df['History'] = round(macdhist)

        for i in range(2,df.shape[0]):
            
            current = df.iloc[i,:]
            prev = df.iloc[i-1,:]
            prev_2 = df.iloc[i-2,:]
            realbody = abs(current['Open'] - current['Close'])
            candle_range = current['High'] - current['Low']
            idx = df.index[i]

            # df.loc[idx,'EMA--'] = current["EMA"] >= prev["EMA"]
            # df.loc[idx,'WMA--'] = current["WMA"] >= prev["WMA"]
            # df.loc[idx,'BOP--'] = current["BOP"] >= prev["BOP"]

            # df.loc[idx,'BullS'] = current['Low'] > prev['Low'] and prev['Low'] < prev_2['Low'] #Bullish Swing
            # df.loc[idx,'BullPB'] = realbody <= candle_range/3 and  min(current['Open'], current['Close']) > (current['High'] + current['Low'])/2 and current['Low'] < prev['Low'] # Bullish pin bar

            df.loc[idx,'BullE'] = current['High'] > prev['High'] and current['Low'] < prev['Low'] and realbody >= 0.8 * candle_range and current['Close'] > current['Open'] #Bullish engulfing
            
            # df.loc[idx,'BearS'] = current['High'] < prev['High'] and prev['High'] > prev_2['High'] #Bearish Swing
            # df.loc[idx,'BearPB'] = realbody <= candle_range/3 and max(current['Open'] , current['Close']) < (current['High'] + current['Low'])/2 and current['High'] > prev['High'] # Bearish pin bar
            
            df.loc[idx,'BearE'] = current['High'] > prev['High'] and current['Low'] < prev['Low'] and realbody >= 0.8 * candle_range and current['Close'] < current['Open'] # Bearish engulfing
            # If current candle shows position exit or stay next position.

            # Still needs historical data
            # df.loc[idx,'IB'] = current['High'] < prev['High'] and current['Low'] > prev['Low'] # Inside bar
            # df.loc[idx,'OB'] = current['High'] > prev['High'] and current['Low'] < prev['Low'] # Outside bar

            # df.loc[idx,'SUM'] = abs(prev["Close"] - current["Close"])

            # v1 = current['Open']
            # v2 = current['Close']
            # df.loc[idx,'SIDE'] = np.where(v1 < v2, 1, -1)

        rr = len(df.index)
        # FIX EACH CURRENT LINE ==========
        # pp = df.tail(4)

        # dd = pd.DataFrame(pp)
        # dd = dd.loc[:, ['Time', 'Open', 'High', 'Low', 'Close', 'BOP', 'RSI', 'fastd', 'fastk']]

        # 0.63  51.0   35.0   75.0 -261.0   -79.0   -182.0
        # 0.58  57.0   68.0  100.0   73.0   -61.0    135.0
        # 0.25  58.0   92.0  100.0  248.0   -25.0    273.0
        # -0.19  56.0   96.0   88.0  258.0     8.0    250.0
        
        # df['BOPT'] = np.where(df["BOP"][rr - 5] < df['BOP'][rr - 4], 1, -1)
        # df['BOPT'] = np.where(df["BOP"][rr - 4] < df['BOP'][rr - 3], 1, -1)
        # df['BOPT'] = np.where(df["BOP"][rr - 3] < df['BOP'][rr - 2], 1, -1)
        # df['BOPT'] = np.where(df["BOP"][rr - 2] < df['BOP'][rr - 1], 1, -1)

        # df['BOPT'] = np.where(df["BOP"][rr - 4] < df['BOP'], 1, -1)
        # df['RSIT'] = np.where(df["RSI"][rr - 4] < df['RSI'], 1, -1)
        # df['fastdT'] = np.where(df["fastd"][rr - 4] < df['fastd'], 1, -1)
        # df['fastkT'] = np.where(df["fastk"][rr - 4] < df['fastk'], 1, -1)
        # df['MACDT'] = np.where(df["MACD"][rr - 4] < df['MACD'], 1, -1)
        # df['SignalT'] = np.where(df["Signal"][rr - 4] < df['Signal'], 1, -1)
        # df['HistoryT'] = np.where(df["History"][rr - 4] < df['History'], 1, -1)
        # print(df.tail(4))
        # quit()

        #==================

        # yy = 5
        # BOPT1 = 0
        # BOPT2 = 0
        # for y in df:
        #     yy -= 1
        #     n = df['BOPT'][rr - yy]
                
        #     if n < 0:
        #         BOPT1 += 1
        #     else:
        #         BOPT2 += 1

        #     if yy == 1: break
        # BOPTOTAL = (BOPT1 * -1) + BOPT2
        # print("BOPTOTAL", BOPTOTAL)

        # yy = 5
        # RSIT1 = 0
        # RSIT2 = 0
        # for y in df:
        #     yy -= 1
        #     n = df['RSIT'][rr - yy]
                
        #     if n < 0:
        #         RSIT1 += 1
        #     else:
        #         RSIT2 += 1

        #     if yy == 1: break
        # RSITOTAL = (RSIT1 * -1) + RSIT2
        # print("RSITOTAL", RSITOTAL)

        # yy = 5
        # fastdT1 = 0
        # fastdT2 = 0
        # for y in df:
        #     yy -= 1
        #     n = df['fastdT'][rr - yy]
                
        #     if n < 0:
        #         fastdT1 += 1
        #     else:
        #         fastdT2 += 1

        #     if yy == 1: break
        # fastdTOTAL = (fastdT1 * -1) + fastdT2
        # print("fastdTOTAL", fastdTOTAL)

        # yy = 5
        # fastkT1 = 0
        # fastkT2 = 0
        # for y in df:
        #     yy -= 1
        #     n = df['fastkT'][rr - yy]
                
        #     if n < 0:
        #         fastkT1 += 1
        #     else:
        #         fastkT2 += 1

        #     if yy == 1: break
        # fastkTOTAL = (fastkT1 * -1) + fastkT2
        # print("fastkTOTAL", fastkTOTAL)

        # yy = 5
        # MACDT1 = 0
        # MACDT2 = 0
        # for y in df:
        #     yy -= 1
        #     n = df['MACDT'][rr - yy]
                
        #     if n < 0:
        #         MACDT1 += 1
        #     else:
        #         MACDT2 += 1

        #     if yy == 1: break
        # MACDTOTAL = (MACDT1 * -1) + MACDT2
        # print("MACDTOTAL", MACDTOTAL)

        # yy = 5
        # SignalT1 = 0
        # SignalT2 = 0
        # for y in df:
        #     yy -= 1
        #     n = df['SignalT'][rr - yy]
                
        #     if n < 0:
        #         SignalT1 += 1
        #     else:
        #         SignalT2 += 1

        #     if yy == 1: break
        # SignalTOTAL = (SignalT1 * -1) + SignalT2
        # print("SignalTOTAL", SignalTOTAL)

        # yy = 5
        # HistoryT1 = 0
        # HistoryT2 = 0
        # for y in df:
        #     yy -= 1
        #     n = df['HistoryT'][rr - yy]
                
        #     if n < 0:
        #         HistoryT1 += 1
        #     else:
        #         HistoryT2 += 1

        #     if yy == 1: break
        # HistoryTOTAL = (HistoryT1 * -1) + HistoryT2
        # print("HistoryTOTAL", HistoryTOTAL)
        
        # if BOPTOTAL <= -3 and RSITOTAL <= -3 and fastdTOTAL <= -3 and fastkTOTAL <= -3 and MACDTOTAL <= -3 and HistoryTOTAL <= -3:
        #     side = "SELL"
        # elif BOPTOTAL >= 3 and RSITOTAL >= 3 and fastdTOTAL >= 3 and fastkTOTAL >= 3 and MACDTOTAL >= 3 and HistoryTOTAL >= 3:        
        #     side = "BUY"
        # else:
        #     side = "NONE"

        #==================

        # if side == "NONE":
            
        #     BOP2 = dd["BOP"][rr - 2]
        #     BOP3 = dd["BOP"][rr - 3]

        #     RSI2 = dd["RSI"][rr - 2]
        #     RSI3 = dd["RSI"][rr - 3]

        #     fastd2 = dd["fastd"][rr - 2]
        #     fastd3 = dd["fastd"][rr - 3]

        #     fastk2 = dd["fastk"][rr - 2]
        #     fastk3 = dd["fastk"][rr - 3]

        #     # 42 2022-05-16 04:00:00  30314.9  30436.9  30105.0  30313.9 -0.00  50.0    0.0    0.0
        #     # 43 2022-05-16 05:00:00  30313.4  30461.3  30233.0  30280.0 -0.15  49.0    0.0    0.0 

        #     # BOP3 = 0.40  
        #     # RSI3 = 59.0   
        #     # fastd3 = 67.0   
        #     # fastk3 = 100.0
        #     # BOP2 = 0.39
        #     # RSI2 = 60.0   
        #     # fastd2 = 67.0  
        #     # fastk2 = 100

        #                     #   Time     Open     High      Low    Close   BOP   RSI  fastd  fastk
        #     # 67 2022-05-17 05:00:00  30365.1  30519.3  30260.2  30445.6  0.31  58.0  100.0  100.0
        #     # 68 2022-05-17 06:00:00  30445.6  30539.0  30335.0  30514.5  0.34  59.0  100.0  100.0
        #     # 69 2022-05-17 07:00:00  30514.5  30576.4  30335.0  30394.3 -0.50  56.0   67.0    0.0 SHORT

        #     if BOP2 > BOP3 and RSI2 == RSI3 and RSI2 > 55 and fastd2 == fastd3 and fastd2 == 100 and fastk2 == fastk3 and fastk2 > 90:
        #         side = "SELL"
        #         print("1")
        #     elif BOP2 > BOP3 and RSI2 > RSI3 and RSI2 > 55 and fastd2 == fastd3 and fastd2 == 100 and fastk2 == fastk3 and fastk2 > 90:
        #         side = "SELL"   
        #         print("2")
        #                     #   Time     Open     High      Low    Close   BOP   RSI  fastd  fastk            
        #     # 70 2022-05-17 08:00:00  30394.2  30794.0  30375.0  30559.9  0.40  59.0   67.0  100.0
        #     # 71 2022-05-17 09:00:00  30560.0  30717.3  30550.0  30625.0  0.39  60.0   67.0  100.0
        #     # 72 2022-05-17 10:00:00  30625.0  30641.6  30429.7  30440.0 -0.87  56.0   67.0    0.0 SHORT
        #     #                  
        #     elif BOP2 < BOP3 and RSI2 == RSI3 and RSI2 > 55 and fastd2 == fastd3 and fastd2 > 60 and fastk2 == fastk3 and fastk2 > 90:
        #         side = "SELL"   
        #         print("3")     
        #     elif BOP2 < BOP3 and RSI2 > RSI3 and RSI2 > 55 and fastd2 == fastd3 and fastd2 > 60 and fastk2 == fastk3 and fastk2 > 90:
        #         side = "SELL"        
        #         print("4")
        #                     #   Time     Open     High      Low    Close   BOP   RSI  fastd  fastk            
        #     # 42 2022-05-16 04:00:00  30314.9  30436.9  30105.0  30313.9 -0.00  50.0    0.0    0.0
        #     # 43 2022-05-16 05:00:00  30313.4  30461.3  30233.0  30280.0 -0.15  49.0    0.0    0.0 
        #     # 44 2022-05-16 06:00:00  30279.9  30280.0  29361.1  29557.4 -0.79  38.0    0.0    0.0 SHORT

        #     elif BOP2 < BOP3 and RSI2 == RSI3 and RSI2 < 50 and fastd2 == fastd3 and fastd2 < 10 and fastk2 == fastk3 and fastk2 < 10:
        #         side = "SELL" 
        #         print("5")       
        #     elif BOP2 < BOP3 and RSI2 < RSI3 and RSI2 < 50 and fastd2 == fastd3 and fastd2 < 10 and fastk2 == fastk3 and fastk2 < 10:
        #         side = "SELL"   
        #         print("6")
        #                     #   Time     Open     High      Low    Close   BOP   RSI  fastd  fastk            
        #     # 38 2022-05-15 23:00:00  31087.7  31422.6  31035.9  31324.4  0.61  72.0  100.0  100.0
        #     # 39 2022-05-16 00:00:00  31324.3  31327.4  31040.0  31105.0 -0.76  66.0   67.0    0.0
        #     # 40 2022-05-16 01:00:00  31105.0  31152.0  30678.1  30768.6 -0.71  58.0   33.0    0.0 SHORT

        #     elif BOP2 < 0 and BOP2 < BOP3 and RSI2 < RSI3 and RSI2 < 70 and fastd2 < fastd3 and fastk2 < fastk3 and fastd3 > 90 and fastk2 > 90:
        #         side = "SELL"
        #         print("7-1")

        #                     #   Time     Open     High      Low    Close   BOP   RSI  fastd  fastk
        #     # 26  2022-05-11 10:00:00  31742.2  32197.6  31555.0  31835.0  0.14  55.0  100.0  100.0
        #     # 27  2022-05-11 11:00:00  31835.1  31895.8  31452.0  31517.1 -0.72  51.0   91.0   73.0
        #     # 28  2022-05-11 12:00:00  31517.1  31776.0  29000.0  29298.7 -0.80  34.0   58.0    0.0 SHORT =======
        #     elif BOP3 > 0 and BOP2 < 0 and BOP2 < BOP3 and RSI2 < RSI3 and RSI2 < 55 and fastd2 < fastd3 and fastk2 < fastk3 and fastd3 > 90 and fastk3 == 100:
        #         side = "SELL"
        #         print("7-2")        
        #                     #   Time     Open     High      Low    Close   BOP   RSI  fastd  fastk            
        #     # 89 2022-05-18 03:00:00  30204.8  30205.4  29700.0  29815.2 -0.77  42.0    8.0    0.0
        #     # 90 2022-05-18 04:00:00  29815.3  29913.0  29740.0  29809.5 -0.03  42.0    8.0    0.0
        #     # 91 2022-05-18 05:00:00  29809.5  30021.0  29779.7  30002.2  0.80  47.0   20.0   61.0 LONG  
    
        #     elif BOP2 > BOP3 and RSI2 == RSI3 and RSI2 < 50 and fastd2 == fastd3 and fastd2 < 10 and fastk2 == fastk3 and fastk2 < 10:
        #         side = "BUY"
        #         print("8")
        #                     #   Time     Open     High      Low    Close   BOP   RSI  fastd  fastk
        #     # 44 2022-05-16 08:00:00  29572.7  29900.0  29554.4  29782.0  0.61  43.0   14.0   38.0
        #     # 45 2022-05-16 09:00:00  29782.0  29782.1  29449.3  29595.7 -0.56  40.0   19.0   17.0

        #     # 46 2022-05-16 10:00:00  29595.7  30196.1  29417.3  30161.8  0.73  51.0   52.0  100.0 LONG
        #     elif BOP2 < BOP3 and RSI2 < RSI3 and RSI2 < 45 and fastd2 > fastd3 and fastk2 < fastk3 and fastd2 < 20 and fastk2 < 20:
        #         side = "BUY"
        #         print("9")
        #                     #   Time     Open     High      Low    Close   BOP   RSI  fastd  fastk
        #     # 27  2022-05-11 11:00:00  31835.1  31895.8  31452.0  31517.1 -0.72  51.0   91.0   73.0
        #     # 28  2022-05-11 12:00:00  31517.1  31776.0  29000.0  29298.7 -0.80  34.0   58.0    0.0 
        #     # 29  2022-05-11 13:00:00  29294.6  31889.6  29118.2  31223.0  0.70  50.0   50.0   76.0 LONG =======
        #     elif BOP3 < 0 and BOP2 < -0.7 and BOP3 < -0.7 and BOP2 < BOP3 and RSI2 < RSI3 and RSI2 < 35 and fastd2 < fastd3 and fastk2 < fastk3 and fastd3 > 90 and fastk2 == 0:
        #         side = "BUY"
        #         print("10")

        high = df["High"][rr - 2] 
        low = df["Low"][rr - 2] 
        close = df['Close'][rr - 2] 
        oopen = df['Open'][rr - 2] 
        volume = df['Volume'][rr - 2] 
        obv = df['Volume'][rr - 2] 

        high1 = df["High"][rr - 1] 
        low1 = df["Low"][rr - 1] 
        close1 = df['Close'][rr - 1] 
        open1 = df['Open'][rr - 1] 
        volume1 = df['Volume'][rr - 1] 

        dd = df.tail(4)
        print(dd)
        # print(side)
        # quit()

        # (high-low) / open * 100%
        # if 3rd gets rejected and 2nd was the confirmed it.
        # 32045.90, 32148.40, 99.7
        # 32148.50, 32106.50, 99.9
        # (New Price - Old Price) / Old Price x 100
        # -42, 32148.50, 0.13%

        # change1  = close1 - open1
        # change2 = change1 / open1
        # change = change2 * 100
        # print(close1)
        # print(open1)
        # print(round(change, 3), "%")

        # 1. If today's closing price is higher than yesterday's closing price, then: Current OBV = Previous OBV + today's volume
        # if close1 > close:
        #     Current_OBV = round(obv + volume1)
        #     print("OBV:", Current_OBV)
        # else:
        #     Current_OBV = round(obv - volume1)
        #     print("OBV:", Current_OBV)          

        # 2. If today's closing price is lower than yesterday's closing price, then: Current OBV = Previous OBV - today's volume
        # 31570.5  31720.0  31562.7  31616.6
        amp1 = high - low
        amp2 = amp1 / oopen 
        amp = round(float(amp2 * 100), 2)
        print(amp)

        amp1 = high1 - low1
        amp2 = amp1 / open1 
        amp = round(float(amp2 * 100), 2)
        print(amp)

        with open('output.txt', 'w') as f:
            f.write(
                df.to_string()
            )
            
#=====================================================================================================================

if __name__ == '__main__':
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    pattern_detect = PatternDetect()
    asyncio.get_event_loop().run_until_complete(pattern_detect.main())
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))