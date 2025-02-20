import requests
import time
from datetime import datetime
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd

# Define stock symbols to track (Pelosi trades, Most Actives, and Big 8)
PELOSI_TRADES_URL = "https://www.capitoltrades.com/"
MOST_ACTIVE_URL = "https://financialmodelingprep.com/api/v3/actives?apikey=VhWsVJxcLWfqQ10v4h5r5HlfrpXGz3ek"
BIG_8 = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "PLTR"]

# Function to scrape Pelosi trades from CapitolTrades
def fetch_pelosi_trades():
    try:
        response = requests.get(PELOSI_TRADES_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        
        trades = []
        table = soup.find("table")  # Locate the table on the page
        if table:
            rows = table.find_all("tr")[1:]  # Skip header row
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 4:
                    trade_data = {
                        "Ticker": cols[0].text.strip(),
                        "Transaction": cols[1].text.strip(),
                        "Date": cols[2].text.strip(),
                        "Amount": cols[3].text.strip()
                    }
                    trades.append(trade_data)
        print("Scraped Pelosi Trades:", trades)  # Debugging print
        return trades
    except Exception as e:
        st.error(f"Error fetching Pelosi trades: {e}")
        return []

# Function to fetch most active stocks from Financial Modeling Prep API
def fetch_most_active():
    try:
        response = requests.get(MOST_ACTIVE_URL)
        print("Most Active API Response:", response.text)  # Debugging print
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching most active stocks: {e}")
        return []

# Function to generate alerts
def generate_alerts(pelosi_trades, most_active):
    alerts = []
    
    # Check Pelosi trades against Big 8 and Most Active
    for trade in pelosi_trades:
        symbol = trade.get('Ticker', '')
        action = trade.get('Transaction', 'Unknown')
        date = trade.get('Date', 'Unknown')
        
        if symbol in BIG_8:
            alerts.append(f"Pelosi traded {symbol} ({action}) on {date}")
        
        if symbol in [stock['ticker'] for stock in most_active]:
            alerts.append(f"Pelosi traded {symbol} ({action}), which is among today's most active stocks")
    
    return alerts

# Streamlit App Interface
def main():
    st.title("Pelosi Trade Tracker")
    st.write("Tracking Pelosi trades, most active stocks, and Big 8 companies")
    
    if st.button("Fetch Latest Data"):
        pelosi_trades = fetch_pelosi_trades()
        most_active = fetch_most_active()
        alerts = generate_alerts(pelosi_trades, most_active)
        
        # **Display Pelosi Portfolio**
        if pelosi_trades:
            st.subheader("Pelosi Portfolio")
            st.dataframe(pd.DataFrame(pelosi_trades))
        else:
            st.warning("No Pelosi trades found.")
        
        # **Display Most Active Stocks**
        if most_active:
            st.subheader("Most Active Stocks")
            st.dataframe(pd.DataFrame(most_active))
        else:
            st.warning("No most active stocks found.")
        
        # **Display Alerts**
        if alerts:
            for alert in alerts:
                st.warning(alert)
        else:
            st.success("No significant trade alerts at this time.")

if __name__ == "__main__":
    main()