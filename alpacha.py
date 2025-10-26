# %% 

import requests
import pprint

class AlphcaAPI:
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://paper-api.alpaca.markets/v2"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret
        }

    def get_account_info(self):
        url = f"{self.base_url}/account"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_market_data(self, symbol: str):
        url = f"https://data.alpaca.markets/v2/stocks/{symbol}/bars?timeframe=1Day&limit=5"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def place_order(self, symbol: str, qty: int, side: str, order_type: str = "market", time_in_force: str = "day"):
        url = f"{self.base_url}/orders"
        data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": order_type,
        "time_in_force": time_in_force
    }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_positions(self):
        """Get all open positions in the account."""
        url = f"{self.base_url}/positions"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def show_positions(self, positions):
        for position in positions:
            print(f"{position['symbol']}: {position['qty']} shares")

    
# %%
