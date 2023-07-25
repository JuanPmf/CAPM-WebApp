# Import libraries

import streamlit as st
import pandas as pd
import yfinance as yf
#from pandas_datareader import wb
import pandas_datareader.data as web
import datetime

st.set_page_config(page_title = "CAMP",
    page_icon = "Chart_with:upwards_trend",
    layout = 'wide')

#Run the app using terminal in the folder: py -m streamlit run CAMP_return.py

st.title("CAMP: Capital Asset Pricing Model")

# Getting input from user

col1, col2 = st.columns([1,1])

with col1:
    stocks_list = st.multiselect("Choose 4 stocks", ("TSLA","APPL", "NFLX", "MSFT", "MGM", "NVDA","GOOGL"), ["TSLA","APPL", "NFLX","GOOGL"])
with col2:
    year = st.number_input("Number of Years", 1, 10)


# Downloading data from SP500

end = datetime.date.today()

start = datetime.date(datetime.date.today().year-year, datetime.date.today().month, datetime.date.today().day)

SP500 = wb.DataReader(['sp500', 'fred', start, end])

print(SP500.head())
