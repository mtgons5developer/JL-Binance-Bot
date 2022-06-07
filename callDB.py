import mysql.connector
from mysql.connector import errorcode

import config

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

        except:
            cursor.close()
            cnx.close()

    #====================

    def get_status(self, pair):
        
        self.get_cnx()
        cursor = cnx.cursor(dictionary=True)

        try:
            cursor.execute("SELECT timeframe, orderId, orderIdTP, entry_date, pair, order_type, status  FROM order_entry WHERE pair='" + pair + "' AND " + "status='1'")
            status = cursor.fetchall()
            cursor.close()
            cnx.close()

            return status

        except:
            cursor.close()
            cnx.close()

    def get_order_EntryStatus(self, pair):
        
        self.get_cnx()
        cursor = cnx.cursor(dictionary=True)

        try:
            cursor.execute("SELECT status FROM order_entry WHERE pair='" + pair + "'")
            status = cursor.fetchall()
            cursor.close()
            cnx.close()

            return status

        except:
            cursor.close()
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

    # def get_startDate(self, timeframe):
        
    #     self.get_cnx()
    #     cursor = cnx.cursor(dictionary=True)

    #     try:
    #         cursor.execute("SELECT datetime FROM settings WHERE timeframe='" + timeframe + "' AND toggle='1'")

    #         dd = cursor.fetchone()
    #         date = dd["datetime"]
    #         startDate = date.strftime("%d-%m-%Y")  

    #     except:
    #         t = date.today()
    #         y = t - timedelta(days = 1)
    #         startDate = y.strftime('%d %m %Y')            

    #     cnx.close()
    #     # print("startDate:", startDate)
    #     return startDate

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
                          
    def put_orderID(self, pair, orderId, side, qty, market_price, take_profit, orderIdTP, timeframe):

        self.get_cnx()
        cursor = cnx.cursor()

        query = """INSERT IGNORE INTO order_entry (pair, orderId, side, qty, entryPrice, status, close_pos, orderIdTP, timeframe) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        values = (pair, int(orderId), side, float(qty), float(market_price), '1', float(take_profit), int(orderIdTP), timeframe)

        cursor.execute(query, values)
            
        cnx.commit()
        cursor.close()
        cnx.close()
        print("-------Order Entry Success-------\n", pair)
                            
    def put_orderTest(self, pair, qty, entry_price, take_profit, side, order_type, timeframe):

        self.get_cnx()
        cursor = cnx.cursor()

        query = """INSERT IGNORE INTO order_entry (pair, qty, entryPrice, status, side, order_type, timeframe, close_pos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        values = (pair, float(qty), float(entry_price), "1", side, order_type, timeframe, int(take_profit))

        cursor.execute(query, values)
            
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Completed put_orderTest")

    def put_orderTest_Exit(self, pair, order_type, timeframe, win_lose):

        self.get_cnx()
        cursor = cnx.cursor()

        query = """INSERT IGNORE INTO order_entry (pair, status, timeframe, win_lose) VALUES (%s, %s, %s, %s)"""

        values = (pair, "2", order_type, timeframe, win_lose)

        cursor.execute(query, values)
            
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Completed put_orderTest_Exit")

    def put_order_Exit(self, pair):

        self.get_cnx()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("UPDATE order_entry SET status='2' WHERE status='1' AND pair='" + pair + "'")

        try:
            cnx.commit()
            print("Completed put_order_Exit")
            status = 1
            return status
        except:
            print("put_order_Exit ERROR")
            cnx.rollback()
            status = 1
            return status            
        
        cnx.close()

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
                print(err, "get_cnx")

        return cnx    