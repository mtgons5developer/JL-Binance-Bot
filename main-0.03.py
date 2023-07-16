
# %matplotlib inline
import os
import psycopg2
from datetime import datetime, timedelta
import talib
import time
import schedule
import asyncio
import pandas as pd
import numpy as np
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
    
    def __init__(self):
        self.pp = None  # Initialize pp as an instance variable

    async def main(self):
        global pair, timeframe, error_set, deltaSMA
        
        timeframe = "15m"
        pair = "BTCUSDT"
            
        try:                  
            client = await AsyncClient.create(BINANCE_API_KEY, BINANCE_SECRET_KEY)

            if timeframe == "1m": deltaSMA = 10
            if timeframe == "3m": deltaSMA = 20
            if timeframe == "5m": deltaSMA = 20
            if timeframe == "15m": deltaSMA = 16
            if timeframe == "30m": deltaSMA = 24
            if timeframe == "1h": deltaSMA = 60
            if timeframe == "2h": deltaSMA = 80
            if timeframe == "4h": deltaSMA = 140
            if timeframe == "6h": deltaSMA = 200                        
            if timeframe == "8h": deltaSMA = 300                        
            if timeframe == "12h": deltaSMA = 500
            if timeframe == "1d": deltaSMA = 2000
                
            last_hour_date_time = datetime.now() - timedelta(hours = deltaSMA)
            get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')

            msg = await client.futures_historical_klines(symbol=pair, interval=timeframe, start_str=get_startDate, end_str=None)
            data = self.get_data_frame(symbol=pair, msg=msg) 
            self.Pattern_Detect()
            print(f'\nRetrieving Historical data from Binance for: {pair, timeframe} \n')

            # await client.close_connection()
            # while 1 == 1:
            #     try:
            #         last_hour_date_time = datetime.now() - timedelta(hours = deltaSMA)
            #         get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')

            #         msg = await client.futures_historical_klines(symbol=pair, interval=timeframe, start_str=get_startDate, end_str=None)
            #         dd = self.get_data_frame(symbol=pair, msg=msg) 

            #         rr = len(dd.index)
            #         RSI = dd['RSI'][rr - 1]
            #         STOCHRSI_1 = dd['fastd'][rr - 1]
            #         STOCHRSI_2 = dd['fastk'][rr - 1]
            #         print(RSI, STOCHRSI_1, STOCHRSI_2)

            #         time.sleep(1)
            #     except Exception as e:
            #         print(f"Error: {e}")
            #         time.sleep(5)  # Add a delay before retrying

            await client.close_connection()
            # quit()

            # CreateOrder.futures_order(pair, qty, side, order_type, take_profit, timeframe)
            # print('------------futures_order------------')
            
            # await client.close_connection()

        except Exception as e:
            print(f"Error2: {e}")
        finally:
            print('finally')
            await client.close_connection()  

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

        # df = df.tail(4)
        # print(df)
        df['BOP'] = round(BOP, 1)
        df['RSI'] = round(RSI)
        df['fastd'] = round(fastd)
        df['fastk'] = round(fastk)
        df['MACD'] = round(macd )
        df['Signal'] = round(macdsignal)
        df['History'] = round(macdhist)                 
        rr = len(df.index)
        # df['OpenT'] = np.where(df["Open"][rr - 4] < df['Close'], -1, 1)
        df['BOPT'] = np.where(df["BOP"][rr - 4] < df['BOP'], -1, 1)
        df['RSIT'] = np.where(df["RSI"][rr - 4] < df['RSI'], -1, 1)
        df['fastdT'] = np.where(df["fastd"][rr - 4] < df['fastd'], -1, 1)
        df['fastkT'] = np.where(df["fastk"][rr - 4] < df['fastk'], -1, 1)
        df['MACDT'] = np.where(df["MACD"][rr - 4] < df['MACD'], -1, 1)
        df['SignalT'] = np.where(df["Signal"][rr - 4] < df['Signal'], -1, 1)
        df['HistoryT'] = np.where(df["History"][rr - 4] < df['History'], -1, 1)
        # print(df)
        # quit()

        # Find fastd+fastk on all TF= 0 / Create per second TF for fastd+fastk
        # X Pump/Support
        # Detect a battle and BOP has higher signal from all.
        # Separate code for signals
        # Cross Entry test
        # Show Win rate in %, select win rate entry.
        # Not enough balance.
        # Insuffient Margin balance.
        # Support current TF by Higher TF
        # Cancel all existing trades.
        # Multiple API Code
        # Quantity Test orders
        # Leverage Changer
        # Check orders and monitor
        # Signals must read 4 3 2 1
        # PNL Calculation
        # https://stackoverflow.com/questions/67643077/how-can-i-adjust-the-leverage-with-bianance-api
        # https://dev.binance.vision/t/how-to-calculate-cumb-while-calculating-liquidation-price/883
        # https://www.binance.com/en/support/faq/b3c689c1f50a44cabb3a84e663b81d93
        # https://gist.github.com/highfestiva/b71e76f51eed84d56c1be8ebbcc286b5?permalink_comment_id=3617078
        # https://binance-docs.github.io/apidocs/futures/en/#change-log

        yy = 5
        RSIT = "NONE"
        for y in df:
            yy -= 1
            n = df['RSIT'][rr - yy]
            if n < 0:
                RSIT = "SHORT"
            else:
                RSIT = "LONG"

            if yy == 1: break

        yy = 5
        fastdT = "NONE"
        for y in df:
            yy -= 1
            n = df['fastdT'][rr - yy]
            if n < 0:
                fastdT = "SHORT"
            else:
                fastdT = "LONG"

            if yy == 1: break

        yy = 5
        MACDT = "NONE"
        for y in df:
            yy -= 1
            n = df['MACDT'][rr - yy]
            if n < 0:
                MACDT = "SHORT"
            else:
                MACDT = "LONG"

            if yy == 1: break

        yy = 5
        SignalT = "NONE"
        for y in df:
            yy -= 1
            n = df['SignalT'][rr - yy]
            if n < 0:
                SignalT = "LONG"
            else:
                SignalT = "SHORT"

            if yy == 1: break

        yy = 5
        HistoryT = "NONE"
        for y in df:
            yy -= 1
            n = df['HistoryT'][rr - yy]
            if n < 0:
                HistoryT = "SHORT"
            else:
                HistoryT = "LONG"

            if yy == 1: break

        print(RSIT)
        print(fastdT)
        print(MACDT)
        print(SignalT)
        print(HistoryT)
        side = "NONE"

        if RSIT == "LONG" and fastdT == "LONG" and MACDT == "LONG" and SignalT == "LONG" and HistoryT == "LONG":
            print("======== B U Y =======")
            side = "BUY"
        elif RSIT == "SHORT" and fastdT == "SHORT" and MACDT == "SHORT" and SignalT == "SHORT" and HistoryT == "SHORT":
            print("======= S E L L =======")
            side = "SELL"
        #dldl

        # pp = df.tail(4)
        self.pp = df.tail(4)
        print(self.pp)
        print("\n" + side)
        # val = pp['OpenT'].value_counts()
        # print(val[0:1]) #- Column
        # print(val[0:2]) #+ Column

        with open('output.txt', 'w') as f:
            f.write(
                self.pp.to_string()
            )  

    # Function to insert the "pp" data into the "bnb" table
    def insert_pp_to_database(self):
        try:
            # Open a connection to the PostgreSQL database
            connection = psycopg2.connect(
                host=HOST,
                database=DATABASE,
                user=USER,
                password=PASSWORD
            )
            cursor = connection.cursor()

            # Iterate through each row of the "pp" dataframe and insert it into the "bnb" table
            for index, row in self.pp.iterrows():
                query = f"""
                    INSERT INTO bnb (Time, Open, High, Low, Close, Volume, BOP, RSI, fastd, fastk, MACD, Signal, History, BOPT, RSIT, fastdT, fastkT, MACDT, SignalT, HistoryT)
                    VALUES (
                        '{row['Time']}', {row['Open']}, {row['High']}, {row['Low']}, {row['Close']}, {row['Volume']}, {row['BOP']}, {row['RSI']}, {row['fastd']}, {row['fastk']},
                        {row['MACD']}, {row['Signal']}, {row['History']}, {row['BOPT']}, {row['RSIT']}, {row['fastdT']}, {row['fastkT']}, {row['MACDT']}, {row['SignalT']}, {row['HistoryT']}
                    )
                """
                cursor.execute(query)

            # Commit the changes and close the connection
            connection.commit()
            cursor.close()
            connection.close()

        except (Exception, psycopg2.Error) as error:
            # print("Error inserting data:", error)
            pass
        finally:
            print('Data inserted successfully!')

# if __name__ == '__main__':
#     print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     pattern_detect = PatternDetect()

#     while True:
#         try:
#             # Run the main method to gather data
#             asyncio.get_event_loop().run_until_complete(pattern_detect.main())

#             # Insert the data to the database
#             pattern_detect.insert_pp_to_database()

#         except Exception as e:
#             print("Error:", str(e))

#         # Sleep for 15 minutes before running again
#         time.sleep(60)
# Schedule the task to run every 15 minutes

def run_every_15_minutes():
    try:
        # Run the main method to gather data
        asyncio.get_event_loop().run_until_complete(pattern_detect.main())

        # Insert the data to the database
        pattern_detect.insert_pp_to_database()

    except Exception as e:
        print("Error:", str(e))

schedule.every(15).minutes.do(run_every_15_minutes)

if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    pattern_detect = PatternDetect()

    while True:
        # Run the scheduled tasks
        schedule.run_pending()

        # Sleep for 1 second before checking the schedule again
        time.sleep(1)