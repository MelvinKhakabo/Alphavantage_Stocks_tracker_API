
# config/settings.py

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Alpha Vantage API settings
BASE_URL = "https://www.alphavantage.co/query"
SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "INTC", "IBM", "CSCO"]
FUNCTION = "TIME_SERIES_DAILY"  # Daily time series
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY must be set in .env")

# Data output settings
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed")