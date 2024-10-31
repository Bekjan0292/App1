import streamlit as st
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objs as go
import yfinance as yf

# Set the page configuration for the web app.
st.set_page_config(layout="wide", page_title="WebApp_Demo", page_icon="📈")

# Sidebar for input
st.sidebar.title("Input Ticker")
symbol = st.sidebar.text_input('Please enter the stock symbol:', 'NVDA').upper()
col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date', value=datetime.date(2024, 1, 1))
with col2:
    edate = st.date_input('End Date', value=datetime.date.today())

# Display title
st.title(f"{symbol}")

# Fetch stock data and display additional financial information
stock = yf.Ticker(symbol)
if stock is not None:
        # Display company's basic information
        st.write(f"### Sector: {stock.info.get('sector', 'N/A')}")
        st.write(f"### Company Beta: {stock.info.get('beta', 'N/A')}")
        
        # Additional financial metrics
        st.write(f"### P/E Ratio: {stock.info.get('forwardPE', 'N/A')}")
        st.write(f"### P/B Ratio: {stock.info.get('priceToBook', 'N/A')}")
        st.write(f"### Market Cap: {stock.info.get('marketCap', 'N/A')}")
        st.write(f"### Profitability: {stock.info.get('profitMargins', 'N/A')}")
        
        # Retrieve ROE if available
        roe = stock.info.get('returnOnEquity')
        if roe is not None:
            st.write(f"### Return on Equity (ROE): {roe}")
            # Plot ROE (for simplicity, using a static plot)
            fig, ax = plt.subplots()
            ax.bar(['ROE'], [roe], color='skyblue')
            ax.set_ylabel("Return on Equity")
            st.pyplot(fig)
        else:
            st.write("Return on Equity (ROE) data is not available.")
    except Exception as e:
        st.error("Error fetching company information.")
else:
    st.error("Failed to fetch company information.")

# Download historical data and plot
data = yf.download(symbol, start=sdate, end=edate)
if data is not None:
    st.line_chart(data['Close'], x_label="Date", y_label="Close, USD")
else:
    st.error("Failed to fetch historical data.")
