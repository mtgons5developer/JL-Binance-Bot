import tkinter as tk
from tkinter import ttk
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve database connection details from environment variables
db_config = {
    "host": os.getenv('HOST'),
    "database": os.getenv('DATABASE'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('PASSWORD'),
}

# Function to fetch data from the database
def fetch_data():
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM bnb")  # Replace with your table name
        data = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        connection.close()
        return column_names, data
    except (Exception, psycopg2.Error) as error:
        print("Error fetching data:", error)
        return [], []

# Function to refresh the displayed data
def refresh_data():
    column_names, data = fetch_data()
    if column_names and data:
        df = pd.DataFrame(data, columns=column_names)
        tree.delete(*tree.get_children())
        for index, row in df.iterrows():
            tree.insert("", "end", values=tuple(row), tags=("centered",))

# Create the Tkinter app
app = tk.Tk()
app.title("Data Viewer")

# Create a Treeview widget to display the data
tree = ttk.Treeview(app, columns=("timestamp", "date/time", "candle_type", "strong_wick", "wick_size", "body", "timestamp_open", "open", "high", "low", "close", "open_close_diff"))
# Add headings for columns
tree.heading("#1", text="Timestamp")
tree.heading("#2", text="Date/Time")
tree.heading("#3", text="Candle Type")
tree.heading("#4", text="Strong Wick")
tree.heading("#5", text="Wick Size")
tree.heading("#6", text="Body")
tree.heading("#7", text="Timestamp Open")
tree.heading("#8", text="Open")
tree.heading("#9", text="High")
tree.heading("#10", text="Low")
tree.heading("#11", text="Close")
tree.heading("#12", text="Open/Close Diff")
tree.pack()

# Configure style to center-align rows
style = ttk.Style()
style.configure("Treeview", rowheight=25)  # Adjust row height to center-align content
style.configure("Treeview.Heading", anchor="center")  # Center-align column headings

# Configure style for the centered rows
style.configure("centered.Treeview", anchor="center")

# Create a Refresh button
refresh_button = tk.Button(app, text="Refresh Data", command=refresh_data)
refresh_button.pack()

# Initial data retrieval and display
refresh_data()

app.mainloop()
