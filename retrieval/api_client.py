# retrieval/api_client.py

import requests
import time
from config.settings import BASE_URL, SYMBOLS, FUNCTION, API_KEY

class AlphaVantageClient:
    """A client for interacting with the Alpha Vantage API."""
    
    def __init__(self):
        if not API_KEY:
            raise ValueError("API key is missing")
        self.api_key = API_KEY
    
    def fetch_stock_data(self, symbol):
        """Fetch daily time series data for a given stock symbol."""
        params = {
            "function": FUNCTION,
            "symbol": symbol,
            "apikey": self.api_key,
            "datatype": "json"
        }
        
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            if "Error Message" in data or "Note" in data:
                print(f"Error for {symbol}: {data.get('Error Message', data.get('Note'))}")
                return None
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
    
    def get_all_symbols_data(self):
        """Fetch data for all symbols with a delay to respect rate limits."""
        all_data = {}
        for symbol in SYMBOLS:
            data = self.fetch_stock_data(symbol)
            if data and "Time Series (Daily)" in data:
                # Get the last 5 days of data
                time_series = data["Time Series (Daily)"]
                # Sort dates and take the most recent 5
                sorted_dates = sorted(time_series.keys(), reverse=True)[:5]
                all_data[symbol] = {date: time_series[date] for date in sorted_dates}
            time.sleep(12)  # Delay ~12 seconds to stay under 5 calls/minute
        return all_data

if __name__ == "__main__":
    client = AlphaVantageClient()
    data = client.get_all_symbols_data()
    for symbol, time_series in data.items():
        print(f"{symbol}: {list(time_series.keys())}")