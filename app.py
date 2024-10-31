import streamlit as st
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
    # Profitability Metrics
    sector = stock.info.get('sector', 'N/A')
    beta = stock.info.get('beta', 'N/A')
    pe_ratio = stock.info.get('trailingPE', None)
    pb_ratio = stock.info.get('priceToBook', None)
    roe = stock.info.get('returnOnEquity', None)
    
    st.write(f"**Sector:** {sector}")
    st.write(f"**Beta:** {beta}")

    # Profitability Chart
    if pe_ratio and pb_ratio and roe is not None:
        profitability_data = {
            'P/E Ratio': pe_ratio,
            'P/B Ratio': pb_ratio,
            'ROE (%)': roe * 100  # Convert ROE to percentage
        }
        
        fig_profitability = go.Figure([go.Bar(
            x=list(profitability_data.keys()),
            y=list(profitability_data.values()),
            marker_color=['blue', 'orange', 'green']
        )])
        
        fig_profitability.update_layout(
            title=f"{symbol} Profitability Metrics",
            xaxis_title="Metrics",
            yaxis_title="Value",
            height=400
        )
        
        st.plotly_chart(fig_profitability)
    else:
        st.write("Profitability data is unavailable for this stock.")
except KeyError:
    st.error("Failed to retrieve company financial data.")

# Fetch historical stock price data
data = yf.download(symbol, start=sdate, end=edate)

# Display Japanese Candlestick Chart
if not data.empty:
    fig_candlestick = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])
    
    fig_candlestick.update_layout(
        title=f"{symbol} Japanese Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        height=600
    )
    
    st.plotly_chart(fig_candlestick)
else:
    st.error("Failed to fetch historical data.")
