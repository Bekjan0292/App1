import streamlit as st
import datetime
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf

# Set up your web app
st.set_page_config(layout="wide", page_title="Risk&Return")

# Sidebar
st.sidebar.title("Input Ticker")
symbol = st.sidebar.text_input('Please enter the stock symbol: ', 'NVDA').upper()
# Selection for a specific time frame.
col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date', value=datetime.date(2024, 1, 1))
with col2:
    edate = st.date_input('End Date', value=datetime.date.today())

st.title(f"{symbol}")

# Fetch stock data
try:
    stock = yf.Ticker(symbol)

    # Check if the stock symbol is valid
    if not stock.info or 'regularMarketPrice' not in stock.info:
        st.error("Invalid stock symbol. Please check and try again.")
    else:
        # Display company's basics
        sector = stock.info.get('sector', 'N/A')
        beta = stock.info.get('beta', 'N/A')
        pe_ratio = stock.info.get('trailingPE', 'N/A')
        pb_ratio = stock.info.get('priceToBook', 'N/A')
        roe = stock.info.get('returnOnEquity', 'N/A')
        roa = stock.info.get('returnOnAssets', 'N/A')

        st.write(f"# Sector: {sector}")
        st.write(f"# Beta: {beta}")
        st.write(f"# P/E Ratio: {pe_ratio}")
        st.write(f"# P/B Ratio: {pb_ratio}")
        st.write(f"# ROE: {roe}")
        st.write(f"# ROA: {roa}")

        # Fetch historical stock data
        data = yf.download(symbol, start=sdate, end=edate)

        if data.empty:
            st.error("No historical data available for the selected date range.")
        else:
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

            # Net income chart
            financials = stock.financials
            net_income = financials.loc['Net Income']

            if not net_income.empty:
                net_income_fig = go.Figure(data=[go.Bar(x=net_income.index, y=net_income.values)])
                net_income_fig.update_layout(title='Net Income',
                                              xaxis_title='Year',
                                              yaxis_title='Net Income (USD)',
                                              xaxis_tickformat='%Y')

                st.plotly_chart(net_income_fig)
            else:
                st.error("No net income data available.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
