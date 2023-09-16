# JL-Binance-Bot
Imports and Environment Setup:
Import necessary Python libraries and modules.
Load environment variables for database and API keys.
Database Connection Check:
Define a function check_database_connection() to verify the database connection using the provided credentials.
If the database connection is successful, the script proceeds; otherwise, it prints an error message and suggests actions to take.
Fetching Binance Data:
Define functions to retrieve current Bitcoin (BTCUSDT) futures price and statistics (e.g., open, close, RSI, MACD) from the Binance API.
Pattern Detection Class:
Create a PatternDetect class, which contains methods for pattern detection, data manipulation, and database interaction.
Data Retrieval from Binance:
Within the main() method of the PatternDetect class:
Initialize the Binance client using API keys.
Determine the timeframe and set parameters accordingly.
Retrieve historical kline (candlestick) data for BTCUSDT.
Process and format the retrieved data.
Pattern Detection:
Implement various technical indicators like RSI, BOP, MACD, etc., using the talib library.
Determine the "candle_type" (Bullish or Bearish) based on open and close prices.
Calculate and update "count_long" and "count_short" based on detected patterns.
Determine the "side" (Bullish, Bearish, or None) based on pattern counts.
Database Interaction:
Define methods for inserting pattern data (pp) into a PostgreSQL database and updating entries with profit and verification.
Main Execution:
Define a head() function:
Initialize the PatternDetect class.
Continuously run the pattern detection and database interaction code, with a delay based on Binance's 15-minute intervals.
Script Execution:
The if __name__ == '__main__': block executes the head() function, effectively starting the script.
Handling KeyboardInterrupt:
The script is designed to run continuously until stopped by the user, at which point it prints a message indicating that code execution has been stopped by the user.
