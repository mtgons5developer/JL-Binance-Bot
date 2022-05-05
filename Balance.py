import config

from binance.client import Client

client = Client(config.BINANCE_API_KEY,config.BINANCE_SECRET_KEY)
print("Logged in")

acc_balance = client.futures_account_balance()

for check_balance in acc_balance:
    if check_balance["asset"] == "USDT":
        usdt_balance = check_balance["balance"]
        print(usdt_balance)

pair = 'BTCUSDT'
order = 47003526132
# result = client.futures_get_order(symbol=pair,orderId=order)
# info = client.get_account()

# df = pd.DataFrame(info["balances"])
# df["free"] = df["free"].astype(float).round(4)
# df = df[df["free"] > 0]
# print(df)