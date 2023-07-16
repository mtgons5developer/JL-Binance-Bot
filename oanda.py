import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.exceptions as ex
import pandas as pd
import numpy as np
import time

accountID = "YOUR_ACCOUNT_ID"
access_token = "YOUR_ACCESS_TOKEN"
api = oandapyV20.API(access_token=access_token, environment="practice")

def get_price_data(instrument, granularity, count):
    params = {
        "count": count,
        "granularity": granularity
    }
    r = instruments.InstrumentsCandles(instrument=instrument, params=params)
    data = api.request(r)["candles"]
    prices = pd.DataFrame(columns=["time", "open", "high", "low", "close"])
    for candle in data:
        prices = prices.append(pd.Series([
            candle["time"],
            candle["mid"]["o"],
            candle["mid"]["h"],
            candle["mid"]["l"],
            candle["mid"]["c"]
        ], index=["time", "open", "high", "low", "close"]), ignore_index=True)
    prices["time"] = pd.to_datetime(prices["time"])
    prices.set_index("time", inplace=True)
    prices = prices.astype(float)
    return prices

def get_current_price(instrument):
    params = {
        "instruments": instrument
    }
    r = accounts.AccountInstruments(accountID=accountID, params=params)
    data = api.request(r)["instruments"][0]
    return float(data["ask"])

def get_account_summary():
    r = accounts.AccountSummary(accountID)
    data = api.request(r)
    balance = float(data["account"]["balance"])
    return balance

def place_order(units, instrument, take_profit, stop_loss, order_type):
    data = {
        "order": {
            "units": str(units),
            "instrument": instrument,
            "timeInForce": "FOK",
            "type": order_type,
            "positionFill": "DEFAULT",
            "takeProfitOnFill": {
                "price": str(take_profit)
            },
            "stopLossOnFill": {
                "price": str(stop_loss)
            }
        }
    }
    r = orders.OrderCreate(accountID, data=data)
    api.request(r)

def close_trade(trade_id):
    r = trades.TradeClose(accountID, tradeID=trade_id)
    api.request(r)

def get_open_trades():
    r = trades.OpenTrades(accountID)
    data = api.request(r)["trades"]
    trades_list = []
    for trade in data:
        trades_list.append(trade["id"])
    return trades_list

def get_positions():
    r = positions.OpenPositions(accountID)
    data = api.request(r)["positions"]
    return data

def get_balance():
    r = accounts.AccountSummary(accountID)
    data = api.request(r)["account"]
    balance = float(data["balance"])
    return balance

def main():
    instrument = "EUR_USD"
    granularity = "M5"
    count = 50
    units = 10000
    take_profit = 1.01
    stop_loss = 0.99
    order_type = "MARKET"
    
    while True:
        try:
            prices = get_price_data(instrument, granularity, count)
            current_price = get_current_price(instrument)
