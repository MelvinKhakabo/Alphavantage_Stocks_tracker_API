# utils/excel_writer.py

import os
import pandas as pd
from datetime import datetime
from config.settings import OUTPUT_DIR

def calculate_daily_change(prev_close, curr_close):
    """Calculate the percentage change between two closing prices."""
    if not prev_close or not curr_close:
        return 0.0
    return ((float(curr_close) - float(prev_close)) / float(prev_close)) * 100

def write_to_excel(data):
    """Write stock data to an Excel file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_rows = []
    
    for symbol, time_series in data.items():
        # Convert time series to list of daily data, sorted by date
        daily_data = [(date, values["4. close"]) for date, values in time_series.items()]
        daily_data.sort(key=lambda x: x[0])  # Sort by date
        
        if len(daily_data) < 2:
            print(f"Not enough data for {symbol} to calculate change.")
            continue
        
        # Use the last two days
        prev_date, prev_close = daily_data[-2]
        curr_date, curr_close = daily_data[-1]
        change_percent = calculate_daily_change(prev_close, curr_close)
        
        row = {
            "Date": curr_date,
            "Symbol": symbol,
            "Previous Close": prev_close,
            "Current Close": curr_close,
            "Change (%)": change_percent
        }
        all_rows.append(row)
    
    if not all_rows:
        print("No data to write to Excel.")
        return
    
    df = pd.DataFrame(all_rows)
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"stock_rates_{today}.xlsx"
    filepath = os.path.join(OUTPUT_DIR, filename)
    df.to_excel(filepath, index=False)
    print(f"Data written to {filepath}")