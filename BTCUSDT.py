from datetime import datetime, timedelta

import talib
import asyncio
import pandas as pd
import numpy as np

from binance.client import AsyncClient

import config
import callDB
import CO

db = callDB.call()
CreateOrder = CO.call()

class PatternDetect:

#=====================================================================================================================

    async def main(self):
        global pair, timeframe, error_set, deltaSMA, rsiLong, rsiShort
        
        error_set = 0
        error_set2 = 0
        result = db.get_toggle()

        yy = 0
        for y in result:
            yy += 1

        xx = 0
        for x in result:
            xx += 1
            pair = x['pair']
            timeframe = x['timeframe']
            qty = x['qty']
            volume_set = x['vol']

            rsiLong = x['rsiLong']
            rsiShort = x['rsiShort']
            deltaSMA = x['deltaSMA']
            order_type = x['order_type']

            # BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT, SOLUSDT, LUNAUSDT, ADAUSDT, USTUSDT, BUSDUSDT, 
            # DOGEUSDT, AVAXUSDT, DOTUSDT, SHIBUSDT, WBTCUSDT, DAIUSDT, MATICUSDT

            if pair == "BTCUSDT":# and error_set2 == 0:

                try:
                    
                    client = await AsyncClient.create(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
                    last_hour_date_time = datetime.now() - timedelta(hours = deltaSMA)
                    get_startDate = last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')
                    msg = await client.futures_historical_klines(symbol=pair, interval=timeframe, start_str=get_startDate, end_str=None)
                    data = self.get_data_frame(symbol=pair, msg=msg) 
                    self.d_Candle()  
                    self.d_RSI()
                    self.d_SMA()
                    print(f'\nRetrieving Historical data from Binance for: {pair, timeframe} \n')          

                    if error_set == 0:

                        #Not important on final code      
                        side = "NONE"

                        print("SMA >= curPrice: %(g)s >= %(a)s \nRSI+rsiLong: %(c)s <= %(d)s\nVolume >= Volume_SET: %(e)s >= %(f)s" % 
                                {'a': curPrice, 'c': rsi, 'd': rsiLong, 'e': volume, 'f': volume_set, 'g': sma})    

                        if rsiShort == 1 and rsiLong == 1 and volume_set == 1:
                            print("---Settings Disabled---")
                            side = "SELL"
                            # entry_price = round(curPrice / 2, 8)
                            entry_price = curPrice
                            entry_price = CreateOrder.get_rounded_price(pair, entry_price)
                            tp1 = high - close
                            tp2 = tp1 * 0.30
                            take_profit = round(close + tp2, 8)   

                            if curPrice > sma and volume >= volume_set and candle < 0:
                                side = "BUY" 
                            elif curPrice < sma and volume >= volume_set and candle > 0:
                                side = "SELL"  

                        elif rsiShort == 1 and rsiLong == 1 and volume_set > 1:
                            print("---RSI Disabled---")
                            # entry_price = round(curPrice / 2, 8)
                            entry_price = curPrice
                            entry_price = CreateOrder.get_rounded_price(pair, entry_price)
                            tp1 = high - close
                            tp2 = tp1 * 0.30
                            take_profit = round(close + tp2, 8)   
                            candle = open - close

                            if curPrice > sma and volume >= volume_set and candle < 0:
                                side = "BUY" 
                            elif curPrice < sma and volume >= volume_set and candle > 0:
                                side = "SELL"                                       

                        elif rsiShort > 1 and rsiLong > 1 and volume_set > 1: #Detect Bearish/Bullish Candle

                            # 29502.7  29506.6  29320.1  29387.9 
                            # HL = 29506.6 - 29320.1
                            # HL = 186.5
                            # 2D = 93.25
                            # x = 29320.1 + 93.25; LOW + 2D
                            # x = 29413.35
                            # Lx = 29506.15
                            # SMA = 29091.51      
                            # candle = 29502.7 - 29387.9
                            # candle = 114.8; RED

                            # 29388.0  29622.6  29388.0  29600.0
                            # HL = 29622.6 - 29388.0
                            # HL = 234.6
                            # 2D = 117.3
                            # x = 29388.0 + 117.3; LOW + 2D
                            # x = 29505.3
                            # Lx = 29388 ; 29505.3
                            # SMA = 29127.39    
                            # candle = 29388 - 29600
                            # candle = -212; GREEN
                                                        
                            # 29600.0  29840.0  29557.0  29790.4
                            # HL = 29840 - 29557
                            # HL = 283
                            # 2D = 141.5
                            # x = 29557 + 141.5; LOW + 2D
                            # x = 29698.5
                            # Lx = 29557 ; 29698.5
                            # SMA = 29091.51      
                            # candle = 29600 - 29790.4
                            # candle = -190.4; GREEN

                            #29790.4  29934.7  29700.1  29739.9
                            # HL = 29934.7 - 29700.1
                            # HL = 234.6
                            # 2D = 117.3
                            # x = 29700.1 + 117.3; LOW + 2D
                            # x = 29817.4
                            # Lx = 29700.1 ; 29817.4
                            # SMA = 29106.49
                            # candle = 29790.4 - 29739.9
                            # candle = 50.5; RED                            

                            # 29739.9  29776.8  29536.7  29607.0
                            # HL = 29776.8 - 29536.7
                            # HL = 240.1
                            # 2D = 120.05
                            # x = 29536.7 + 120.05; LOW + 2D
                            # x = 29656.75
                            # Lx = 29536.7 ; 29656.75; Compare LOW and x
                            # SMA = 29126.45    
                            # candle = 29502.7 - 29387.9
                            # candle = 114.8; RED




                            # Entry Price: 29900.0 ;Error
                            # Take Profit: 29900.0 



                            print("---RSI Disabled---")
                            entry_price = CreateOrder.get_rounded_price(pair, curPrice)
                            tp1 = high - close
                            tp2 = tp1 * 0.30
                            take_profit = round(close + tp2, 8)   
                            candle = open - close

                            if curPrice > sma and volume >= volume_set and candle < 0:
                                side = "BUY" 
                            elif curPrice < sma and volume >= volume_set and candle > 0:
                                side = "SELL"    

                        # if side != "NONE":
                        print("\nVolume: %(c)s \nHigh: %(a)s Close: %(b)s Current Price: %(d)s \nRSI: %(e)s SMA: %(f)s \nQTY: %(g)s \nSIDE: %(i)s \nEntry Price: %(k)s \nTake Profit: %(j)s \n" % 
                            {'a': close, 'b': high, 'c': volume, 'd': curPrice, 'e': rsi, 'f': sma, 'g': qty, 'i':side, 
                            'j':take_profit, 'k':entry_price})

                        # CreateOrder.futures_order(pair, qty, entry_price, side, order_type, take_profit, timeframe)
                        # print('------------futures_order------------')
                    
                    await client.close_connection()

                except: await client.close_connection()      
#=====================================================================================================================
                
    def get_data_frame(self, symbol, msg):
        global rows_count, df, volume, high, close

        df = pd.DataFrame(msg)
        df.columns = ['Time','Open', 'High', 'Low', 'Close', 'Volume','CloseTime', 'qav','num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
        df = df.loc[:, ['Time','Open', 'High', 'Low', 'Close', 'Volume']]
        df["Time"] = pd.to_datetime(df["Time"], unit='ms')
        df["Open"] = df["Open"].astype(float)
        df["High"] = df["High"].astype(float)
        df["Low"] = df["Low"].astype(float)
        df["Close"] = df["Close"].astype(float)
        df["Volume"] = df["Volume"].astype(float)

        rows_count = len(df.index)
        vv = df["Volume"]
        volume = round(vv[rows_count - 1])
        cc = df["Close"]
        close = cc[rows_count - 1]
        hh = df["High"]
        high = hh[rows_count - 1]   
        print(df)
        return df

#=====================================================================================================================
    def d_Candle(self):
        global open

        cc = df["Open"]
        rw = len(df.index)
        tt = str(cc[rw - 1])
        open = float(tt)
        # print(open)

    def d_RSI(self):
        global rsi, error_set

        rsi = talib.RSI(df["Close"])
        rw = len(df.index)
        tt = str(rsi[rw - 1])
        rsi = round(float(tt))

        if tt == "nan":
            print("\n RSI: ERROR deltatime adjust to a higher value\n")
            # db.put_dateErrorRSI(timeframe, pair)
            error_set = 1

#=====================================================================================================================

    def d_SMA(self):
        global curPrice, sma, error_set

        sma = talib.SMA(df['Close'])
        rw = len(df.index)
        tt = str(sma[rw - 1])
        sma = round(float(tt), 6)
        curPrice = df['Close'].iloc[-1]
        
        if tt == "nan":
            print("\n SMA: ERROR deltatime adjust to a higher value\n")
            # db.put_dateErrorSMA(timeframe, pair)
            error_set = 1   
            
#=====================================================================================================================

if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    pattern_detect = PatternDetect()
    asyncio.get_event_loop().run_until_complete(pattern_detect.main())
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))