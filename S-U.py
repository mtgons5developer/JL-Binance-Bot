import mysql.connector
from mysql.connector import errorcode
import config

cnx = mysql.connector.connect(user=config.USER, password=config.PASSWORD, host=config.HOST, database=config.DATABASE)    

mycursor = cnx.cursor()

# =======================SELECT=======================
# mycursor.execute("SELECT id, orderId FROM Trade_History")
# myresult = mycursor.fetchall()

# mycursor.execute("SELECT * FROM Trade_History")
# myresult = mycursor.fetchone()
# print(myresult)

# for x in myresult:
#   print(x)
# print(mycursor.rowcount, "record(s) affected")

# =======================UPDATE=======================
# sql = "UPDATE Settings SET entry_price = '40111' WHERE timeframe = '1h'"

# sql = "UPDATE Settings SET entry_price = %s WHERE timeframe = %s"
# val = ("39000", "1h")

# mycursor.execute(sql, val)
# cnx.commit()

# print(mycursor.rowcount, "record(s) affected")