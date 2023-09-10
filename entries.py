import os
import psycopg2
from datetime import datetime
from decimal import Decimal

# Define the Cloud SQL PostgreSQL connection details
from dotenv import load_dotenv
load_dotenv()

HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD')
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

def convert_value(value):
    # Check if the value is of Decimal type
    if isinstance(value, Decimal):
        # Convert Decimal to float
        return float(value)
    # Check if the value is of datetime type
    elif isinstance(value, datetime):
        # Format datetime as a string
        return value.strftime("%Y-%m-%d %H:%M:%S")
    else:
        # Keep the value as-is
        return value
    
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

    # Execute the SQL query to retrieve the row with the maximum "time" value for pair 'BTCUSDT'
    max_time_query = """
    SELECT MAX("time")
    FROM bnb
    WHERE pair = 'BTCUSDT';
    """
    cursor.execute(max_time_query)
    max_time = cursor.fetchone()

    if max_time:
        # Extract the maximum "time" value
        max_time_value = max_time[0]

        # Execute the SQL query to retrieve all rows with the same "time" value and pair 'BTCUSDT'
        main_query = """
        SELECT *
        FROM bnb
        WHERE "time" = %s AND pair = 'BTCUSDT';
        """
        cursor.execute(main_query, (max_time_value,))
        result = cursor.fetchall()

        # Remove type information (e.g., "Decimal") and convert values
        result_without_types = [[convert_value(val) for val in row] for row in result]

        # Display the result without type information
        print("Result:")
        if result_without_types:
            for row in result_without_types:
                print(row)

    else:
        print("No entries found for pair 'BTCUSDT'.")

except (Exception, psycopg2.Error) as error:
    print("Error:", error)

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()