# Import libraries

import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as pdr
import datetime as dt
import CAPM_Functions
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
    stocks_list = st.multiselect("Choose the stocks", (tickers['Symbol'].tolist()), ["TSLA"])
with col2:
    year = st.number_input("Number of Years", 1, 5)

# Downloading S&P500 data from https://fred.stlouisfed.org/series/SP500

url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=SP500&scale=left&cosd=2018-08-14&coed=2023-08-14&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily%2C%20Close&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2023-08-15&revision_date=2023-08-15&nd=2013-08-15'
sp500 = pd.read_csv(url)
sp500.columns = ['Date', 'S&P500']
sp500['Date'] = sp500['Date'].astype('datetime64[ns]')
sp500['Date'] = sp500['Date'].apply(lambda x:str(x)[:10])
sp500['Date'] = pd.to_datetime(sp500['Date'])
sp500['S&P500'] = pd.to_numeric(sp500['S&P500'], errors= 'coerce')

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

# Mergin S&P500 and Stocks data
stocks_df = pd.merge(stocks_df, sp500, on= 'Date', how = 'inner')

# Split head and tail in 2 columns

col1, col2 = st.columns([1,1])
with col1:
    st.markdown("### Dataframe Head")
    st.dataframe(stocks_df.head(), use_container_width= True)
with col2:
    st.markdown("### Dataframe Tail")
    st.dataframe(stocks_df.tail(), use_container_width= True)

# Plot stocks.
col1, col2 = st.columns([1,1])
with col1:
    st.markdown("### Price of Selected Stocks")
    st.plotly_chart(CAPM_Functions.interactive_plot(stocks_df))
# Plot stocks after normalization
with col2:
    #print(CAPM_Functions.normalize(stocks_df)) Normalizing function
    st.markdown("### Price After Normalization")
    st.plotly_chart(CAPM_Functions.interactive_plot(CAPM_Functions.normalize(stocks_df)))

# Daily return

stocks_daily_return = CAPM_Functions.daily_return(stocks_df)
print(stocks_daily_return.head())

beta={}
alpha={}

for i in stocks_daily_return.columns:
    if i !='Date' and i != 'S&P500':
        b, a = CAPM_Functions.calculate_beta(stocks_daily_return, i)

        beta[i] = b
        alpha[i] = a
print(beta, alpha)

beta_df = pd.DataFrame(columns= ['Stock', 'Beta Value'])
beta_df['Stock']=beta.keys()
beta_df['Beta Value']= [str(round(i,2)) for i in beta.values()]

with col1:
    st.markdown('### Calculated Beta Value')
    st.dataframe(beta_df, use_container_width= True)

rf = 0
rm = stocks_daily_return['S&P500'].mean()*252

return_df = pd.DataFrame()
return_value = []
for stock, value in beta.items():
    return_value.append(str(round(rf+(value*(rm+rf)),2)))

return_df['Stock'] = stocks_list

return_df['Return Value'] = return_value

with col2:
    st.markdown('### Calculated Return Using CAPM')
    st.dataframe(return_df, use_container_width=True)


#Run from anaconda promt: streamlit run D:\Projects\CAMP-WebApp\CAPM_Return.py