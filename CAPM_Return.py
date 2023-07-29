# Import libraries

import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as pdr
import datetime as dt


st.set_page_config(page_title = "CAPM",
    page_icon = "Chart_with:upwards_trend",
    layout = 'wide')

#Run the app using terminal in the folder: py -m streamlit run CAMP_return.py

st.title("CAMP: Capital Asset Pricing Model")

# Getting input from user

col1, col2 = st.columns([1,1])

with col1:
    stocks_list = st.multiselect("Choose 4 stocks", ("TSLA","APPL", "NFLX", "MSFT", "MGM", "NVDA","GOOGL"), ["TSLA","APPL", "NFLX"])
with col2:
    year = st.number_input("Number of Years", 1, 10)

# Downloading data from SP500

start = dt.date(dt.date.today().year-year, dt.date.today().month, dt.date.today().day)

end = dt.date.today()

sp500 = pdr.get_data_yahoo(stocks_list, start, end)

sp500
