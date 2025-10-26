# %%

import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil
from alpacha import AlphcaAPI
from analyze_equity import analyze_stock

api_key = os.getenv("ALPACA_API_KEY")
api_secret = os.getenv("ALPACA_SECRET_KEY")

api = AlphcaAPI(api_key=api_key, api_secret=api_secret)

positions = api.get_positions()

# %%

print(api.show_positions(positions))

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

n_stocks = len(ticker_symbols)
n_cols = 2  # We'll use 2 columns
n_rows = ceil(n_stocks / n_cols)

plt.style.use('ggplot')
fig = plt.figure(figsize=(15, 5*n_rows))
fig.suptitle('Moving Average Crossover Strategy Analysis', fontsize=16, y=1.02)

for i, symbol in enumerate(ticker_symbols):
    ax = plt.subplot(n_rows, n_cols, i+1)
    analyze_stock(symbol, ax, positions)

plt.tight_layout()
plt.show()

# %%
