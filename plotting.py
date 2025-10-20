# Plotting trading signals

# Plot closing price and SMAs
plt.figure(figsize=(14, 7))
plt.plot(stock_data['Close'], label='Close Price', alpha=0.5)
plt.plot(stock_data['sma_50'], label='50-day SMA', linestyle='--')
plt.plot(stock_data['sma_200'], label='200-day SMA', linestyle='--')

# Plot buy signals
plt.scatter(stock_data.index[stock_data['signal'] == 1], stock_data['Close'][stock_data['signal'] == 1], 
                label='Buy Signal', marker='^', color='green', s=100)

# Plot sell signals
plt.scatter(stock_data.index[stock_data['signal'] == -1], stock_data['Close'][stock_data['signal'] == -1], 
                label='Sell Signal', marker='v', color='red', s=100)

plt.title(f"{ticker_symbol} Moving Average Crossover Strategy")
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()