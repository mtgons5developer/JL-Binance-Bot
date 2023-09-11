import os
import psycopg2
from datetime import datetime, timedelta
import talib
import pandas as pd
import numpy as np
from binance.client import AsyncClient
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Define the Cloud SQL PostgreSQL connection details
from dotenv import load_dotenv
load_dotenv()

HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD')
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')
TABLE_NAME = "ml"

# Load data from your database
def load_data():
    try:
        # Establish a database connection
        connection = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )

        # Define your SQL query to fetch data
        query = f"SELECT * FROM {TABLE_NAME}"  # Modify this with your query

        # Fetch data from the database into a DataFrame
        data = pd.read_sql(query, connection)

        # Close the database connection
        connection.close()

        return data
    except Exception as e:
        print(f"Error loading data from the database: {e}")
        return None

# ... (Other setup code) ...

class PatternDetect:
    # ...

    def train_machine_learning_model(self, df):
        X = df[['RSI', 'MACD']]  # Features
        y = df['SignalT']  # Target variable

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize and train a machine learning model (Random Forest in this example)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Make predictions on the test set
        y_pred = model.predict(X_test)

        # Evaluate the model's accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model Accuracy: {accuracy * 100:.2f}%")

    def main(self):
        # Load data from your database
        df = load_data()

        if df is not None:
            # ... (Existing code to calculate signals) ...

            # Train the machine learning model using the loaded data
            self.train_machine_learning_model(df)

            # ... (Existing code to determine trading strategy and update database) ...

if __name__ == '__main__':
    pattern_detect = PatternDetect()

    try:
        pattern_detect.main()
        pattern_detect.insert_pp_to_database()
    except Exception as e:
        print("Error:", str(e))
