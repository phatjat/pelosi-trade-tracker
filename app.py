import os
import requests
import streamlit as st
import pandas as pd
import httpx
from bs4 import BeautifulSoup

# OpenInsider Pelosi Trade URL
OPENINSIDER_URL = "https://www.openinsider.com/screener?s=pelosi"

# Function to fetch Pelosi trades from OpenInsider
def fetch_pelosi_trades():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = httpx.get(OPENINSIDER_URL, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        trades = []

        trade_rows = soup.select("tr[onmouseover]")  # Find table rows

        for row in trade_rows:
            try:
                columns = row.find_all("td")
                ticker = columns[2].text.strip()
                transaction = columns[6].text.strip()
                date = columns[3].text.strip()
                amount = columns[8].text.strip()

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
