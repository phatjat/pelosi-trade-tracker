import os
import streamlit as st
import pandas as pd
import httpx

# GovTrack API URL for Politician Trades
GOVTRACK_API_URL = "https://api.govtrack.us/v2/trades?politician=Nancy+Pelosi"

# Function to fetch Pelosi trades using GovTrack API
def fetch_pelosi_trades():
    try:
        response = httpx.get(GOVTRACK_API_URL)

        if response.status_code != 200:
            st.error(f"API error: {response.status_code}")
            return []

        data = response.json()
        trades = [
            {
                "Ticker": trade["ticker"],
                "Transaction": trade["transactionType"],
                "Date": trade["transactionDate"],
                "Amount": trade["value"]
            }
            for trade in data["results"]
        ]

        return trades
    except Exception as e:
        st.error(f"Error fetching Pelosi trades: {e}")
        return []
