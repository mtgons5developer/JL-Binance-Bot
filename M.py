import time
from datetime import datetime

import mysql.connector
from mysql.connector import errorcode
import config
import re

cnx = mysql.connector.connect(user=config.USER, 
                                password=config.PASSWORD, 
                                host=config.HOST, 
                                database=config.DATABASE)    

mycursor = cnx.cursor()

mycursor.execute("SELECT toggle FROM settings WHERE timeframe='1h' AND pair='BTCUSDT'")
# myresult = mycursor.fetchall()
myresult = str(mycursor.fetchone())
pattern = re.compile('\W')
toggle = re.sub(pattern, '', myresult)

while True:
    now = datetime.now()
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    second = now.strftime("%S")
    time.sleep(1)
    timer = hour + ":" + minute + ":" + second
    # print(timer)

    if int(minute) == 59 and int(second) == 59 and toggle == 1:
        print(timer)
        print("EXIT")

    if int(minute) == 0 and int(second) == 1:
        print(timer)
        print("ENTRY")

    

    
