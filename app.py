import os
import requests
import time
from datetime import datetime
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import httpx

# Define stock symbols to track (Pelosi trades, Most Actives, and Big 8)
PELOSI_TRADES_URL = "https://www.capitoltrades.com/"
API_KEY = os.getenv("FMP_API_KEY")  # Load API key from environment variable
MOST_ACTIVE_URL = f"https://financialmodelingprep.com/api/v3/actives?apikey={API_KEY}"
BIG_8 = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "PLTR"]

# Function to scrape Pelosi trades from CapitolTrades using httpx and BeautifulSoup
def fetch_pelosi_trades():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = httpx.get(PELOSI_TRADES_URL, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        trades = []

        trade_rows = soup.select(".trade-list-item")  # Adjust selector as needed

        for row in trade_rows:
            try:
                politician = row.select_one(".politician-name").text.strip()
                if "Pelosi" not in politician:  # Filter only Pelosi trades
                    continue
                
                ticker = row.select_one(".ticker").text.strip()
                transaction = row.select_one(".transaction").text.strip()
                date = row.select_one(".date").text.strip()
                amount = row.select_one(".amount").text.strip()

                trades.append({
                    "Politician": politician,
                    "Ticker": ticker,
                    "Transaction": transaction,
                    "Date": date,
                    "Amount": amount
                })
            except:
                continue

        print("Fetched Pelosi Trades:", trades)  # Debugging
        return trades
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
        
        if pelosi_trades:
            st.subheader("Pelosi Portfolio")
            st.dataframe(pd.DataFrame(pelosi_trades))
        else:
            st.warning("No Pelosi trades found.")
        
        if most_active:
            st.subheader("Most Active Stocks")
            st.dataframe(pd.DataFrame(most_active))
        else:
            st.warning("No most active stocks found.")
        
        if alerts:
            for alert in alerts:
                st.warning(alert)
        else:
            st.success("No significant trade alerts at this time.")

if __name__ == "__main__":
    main()
