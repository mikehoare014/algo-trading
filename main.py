# %%

import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil
from alpacha import AlphcaAPI

api_key = os.getenv("ALPACA_API_KEY")
api_secret = os.getenv("ALPACA_SECRET_KEY")

api = AlphcaAPI(api_key=api_key, api_secret=api_secret)

# List of stocks to analyze
ticker_symbols = [
    'NVDA', 'AAPL', 'MSFT', 'GOOG', 'GOOGL',
    'AMZN', 'META', 'AVGO', 'TSLA', 'BRK.B',
    'WMT', 'JPM', 'ORCL', 'LLY', 'V',
    'NFLX', 'MA', 'XOM', 'JNJ', 'PLTR',
    'COST', 'ABBV', 'HD', 'AMD', 'BAC',
    'PG', 'UNH', 'GE', 'CVX', 'KO',
    'CSCO', 'WFC', 'IBM', 'TMUS', 'MS',
    'CRM', 'CAT', 'AXP', 'GS', 'PM',
    'RTX', 'MU', 'ABT', 'MCD', 'MRK',
    'LIN', 'TMO', 'PEP', 'DIS', 'BX'
]
print("Starting analysis for multiple stocks...")

end_date = pd.Timestamp.today().date().isoformat()
start_date = (pd.Timestamp.today() - pd.Timedelta(days=1825)).date().isoformat()

def analyze_stock(symbol, ax=None):
    print(f"\nAnalyzing {symbol}...")
    
    # Download and process data
    stock_data = yf.download(symbol, start=start_date, end=end_date, progress=False)
    if stock_data.empty:
        print(f"No data available for {symbol}")
        return None
        
    stock_data['sma_50'] = stock_data['Close'].rolling(window=20).mean()
    stock_data['sma_200'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['signal'] = 0

    buy_signals = (stock_data['sma_50'] > stock_data['sma_200']) & (stock_data['sma_50'].shift(1) <= stock_data['sma_200'].shift(1))
    sell_signals = (stock_data['sma_50'] < stock_data['sma_200']) & (stock_data['sma_50'].shift(1) >= stock_data['sma_200'].shift(1))
    stock_data.loc[buy_signals, 'signal'] = 1
    stock_data.loc[sell_signals, 'signal'] = -1

    latest_row = stock_data.iloc[[-1]]

    if latest_row['signal'].item() == 1:
        try:
            order = api.place_order(symbol, 10, "buy")
            print(f"Trade executed for {symbol}:", order)
        except Exception as e:
            print(f"Error placing order for {symbol}:", str(e))
    else:
        print(f"No buy signal for {symbol} on the latest date.")
    
    # Plot the data if an axis is provided
    if ax is not None:
        # Plot closing price and SMAs
        ax.plot(stock_data['Close'], label='Close Price', alpha=0.5)
        ax.plot(stock_data['sma_50'], label='50-day SMA', linestyle='--')
        ax.plot(stock_data['sma_200'], label='200-day SMA', linestyle='--')

        # Plot buy signals
        ax.scatter(stock_data.index[stock_data['signal'] == 1], 
                  stock_data['Close'][stock_data['signal'] == 1],
                  label='Buy Signal', marker='^', color='green', s=100)

        # Plot sell signals
        ax.scatter(stock_data.index[stock_data['signal'] == -1],
                  stock_data['Close'][stock_data['signal'] == -1],
                  label='Sell Signal', marker='v', color='red', s=100)

        ax.set_title(f"{symbol} Moving Average Crossover Strategy")
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        ax.tick_params(axis='x', rotation=45)
    
    return stock_data

# Create a grid of subplots
n_stocks = len(ticker_symbols)
n_cols = 2  # We'll use 2 columns
n_rows = ceil(n_stocks / n_cols)

plt.style.use('ggplot')
fig = plt.figure(figsize=(15, 5*n_rows))
fig.suptitle('Moving Average Crossover Strategy Analysis', fontsize=16, y=1.02)

# Process each stock in the list and create its plot
for i, symbol in enumerate(ticker_symbols):
    ax = plt.subplot(n_rows, n_cols, i+1)
    analyze_stock(symbol, ax)

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()

# %%
