import streamlit as st
import requests
import json

# Ticker symbols
tickers = ['AEE', 'REZ', '1AE', '1MC', 'NRZ']

# Function to fetch announcements using Requests
def fetch_announcements(ticker):
    url = f"https://www.asx.com.au/asx/1/company/{ticker}/announcements?count=20&market_sensitive=false"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError on bad response
        
        if 'application/json' in response.headers.get('Content-Type', ''):
            announcements = response.json().get('data', [])
            return announcements
        else:
            st.error(f"Unexpected response for {ticker}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch announcements for {ticker}: {str(e)}")
        return None

# Fetch all announcements
all_announcements = {ticker: fetch_announcements(ticker) for ticker in tickers}

# Streamlit UI
st.title("ASX Announcements Viewer")

# Dropdown to select ticker
selected_ticker = st.selectbox("Select a Ticker Symbol", tickers)

# Display announcements for the selected ticker
if selected_ticker:
    announcements = all_announcements.get(selected_ticker, [])
    if announcements:
        st.write(f"Recent announcements for {selected_ticker}:")
        for announcement in announcements:
            st.write(announcement['header'])  # Display the announcement header
    else:
        st.write(f"No announcements found for {selected_ticker}")

# Function to check for "Trading Halt"
def has_trading_halt(announcements):
    return any("Trading Halt" in announcement['header'] for announcement in announcements)

# Display tickers with "Trading Halt"
st.write("Tickers with a Trading Halt:")
for ticker, announcements in all_announcements.items():
    if announcements and has_trading_halt(announcements):
        st.write(ticker)
