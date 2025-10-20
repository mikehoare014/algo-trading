import os
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from alpacha import AlphcaAPI



# Get API credentials from environment variables
api = AlphcaAPI(
    api_key=os.environ.get("ALPACA_API_KEY"),
    api_secret=os.environ.get("ALPACA_API_SECRET")
)
account_info = api.get_account_info()

ticker_symbol = "AAPL"

end_date = pd.Timestamp.today().date().isoformat()
start_date = (pd.Timestamp.today() - pd.Timedelta(days=1825)).date().isoformat()

stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

print(stock_data.tail())

# Data Preprocessing
stock_data['sma_50'] = stock_data['Close'].rolling(window=50).mean()
stock_data['sma_200'] = stock_data['Close'].rolling(window=200).mean()

print(stock_data.tail())

# Generate buy/sell signals
stock_data['signal'] = 0
buy_signals = (stock_data['sma_50'] > stock_data['sma_200']) & (stock_data['sma_50'].shift(1) <= stock_data['sma_200'].shift(1))
stock_data.loc[buy_signals, 'signal'] = 1

sell_signals = (stock_data['sma_50'] < stock_data['sma_200']) & (stock_data['sma_50'].shift(1) >= stock_data['sma_200'].shift(1))
stock_data.loc[sell_signals, 'signal'] = -1

print(stock_data.tail())

position = 0
capital = 10000

for i in range(len(stock_data)):
    if stock_data['signal'].iloc[i] == 1 and position != 1:
        position = 1
        capital -= stock_data['Close'].iloc[i]
        print(f"Buy at {stock_data['Close'].iloc[i]} on {stock_data.index[i]}")

    elif stock_data['signal'].iloc[i] == -1 and position != -1:
        position = -1
        capital = position * stock_data['Close'].iloc[i]
        print(f"Sell at {stock_data['Close'].iloc[i]} on {stock_data.index[i]}")

latest_row = stock_data.iloc[[-1]]

if latest_row['signal'].item() == 1:
    order = api.place_order(ticker_symbol, 10, "buy")
    print("Trade executed:", order)
else:
    print("No buy signal on the latest date.")