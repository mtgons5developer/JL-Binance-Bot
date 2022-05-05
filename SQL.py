import mysql.connector
from mysql.connector import errorcode
import config

try:
    cnx = mysql.connector.connect(user=config.USER, password=config.PASSWORD, host=config.HOST, database=config.DATABASE)    

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    #Creating a cursor object using the cursor() method
    cursor = cnx.cursor()
    print("Connected")
    #Dropping EMPLOYEE table if already exists.
    # cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

    # sql1 ='''CREATE TABLE order_entry(
    # `id` INT AUTO_INCREMENT primary key NOT NULL,
    # orderId INT, 
    # entryPrice FLOAT,
    # qty FLOAT,
    # `entry_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    # )'''
    # cursor.execute(sql1)
    # quit()

    # sql3 ='''CREATE TABLE settings(
    # `id` INT AUTO_INCREMENT primary key NOT NULL,
    # qty FLOAT,
    # timeframe CHAR(5) NOT NULL,
    # pair CHAR(10) NOT NULL,
    # toggle TINYINT NOT NULL,
    # `datetime` TIMESTAMP DEFAULT CURRENT_TIMESTAMP    
    # )'''
    # cursor.execute(sql3)
    # quit()
    # sql2 ='''CREATE TABLE 1hTF(
    # `id` INT AUTO_INCREMENT primary key NOT NULL,      
    # pair CHAR(10) NOT NULL,
    # open FLOAT NOT NULL,
    # close FLOAT NOT NULL,
    # high FLOAT NOT NULL,
    # low FLOAT NOT NULL,
    # CDLENGULFING CHAR(10) NOT NULL,
    # `date_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    # )'''
    # cursor.execute(sql2)
    # quit()

    # sql2 ='''CREATE TABLE tradeHistory(
    # symbol CHAR(10) NOT NULL,
    # id BIGINT(11) UNIQUE NOT NULL,
    # orderId BIGINT(11) NOT NULL,
    # side CHAR(4) NOT NULL,
    # price FLOAT,
    # qty FLOAT,
    # realizedPnl FLOAT,
    # marginAsset CHAR(10) NOT NULL,
    # quoteQty FLOAT,
    # commission FLOAT,
    # commissionAsset CHAR(10) NOT NULL,
    # time BIGINT(11) NOT NULL,
    # positionSide CHAR(5) NOT NULL,
    # buyer tinyint(1) NOT NULL,
    # maker tinyint(1) NOT NULL                    
    # )'''
    # cursor.execute(sql2)
    # quit()

    entry_price = "2000"
    quantity = "0.002"
    timeframe = "1h"
    pair = "BNBUSDT"
    # pair = "ETHUSDT"
    
    # cursor = cnx.cursor(dictionary=True)
    sql = "SELECT symbol FROM tradeHistory WHERE orderId=52583020839;"
    cursor.execute(sql)
    dd = cursor.fetchone()[0]
    print(dd)
    cnx.close()
    quit()
    # {'MAX( uuid )': 10}
    
    # Preparing SQL query to INSERT a record into the database.
    # sql = """INSERT IGNORE INTO settings(
    #   entryPrice, qty, timeframe, pair)
    #   VALUES (""" + "'" + entry_price + "','" + quantity + "','" + timeframe + "','" + pair + "')"

    #Preparing the query to update the records
    # sql = "UPDATE Settings SET Entry_Price = " + entry_price + " WHERE Timeframe = '1h' AND Pair = 'BTCUSDT'"    

    try:
      # Executing the SQL command
      cursor.execute(sql)

      # Commit your changes in the database
      cnx.commit()

    except:
      # Rolling back in case of error
      cnx.rollback()

    # print("Data inserted")

    # #Retrieving data
    # sql = '''SELECT * from settings'''

    # #Executing the query
    # cursor.execute(sql)

    #Displaying the result
    print(cursor.fetchall())

    #Closing the connection
    cnx.close()

# http://mysql-python.sourceforge.net/MySQLdb.html
# https://www.tutorialspoint.com/python_data_access/python_mysql_create_table.htm