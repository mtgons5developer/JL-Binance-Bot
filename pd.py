import talib
import asyncio
import pandas as pd
from binance.client import Client, AsyncClient
import config

class PatternDetect:

    # Get dataframe
    def get_data_frame(self, symbol, msg):
        global rows_count, df
        # Converting the data to pandas dataframe
        df = pd.DataFrame(msg)
        df.columns = ['Time','Open', 'High', 'Low', 'Close', 'Volume','CloseTime', 'qav','num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
        df = df.loc[:, ['Time','Open', 'High', 'Low', 'Close']]
        df["Time"] = pd.to_datetime(df["Time"], unit='ms')
        df["Open"] = df["Open"].astype(float)
        df["High"] = df["High"].astype(float)
        df["Low"] = df["Low"].astype(float)
        df["Close"] = df["Close"].astype(float)        
   
        rows_count = len(df.index)
        close = df["Close"]
        print(close)
        rsi = talib.RSI(close)
        print(df)
        print(rsi)
        print(rows_count)

        quit()
        return df

    def detect_pattern(self, symbol, data):
        data["Time"] = pd.to_datetime(data["Time"])
        # ms = talib.CDLMORNINGSTAR(data["Open"], data["High"], data["Low"], data["Close"])
        eng = talib.CDLENGULFING(data["Open"], data["High"], data["Low"], data["Close"])
        # quit()
        # data['msi'] = ms
        data['CDLENGULFING'] = eng
        cdcd = data[data['CDLENGULFING'] != 0]
        # print(cdcd.iloc[-1])
        # print(df.iloc[-1])
        dd = pd.DataFrame(cdcd)
        
        rows_count2 = cdcd.index.name
        # print(rows_count + " " + rows_count2)
        # print(cdcd.index.name)

    async def main(self):

        client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
        symbol = 'BTCUSDT'
        print(f'Retrieving and Uploading Historical data from Binance for: {symbol}')
        msg = await client.futures_historical_klines(symbol=symbol, interval='1h', start_str='01 Mar 2022', end_str='01 Apr 2022')
        data = self.get_data_frame(symbol=symbol, msg=msg)
        self.detect_pattern(symbol=symbol, data=data)
        await client.close_connection()
        print("Connection Closed")

if __name__ == '__main__':
    pattern_detect = PatternDetect()
    asyncio.get_event_loop().run_until_complete(pattern_detect.main())
