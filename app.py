import os
import requests
import time
from datetime import datetime
import streamlit as st
import pandas as pd
import asyncio
from pyppeteer import launch

# Define stock symbols to track (Pelosi trades, Most Actives, and Big 8)
PELOSI_TRADES_URL = "https://www.capitoltrades.com/trades?politician=P000197"
API_KEY = os.getenv("FMP_API_KEY")  # Load API key from environment variable
MOST_ACTIVE_URL = f"https://financialmodelingprep.com/api/v3/actives?apikey={API_KEY}"
BIG_8 = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "PLTR"]

# Function to scrape Pelosi trades using Pyppeteer
async def fetch_pelosi_trades():
    try:
        browser = await launch(headless=True)
        page = await browser.newPage()
        await page.goto(PELOSI_TRADES_URL, {"waitUntil": "networkidle2"})

        # Accept cookies if required
        accept_button = await page.querySelector("button:has-text('Accept All')")
        if accept_button:
            await accept_button.click()
            await page.waitForSelector(".trade-list-item")

        trades = []
        trade_rows = await page.querySelectorAll(".trade-list-item")

        for row in trade_rows:
            try:
                ticker = await (await row.querySelector(".ticker")).evaluate("node => node.innerText")
                transaction = await (await row.querySelector(".transaction")).evaluate("node => node.innerText")
                date = await (await row.querySelector(".date")).evaluate("node => node.innerText")
                amount = await (await row.querySelector(".amount")).evaluate("node => node.innerText")

                trades.append({
                    "Ticker": ticker,
                    "Transaction": transaction,
                    "Date": date,
                    "Amount": amount
                })
            except:
                continue

        await browser.close()
        return trades
    except Exception as e:
        st.error(f"Error fetching Pelosi trades: {e}")
        return []

# Wrapper function for Streamlit to call async Pyppeteer function
def get_pelosi_trades():
    return asyncio.run(fetch_pelosi_trades())

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
        pelosi_trades = get_pelosi_trades()
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
