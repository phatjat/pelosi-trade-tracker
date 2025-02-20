import requests
import time
from datetime import datetime
import streamlit as st

# Define stock symbols to track (Pelosi trades, Most Actives, and Big 7)
PELOSI_TRADES_URL = "https://example.com/pelosi-trades"  # Placeholder for Pelosi trade data source
MOST_ACTIVE_URL = "https://example.com/most-active"  # Placeholder for most active stocks data
BIG_7 = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA"]

# Function to fetch Pelosi trades (mockup function, replace with actual API or web scraping logic)
def fetch_pelosi_trades():
    try:
        response = requests.get(PELOSI_TRADES_URL)
        return response.json()
    except Exception as e:
        st.error(f"Error fetching Pelosi trades: {e}")
        return []

# Function to fetch most active stocks
def fetch_most_active():
    try:
        response = requests.get(MOST_ACTIVE_URL)
        return response.json()
    except Exception as e:
        st.error(f"Error fetching most active stocks: {e}")
        return []

# Function to generate alerts
def generate_alerts(pelosi_trades, most_active):
    alerts = []
    
    # Check Pelosi trades against Big 7 and Most Active
    for trade in pelosi_trades:
        if trade['symbol'] in BIG_7:
            alerts.append(f"Pelosi traded {trade['symbol']} ({trade['action']}) on {trade['date']}")
        
        if trade['symbol'] in [stock['symbol'] for stock in most_active]:
            alerts.append(f"Pelosi traded {trade['symbol']} ({trade['action']}), which is among today's most active stocks")
    
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
