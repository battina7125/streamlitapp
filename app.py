import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

# Set up ChromeDriver with options
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_service = Service('chromedriver.exe')  
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Ticker symbols
tickers = ['AEE', 'REZ', '1AE', '1MC', 'NRZ']

# Function to fetch announcements using Selenium
def fetch_announcements(ticker):
    url = f"https://www.asx.com.au/asx/1/company/{ticker}/announcements?count=20&market_sensitive=false"
    driver.get(url)
    time.sleep(3)  
    
    try:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        # Find the preformatted JSON data in the page source
        pre_tag = soup.find('pre')
        if pre_tag:
            json_data = pre_tag.text
            announcements = json.loads(json_data).get('data', [])
            return announcements
        else:
            st.error(f"Failed to find JSON for {ticker}")
            return None
    except Exception as e:
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

driver.quit()  
