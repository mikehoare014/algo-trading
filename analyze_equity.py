import yfinance as yf
import pandas as pd

def analyze_stock(symbol, ax=None, positions=None):
    print(f"\nAnalyzing {symbol}...")

    end_date = pd.Timestamp.today().date().isoformat()
    start_date = (pd.Timestamp.today() - pd.Timedelta(days=1825)).date().isoformat()
    
    # Download and process data
    stock_data = yf.download(symbol, start=start_date, end=end_date, progress=False)
    if stock_data.empty:
        print(f"No data available for {symbol}")
        return None
        
    stock_data['sma_20'] = stock_data['Close'].rolling(window=20).mean()
    stock_data['sma_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['signal'] = 0

    buy_signals = (stock_data['sma_20'] > stock_data['sma_50']) & (stock_data['sma_20'].shift(1) <= stock_data['sma_50'].shift(1))
    sell_signals = (stock_data['sma_20'] < stock_data['sma_50']) & (stock_data['sma_20'].shift(1) >= stock_data['sma_50'].shift(1))
    stock_data.loc[buy_signals, 'signal'] = 1
    stock_data.loc[sell_signals, 'signal'] = -1

    latest_row = stock_data.iloc[[-1]]

    # Check if we have a position in this stock
    current_position = next((pos for pos in positions if pos['symbol'] == symbol), None)
    
    if latest_row['signal'].item() == 1:
        try:
            order = api.place_order(symbol, 10, "buy")
            print(f"Buy order executed for {symbol}:", order)
        except Exception as e:
            print(f"Error placing buy order for {symbol}:", str(e))
    elif latest_row['signal'].item() == -1 and current_position:
        # If we have a sell signal and own the stock, sell our position
        try:
            qty_to_sell = int(current_position['qty'])
            order = api.place_order(symbol, qty_to_sell, "sell")
            print(f"Sell order executed for {symbol} ({qty_to_sell} shares):", order)
        except Exception as e:
            print(f"Error placing sell order for {symbol}:", str(e))
    else:
        print(f"No trading signal for {symbol} on the latest date.")
    
    # Plot the data if an axis is provided
    if ax is not None:
        # Plot closing price and SMAs
        ax.plot(stock_data['Close'], label='Close Price', alpha=0.5)
        ax.plot(stock_data['sma_20'], label='20-day SMA', linestyle='--')
        ax.plot(stock_data['sma_50'], label='50-day SMA', linestyle='--')

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