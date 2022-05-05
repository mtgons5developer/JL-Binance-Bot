from datetime import timedelta

import mysql.connector
from mysql.connector import errorcode

import config
    
def get_toggle(timeframe):
    
    get_cnx()
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

def get_status(timeframe):
    
    get_cnx()
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

def get_TH_pair(uuid):

    get_cnx()
    cursor = cnx.cursor()
    sql = "SELECT symbol FROM tradeHistory WHERE uuid='" + uuid + "';"
    cursor.execute(sql)
    pair = cursor.fetchone()[0]
    cnx.close()

    return pair

def get_TH_orderID(uuid):

    get_cnx()
    cursor = cnx.cursor()
    sql = "SELECT orderId FROM tradeHistory WHERE uuid='" + uuid + "';"
    cursor.execute(sql)
    orderId = cursor.fetchone()[0]
    cnx.close()

    return orderId

def get_TH_uuid():
    global th_orderID

    get_cnx()
    cursor = cnx.cursor()
    sql = "SELECT MAX(uuid) FROM tradeHistory;"
    cursor.execute(sql)
    th_orderID = cursor.fetchone()[0]    
    cnx.close()

    return str(th_orderID)

def get_qty(timeframe, pair):
    
    get_cnx()
    cursor = cnx.cursor(dictionary=True)

    cursor.execute("SELECT qty FROM settings WHERE pair='" + pair + "' AND timeframe='" + timeframe + "' AND toggle='1'")

    dd = cursor.fetchone()
    qty = dd["qty"]

    cnx.close()
    # print("Quantity:", qty)
    return qty

def get_startDate(timeframe):
    
    get_cnx()
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

def put_dateError(timeframe, pair):
    
    get_cnx()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("UPDATE settings SET Error='1', toggle='0' WHERE timeframe='" + timeframe  + "' AND Pair='" + pair + "'")

    try:
        cnx.commit()
    except:
        cnx.rollback()
    
    cnx.close()

def put_orderID(orderId, qty, entryPrice, status, close_pos):
    
    get_cnx()
    cursor = cnx.cursor(dictionary=True)
    # cursor.execute("INSERT order_entry SET Error='1', toggle='0' WHERE '")
    sql = """INSERT IGNORE INTO order_entry(
      orderId, qty, entryPrice, status, close_pos)
      VALUES (""" + "'" + orderId + "','" + qty + "','" + entryPrice + "','" + status + "','" + close_pos + "')"

    try:
      cursor.execute(sql)
      cnx.commit()

    except:
      cnx.rollback()

    sql = '''SELECT * from order_entry'''
    cursor.execute(sql)
    print(cursor.fetchall())
    cnx.close()

def get_cnx():
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