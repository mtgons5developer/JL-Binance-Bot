from datetime import datetime

import mysql.connector
from mysql.connector import errorcode

import config

def get_startDate():
    
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

        cursor = cnx.cursor(dictionary=True)

        try:
            cursor.execute("SELECT datetime FROM settings WHERE timeframe='15m' AND toggle='1'")

            dd = cursor.fetchone()
            date = dd["datetime"]
            startDate = date.strftime("%d-%m-%Y")  

        except:
            t = date.today()
            y = t - timedelta(days = 1)
            startDate = y.strftime('%d %m %Y')            

        cnx.close()

        return startDate

def get_toggle_5m():

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
        cursor = cnx.cursor()
        try:
            cursor.execute("SELECT Error, pair FROM settings WHERE timeframe='15m' AND toggle='1'") #if error disable all from DB
            myresult = cursor.fetchall()
            for x in myresult:
                print(x)

            print(x[1])
        except:
            cnx.rollback()

        cnx.close()

def get_toggle_15m():

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
        cursor = cnx.cursor()
        try:
            cursor.execute("SELECT Error, pair FROM settings WHERE timeframe='15m' AND toggle='1'") #if error disable all from DB
            cursor.execute("SELECT datetime FROM settings WHERE timeframe='15m' AND toggle='1'") #if error disable all from DB

            myresult = cursor.fetchall()
            for x in myresult:
                print(x)

            print(x[1])
        except:
            cnx.rollback()

        cnx.close()

def get_toggle_30m():

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
        cursor = cnx.cursor()
        try:
            cursor.execute("SELECT Error, pair FROM settings WHERE timeframe='15m' AND toggle='1'") #if error disable all from DB
            myresult = cursor.fetchall()
            for x in myresult:
                print(x)

            print(x[1])
        except:
            cnx.rollback()

        cnx.close()

def get_toggle_1h():

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
        cursor = cnx.cursor()
        try:
            cursor.execute("SELECT Error, pair FROM settings WHERE timeframe='15m' AND toggle='1'") #if error disable all from DB
            myresult = cursor.fetchall()
            for x in myresult:
                print(x)

            print(x[1])
        except:
            cnx.rollback()

        cnx.close()

def get_date():

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
        cursor = cnx.cursor()
        try:
            cursor.execute("SELECT datetime FROM settings WHERE timeframe='15m' AND toggle='1'") #if error disable all from DB
            myresult = cursor.fetchall()
            for x in myresult:
                print(x)

            print(x[1])
        except:
            cnx.rollback()

        cnx.close()