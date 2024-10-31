import streamlit as st
import datetime
import plotly.graph_objs as go
import pandas as pd
import yfinance as yf

st.set_page_config(layout="wide", page_title="Risk&Return")

st.sidebar.title("Input Ticker")
symbol = st.sidebar.text_input('Please enter the stock symbol: ', 'NVDA').upper()

col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date', value=datetime.date(2024, 1, 1))
with col2:
    edate = st.date_input('End Date', value=datetime.date.today())

st.title(f"{symbol}")

stock = yf.Ticker(symbol)
if stock is not None:
    # Display company's basics
    st.write(f"# Sector: {stock.info.get('sector', 'N/A')}")
    st.write(f"# Company Beta: {stock.info.get('beta', 'N/A')}")
else:
    st.error("Failed to fetch historical data.")

data = yf.download(symbol, start=sdate, end=edate)
if not data.empty:
    # Create a candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                          open=data['Open'],
                                          high=data['High'],
                                          low=data['Low'],
                                          close=data['Close'])])

    fig.update_layout(title=f'{symbol} Candlestick Chart',
                      xaxis_title='Date',
                      yaxis_title='Price (USD)',
                      xaxis_rangeslider_visible=False)

    st.plotly_chart(fig)
else:
    st.error("Failed to fetch historical data.")
