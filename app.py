import streamlit as st
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objs as go
import yfinance as yf

# Set up web app configuration
st.set_page_config(layout="wide", page_title="Stock Analysis WebApp")

# Sidebar Inputs
st.sidebar.title("Input Ticker")
symbol = st.sidebar.text_input('Please enter the stock symbol:', 'NVDA').upper()
col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date', value=datetime.date(2024,1,1))
with col2:
    edate = st.date_input('End Date', value=datetime.date.today())

st.title(f"{symbol}")

# Fetch stock data
stock = yf.Ticker(symbol)
try:
    st.write(f"**Sector:** {stock.info.get('sector', 'N/A')}")
    st.write(f"**Beta:** {stock.info.get('beta', 'N/A')}")
    st.write(f"**P/E Ratio:** {stock.info.get('trailingPE', 'N/A')}")
    st.write(f"**P/B Ratio:** {stock.info.get('priceToBook', 'N/A')}")
    st.write(f"**Return on Equity (ROE):** {stock.info.get('returnOnEquity', 'N/A') * 100:.2f}%")
except KeyError:
    st.error("Failed to retrieve company financial data.")

# Fetch historical stock price data
data = yf.download(symbol, start=sdate, end=edate)

# Plot Close Price
if not data.empty:
    st.line_chart(data['Close'], x_label="Date", y_label="Close, USD")

    # Candlestick Chart
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])
    fig.update_layout(title=f"{symbol} Japanese Candlestick Chart", xaxis_title="Date", yaxis_title="Price (USD)")
    st.plotly_chart(fig)

    # Display Moving Averages
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    st.line_chart(data[['Close', 'MA20', 'MA50']])
else:
    st.error("Failed to fetch historical data.")
