
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
import requests
import pytz
from binance.client import Client

# import callDB
# import CO
from binance.client import AsyncClient

# Define the Cloud SQL PostgreSQL connection details
from dotenv import load_dotenv
load_dotenv()

HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD')
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

# db = callDB.call()
# CreateOrder = CO.call()

# Function to check the database connection
def check_database_connection():
    try:
        # Attempt to establish a connection to the database
        conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )
        # If the connection is successful, close it and return True
        conn.close()
        return True
    except Exception as e:
        # If there's an error, print the error message and return False
        print(f"Database connection error: {e}")
        return False

# Check the database connection before proceeding
if check_database_connection():
    # Database connection is successful, you can proceed with the rest of your code
    print("Database connection successful. Proceeding with the rest of the script.")
else:
    # Database connection failed, you may want to handle this situation gracefully
    print("Database connection failed. Run this on terminal pg_ctl -D /opt/homebrew/var/postgresql@14 start")
    #pip install --upgrade --force-reinstall numpy
    #pg_ctl -D /opt/homebrew/var/postgresql@14 stop
    #pg_ctl -D /opt/homebrew/var/postgresql@14 start
    quit()

def get_current_btc_futures_price():
    try:
        url = "https://fapi.binance.com/fapi/v1/ticker/price"
        params = {"symbol": "BTCUSDT"}
        response = requests.get(url, params=params)
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print("Error fetching BTCUSDT price:", str(e))
        return None

import requests

def get_current_btc_futures_stats():
    try:
        url = "https://fapi.binance.com/fapi/v1/klines"
        params = {
            "symbol": "BTCUSDT",
            "interval": "15m",  # 15-minute interval
            "limit": 1  # Retrieve the latest data point
        }
        response = requests.get(url, params=params)
        data = response.json()[0]  # Get the first (latest) data point

        # Extracting the required data from the Kline/Candlestick data
        open_price = float(data[1])  # Open price is at index 1
        close_price = float(data[4])  # Close price is at index 4
        high_price = float(data[2])   # High price is at index 2
        low_price = float(data[3])    # Low price is at index 3
        volume = float(data[5])       # Volume is at index 5

        # Calculate the candle_type based on lastPrice and openPrice
        candle_type = 'Bullish' if close_price > open_price else 'Bearish'

        # print("Candle Type:", candle_type)
        # print("Close Price:", close_price)

        # return candle_type
        return candle_type, open_price, close_price, high_price, low_price, volume

    except Exception as e:
        print("Error fetching BTCUSDT stats:", str(e))
        return None

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
            current_datetime = datetime.now()
            print(f'\nRetrieving Historical data from Binance for: {pair, timeframe} \n')
            await client.close_connection()

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
        df["Time"] = df["Time"] + pd.Timedelta(hours=8)
        df["Open"] = df["Open"].astype(float)
        df["High"] = df["High"].astype(float)
        df["Low"] = df["Low"].astype(float)
        df["Close"] = df["Close"].astype(float)
        df["Volume"] = df["Volume"].astype(float)

        return df
        
#=====================================================================================================================

    def Pattern_Detect(self):
        global side, count_long, count_short

        RSI = talib.RSI(df['Close'], timeperiod=14)
        BOP = talib.BOP(df['Open'], df['High'], df['Low'], df['Close'])
        macd, macdsignal, macdhist = talib.MACD(df['Close'], fastperiod=3, slowperiod=10, signalperiod=16) #HIGH TF
        fastk, fastd = talib.STOCHRSI(df['Close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

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

# Initialize counters for LONG and SHORT
        count_long = 0
        count_short = 0

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

        if RSIT == "SHORT":
            count_short += 1
        if RSIT == "LONG":
            count_long += 1

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

        if fastdT == "SHORT":
            count_short += 1
        if fastdT == "LONG":
            count_long += 1

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

        if MACDT == "SHORT":
            count_short += 1
        if MACDT == "LONG":
            count_long += 1

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

        if SignalT == "SHORT":
            count_short += 1
        if SignalT == "LONG":
            count_long += 1

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

        if HistoryT == "SHORT":
            count_short += 1
        if HistoryT == "LONG":
            count_long += 1

        # print(RSIT)
        # print(fastdT)
        # print(MACDT)
        # print(SignalT)
        # print(HistoryT)

        print(f"LONG Count: {count_long}")
        print(f"SHORT Count: {count_short}")     

        # Check if LONG is greater than or equal to 3 times SHORT
        if count_long >= 3 * count_short:
            print("LONG is greater than SHORT")
            side = "Bullish"
        elif count_short >= 3 * count_long:
            print("SHORT is greater than LONG")
            side = "Bearish"
        else:
            print("No significant difference between LONG and SHORT")
            side = "NONE"

        self.pp = df.tail(4)
        print(self.pp)
        print("\n" + str(side))

        # with open('output.txt', 'w') as f:
        #     f.write(
        #         self.pp.to_string()
        #     )  

    # Function to insert the "pp" data into the "bnb" table
    def insert_pp_to_database(self):
        try:

            btc_futures_price = get_current_btc_futures_price()

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
                    INSERT INTO bnb (pair, side, "time", count_long, count_short, "open", "high", "low", "close", "volume", "bop", "rsi", "fastd", "fastk", "macd", "signal", "history", "bopt", "rsit", "fastdt", "fastkt", "macdt", "signalt", "historyt")
                    VALUES (
                        '{pair}', '{side}', '{row['Time']}', {count_long}, {count_short}, {row['Open']}, {row['High']}, {row['Low']}, {row['Close']}, {row['Volume']}, {row['BOP']}, {row['RSI']}, {row['fastd']}, {row['fastk']},
                        {row['MACD']}, {row['Signal']}, {row['History']}, {row['BOPT']}, {row['RSIT']}, {row['fastdT']}, {row['fastkT']}, {row['MACDT']}, {row['SignalT']}, {row['HistoryT']}
                    )
                """
                cursor.execute(query)

            query2 = f"""
                INSERT INTO entries (pair, prophecy, entry, open, close)
                VALUES (
                    '{pair}', '{side}', {btc_futures_price}, '{row['Open']}', '{row['Close']}'
                )
            """
            cursor.execute(query2)

            # Commit the changes and close the connection
            connection.commit()
            cursor.close()
            connection.close()

        except (Exception, psycopg2.Error) as error:
            print("Error inserting data1:", error)
            pass
        finally:
            print('Data inserted successfully!')


    def entry(self):
        btc_futures_price = get_current_btc_futures_price()
        try:
            # Connect to the PostgreSQL database
            connection = psycopg2.connect(
                host=HOST,
                database=DATABASE,
                user=USER,
                password=PASSWORD
            )

            # Create a cursor object
            cursor = connection.cursor()

            # Define the SQL query to select rows with 'pair' as 'BTCUSDT' and 'verified' column is NULL
            select_query = """
            SELECT entry
            FROM entries
            WHERE pair = 'BTCUSDT' AND verified IS NULL;
            """
            # WHERE pair = 'BTCUSDT' AND verified IS NULL;
            # Execute the query to fetch the entry values
            cursor.execute(select_query)

            entry_values = cursor.fetchall()

            data = get_current_btc_futures_stats()

            # Process the entry values as needed dldl
            for entry_value in entry_values:
                entry = float(entry_value[0])  # Assuming 'entry' is the first (and only) column
                profit = round(entry - btc_futures_price, 1)

                # Define the SQL query to update the 'profit' column in the 'entries' table
                update_query = """
                UPDATE entries
                SET profit = %s, verified = %s
                WHERE entry = %s;
                """
                
                # Execute the update query with the calculated profit and entry values
                cursor.execute(update_query, (profit, data[0], entry))

                # Commit the changes to the database
                connection.commit()
            
            # Close the cursor and connection
            cursor.close()
            connection.close()

        except (Exception, psycopg2.Error) as error:
            print("Error:", error)

# def run_every_15_minutes():
#     try:
#         # Run the main method to gather data
#         asyncio.get_event_loop().run_until_complete(pattern_detect.main())

#         # Insert the data to the database
#         pattern_detect.insert_pp_to_database()
#         pattern_detect.insert_pp_to_database2()

#     except Exception as e:
#         print("Error:", str(e))

# schedule.every(15).minutes.do(run_every_15_minutes)


def run_every_15_minutes():
    try:
        # Initialize the Binance client
        client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)
        # Get the Binance server time
        server_time = client.get_server_time()
        binance_time = datetime.datetime.utcfromtimestamp(server_time['serverTime'] / 1000.0)
        binance_time = pytz.utc.localize(binance_time)

        # Adjust the schedule to run 15 minutes from the next Binance minute
        next_binance_minute = (binance_time.minute // 15 + 1) * 15
        next_run_time = binance_time.replace(minute=next_binance_minute, second=0, microsecond=0)

        # Run the main method to gather data
        asyncio.get_event_loop().run_until_complete(pattern_detect.main())

        # Insert the data to the database
        pattern_detect.insert_pp_to_database()
        pattern_detect.entry()

        # Print the scheduled run time
        print("Scheduled run time:", next_run_time.strftime("%Y-%m-%d %H:%M:%S"))

    except Exception as e:
        print("Error:", str(e))

if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # quit()
    pattern_detect = PatternDetect()

    while True:
        # Run the scheduled tasks
        schedule.run_pending()

        # Sleep for 1 second before checking the schedule again
        time.sleep(1)

# if __name__ == '__main__':
#     print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     pattern_detect = PatternDetect()

#     try:
#         asyncio.get_event_loop().run_until_complete(pattern_detect.main())
#         pattern_detect.insert_pp_to_database()
#         pattern_detect.entry()
#         quit()
#     except Exception as e:
#         print("Error:", str(e))




# entry_price = 30257.10
# leverage = 50
# profit_percentage = 0.25

# exit_price = entry_price * (1 + (profit_percentage / (leverage * 100)))
# print(f"Exit Price = {exit_price:.2f} USDT")

