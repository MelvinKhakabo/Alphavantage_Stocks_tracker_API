# Alpha Vantage Stock Tracker

## Overview
A Python application that fetches daily stock data for the top 10 tech companies from the Alpha Vantage API, calculates various metrics, and exports them to Excel.

## Features
- Fetches data for 10 tech companies: AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA, INTC, IBM, CSCO.
- Outputs:
  - `stock_summary_YYYY-MM-DD.xlsx`: Latest day's data with Open, High, Low, Close, Volume, Daily Range, Volatility, and Change (%).
  - `stock_trend_YYYY-MM-DD.xlsx`: 5-day closing price trend for each company.
  - Includes a simple analysis identifying the most volatile stock, biggest gainer, and biggest loser.
- Respects Alpha Vantage rate limits with a 12-second delay between requests.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Create a `.env` file with your Alpha Vantage API key:
 API_KEY=your_api_key_here
3. Activate virtual environment: `source venv/Scripts/activate`
4. Run: `python main.py`

## Structure
- `config/`: API settings.
- `data/`: Output files.
- `retrieval/`: API client.
- `utils/`: Data processing.

## Notes
- Free tier limit: 5 calls/minute, 25 calls/day (based on recent reports).
- Uses `LF` line endings in `.env` to ensure compatibility. 


