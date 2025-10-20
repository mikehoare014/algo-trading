# %%

import os
import yfinance as yf
import pandas as pd
from alpacha import AlphcaAPI

api_key = os.getenv("ALPACA_API_KEY")
api_secret = os.getenv("ALPACA_SECRET_KEY")

api = AlphcaAPI(api_key=api_key, api_secret=api_secret)

ticker_symbol = "AAPL"

print("Searching for buy signal for:", ticker_symbol)

end_date = pd.Timestamp.today().date().isoformat()
start_date = (pd.Timestamp.today() - pd.Timedelta(days=1825)).date().isoformat()

stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
stock_data['sma_50'] = stock_data['Close'].rolling(window=50).mean()
stock_data['sma_200'] = stock_data['Close'].rolling(window=200).mean()
stock_data['signal'] = 0

buy_signals = (stock_data['sma_50'] > stock_data['sma_200']) & (stock_data['sma_50'].shift(1) <= stock_data['sma_200'].shift(1))
sell_signals = (stock_data['sma_50'] < stock_data['sma_200']) & (stock_data['sma_50'].shift(1) >= stock_data['sma_200'].shift(1))
stock_data.loc[buy_signals, 'signal'] = 1
stock_data.loc[sell_signals, 'signal'] = -1

latest_row = stock_data.iloc[[-1]]

if latest_row['signal'].item() == 1:
    order = api.place_order(ticker_symbol, 10, "buy")
    print("Trade executed:", order)
else:
    print("No buy signal on the latest date.")

# %%
