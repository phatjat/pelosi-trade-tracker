import os
import requests
import time
from datetime import datetime
import streamlit as st
import pandas as pd
from requests_html import HTMLSession

# Define stock symbols to track (Pelosi trades, Most Actives, and Big 8)
PELOSI_TRADES_URL = "https://www.capitoltrades.com/trades?politician=P000197"
API_KEY = os.getenv("FMP_API_KEY")  # Load API key from environment variable
MOST_ACTIVE_URL = f"https://financialmodelingprep.com/api/v3/actives?apikey={API_KEY}"
BIG_8 = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "PLTR"]

# Function to scrape Pelosi trades using requests_html with sync rendering
def fetch_pelosi_trades():
    try:
        session = HTMLSession()
        response = session.get(PELOSI_TRADES_URL)

        # Use sync_render() instead of render() to avoid threading issues
        response.html.arender(timeout=30)

        trades = []
        trade_rows = response.html.find(".trade-list-item")

        for row in trade_rows:
            try:
                ticker = row.find(".ticker", first=True).text
                transaction = row.find(".transaction", first=True).text
                date = row.find(".date", first=True).text
                amount = row.find(".amount", first=True).text

                trades.append({
                    "Ticker": ticker,
                    "Transaction": transaction,
                    "Date": date,
                    "Amount": amount
                })
            except:
                continue

        return trades
    except Exception as e:
        st.error(f"Error fetching Pelosi trades: {e}")
        return []
