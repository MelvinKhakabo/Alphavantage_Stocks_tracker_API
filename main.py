
# main.py

from retrieval.api_client import AlphaVantageClient
from utils.excel_writer import write_to_excel

def main():
    """Fetch stock data and export it to Excel."""
    client = AlphaVantageClient()
    symbol_data = client.get_all_symbols_data()
    
    if not symbol_data:
        print("No data fetched. Exiting.")
        return
    
    write_to_excel(symbol_data)
    print("Program completed successfully.")

if __name__ == "__main__":
    main()