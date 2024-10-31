import streamlit as st
import datetime
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# Set up your web app
st.set_page_config(layout="wide", page_title="Stock Info WebApp")

# Sidebar for stock input
st.sidebar.title("Input Ticker")
symbol = st.sidebar.text_input('Please enter the stock symbol:', 'NVDA').upper()

# Date input for historical data
col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date', value=datetime.date(2024, 1, 1))
with col2:
    edate = st.date_input('End Date', value=datetime.date.today())

# Sidebar options for metrics selection
st.sidebar.header("Select Metrics")
metrics_options = {
    "Previous Close": "previousClose",
    "Open": "open",
    "Day Range": "dayRange",
    "Year Range": "yearRange",
    "Market Cap": "marketCap",
    "Avg Volume": "averageVolume",
    "P/E Ratio": "trailingPE",
    "Dividend Yield": "dividendYield",
    "Primary Exchange": "primaryExchange"
}
selected_metrics = st.sidebar.multiselect("Choose metrics to display:", list(metrics_options.keys()), default=list(metrics_options.keys()))

# Display the symbol title
st.title(f"{symbol} Stock Information")

# Fetch the stock data
stock = yf.Ticker(symbol)

# Check if the stock information is available
if stock.info:
    # Display company sector and beta
    st.subheader("Company Overview")
    st.write(f"**Sector:** {stock.info.get('sector', 'N/A')}")
    st.write(f"**Company Beta:** {stock.info.get('beta', 'N/A')}")

    # Create a DataFrame for selected stock information
    stock_data = {metric: stock.info.get(metrics_options[metric], 'N/A') for metric in selected_metrics}

    # Create a DataFrame and display it
    df = pd.DataFrame(stock_data.items(), columns=['Metric', 'Value'])
    st.table(df)

    # Download historical data for the specified date range
    data = yf.download(symbol, start=sdate, end=edate)
    if not data.empty:
        # Display closing price line chart
        st.subheader("Stock Price Over Time")
        st.line_chart(data['Close'])

        # Create a candlestick chart for more detailed information
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                                              open=data['Open'],
                                              high=data['High'],
                                              low=data['Low'],
                                              close=data['Close'])])
        fig.update_layout(title=f'{symbol} Candlestick Chart', xaxis_title='Date', yaxis_title='Price (USD)')
        st.plotly_chart(fig)

        # Display additional metrics
        st.subheader("Additional Metrics")
        st.write(f"**Volume:** {data['Volume'].sum()} over the selected period")
        st.write(f"**Average Closing Price:** ${data['Close'].mean():.2f}")
    else:
        st.error("Failed to fetch historical data.")
else:
    st.error("Failed to fetch stock information.")

st.sidebar.info("Enter a stock symbol to fetch its information and historical data. Adjust the date range to see specific performance.")
