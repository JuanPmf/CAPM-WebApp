# Import libraries

import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as pdr
import datetime as dt

# To solve string indeces error
yf.pdr_override()

#Get NASDAQ tickers from local CSV
tickers = pd.read_csv('D:/Projects/CAMP-WebApp/NASDAQ.csv')

st.set_page_config(page_title = "CAPM",
    page_icon = "Chart_with:upwards_trend",
    layout = 'wide')

st.title("CAMP: Capital Asset Pricing Model")

# Getting input from user

col1, col2 = st.columns([1,1])

with col1:
    stocks_list = st.multiselect("Choose 4 stocks", (tickers['Symbol'].tolist()), ["TSLA"])
with col2:
    year = st.number_input("Number of Years", 1, 10)

# Downloading data from SP500

start = dt.date(dt.date.today().year-year, dt.date.today().month, dt.date.today().day)

end = dt.date.today()

sp500 = pdr.get_data_yahoo(stocks_list, start, end)

sp500

#Run from anaconda promt: streamlit run D:\Projects\CAMP-WebApp\CAPM_Return.py