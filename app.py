import streamlit as st
import datetime
import yfinance as yf
import pandas as pd
import plotly.express as px

# Set up the web app layout and title
st.set_page_config(layout="wide", page_title="Stock Info WebApp")

# Sidebar for stock input with validation
def validate_symbol(symbol):
    """Checks if the input symbol is valid."""
    if not symbol.isalpha():
        raise ValueError("Please enter a valid stock symbol (letters only).")
    return symbol.upper()

try:
    symbol = st.sidebar.text_input('Please enter the stock symbol:', validate_symbol('NVDA'))
except ValueError as e:
    st.error(e)
    symbol = None

# Enhanced date input for flexibility
col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date', value=datetime.date(2024, 1, 1))
with col2:
    edate = st.date_input('End Date', value=datetime.date.today())
    if sdate > edate:
        st.error("Start date cannot be after end date.")

# Sidebar options for metric selection with search
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

# Enable search functionality for metrics
search_term = st.sidebar.text_input("Search Metrics:", "")
filtered_metrics = {k: v for k, v in metrics_options.items() if search_term.lower() in k.lower()}
selected_metrics = st.sidebar.multiselect("Choose metrics to display:", list(filtered_metrics.keys()), default=list(filtered_metrics.keys()))

# Display the stock symbol prominently
st.title(f"{symbol} Stock Information")

# Fetch stock data and handle errors gracefully
if symbol:
    try:
        stock = yf.Ticker(symbol)

        # Display company sector, beta, and last traded date
        if stock.info:
            st.subheader("Company Overview")
            st.write(f"**Sector:** {stock.info.get('sector', 'N/A')}")
            st.write(f"**Company Beta:** {stock.info.get('beta', 'N/A')}")
            st.write(f"**Last Traded Date:** {stock.info.get('lastTradedDate', 'N/A')}")

            # Create a DataFrame for selected stock information
            stock_data = {metric: stock.info.get(metrics_options[metric], 'N/A') for metric in selected_metrics}
            df = pd.DataFrame(stock_data.items(), columns=['Metric', 'Value'])

            # Display stock information table
            st.table(df)

            # Download historical data and handle absence or errors
            data = yf.download(symbol, start=sdate, end=edate)
            if not data.empty:
                st.subheader("Stock Price Over Time")
                st.line_chart(data['Close'])
            else:
                st.error("Failed to fetch historical data for the specified date range.")

            # Fetch and display quarterly financial data, including error handling
            st.subheader("Quarterly Financial Data")
            quarterly_data = stock.quarterly_financials
            if not quarterly_data.empty:
                # Improve formatting and clarity
                quarterly_data = quarterly_data.transpose()
                quarterly_data.reset_index(inplace=True)
                quarterly_data.columns = ['Quarter'] + list(quarterly_data.columns[1:])  # Rename columns
                st.write(quarterly_data)

                # Create and display bar chart for Revenue and Net Income
                fig = px.bar(quarterly_data, x='Quarter', y=['Revenue', 'Net Income'],
                             title='Quarterly Revenue and Net Income',
                             labels={'value
