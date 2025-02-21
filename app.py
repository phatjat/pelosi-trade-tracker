import os
import streamlit as st
import pandas as pd
import httpx
from bs4 import BeautifulSoup

# SEC Pelosi Insider Trading URL
SEC_PELSOI_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=Nancy+Pelosi&type=&dateb=&owner=include&count=100"

# Function to fetch Pelosi trades from SEC
def fetch_pelosi_trades():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = httpx.get(SEC_PELSOI_URL, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        trades = []

        trade_rows = soup.select("tr")  # Adjust selector based on SEC HTML structure

        for row in trade_rows:
            try:
                columns = row.find_all("td")
                ticker = columns[1].text.strip()
                transaction = columns[3].text.strip()
                date = columns[4].text.strip()
                amount = columns[5].text.strip()

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
