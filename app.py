import streamlit as st
import datetime
import plotly.graph_objs as go
import yfinance as yf

# Set up your web app
st.set_page_config(layout="wide", page_title="Stock Dashboard", page_icon="📈")

# Sidebar
st.sidebar.title("Input Ticker")
symbol = st.sidebar.text_input('Please enter the stock symbol:', 'TSLA').upper()

# Date selection
col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date', value=datetime.date(2024, 1, 1))
with col2:
    edate = st.date_input('End Date', value=datetime.date.today())

# Validate date input
if edate < sdate:
    st.error("End date must be after the start date.")
else:
    st.title(f"{symbol} Stock Overview")

    with st.spinner('Fetching data...'):
        stock = yf.Ticker(symbol)

        # Display company basics
        if stock.info:
            st.markdown(f"### Sector: **{stock.info.get('sector', 'N/A')}**")
            st.markdown(f"### Company Beta: **{stock.info.get('beta', 'N/A')}**")
            st.markdown(f"### Market Cap: **${stock.info.get('marketCap', 'N/A')}**")
            st.markdown(f"### Current Price: **${stock.info.get('currentPrice', 'N/A')}**")
        else:
            st.error("Failed to fetch stock information.")

        data = yf.download(symbol, start=sdate, end=edate)

        if not data.empty:
            # Create an interactive plot using Plotly
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price', line=dict(color='royalblue')))
            fig.update_layout(title=f'{symbol} Closing Prices',
                              xaxis_title='Date',
                              yaxis_title='Close Price (USD)',
                              template='plotly_white',
                              margin=dict(l=40, r=40, t=40, b=40))
            st.plotly_chart(fig)

            # Display additional stock information (e.g., volume)
            st.markdown("### Additional Information")
            st.write(data[['Open', 'High', 'Low', 'Close', 'Volume']].tail())  # Show the last few rows of data
        else:
            st.error("Failed to fetch historical data.")
