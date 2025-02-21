import os
import requests
import time
from datetime import datetime
import streamlit as st
import pandas as pd
from playwright.sync_api import sync_playwright
import subprocess

# Ensure Playwright browsers are installed
subprocess.run(["playwright", "install"], check=True)

# Define stock symbols to track (Pelosi trades, Most Actives, and Big 8)
PELOSI_TRADES_URL = "https://www.capitoltrades.com/trades?politician=P000197"
API_KEY = os.getenv("FMP_API_KEY")  # Load API key from environment variable
MOST_ACTIVE_URL = f"https://financialmodelingprep.com/api/v3/actives?apikey={API_KEY}"
BIG_8 = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "PLTR"]

# Function to scrape Pelosi trades using Playwright
def fetch_pelosi_trades():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(PELOSI_TRADES_URL)
            
            # Wait for the page to load completely
            page.wait_for_load_state("networkidle")
            
            # Accept cookies if required
            accept_button = page.query_selector("button:has-text('Accept All')")
            if accept_button:
                accept_button.click()
                page.wait_for_load_state("networkidle")

            trades = []
            trade_rows = page.query_selector_all(".trade-list-item")
            
            for row in trade_rows:
                try:
                    ticker = row.query_selector(".ticker").inner_text()
                    transaction = row.query_selector(".transaction").inner_text()
                    date = row.query_selector(".date").inner_text()
                    amount = row.query_selector(".amount").inner_text()
                    
                    trades.append({
                        "Ticker": ticker,
                        "Transaction": transaction,
                        "Date": date,
                        "Amount": amount
                    })
                except:
                    continue
            
            browser.close()
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
