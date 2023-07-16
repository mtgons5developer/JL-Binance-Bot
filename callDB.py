import os
from datetime import datetime

import mysql.connector
from mysql.connector import errorcode

# import config
# Define the Cloud SQL PostgreSQL connection details
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')
HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD')


class call:

    def get_toggle(self):
        
        self.get_cnx()
        cursor = cnx.cursor(dictionary=True)

        try:
            cursor.execute("SELECT order_type, timeframe, pair, qty, vol, deltaSMA, rsiLong, rsiShort  FROM settings WHERE toggle='1'")
            toggle = cursor.fetchall()
            cursor.close()
            cnx.close()

            return toggle

        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")

    #====================

    def get_status(self, pair):
        
        self.get_cnx()
        cursor = cnx.cursor(dictionary=True)

        try:
            cursor.execute("SELECT orderId, orderIdTP FROM order_entry WHERE pair='" + pair + "' AND " + "status='1'")
            status = cursor.fetchall()
            cursor.close()
            cnx.close()

            return status

        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")

    def get_order_EntryStatus(self, pair):
        
        self.get_cnx()
        cursor = cnx.cursor(dictionary=True)

        try:
            cursor.execute("SELECT status FROM order_entry WHERE pair='" + pair + "'")
            status = cursor.fetchall()
            cursor.close()
            cnx.close()

            return status

        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")

    def get_TH_pair(self, uuid):

        try:
            self.get_cnx()
            cursor = cnx.cursor()
            sql = "SELECT symbol FROM tradeHistory WHERE uuid='" + uuid + "';"
            cursor.execute(sql)
            pair = cursor.fetchone()[0]
            cnx.close()

            return pair
            
        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")


    def get_TH_orderID(self, uuid):

        try:

            self.get_cnx()
            cursor = cnx.cursor()
            sql = "SELECT orderId FROM tradeHistory WHERE uuid='" + uuid + "';"
            cursor.execute(sql)
            orderId = cursor.fetchone()[0]
            cnx.close()

            return orderId

        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")


    def get_TH_uuid(self):
        global th_orderID

        try:

            self.get_cnx()
            cursor = cnx.cursor()
            sql = "SELECT MAX(uuid) FROM tradeHistory;"
            cursor.execute(sql)
            th_orderID = cursor.fetchone()[0]    
            cnx.close()

            return str(th_orderID)

        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")

    def get_qty(self, timeframe, pair):
        
        try:
            self.get_cnx()
            cursor = cnx.cursor(dictionary=True)

            cursor.execute("SELECT qty FROM settings WHERE pair='" + pair + "' AND timeframe='" + timeframe + "' AND toggle='1'")

            dd = cursor.fetchone()
            qty = dd["qty"]

            cnx.close()
            # print("Quantity:", qty)
            return qty

        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")


    def put_dateErrorSMA(self, timeframe, pair):

        try:
            self.get_cnx()
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("UPDATE settings SET Error='SMA Add more DF.', toggle='2' WHERE timeframe='" + timeframe  + "' AND pair='" + pair + "'")            
            cnx.commit()
            cnx.close() 

        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")

    def put_dateErrorRSI(self, timeframe, pair):

        try:
            self.get_cnx()
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("UPDATE settings SET Error='RSI Add more DF.', toggle='2' WHERE timeframe='" + timeframe  + "' AND pair='" + pair + "'")            
            cnx.commit()
            cnx.close()

        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")

    def put_dateErrorPair(self, timeframe, pair):

        try:
            self.get_cnx()
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("UPDATE settings SET Error='Duplicate pair detected.', toggle='2' WHERE timeframe='" + timeframe  + "' AND pair='" + pair + "'")            
            cnx.commit()
            cnx.close()

        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")

    def put_orderID(self, pair, orderId, side, qty, market_price, take_profit, orderIdTP, timeframe, balance):

        try:
            self.get_cnx()
            cursor = cnx.cursor()

            query = """INSERT IGNORE INTO order_entry (pair, orderId, side, qty, entryPrice, status, close_pos, orderIdTP, timeframe, balance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            values = (pair, int(orderId), side, float(qty), float(market_price), '1', float(take_profit), int(orderIdTP), timeframe, float(balance))

            cursor.execute(query, values)            
            cnx.commit()
            cursor.close()
            cnx.close()

        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")

        

    def put_homemsg(self, pair, timeframe, side, username):

        try:
            self.get_cnx()
            cursor = cnx.cursor()
            query = """INSERT IGNORE INTO home_msg (pair, timeframe, side, username) VALUES (%s, %s, %s, %s)"""
            values = (pair, timeframe, side, username)
            cursor.execute(query, values)
            cnx.commit()
            cursor.close()
            cnx.close()

        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")

                                    
    def put_orderTest(self, pair, qty, entry_price, take_profit, side, order_type, timeframe):

        try:

            self.get_cnx()
            cursor = cnx.cursor()

            query = """INSERT IGNORE INTO order_entry (pair, qty, entryPrice, status, side, order_type, timeframe, close_pos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

            values = (pair, float(qty), float(entry_price), "1", side, order_type, timeframe, int(take_profit))

            cursor.execute(query, values)
                
            cnx.commit()
            cursor.close()
            cnx.close()

        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")

    def put_orderTest_Exit(self, pair, order_type, timeframe, win_lose):

        try:

            self.get_cnx()
            cursor = cnx.cursor()

            query = """INSERT IGNORE INTO order_entry (pair, status, timeframe, win_lose) VALUES (%s, %s, %s, %s)"""

            values = (pair, "2", order_type, timeframe, win_lose)

            cursor.execute(query, values)
                
            cnx.commit()
            cursor.close()
            cnx.close()

        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")

    def put_order_Exit(self, pair):

        try:
            self.get_cnx()
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("UPDATE order_entry SET status='2' WHERE status='1' AND pair='" + pair + "'")
            cnx.commit()
            cnx.close()
            print("Completed put_order_Exit")

            status = 1
            return status
       
        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")

    def get_user(self):

        try:
            self.get_cnx()
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("SELECT name FROM users WHERE api_key='" + BINANCE_API_KEY + "'")
            dd = cursor.fetchone()
            cnx.close()

            return dd

        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")

    def write_error(self, error_info):

        with open('debug.txt', 'a') as f:
            f.write(error_info)
                

    def get_cnx(self):
        global cnx

        try:
            cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)    

        except mysql.connector.Error as err:

            datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error_info = "\n" + datetime + errorcode.ER_ACCESS_DENIED_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error_info = "\n" + datetime + errorcode.ER_BAD_DB_ERROR + "\n"
                print(error_info)
                self.write_error(error_info)  
            else:
                print(err, "Error: get_cnx")

        return cnx    