import os
import streamlit as st
import pandas as pd
import httpx
from bs4 import BeautifulSoup

# Define stock symbols to track (Pelosi trades, Most Actives, and Big 8)
PELOSI_TRADES_URL = "https://www.capitoltrades.com/trades?politician=P000197"
API_KEY = os.getenv("FMP_API_KEY")
MOST_ACTIVE_URL = f"https://financialmodelingprep.com/api/v3/actives?apikey={API_KEY}"
BIG_8 = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "PLTR"]

# Function to scrape Pelosi trades using httpx + BeautifulSoup
def fetch_pelosi_trades():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.capitoltrades.com",
            "Origin": "https://www.capitoltrades.com",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "DNT": "1",
            "Connection": "keep-alive"
        }

        session = httpx.Client()

        # Step 1: Visit the homepage to establish session cookies
        session.get("https://www.capitoltrades.com", headers=headers)

        # Step 2: Fetch Pelosi's trades using session cookies
        response = session.get(PELOSI_TRADES_URL, headers=headers, cookies=session.cookies)

        # Debugging: Print response details
        print("Response Status:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Text (first 500 chars):", response.text[:500])

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        trades = []

        trade_rows = soup.select(".trade-list-item")  # Verify selector

        for row in trade_rows:
            try:
                ticker = row.select_one(".ticker").text.strip()
                transaction = row.select_one(".transaction").text.strip()
                date = row.select_one(".date").text.strip()
                amount = row.select_one(".amount").text.strip()

                trades.append({
                    "Ticker": ticker,
                    "Transaction": transaction,
                    "Date": date,
                    "Amount": amount
                })
            except:
                continue

        print("Fetched Pelosi Trades:", trades)
        return trades
    except Exception as e:
        st.error(f"Error fetching Pelosi trades: {e}")
        return []
