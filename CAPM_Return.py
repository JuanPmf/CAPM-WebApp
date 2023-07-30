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

# Downloading NASDAQCOMP data from https://fred.stlouisfed.org/series/NASDAQCOM

url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=718&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=NASDAQCOM&scale=left&cosd=2018-07-27&coed=2023-07-27&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily%2C%20Close&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2023-07-30&revision_date=2023-07-30&nd=1971-02-05'
nasdaq = pd.read_csv(url)
nasdaq.columns = ['Date', 'NSDQ']
nasdaq['Date'] = nasdaq['Date'].astype('datetime64[ns]')
nasdaq['Date'] = nasdaq['Date'].apply(lambda x:str(x)[:10])
nasdaq['Date'] = pd.to_datetime(nasdaq['Date'])
nasdaq['NSDQ'] = pd.to_numeric(nasdaq['NSDQ'], errors= 'coerce')

# Getting stocks data from yahoo finance
stocks_df = pd.DataFrame()

for stock in stocks_list:
    data = yf.download(stock, period= f'{year}y')
    stocks_df[f'{stock}'] = data['Close']
print(stocks_df.dtypes)


stocks_df.reset_index(inplace= True)
stocks_df['Date'] = stocks_df['Date'].astype('datetime64[ns]')
stocks_df['Date'] = stocks_df['Date'].apply(lambda x:str(x)[:10])
stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])

# Mergin NASDAQ and Stocks data
stocks_df = pd.merge(stocks_df, nasdaq, on= 'Date', how = 'inner')

stocks_df

#Run from anaconda promt: streamlit run D:\Projects\CAMP-WebApp\CAPM_Return.py