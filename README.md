# JL-Binance-Bot
Imports and Environment Setup:<br>
Import necessary Python libraries and modules.<br>
Load environment variables for database and API keys.<br>
Database Connection Check:<br>
Define a function check_database_connection() to verify the database connection using the provided credentials.<br>
If the database connection is successful, the script proceeds; otherwise, it prints an error message and suggests actions to take.<br>
Fetching Binance Data:<br>
Define functions to retrieve current Bitcoin (BTCUSDT) futures price and statistics (e.g., open, close, RSI, MACD) from the Binance API.<br>
Pattern Detection Class:<br>
Create a PatternDetect class, which contains methods for pattern detection, data manipulation, and database interaction.<br>
Data Retrieval from Binance:<br>
Within the main() method of the PatternDetect class:<br>
Initialize the Binance client using API keys.<br>
Determine the timeframe and set parameters accordingly.<br>
Retrieve historical kline (candlestick) data for BTCUSDT.<br>
Process and format the retrieved data.<br>
Pattern Detection:<br>
Implement various technical indicators like RSI, BOP, MACD, etc., using the talib library.<br>
Determine the "candle_type" (Bullish or Bearish) based on open and close prices.<br>
Calculate and update "count_long" and "count_short" based on detected patterns.<br>
Determine the "side" (Bullish, Bearish, or None) based on pattern counts.<br>
Database Interaction:<br>
Define methods for inserting pattern data (pp) into a PostgreSQL database and updating entries with profit and verification.<br>
Main Execution:<br>
Define a head() function:<br>
Initialize the PatternDetect class.<br>
Continuously run the pattern detection and database interaction code, with a delay based on Binance's 15-minute intervals.<br>
Script Execution:<br>
The if __name__ == '__main__': block executes the head() function, effectively starting the script.<br>
Handling KeyboardInterrupt:<br>
The script is designed to run continuously until stopped by the user, at which point it prints a message indicating that code execution has been stopped by the user.<br>
