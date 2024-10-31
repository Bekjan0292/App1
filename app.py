import streamlit as st
import datetime
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# Set up your web app
st.set_page_config(layout="wide", page_title="Stock Info WebApp")

# Sidebar
st.sidebar.title("Input Ticker")
symbol = st.sidebar.text_input('Please enter the stock symbol:', 'NVDA').upper()

# Date input for historical data
col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date', value=datetime.date(2024, 1, 1))
with col2:
    edate = st.date_input('End Date', value=datetime.date.today())

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
    
    # Create a DataFrame for stock information
    stock_data = {
        "Metric": [
            "Previous Close",
            "Open",
            "Day Range",
            "Year Range",
            "Market Cap",
            "Avg Volume",
            "P/E Ratio",
            "Dividend Yield",
            "Primary Exchange"
        ],
        "Value": [
            f"${stock.info.get('previousClose', 'N/A')}",
            f"${stock.info.get('open', 'N/A')}",
            f"${stock.info.get('dayLow', 'N/A')} - ${stock.info.get('dayHigh', 'N/A')}",
            f"${stock.info.get('fiftyTwoWeekLow', 'N/A')} - ${stock.info.get('fiftyTwoWeekHigh', 'N/A')}",
            f"{stock.info.get('marketCap', 'N/A')} USD",
            f"{stock.info.get('averageVolume', 'N/A')}",
            f"{stock.info.get('trailingPE', 'N/A')}",
            f"{stock.info.get('dividendYield', 'N/A')}",
            stock.info.get('primaryExchange', 'N/A')
        ]
    }
    
    # Create a DataFrame and display it
    df = pd.DataFrame(stock_data)
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
