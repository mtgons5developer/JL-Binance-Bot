from datetime import timedelta

import mysql.connector
from mysql.connector import errorcode

import config

class call:

    def get_toggle(self):
        
        self.get_cnx()
        cursor = cnx.cursor(dictionary=True)

        try:
            cursor.execute("SELECT timeframe, pair, qty, vol, deltaRSI, deltaSMA, rsiLong, rsiShort  FROM settings WHERE toggle='1'")
            toggle = cursor.fetchall()
            cnx.close()

            return toggle

        except:
            cnx.close()

    #====================

    def get_status(self, timeframe):
        
        self.get_cnx()
        cursor = cnx.cursor(dictionary=True)

        try:
            cursor.execute("SELECT pair FROM settings WHERE timeframe='" + timeframe + "' AND toggle='1'")
            myresult = cursor.fetchall()
            # print(myresult)
            cnx.close()
            # print("-MySQL connection closed-")
            return myresult

        except:
            cnx.close()

    def get_TH_pair(self, uuid):

        self.get_cnx()
        cursor = cnx.cursor()
        sql = "SELECT symbol FROM tradeHistory WHERE uuid='" + uuid + "';"
        cursor.execute(sql)
        pair = cursor.fetchone()[0]
        cnx.close()

        return pair

    def get_TH_orderID(self, uuid):

        self.get_cnx()
        cursor = cnx.cursor()
        sql = "SELECT orderId FROM tradeHistory WHERE uuid='" + uuid + "';"
        cursor.execute(sql)
        orderId = cursor.fetchone()[0]
        cnx.close()

        return orderId

    def get_TH_uuid(self):
        global th_orderID

        self.get_cnx()
        cursor = cnx.cursor()
        sql = "SELECT MAX(uuid) FROM tradeHistory;"
        cursor.execute(sql)
        th_orderID = cursor.fetchone()[0]    
        cnx.close()

        return str(th_orderID)

    def get_qty(self, timeframe, pair):
        
        self.get_cnx()
        cursor = cnx.cursor(dictionary=True)

        cursor.execute("SELECT qty FROM settings WHERE pair='" + pair + "' AND timeframe='" + timeframe + "' AND toggle='1'")

        dd = cursor.fetchone()
        qty = dd["qty"]

        cnx.close()
        # print("Quantity:", qty)
        return qty

    def get_startDate(self, timeframe):
        
        self.get_cnx()
        cursor = cnx.cursor(dictionary=True)

        try:
            cursor.execute("SELECT datetime FROM settings WHERE timeframe='" + timeframe + "' AND toggle='1'")

            dd = cursor.fetchone()
            date = dd["datetime"]
            startDate = date.strftime("%d-%m-%Y")  

        except:
            t = date.today()
            y = t - timedelta(days = 1)
            startDate = y.strftime('%d %m %Y')            

        cnx.close()
        # print("startDate:", startDate)
        return startDate

    def put_dateErrorSMA(self, timeframe, pair):
        
        self.get_cnx()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("UPDATE settings SET Error='SMA Add more DF.', toggle='2' WHERE timeframe='" + timeframe  + "' AND pair='" + pair + "'")

        try:
            cnx.commit()
        except:
            cnx.rollback()
        
        cnx.close()

    def put_dateErrorRSI(self, timeframe, pair):
        
        self.get_cnx()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("UPDATE settings SET Error='RSI Add more DF.', toggle='2' WHERE timeframe='" + timeframe  + "' AND pair='" + pair + "'")

        try:
            cnx.commit()
        except:
            cnx.rollback()
        
        cnx.close()

    def put_dateErrorPair(self, timeframe, pair):
        
        self.get_cnx()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("UPDATE settings SET Error='Duplicate pair detected.', toggle='2' WHERE timeframe='" + timeframe  + "' AND pair='" + pair + "'")

        try:
            cnx.commit()
        except:
            cnx.rollback()
        
        cnx.close()

    def put_orderID(self, orderId, entryPrice, qty, status, take_profit, orderIdTP):

        self.get_cnx()
        cursor = cnx.cursor()

        query = """INSERT IGNORE INTO order_entry (orderId, qty, entryPrice, status, close_pos, orderIdTP) VALUES (%s, %s, %s, %s, %s, %s)"""

        values = (int(orderId), float(qty), float(entryPrice), int(status), float(take_profit), int(orderIdTP))

        cursor.execute(query, values)
            
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Completed")


    def get_cnx(self):
        global cnx

        try:
            cnx = mysql.connector.connect(user=config.USER, password=config.PASSWORD, host=config.HOST, database=config.DATABASE)    

        except mysql.connector.Error as err:

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        return cnx    