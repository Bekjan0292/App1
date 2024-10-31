import streamlit as st
import datetime
import yfinance as yf
import pandas as pd
import plotly.express as px

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
    else:
        st.error("Failed to fetch historical data.")

    # Fetch and display quarterly financial data
    st.subheader("Quarterly Financial Data")
    quarterly_data = stock.quarterly_financials
    if not quarterly_data.empty:
        # Transpose and format the quarterly data
        quarterly_data = quarterly_data.transpose()
        quarterly_data.reset_index(inplace=True)
        quarterly_data.columns = ['Quarter'] + list(quarterly_data.columns[1:])  # Rename columns

        # Display quarterly financial data as a table
        st.write(quarterly_data)

        # Create a bar chart for Revenue and Net Income
        fig = px.bar(quarterly_data, x='Quarter', y=['Revenue', 'Net Income'], 
                     title='Quarterly Revenue and Net Income',
                     labels={'value': 'Amount (in millions)', 'variable': 'Metrics'},
                     barmode='group')
        st.plotly_chart(fig)
    else:
        st.error("No quarterly financial data available.")

else:
    st.error("Failed to fetch stock information.")

st.sidebar.info("Enter a stock symbol to fetch its information and historical data. Adjust the date range to see specific performance.")
