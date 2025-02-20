import requests
import time
from datetime import datetime
import streamlit as st

# Define stock symbols to track (Pelosi trades, Most Actives, and Big 8)
PELOSI_TRADES_URL = "https://housestockwatcher.com/api/transactions/pelosi"  # House Stock Watcher API for Pelosi trades
MOST_ACTIVE_URL = "https://financialmodelingprep.com/api/v3/actives?apikey=VhWsVJxcLWfqQ10v4h5r5HlfrpXGz3ek
BIG_8 = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "PLTR"]

# Function to fetch Pelosi trades from House Stock Watcher API
def fetch_pelosi_trades():
    try:
        response = requests.get(PELOSI_TRADES_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching Pelosi trades: {e}")
        return []

# Function to fetch most active stocks from Financial Modeling Prep API
def fetch_most_active():
    try:
        response = requests.get(MOST_ACTIVE_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching most active stocks: {e}")
        return []

# Function to generate alerts
def generate_alerts(pelosi_trades, most_active):
    alerts = []
    
    # Check Pelosi trades against Big 7 and Most Active
    for trade in pelosi_trades:
        symbol = trade.get('ticker', '')  # Adjusted key based on API response
        action = trade.get('transaction', 'Unknown')
        date = trade.get('transaction_date', 'Unknown')
        
        if symbol in BIG_7:
            alerts.append(f"Pelosi traded {symbol} ({action}) on {date}")
        
        if symbol in [stock['ticker'] for stock in most_active]:
            alerts.append(f"Pelosi traded {symbol} ({action}), which is among today's most active stocks")
    
    return alerts

# Streamlit App Interface
def main():
    st.title("Pelosi Trade Tracker")
    st.write("Tracking Pelosi trades, most active stocks, and Big 7 companies")
    
    if st.button("Fetch Latest Data"):
        pelosi_trades = fetch_pelosi_trades()
        most_active = fetch_most_active()
        alerts = generate_alerts(pelosi_trades, most_active)
        
        if alerts:
            for alert in alerts:
                st.warning(alert)
        else:
            st.success("No significant trade alerts at this time.")

if __name__ == "__main__":
    main()
