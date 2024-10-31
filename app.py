import streamlit as st
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objs as go
import yfinance as yf

# Set up your web app
st.set_page_config(layout="wide", page_title="WebApp_Demo")

# Sidebar
st.sidebar.title("Input Ticker")
symbol = st.sidebar.text_input('Please enter the stock symbol: ', 'NVDA').upper()

# Selection for a specific time frame.
col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date', value=datetime.date(2024, 1, 1))
with col2:
    edate = st.date_input('End Date', value=datetime.date.today())

# Validate date input
if edate < sdate:
    st.error("End date must be after the start date.")
else:
    st.title(f"{symbol}")

    with st.spinner('Fetching data...'):
        stock = yf.Ticker(symbol)
        # Display company's basics
        if stock.info:
            st.write(f"# Sector : {stock.info.get('sector', 'N/A')}")
            st.write(f"# Company Beta : {stock.info.get('beta', 'N/A')}")
        else:
            st.error("Failed to fetch stock information.")

        data = yf.download(symbol, start=sdate, end=edate)
        if not data.empty:
            # Create an interactive plot using Plotly
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
            fig.update_layout(title=f'{symbol} Closing Prices', xaxis_title='Date', yaxis_title='Close Price (USD)')
            st.plotly_chart(fig)
        else:
            st.error("Failed to fetch historical data.")
