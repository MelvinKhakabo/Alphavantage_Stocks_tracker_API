# utils/excel_writer.py

import os
import pandas as pd
from datetime import datetime
from config.settings import OUTPUT_DIR

def calculate_daily_range(high, low):
    """Calculate the daily price range (high - low)."""
    return float(high) - float(low)

def calculate_volatility(daily_range, close):
    """Calculate a simple volatility metric (daily range as % of close)."""
    return (daily_range / float(close)) * 100 if float(close) != 0 else 0.0

def calculate_change_percent(prev_close, curr_close):
    """Calculate the percentage change between two closing prices."""
    if not prev_close or not curr_close:
        return 0.0
    return ((float(curr_close) - float(prev_close)) / float(prev_close)) * 100

def write_to_excel(data):
    """Write stock data to two Excel files: summary and trend."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Summary data (most recent day)
    summary_rows = []
    # Trend data (last 5 days of closing prices)
    trend_data = {symbol: [] for symbol in data.keys()}
    
    for symbol, time_series in data.items():
        # Ensure we have at least 2 days for change calculation
        if not time_series or len(time_series) < 2:
            print(f"Not enough data for {symbol} to calculate metrics.")
            continue
        
        # Sort dates (most recent first)
        sorted_dates = sorted(time_series.keys(), reverse=True)
        
        # Summary for the most recent day
        latest_date = sorted_dates[0]
        latest_data = time_series[latest_date]
        prev_date = sorted_dates[1]
        prev_close = time_series[prev_date]["4. close"]
        
        open_price = latest_data["1. open"]
        high_price = latest_data["2. high"]
        low_price = latest_data["3. low"]
        close_price = latest_data["4. close"]
        volume = latest_data["5. volume"]
        
        daily_range = calculate_daily_range(high_price, low_price)
        volatility = calculate_volatility(daily_range, close_price)
        change_percent = calculate_change_percent(prev_close, close_price)
        
        summary_rows.append({
            "Date": latest_date,
            "Symbol": symbol,
            "Open": float(open_price),
            "High": float(high_price),
            "Low": float(low_price),
            "Close": float(close_price),
            "Volume": int(volume),
            "Daily Range": round(daily_range, 2),
            "Volatility (%)": round(volatility, 2),
            "Change (%)": round(change_percent, 2)
        })
        
        # Trend data for the last 5 days
        for date in sorted_dates:
            trend_data[symbol].append({
                "Date": date,
                "Close": float(time_series[date]["4. close"])
            })
    
    # Write summary file
    if summary_rows:
        summary_df = pd.DataFrame(summary_rows)
        today = datetime.now().strftime('%Y-%m-%d')
        summary_filename = f"stock_summary_{today}.xlsx"
        summary_filepath = os.path.join(OUTPUT_DIR, summary_filename)
        summary_df.to_excel(summary_filepath, index=False)
        print(f"Summary data written to {summary_filepath}")
    else:
        print("No summary data to write to Excel.")
    
    # Write trend file
    if trend_data:
        # Create a DataFrame for each symbol's trend
        trend_rows = []
        for symbol, days in trend_data.items():
            for day in days:
                trend_rows.append({
                    "Symbol": symbol,
                    "Date": day["Date"],
                    "Close": day["Close"]
                })
        trend_df = pd.DataFrame(trend_rows)
        # Pivot to have dates as columns
        trend_pivot = trend_df.pivot(index="Symbol", columns="Date", values="Close")
        trend_filename = f"stock_trend_{today}.xlsx"
        trend_filepath = os.path.join(OUTPUT_DIR, trend_filename)
        trend_pivot.to_excel(trend_filepath)
        print(f"Trend data written to {trend_filepath}")
    else:
        print("No trend data to write to Excel.")